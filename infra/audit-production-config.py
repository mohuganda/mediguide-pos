#!/usr/bin/env python3
"""Compare GitHub's production bundle with the live deployment without printing secrets."""
import argparse
import importlib.util
from pathlib import Path
import subprocess
from urllib.parse import urlsplit


def load_checker(infra):
    spec = importlib.util.spec_from_file_location("production_checker", infra / "check-production-env.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_routes(config):
    env = config["services"]["api"]["environment"]
    public = config["services"]["guidelines"]["environment"]["MEDIGUIDE_API_URL"].rstrip("/")
    parsed = urlsplit(public)
    if parsed.scheme != "https" or not parsed.hostname or parsed.path or parsed.username or parsed.query or parsed.fragment:
        raise ValueError("PUBLIC_API_BASE_URL must be an HTTPS origin")
    if config["services"]["guidelines"]["environment"]["MEDIGUIDE_POS_URL"].rstrip("/") != public + "/admin/login":
        raise ValueError("DASHBOARD_PUBLIC_URL does not match the production origin")
    if env["ALLOWED_ORIGINS"] != public:
        raise ValueError("ALLOWED_ORIGINS does not match the production origin")
    account = env.get("ACCOUNT_ACTION_URL", "").rstrip("/")
    if account and account != public + "/admin":
        raise ValueError("ACCOUNT_ACTION_URL does not match the production dashboard base")
    if env.get("MAIL_DRIVER") not in {"resend", "smtp", "disabled"}:
        raise ValueError("MAIL_DRIVER is not supported in production")


def audit(checker, infra, expected_file):
    compose_file = infra / "docker-compose.yml"
    checker.validate(expected_file, compose_file)
    checker.validate(infra / "production.env", compose_file)
    common = ["docker", "compose", "--env-file", str(infra / "production.env")]
    current_command = common + ["--env-file", str(infra / "release.env"), "-f", str(compose_file)]
    expected_command = common + ["--env-file", str(expected_file), "--env-file", str(infra / "release.env"), "-f", str(compose_file)]
    expected = checker.run_json(expected_command + ["config", "--format", "json"])
    current = checker.run_json(current_command + ["config", "--format", "json"])
    validate_routes(expected)
    validate_routes(current)
    # Compare rendered environments: quote/interpolation syntax and ignored
    # development settings must not produce false drift reports.
    mismatches = []
    for name, service in expected["services"].items():
        actual = current["services"].get(name, {}).get("environment", {})
        for key, value in service.get("environment", {}).items():
            if actual.get(key) != value:
                mismatches.append(name + ":" + key)
        if current["services"].get(name, {}).get("image") != service.get("image"):
            mismatches.append(name + ":image")
    if mismatches:
        raise ValueError("Server configuration differs from GitHub production settings: " + ", ".join(mismatches))
    ids = subprocess.run(current_command + ["ps", "--all", "--quiet"], capture_output=True, text=True)
    if ids.returncode or not ids.stdout.split():
        raise ValueError("Unable to identify production containers")
    containers = checker.run_json(["docker", "inspect", *ids.stdout.split()])
    count = checker.compare(expected, containers)
    for container in containers:
        name = container["Config"]["Labels"]["com.docker.compose.service"]
        if container["Config"]["Image"] != expected["services"][name]["image"]:
            raise ValueError("Running image differs from configured release: " + name)
        state = container["State"]
        if name == "ollama-pull-models":
            if state["Status"] != "exited" or state["ExitCode"] != 0:
                raise ValueError("Model initialization has not completed successfully")
        elif state["Status"] != "running" or state.get("Health", {}).get("Status", "healthy") != "healthy":
            raise ValueError("Production service is not healthy: " + name)
    print(f"GitHub bundle, server configuration and {count} running environment values match across {len(containers)} containers")
    print("Production URL, CORS, account-link and image settings are aligned; services are healthy")
    print("Account mail provider: " + expected["services"]["api"]["environment"]["MAIL_DRIVER"])
    postgres = next(c for c in containers if c["Config"]["Labels"]["com.docker.compose.service"] == "postgres")
    query = "SELECT to_regclass('public.account_email_deliveries') IS NOT NULL; SELECT max(version_id) FROM goose_db_version WHERE is_applied;"
    result = subprocess.run(["docker", "exec", "-i", postgres["Id"], "sh", "-c", 'exec psql -X -At -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB"'], input=query, capture_output=True, text=True)
    if result.returncode:
        raise ValueError("Unable to verify production database schema; diagnostic output suppressed")
    rows = result.stdout.splitlines()
    if len(rows) != 2 or rows[0] != "t" or not rows[1].isdigit() or int(rows[1]) < 78:
        raise ValueError("Production account email schema is missing or migrations are behind")
    print("Account email table exists; applied migration version: " + rows[1])
    for service in ("api", "postgres"):
        container = next(c for c in containers if c["Config"]["Labels"]["com.docker.compose.service"] == service)
        logs = subprocess.run(["docker", "logs", "--since", "10m", container["Id"]], capture_output=True, text=True)
        if logs.returncode:
            raise ValueError("Unable to inspect recent logs: " + service)
        errors = sum("account_email_deliveries" in line and "does not exist" in line for line in (logs.stdout + logs.stderr).splitlines())
        print(f"{service}: {errors} missing account-email-table errors in the last 10 minutes")
        if errors:
            raise ValueError("Recent account-email schema errors remain: " + service)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("infra", type=Path)
    parser.add_argument("expected", type=Path)
    args = parser.parse_args()
    try:
        audit(load_checker(args.infra), args.infra, args.expected)
    except (ValueError, OSError) as error:
        raise SystemExit(str(error) if isinstance(error, ValueError) else "Production audit failed; no credential values printed")


if __name__ == "__main__":
    main()
