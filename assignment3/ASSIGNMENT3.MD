<table width="100%">
<tr>
<td>

<h1 style="margin:-10;">Assignment 3</h1>

</td>
<td align="right">

**Fatima Madey**  
MPCS 56540  
April 24, 2026  

</td>
</tr>
</table>

## Overview
Backend of a To-Do List application — domain model + unit test suite. No UI, database, or web server.

**Repository:** <!-- TODO: add GitHub URL -->

---

## Question 1: What You Built (≈75 words)

<!-- TODO: Describe your domain model:
- Which classes exist (e.g., Task, User, TaskManager, ReminderService)?
- How they interact / call each other
- Which collaborators are injected through constructors (dependency injection seams)
Someone reading this should understand the architecture without opening the repo.
-->

> _[Your answer here]_

---

## Question 2: Test Strategy and Coverage (≈100 words)

### Coverage Report

<!-- TODO: Paste full line-coverage and branch-coverage output here.
Run: pytest --cov=src --cov-branch --cov-report=term-missing tests/
Both line % and branch % must be visible per file.
-->

```
[paste coverage report output here]
```

### Analysis

**Hardest test category to design, and why:**

> _[Which category — happy path / invalid input / edge / equivalence / exception / business logic — was hardest and why?]_

**Lowest branch coverage area:**

> _[Where is branch coverage lowest? What would it take to close the gap? If you deliberately left something uncovered, justify it.]_

---

## Question 3: Test Doubles and Isolation (≈100 words)

### Doubles Used

| Double Type | Collaborator | Test File / Test Name | Justification |
|-------------|-------------|----------------------|---------------|
| Mock        | <!-- e.g., ReminderService --> | <!-- test file + test name --> | <!-- why mock vs other double --> |
| Stub        | <!-- e.g., DateProvider -->    | <!-- test file + test name --> | <!-- why stub --> |
| Fake        | <!-- e.g., InMemoryUserRepo --> | <!-- test file + test name --> | <!-- why fake --> |
| Spy         | <!-- if used -->               | <!-- test file + test name --> | <!-- why spy --> |
| Dummy       | <!-- if used -->               | <!-- test file + test name --> | <!-- why dummy --> |

### London vs. Classical School

> _[Did you take a London-school (mock every collaborator) or Classical (real collaborators, mock only shared/external dependencies) approach? Why was that the right call for this project?]_

---

## Question 4: The Four Pillars — Best and Weakest Test (≈125 words)

### Best Test

**Test name:** `<!-- TODO: paste exact test function name -->`

> _[Explain why this test is strong on all four pillars:]_
> - **Regression protection:** _[how it catches real bugs]_
> - **Refactoring resistance:** _[why it tests behavior, not implementation]_
> - **Fast feedback:** _[why it runs quickly and pinpoints failures]_
> - **Maintainability:** _[why it is easy to read and update]_

### Weakest Test

**Test name:** `<!-- TODO: paste exact test function name -->`

> _[Which pillar does it sacrifice and why? Why did you keep it in the suite anyway?]_

---

## Question 5: Looking Back (≈75 words)

**One thing you would design differently if you started over:**

> _[Be specific — name a class, seam, or decision]_

**One thing that surprised you while writing the tests:**

> _[Ground it in a specific test name, file, or code excerpt]_

---

## AI Usage Disclosure

<!-- List files where you used generative AI and what you asked for, or write "None". -->

> _[e.g., "Used AI to help write src/task.py — prompted for initial class skeleton. All tests, reflection, and README written independently."]_
