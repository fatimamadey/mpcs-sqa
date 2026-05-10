/**
 * Exercise 2 — Load Test
 * Tool:  k6
 * Target: https://jsonplaceholder.typicode.com
 */

import http from "k6/http";
import { sleep, check } from "k6";
import { Trend } from "k6/metrics";

const BASE_URL = "https://jsonplaceholder.typicode.com";

// Custom metric to track each step separately
const listTrend   = new Trend("req_posts_list",    true);
const detailTrend = new Trend("req_post_detail",   true);
const commentTrend = new Trend("req_comments",     true);

export const options = {
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
  stages: [
    { duration: "30s", target: 50 },  // ramp up
    { duration: "1m",  target: 50 },  // steady state
    { duration: "30s", target: 0  },  // ramp down
  ],
  thresholds: {
    http_req_duration: ["p(95)<500"],
    http_req_failed:   ["rate<0.01"],
    req_posts_list:   ["p(95)<500"],
    req_post_detail:  ["p(95)<500"],
    req_comments:     ["p(95)<500"],
  },
};

export default function () {
  // Step 1 — List posts
  const r1 = http.get(`${BASE_URL}/posts`);
  listTrend.add(r1.timings.duration);
  check(r1, { "posts list 200": (r) => r.status === 200 });

  sleep(1);

  // Step 2 — View a single post (use VU id to spread across records 1-100)
  const postId = (__VU % 100) + 1;
  const r2 = http.get(`${BASE_URL}/posts/${postId}`);
  detailTrend.add(r2.timings.duration);
  check(r2, { "post detail 200": (r) => r.status === 200 });

  sleep(1);

  // Step 3 — Fetch comments for that post
  const r3 = http.get(`${BASE_URL}/comments?postId=${postId}`);
  commentTrend.add(r3.timings.duration);
  check(r3, { "comments 200": (r) => r.status === 200 });

  sleep(1);
}
