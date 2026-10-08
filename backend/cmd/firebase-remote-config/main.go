// Command firebase-remote-config audits the protected production Firebase project.
package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"reflect"
	"sort"
	"time"

	"github.com/joho/godotenv"

	"mediguide/internal/config"
	"mediguide/internal/services"
)

type object = map[string]json.RawMessage

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func run() error {
	publish := flag.Bool("publish", false, "Add missing documented production parameters")
	flag.Parse()
	var mobile map[string]any
	if err := json.Unmarshal([]byte(os.Getenv("FIREBASE_MOBILE_CONFIG_JSON")), &mobile); err != nil {
		return fmt.Errorf("invalid production mobile Firebase configuration")
	}
	project, _ := mobile["FIREBASE_PROJECT_ID"].(string)
	if project == "" {
		return fmt.Errorf("production mobile Firebase project is missing")
	}
	env, err := godotenv.Unmarshal(os.Getenv("PRODUCTION_ENV_FILE"))
	if err != nil {
		return fmt.Errorf("invalid protected production environment file")
	}
	if configured := env["FIREBASE_PROJECT_ID"]; configured != "" && configured != project {
		return fmt.Errorf("backend Firebase project differs from production mobile project")
	}
	service, err := services.NewFirebaseService(nil, config.Config{FirebaseProjectID: project, FirebaseCredentials: env["FIREBASE_SERVICE_ACCOUNT_BASE64"]})
	if err != nil {
		return err
	}
	if !service.Enabled() {
		return fmt.Errorf("production Firebase credentials are not configured")
	}
	ctx, cancel := context.WithTimeout(context.Background(), 90*time.Second)
	defer cancel()
	raw, etag, err := service.GetRemoteConfig(ctx)
	if err != nil {
		return err
	}
	fmt.Printf("Production Firebase project: %s\n", service.Project)
	var template object
	if err := json.Unmarshal(raw, &template); err != nil {
		return err
	}
	defaultsRaw, err := os.ReadFile("../firebase/remote-config.production.defaults.json")
	if err != nil {
		return err
	}
	var defaults struct {
		Parameters object `json:"parameters"`
	}
	if err := json.Unmarshal(defaultsRaw, &defaults); err != nil {
		return err
	}
	next, missing, err := align(template, defaults.Parameters)
	if err != nil {
		return err
	}
	fmt.Printf("Missing documented parameters: %v\n", missing)
	var version struct {
		VersionNumber string `json:"versionNumber"`
	}
	_ = json.Unmarshal(template["version"], &version)
	fmt.Printf("Current template version: %s\n", version.VersionNumber)
	if !*publish || len(missing) == 0 {
		return nil
	}
	if err := os.WriteFile("remote-config-before.json", raw, 0600); err != nil {
		return err
	}
	delete(next, "version")
	payload, err := json.Marshal(next)
	if err != nil {
		return err
	}
	if _, _, err := service.PutRemoteConfig(ctx, payload, etag, true); err != nil {
		return fmt.Errorf("template validation: %w", err)
	}
	if _, _, err := service.PutRemoteConfig(ctx, payload, etag, false); err != nil {
		return fmt.Errorf("template publication: %w", err)
	}
	after, _, err := service.GetRemoteConfig(ctx)
	if err != nil {
		return err
	}
	var verified object
	if err := json.Unmarshal(after, &verified); err != nil {
		return err
	}
	delete(verified, "version")
	expected, _ := json.Marshal(next)
	actual, _ := json.Marshal(verified)
	var expectedValue, actualValue any
	_ = json.Unmarshal(expected, &expectedValue)
	_ = json.Unmarshal(actual, &actualValue)
	if !reflect.DeepEqual(expectedValue, actualValue) {
		return fmt.Errorf("published template differs from requested template; inspect Firebase version history")
	}
	if err := os.WriteFile("remote-config-after.json", after, 0600); err != nil {
		return err
	}
	fmt.Printf("Published and verified %d missing production parameters\n", len(missing))
	return nil
}

// Preserve all existing defaults, targeting conditions, groups and unrelated keys.
func align(template object, defaults object) (object, []string, error) {
	params := object{}
	if raw, ok := template["parameters"]; ok {
		if err := json.Unmarshal(raw, &params); err != nil {
			return nil, nil, err
		}
	}
	known := object{}
	for k, v := range params {
		known[k] = v
	}
	groups := map[string]struct {
		Parameters object `json:"parameters"`
	}{}
	if raw, ok := template["parameterGroups"]; ok {
		if err := json.Unmarshal(raw, &groups); err != nil {
			return nil, nil, err
		}
	}
	for _, g := range groups {
		for k, v := range g.Parameters {
			known[k] = v
		}
	}
	keys := []string{}
	for k := range defaults {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	missing := []string{}
	for _, k := range keys {
		current, ok := known[k]
		if !ok {
			missing = append(missing, k)
			params[k] = defaults[k]
			fmt.Printf("%s: missing\n", k)
			continue
		}
		var p struct {
			DefaultValue struct {
				Value           string `json:"value"`
				UseInAppDefault bool   `json:"useInAppDefault"`
			} `json:"defaultValue"`
			ValueType         string `json:"valueType"`
			ConditionalValues object `json:"conditionalValues"`
		}
		if err := json.Unmarshal(current, &p); err != nil {
			return nil, nil, err
		}
		var desired struct {
			DefaultValue struct {
				Value string `json:"value"`
			} `json:"defaultValue"`
			ValueType string `json:"valueType"`
		}
		if err := json.Unmarshal(defaults[k], &desired); err != nil {
			return nil, nil, err
		}
		state := "matches documented default"
		if p.DefaultValue.UseInAppDefault {
			state = "uses app default"
		} else if p.DefaultValue.Value != desired.DefaultValue.Value {
			state = "custom default (preserved)"
		}
		value := "nonempty string"
		if p.DefaultValue.Value == "" {
			value = "empty string"
		}
		if desired.ValueType == "BOOLEAN" {
			value = p.DefaultValue.Value
		}
		fmt.Printf("%s: %s; type=%s; default=%s; conditions=%d\n", k, state, p.ValueType, value, len(p.ConditionalValues))
	}
	raw, err := json.Marshal(params)
	if err != nil {
		return nil, nil, err
	}
	template["parameters"] = raw
	return template, missing, nil
}
