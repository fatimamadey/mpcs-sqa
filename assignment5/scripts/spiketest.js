/**
 * Exercise 2 — Spike Test
 * Tool:  k6
 * Target: https://jsonplaceholder.typicode.com
 */

import http from "k6/http";
import { sleep, check } from "k6";
import { Trend } from "k6/metrics";

const BASE_URL = "https://jsonplaceholder.typicode.com";

const listTrend    = new Trend("spike_posts_list",   true);
const detailTrend  = new Trend("spike_post_detail",  true);
const commentTrend = new Trend("spike_comments",     true);

export const options = {
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
  stages: [
    { duration: "30s", target: 10  },  // baseline
    { duration: "0s",  target: 200 },  // spike — instant ramp
    { duration: "1m",  target: 200 },  // hold spike
    { duration: "0s",  target: 10  },  // instant drop
    { duration: "30s", target: 10  },  // recovery confirmation
  ],
  thresholds: {
    http_req_duration: ["p(95)<500"],
    http_req_failed:   ["rate<0.01"],
    spike_posts_list:  ["p(95)<500"],
    spike_post_detail: ["p(95)<500"],
    spike_comments:    ["p(95)<500"],
  },
};

export default function () {
  // Step 1 — List posts
  const r1 = http.get(`${BASE_URL}/posts`);
  listTrend.add(r1.timings.duration);
  check(r1, { "posts list 200": (r) => r.status === 200 });

  sleep(1);

  // Step 2 — View a single post
  const postId = (__VU % 100) + 1;
  const r2 = http.get(`${BASE_URL}/posts/${postId}`);
  detailTrend.add(r2.timings.duration);
  check(r2, { "post detail 200": (r) => r.status === 200 });

  sleep(1);

  // Step 3 — Fetch comments
  const r3 = http.get(`${BASE_URL}/comments?postId=${postId}`);
  commentTrend.add(r3.timings.duration);
  check(r3, { "comments 200": (r) => r.status === 200 });

  sleep(1);
}
