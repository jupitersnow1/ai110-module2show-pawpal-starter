# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

Phase 4 added algorithmic intelligence to the scheduler. The following features are implemented in `pawpal_system.py` and verified by tests in `test_pawpal_system.py`:

- **Sort by time** — `Scheduler.sort_by_time()` returns scheduled entries ordered by start time, useful for displaying a clean timeline view.
- **Filter tasks** — `Owner.filter_tasks(pet_id, status)` returns tasks narrowed by pet and/or completion status (`"pending"` or `"complete"`). Filters can be combined.
- **Recurring task gating** — `Task.is_due(today)` checks a task's `frequency` (`daily`, `weekly`, `once`) against its `last_scheduled` date before it enters the schedule. When a recurring task is completed via `Scheduler.complete_task()`, the next occurrence is automatically queued on the pet.
- **Conflict detection** — `Scheduler.detect_conflicts()` scans all scheduled entries for overlapping time windows. `Scheduler.warn_conflicts()` returns the same results as human-readable warning strings without crashing the program.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
