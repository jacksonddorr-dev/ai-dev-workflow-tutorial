# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is a teaching repository for an AI-assisted development workflow tutorial (see `README.md`). Students build a small Streamlit sales dashboard (`app.py` and friends) while practicing a PRD → `TASKS.md` → brainstorm → plan → code → commit → push → review → deploy cycle. When working here, the dashboard code and the `TASKS.md` board are equally part of "the codebase" — a milestone isn't done until both the code and the board entry for it are correct.

The product spec lives in `prd/ecommerce-analytics.md`. Treat it as the source of truth for expected values (row counts, KPI figures, category/region breakdowns) when verifying a task's acceptance criteria.

## Commands

```bash
# Activate the existing venv (already has deps installed)
source venv/bin/activate

# Install/sync dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py

# Run the full test suite
pytest

# Run one test file
pytest tests/test_metrics.py

# Run one test
pytest tests/test_metrics.py::test_total_sales_sums_all_transactions
```

There's no pytest config file — `tests/conftest.py` just inserts the repo root onto `sys.path` so test modules can `import` the top-level `data_loader`, `metrics`, and `formatting` modules directly.

## Architecture

The dashboard is deliberately layered so the data/metrics logic is testable without Streamlit:

- **`data_loader.py`** — `load_sales_data()` reads `data/sales-data.csv`, validates required columns, and raises `FileNotFoundError`/`ValueError` on missing file, empty file, or missing columns. This is the only place CSV I/O happens.
- **`metrics.py`** — pure pandas aggregation functions (`total_sales`, `total_orders`, `sales_over_time`, `sales_by_category`, `sales_by_region`) that take the loaded DataFrame and return chart-ready results. No Streamlit or plotting imports here by design — keep it that way so these stay unit-testable in isolation.
- **`formatting.py`** — small display-string helpers (`format_currency`, `format_number`) kept separate from the metrics so formatting logic has its own tests.
- **`app.py`** — the Streamlit page itself. Wires the three modules together: loads data (wrapped in `try/except` around `FileNotFoundError`/`ValueError`, showing `st.error` + `st.stop()` on failure), renders KPI cards, then a Plotly line chart and two bar charts.

When adding a new metric or chart, put the aggregation in `metrics.py` (pure function, DataFrame in → DataFrame/scalar out) and only touch `app.py` for the rendering call — this is what keeps the test suite meaningful.

## The `TASKS.md` workflow

`TASKS.md` has three sections — `## To Do`, `## In Progress`, `## Done` — and each milestone is a `### TASK-N: ...` block with acceptance criteria checkboxes, a `Commit:` line, and (once in Done) a `Notes:` line.

The board's own **Definition of Done** (stated at the top of `TASKS.md`) governs whether a milestone can move to `## Done`:
- All acceptance criteria for that task are met
- `streamlit run app.py` runs with no errors or warnings
- The commit(s) implementing it include the milestone ID (e.g. `TASK-3`) in the commit message

Conventions to follow when closing out a milestone:
- The `Commit:` line should point to whichever commit actually makes that task's acceptance criteria true — usually the milestone-tagged commit, but if a later, non-milestone-tagged commit (e.g. a cross-cutting review-fix commit) is what actually satisfies a specific criterion, cite that commit instead and explain why in `Notes:` (see TASK-6's entry for a worked example).
- `Notes:` should record anything that was wrong, incomplete, or changed during verification — not a restatement of the criteria. Use `Notes: clean.` only when re-verification found nothing to flag.
- Board-only commits (moving a task between sections, checking off criteria) are kept separate from code commits, with their own commit message like `TASK-N: mark done on the board`.
- Never mark a task Done without independently re-verifying its acceptance criteria against the current code/tests — don't just trust that the original implementation commit still holds.

## Lessons

Rules distilled from the `Notes:` lines already recorded in `TASKS.md` — read as precedent for how to handle similar situations elsewhere in this repo.

- **Don't blindly replay a stale plan step against code that's moved on.** A plan step written early in the project (e.g. "revert `app.py` to a minimal placeholder" during TASK-1 re-verification) can clobber real functionality built in later, since-completed tasks. If a step would overwrite work from a later milestone, flag it and ask before executing it instead of following the plan literally. (TASK-1)
- **A milestone's acceptance criteria can be made true by a later, non-milestone-tagged commit.** Gaps found in a subsequent review pass — e.g. `EmptyDataError` handling for TASK-2, a deprecated Streamlit kwarg warning for TASK-6 — got fixed in a shared cross-cutting commit (`920c40c`) rather than a new `TASK-N`-tagged one. When verifying a task, check its criteria against the current code and test suite, not just the diff of its original commit. (TASK-2, TASK-6)
- **The `Commit:` line should name whichever commit actually satisfies the criteria**, even when that's not the commit tagged with the milestone ID — and the `Notes:` line should say so explicitly when the two diverge. (TASK-6)
