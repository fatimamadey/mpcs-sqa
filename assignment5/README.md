# Assignment 5 — Performance Testing

## Directory Structure

```
assignment5/
├── MADEY_Fatima_Assignment5.MD   ← Full submission (answers to all 3 exercises)
├── README.md                     ← This file
├── scripts/
│   ├── loadtest.js               ← k6 load test (ramp 0→50 VUs, hold 1 min, ramp down)
│   └── spiketest.js              ← k6 spike test (10 VUs → instant 200 → recovery)
└── screenshots/                  ← Place screenshots here before converting to PDF
```

---

## Prerequisites

| Tool | Version used | Install |
|------|-------------|---------|
| k6 | v1.7.1 | `brew install k6` |
| Node.js / npx | v22+ | Included with Node.js |
| Lighthouse CLI | v13 | `npx lighthouse` (no install needed) |
| Google Chrome | any recent | Required by Lighthouse headless |

---

## Exercise 2 — Running the k6 Tests

### Target URL
`https://jsonplaceholder.typicode.com`

No account or API key required.

### Load Test
```bash
k6 run scripts/loadtest.js
```
Stages: ramp 0 → 50 VUs over 30 s, hold 50 VUs for 1 min, ramp down over 30 s.  
Duration: ~2 min. Expected throughput: ~37 req/s.

### Spike Test
```bash
k6 run scripts/spiketest.js
```
Stages: baseline 10 VUs for 30 s → instant spike to 200 VUs → hold 1 min → instant drop to 10 VUs → hold 30 s.  
Duration: ~2 min. Peak throughput: ~101 req/s.

### SLA Thresholds (pre-defined in scripts)
- p95 response time < 500 ms
- Error rate < 1 %
- Throughput > 10 req/s

---

## Exercise 3 — Running the Lighthouse Tests

### Target URL
`https://books.toscrape.com`

### Mobile (headless)
```bash
npx lighthouse https://books.toscrape.com \
  --output=json \
  --output-path=./screenshots/lighthouse_mobile.json \
  --form-factor=mobile \
  --only-categories=performance \
  --chrome-flags="--headless --no-sandbox"
```

### Desktop (headless)
```bash
npx lighthouse https://books.toscrape.com \
  --output=json \
  --output-path=./screenshots/lighthouse_desktop.json \
  --preset=desktop \
  --only-categories=performance \
  --chrome-flags="--headless --no-sandbox"
```

### Alternatively: Chrome DevTools
1. Open `https://books.toscrape.com` in Chrome
2. Open DevTools (F12) → Lighthouse tab
3. Select "Performance" category only
4. Run once for **Mobile**, screenshot the results panel
5. Run again for **Desktop**, screenshot the results panel

---

## Screenshots Needed for Submission

Before converting to PDF, take the following screenshots and save them to `screenshots/`:

| Filename | What to capture |
|----------|----------------|
| `loadtest_setup.png` | Terminal showing `cat scripts/loadtest.js` or VS Code with the file open |
| `loadtest_run.png` | Terminal live run — showing VU ramp and iteration counter |
| `loadtest_results.png` | Terminal showing the full k6 summary (THRESHOLDS + TOTAL RESULTS) |
| `spiketest_setup.png` | Terminal showing `cat scripts/spiketest.js` |
| `spiketest_run.png` | Terminal at the spike moment (showing `200/200 VUs` at ~1m01s) |
| `spiketest_results.png` | Terminal showing spike test summary |
| `lighthouse_setup.png` | Terminal showing the lighthouse command being run |
| `lighthouse_mobile_results.png` | Lighthouse mobile results (terminal JSON extract or Chrome DevTools panel) |
| `lighthouse_desktop_results.png` | Lighthouse desktop results |

---

## Results Summary

### k6 Load Test (50 VUs, ~2 min)

| Metric | Result | SLA | Pass? |
|--------|--------|-----|-------|
| p50 response time | 21.48 ms | — | — |
| p95 response time | 25.94 ms | < 500 ms | ✅ |
| p99 response time | 30.78 ms | — | — |
| Error rate | 0.00 % | < 1 % | ✅ |
| Throughput | 36.78 req/s | > 10 req/s | ✅ |

### k6 Spike Test (10 → 200 → 10 VUs, ~2 min)

| Metric | Result | SLA | Pass? |
|--------|--------|-----|-------|
| p50 response time | 22.40 ms | — | — |
| p95 response time | 31.40 ms | < 500 ms | ✅ |
| p99 response time | 39.24 ms | — | — |
| Error rate | 0.00 % | < 1 % | ✅ |
| Throughput | 101.26 req/s | > 10 req/s | ✅ |

### Lighthouse — books.toscrape.com

| Metric | Mobile | Desktop |
|--------|--------|---------|
| Performance Score | 95 / 100 | 100 / 100 |
| FCP | 1.9 s | 0.4 s |
| LCP | 2.3 s | 0.5 s |
| TBT | 0 ms | 0 ms |
| CLS | 0 | 0.002 |
| Speed Index | 4.1 s ⚠️ | 0.5 s ✅ |
| TTI | 2.3 s | 0.5 s |
