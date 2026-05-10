#!/usr/bin/env bash
# run_and_screenshot.sh
# Guides you through running all tests and tells you exactly when to screenshot.
# Run from the assignment5/ directory: bash run_and_screenshot.sh

set -e
cd "$(dirname "$0")"

BLUE='\033[1;34m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pause_for_screenshot() {
    echo ""
    echo -e "${YELLOW}>>> SCREENSHOT NOW: $1${NC}"
    echo -e "${YELLOW}    Save as: screenshots/$2${NC}"
    echo -e "${YELLOW}    (Cmd+Shift+4, drag to select this terminal window)${NC}"
    echo ""
    read -rp "    Press Enter when done to continue..."
    echo ""
}

header() {
    echo ""
    echo -e "${BLUE}══════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}══════════════════════════════════════════${NC}"
    echo ""
}

# ─── SETUP: Load Test Script ────────────────────────────────────────────────
header "STEP 1 of 7 — Load Test Setup"
echo "Showing scripts/loadtest.js ..."
echo ""
cat scripts/loadtest.js
pause_for_screenshot "entire terminal showing the loadtest.js content above" "loadtest_setup.png"

# ─── RUN: Load Test ──────────────────────────────────────────────────────────
header "STEP 2 of 7 — Running Load Test (~2 min)"
echo "Starting: k6 run scripts/loadtest.js"
echo "Output saved to: /tmp/loadtest_output.txt"
echo ""
echo "  • Screenshot the terminal at ~1 min in (50/50 VUs, progress bar active)"
echo "  • Then wait for it to finish for the results screenshot"
echo ""
read -rp "Press Enter to start the load test..."
echo ""

k6 run scripts/loadtest.js 2>&1 | tee /tmp/loadtest_output.txt

echo ""
pause_for_screenshot "full k6 summary results above (THRESHOLDS + TOTAL RESULTS)" "loadtest_results.png"

# ─── SETUP: Spike Test Script ────────────────────────────────────────────────
header "STEP 3 of 7 — Spike Test Setup"
echo "Showing scripts/spiketest.js ..."
echo ""
cat scripts/spiketest.js
pause_for_screenshot "entire terminal showing the spiketest.js content above" "spiketest_setup.png"

# ─── RUN: Spike Test ─────────────────────────────────────────────────────────
header "STEP 4 of 7 — Running Spike Test (~2 min)"
echo "Starting: k6 run scripts/spiketest.js"
echo "Output saved to: /tmp/spiketest_output.txt"
echo ""
echo "  • Screenshot the terminal at ~30s in, when VUs jump from 10 to 200"
echo "  • Then wait for it to finish for the results screenshot"
echo ""
read -rp "Press Enter to start the spike test..."
echo ""

k6 run scripts/spiketest.js 2>&1 | tee /tmp/spiketest_output.txt

echo ""
pause_for_screenshot "full k6 summary results above (THRESHOLDS + TOTAL RESULTS)" "spiketest_results.png"

# ─── SETUP: Lighthouse Command ───────────────────────────────────────────────
header "STEP 5 of 7 — Lighthouse Setup"
echo "The following commands will be run for Exercise 3:"
echo ""
echo "  # Mobile (simulated Moto G Power, 4G throttling)"
echo "  npx lighthouse https://books.toscrape.com \\"
echo "    --output=json \\"
echo "    --output-path=/tmp/lighthouse_mobile.json \\"
echo "    --form-factor=mobile \\"
echo "    --only-categories=performance \\"
echo "    --chrome-flags=\"--headless --no-sandbox\""
echo ""
echo "  # Desktop (no throttling)"
echo "  npx lighthouse https://books.toscrape.com \\"
echo "    --output=json \\"
echo "    --output-path=/tmp/lighthouse_desktop.json \\"
echo "    --preset=desktop \\"
echo "    --only-categories=performance \\"
echo "    --chrome-flags=\"--headless --no-sandbox\""
echo ""
pause_for_screenshot "the two lighthouse commands shown above" "lighthouse_setup.png"

