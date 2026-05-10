# Objectives

By completing this assignment you will demonstrate the ability to:

- Distinguish functional regression testing from performance regression testing and select the appropriate approach for a given change.
- Plan and execute a server-side performance test using an industry tool, defining operational and load profiles, SLA thresholds, and percentile-based metrics.
- Evaluate client-side performance on both mobile and desktop.
- Interpret performance test results and propose a concrete remediation.

---

# Exercise 1: Functional vs Performance Regression Testing

First, in 3–5 sentences each, define functional regression testing and performance (non-functional) regression testing, and explain the difference.

Then, for each Canvas-application change below, decide whether functional regression, performance regression, or both are appropriate, and justify in 2–3 sentences. Where performance regression is needed, name the specific test type (load, spike, endurance, etc.) you would run and the metric you would compare against the previous build.

## Scenarios

1. A new validation rule is added to the grade submission form to prevent missing fields.
2. Backend logic is optimized to fetch assignment data more efficiently.
3. A database index is added to improve the speed of grade retrieval.
4. A UI redesign changes the assignment submission button's location and styling.

---

# Exercise 2: Server-Side Performance Testing

Choose one server-side performance testing tool (`k6`, `Locust`, `JMeter`, etc.) and a specific feature on a web application of your choice.

## Complete the following

### Profiles

Define the operational profile (the sequence of user actions) and the load profile (the VU or RPS shape over time). Explain your reasoning for both.

### SLAs

Define explicit pass/fail thresholds before running the test. At minimum:

- p95 response time threshold
- error rate threshold
- throughput threshold

### Tests

Run two different performance test types from the seven covered in lecture (e.g., load + spike, load + stress, load + endurance). Reuse the same operational profile across both.

### Metrics

Report at minimum:

- Response time as p50, p95, and p99
- Error rate
- Throughput (RPS or TPS)

## Deliverable

Include screenshots of:

- Test setup (script or config)
- Test execution (live run)
- Test results (summary metrics or dashboard)

Discuss the results and reflect on what you learned in 1–2 paragraphs at the end.

---

# Exercise 3: Client-Side Performance Testing

Choose a client-side performance testing tool (`Google Lighthouse`, `Chrome DevTools Performance tab`, `k6 browser module`, `PageSpeed Insights`, `WebPageTest`) and a specific feature on a web application of your choice.

## Complete the following

### Run the tool on both mobile and desktop

Track at least three Core Web Vitals or related metrics for each platform. Pick from:

- LCP (Largest Contentful Paint)
- INP (Interaction to Next Paint)
- FID (First Input Delay)
- CLS (Cumulative Layout Shift)
- FCP (First Contentful Paint)
- TTFB (Time to First Byte)
- TBT (Total Blocking Time)

### Improvement Analysis

Identify one area of improvement and propose a concrete remediation.

## Deliverable

Include screenshots of:

- Test setup
- Execution
- Results for both platforms

Discuss differences between mobile and desktop and reflect on what you learned in 1–2 paragraphs.

---

# Submission

Submit a single document to Canvas that contains both your written answers and a link to your GitHub repository.

## Format

- PDF or DOCX

## Filename

`LASTNAME_FirstName_Assignment5.pdf`

## Contents

- All written answers, analysis, screenshots, and reflections for Exercises 1–3.
- Your GitHub repository URL on the first page.

The repository should contain:

- Test scripts used in Exercise 2 (e.g., `loadtest.js`, `stresstest.js`, `locustfile.py`)
- Any configuration files or environment files needed to reproduce the tests
- Test scripts or configuration used in Exercise 3, if applicable (e.g., `k6` browser scripts, `WebPageTest` API calls)

### README.md Requirements

The repository must include a `README.md` containing:

- Tools used and how to install them
- Exact commands used to run each test
- The web application or feature under test, including any URL or endpoint

## References

Include a References section at the end listing any:

- Sites
- Articles
- Industry reports
- Videos
- AI tools used