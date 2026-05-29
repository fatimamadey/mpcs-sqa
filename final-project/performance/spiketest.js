/**
 * Q4 – Spike Test
 * Tool:   k6  (https://k6.io)
 * Target: Django Poll App  (default: http://127.0.0.1:8000)
 *
 * Scenario: baseline 10 VUs for 30 s,
 *           instant spike to 200 VUs for 1 minute,
 *           instant drop back to 10 VUs for 30 s.
 *
 * Endpoints exercised:
 *   - GET /polls/           (poll list)
 *   - GET /polls/<id>/      (poll detail)
 *   - GET /polls/<id>/results/  (results page)
 *
 * Run:
 *   BASE_URL=http://127.0.0.1:8000 k6 run performance/spiketest.js
 */

import http from "k6/http";
import { sleep, check, group } from "k6";
import { Trend, Rate } from "k6/metrics";

const BASE_URL = __ENV.BASE_URL || "http://127.0.0.1:8000";

const pollListTrend   = new Trend("spike_poll_list",    true);
const pollDetailTrend = new Trend("spike_poll_detail",  true);
const resultsTrend    = new Trend("spike_poll_results", true);
const errorRate       = new Rate("spike_error_rate");

export const options = {
  summaryTrendStats: ["avg", "min", "med", "max", "p(90)", "p(95)", "p(99)"],
  stages: [
    { duration: "30s", target: 10  },  // baseline
    { duration: "0s",  target: 200 },  // instant spike
    { duration: "1m",  target: 200 },  // spike sustained
    { duration: "0s",  target: 10  },  // instant recovery
    { duration: "30s", target: 10  },  // recovery monitoring
  ],
  thresholds: {
    http_req_failed:  ["rate<0.05"],   // allow up to 5 % errors during spike
    spike_poll_list:  ["p(95)<2000"],  // degrade to 2 s during spike is acceptable
    spike_poll_detail:["p(95)<2000"],
  },
};

export default function () {
  group("poll_list", () => {
    const res = http.get(`${BASE_URL}/polls/`, {
      headers: { Accept: "text/html" },
    });
    pollListTrend.add(res.timings.duration);
    errorRate.add(!check(res, { "list not 500": (r) => r.status !== 500 }));
  });

  sleep(0.5);

  group("poll_detail", () => {
    const pollId = (__VU % 10) + 1;
    const res = http.get(`${BASE_URL}/polls/${pollId}/`, {
      headers: { Accept: "text/html" },
    });
    pollDetailTrend.add(res.timings.duration);
    errorRate.add(!check(res, { "detail not 500": (r) => r.status !== 500 }));
  });

  sleep(0.5);

  group("poll_results", () => {
    const pollId = (__VU % 10) + 1;
    const res = http.get(`${BASE_URL}/polls/${pollId}/results/`, {
      headers: { Accept: "text/html" },
    });
    resultsTrend.add(res.timings.duration);
    errorRate.add(!check(res, { "results not 500": (r) => r.status !== 500 }));
  });

  sleep(0.5);
}
