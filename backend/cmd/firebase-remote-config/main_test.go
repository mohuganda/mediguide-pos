package main

import (
	"encoding/json"
	"testing"
)

func TestAlignPreservesTargetingAndGroupedOverrides(t *testing.T) {
	var template object
	original := `{"parameters":{"existing":{"defaultValue":{"value":"false"},"conditionalValues":{"beta":{"value":"true"}},"valueType":"BOOLEAN"}},"parameterGroups":{"Production":{"description":"Keep this","parameters":{"grouped":{"defaultValue":{"value":"false"},"valueType":"BOOLEAN"}}}},"conditions":[{"name":"beta","expression":"true"}]}`
	if err := json.Unmarshal([]byte(original), &template); err != nil {
		t.Fatal(err)
	}
	defaults := object{"existing": json.RawMessage(`{"defaultValue":{"value":"true"},"valueType":"BOOLEAN"}`), "grouped": json.RawMessage(`{"defaultValue":{"value":"true"},"valueType":"BOOLEAN"}`), "missing": json.RawMessage(`{"defaultValue":{"value":"true"},"valueType":"BOOLEAN"}`)}
	groups := string(template["parameterGroups"])
	conditions := string(template["conditions"])
	next, missing, err := align(template, defaults)
	if err != nil {
		t.Fatal(err)
	}
	if len(missing) != 1 || missing[0] != "missing" {
		t.Fatalf("unexpected missing: %v", missing)
	}
	if string(next["parameterGroups"]) != groups || string(next["conditions"]) != conditions {
		t.Fatal("targeting or groups changed")
	}
	var params object
	if err := json.Unmarshal(next["parameters"], &params); err != nil {
		t.Fatal(err)
	}
	if _, ok := params["grouped"]; ok {
		t.Fatal("grouped parameter duplicated")
	}
	var existing object
	_ = json.Unmarshal(params["existing"], &existing)
	if string(existing["defaultValue"]) != `{"value":"false"}` || existing["conditionalValues"] == nil {
		t.Fatal("existing override changed")
	}
	if string(params["missing"]) != string(defaults["missing"]) {
		t.Fatal("missing default not added")
	}
	_, again, err := align(next, defaults)
	if err != nil || len(again) != 0 {
		t.Fatalf("alignment not idempotent: %v %v", again, err)
	}
}
