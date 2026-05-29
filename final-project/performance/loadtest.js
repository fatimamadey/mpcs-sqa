/**
 * Q4 – Load Test
 * Tool:   k6  (https://k6.io)
 * Target: Django Poll App  (default: http://127.0.0.1:8000)
 *
 * Scenario: ramp from 0 → 50 virtual users over 30 s,
 *           hold at 50 VUs for 2 minutes,
 *           ramp back to 0 over 30 s.
 *
 * Endpoints exercised:
 *   - GET /polls/          (poll list)
 *   - GET /polls/<id>/     (poll detail)
 *
 * Run:
 *   BASE_URL=http://127.0.0.1:8000 k6 run performance/loadtest.js
 */

import http from "k6/http";
import { sleep, check, group } from "k6";
import { Trend, Rate } from "k6/metrics";

const BASE_URL = __ENV.BASE_URL || "http://127.0.0.1:8000";

// Custom per-endpoint metrics
const pollListTrend   = new Trend("req_poll_list",   true);
const pollDetailTrend = new Trend("req_poll_detail", true);
const errorRate       = new Rate("error_rate");

export const options = {
  summaryTrendStats: ["avg", "min", "med", "max", "p(90)", "p(95)", "p(99)"],
  stages: [
    { duration: "30s", target: 50 },  // ramp-up
    { duration: "2m",  target: 50 },  // steady-state load
    { duration: "30s", target: 0  },  // ramp-down
  ],
  thresholds: {
    // Overall SLAs
    http_req_duration: ["p(95)<1000"],  // 95th percentile < 1 s
    http_req_failed:   ["rate<0.02"],   // error rate < 2 %
    req_poll_list:     ["p(95)<800"],
    req_poll_detail:   ["p(95)<800"],
  },
};

export default function () {
  // ── Step 1: Poll list ──────────────────────────────────────────────────────
  group("poll_list", () => {
    const res = http.get(`${BASE_URL}/polls/`, {
      headers: { Accept: "text/html" },
    });
    pollListTrend.add(res.timings.duration);
    const ok = check(res, {
      "poll list status 200 or 302": (r) => r.status === 200 || r.status === 302,
    });
    errorRate.add(!ok);
  });

  sleep(1);

  // ── Step 2: Poll detail (spread VUs across first 10 poll IDs) ─────────────
  group("poll_detail", () => {
    const pollId = (__VU % 10) + 1;
    const res = http.get(`${BASE_URL}/polls/${pollId}/`, {
      headers: { Accept: "text/html" },
    });
    pollDetailTrend.add(res.timings.duration);
    const ok = check(res, {
      "poll detail not 500": (r) => r.status !== 500,
    });
    errorRate.add(!ok);
  });

  sleep(1);
}
