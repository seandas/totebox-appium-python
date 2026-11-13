#!/usr/bin/env bash
# Starts Appium, waits until it is ready, then runs pytest. Used by CI inside the emulator step.
# Usage: run-tests.sh [pytest marker expression]
set -uo pipefail

marker="${1:-}"

nohup appium --log-level warn > appium.log 2>&1 &
appium_pid=$!
trap 'kill "$appium_pid" 2>/dev/null' EXIT

for _ in $(seq 1 60); do
  curl -s http://127.0.0.1:4723/status | grep -q '"ready":true' && break
  sleep 2
done

if [ -n "$marker" ]; then
  python -m pytest -m "$marker"
else
  python -m pytest
fi