# ─── RUN: Lighthouse Mobile ──────────────────────────────────────────────────
header "STEP 6 of 7 — Running Lighthouse Mobile"
read -rp "Press Enter to start Lighthouse mobile (~60s)..."
echo ""

npx lighthouse https://books.toscrape.com \
  --output=json \
  --output-path=/tmp/lighthouse_mobile.json \
  --form-factor=mobile \
  --only-categories=performance \
  --chrome-flags="--headless --no-sandbox" 2>&1 | grep -E "Navigating|Auditing|Generating|score|Performance"

echo ""
echo -e "${GREEN}Mobile results extracted:${NC}"
python3 -c "
import json, sys
with open('/tmp/lighthouse_mobile.json') as f:
    d = json.load(f)
cats = d['categories']
aud = d['audits']
print(f\"  Overall Performance Score: {round(cats['performance']['score']*100)}/100\")
keys = [
    ('first-contentful-paint',  'FCP'),
    ('largest-contentful-paint','LCP'),
    ('total-blocking-time',     'TBT'),
    ('cumulative-layout-shift', 'CLS'),
    ('speed-index',             'Speed Index'),
    ('interactive',             'TTI'),
    ('server-response-time',    'TTFB'),
]
for k, label in keys:
    a = aud.get(k, {})
    print(f\"  {label}: {a.get('displayValue','n/a')}  (score: {a.get('score','n/a')})\")
"
echo ""
pause_for_screenshot "mobile results displayed above" "lighthouse_mobile_results.png"

# ─── RUN: Lighthouse Desktop ─────────────────────────────────────────────────
header "STEP 7 of 7 — Running Lighthouse Desktop"
read -rp "Press Enter to start Lighthouse desktop (~60s)..."
echo ""

npx lighthouse https://books.toscrape.com \
  --output=json \
  --output-path=/tmp/lighthouse_desktop.json \
  --preset=desktop \
  --only-categories=performance \
  --chrome-flags="--headless --no-sandbox" 2>&1 | grep -E "Navigating|Auditing|Generating|score|Performance"

echo ""
echo -e "${GREEN}Desktop results extracted:${NC}"
python3 -c "
import json, sys
with open('/tmp/lighthouse_desktop.json') as f:
    d = json.load(f)
cats = d['categories']
aud = d['audits']
print(f\"  Overall Performance Score: {round(cats['performance']['score']*100)}/100\")
keys = [
    ('first-contentful-paint',  'FCP'),
    ('largest-contentful-paint','LCP'),
    ('total-blocking-time',     'TBT'),
    ('cumulative-layout-shift', 'CLS'),
    ('speed-index',             'Speed Index'),
    ('interactive',             'TTI'),
    ('server-response-time',    'TTFB'),
]
for k, label in keys:
    a = aud.get(k, {})
    print(f\"  {label}: {a.get('displayValue','n/a')}  (score: {a.get('score','n/a')})\")
"
echo ""
pause_for_screenshot "desktop results displayed above" "lighthouse_desktop_results.png"

# ─── DONE ────────────────────────────────────────────────────────────────────
header "All tests complete!"
echo "Raw output files saved:"
echo "  /tmp/loadtest_output.txt"
echo "  /tmp/spiketest_output.txt"
echo "  /tmp/lighthouse_mobile.json"
echo "  /tmp/lighthouse_desktop.json"
echo ""
echo "Screenshots to save in screenshots/:"
echo "  loadtest_setup.png  loadtest_run.png  loadtest_results.png"
echo "  spiketest_setup.png spiketest_run.png spiketest_results.png"
echo "  lighthouse_setup.png lighthouse_mobile_results.png lighthouse_desktop_results.png"
echo ""
echo "Note: loadtest_run.png and spiketest_run.png are manual mid-run grabs."
echo "Run the tests, screenshot the live progress, then let it finish for results."
