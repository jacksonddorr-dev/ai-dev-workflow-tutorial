# Tasks

This file tracks all work for the ShopSmart sales dashboard (see [prd/ecommerce-analytics.md](prd/ecommerce-analytics.md)).

## Definition of Done

A milestone can only move to Done when:

- Its acceptance criteria (below) are all met
- The app runs locally with `streamlit run app.py` with no errors or warnings
- Changes are committed with the milestone ID (e.g. `TASK-1`) in the commit message

## To Do

## In Progress

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the finished dashboard and confirm it's publicly reachable.
- [ ] App is deployed to Streamlit Community Cloud
- [ ] Public URL loads the dashboard correctly for a stakeholder with no local setup
- [ ] Deployed version matches the tested local version (same data, same charts)

Commit:

## Done

### TASK-1: Environment setup and project initialization
Set up the Python project structure, dependencies, and repo layout needed to build the dashboard.
- [x] `requirements.txt` (or equivalent) lists Streamlit, Pandas, and Plotly
- [x] Project runs in a clean virtual environment with no missing dependencies
- [x] Basic `app.py` exists and launches without error

Commit: 3f5bf66
Notes: When re-verifying this task, the plan's original step would have
reverted app.py to a minimal placeholder page — I flagged that it would
have overwritten the full dashboard already built in Tasks 2-6, and asked
before touching it. Jackson chose to skip that step and keep app.py as-is;
verified it still launches cleanly instead of checking for an "empty" page.

### TASK-2: Data loading and basic structure
Load `data/sales-data.csv` into a Pandas DataFrame and validate its structure.
- [x] CSV loads without errors and handles date, numeric, and categorical columns correctly
- [x] Row count matches the PRD's expected 482 transaction records
- [x] Malformed/missing data is validated or handled gracefully

Commit: a009d1f
Notes: The "malformed/missing data" handling grew after this task's
original commit — a later review round (during final branch review)
found a gap where a genuinely empty CSV raised an unfriendly pandas
error instead of the loader's own ValueError, and fixed it in commit
920c40c. Re-verified all 5 current tests pass against that fixed
version, not just the original.

### TASK-3: KPI cards implementation
Display the Total Sales and Total Orders KPIs at the top of the dashboard.
- [x] Total Sales and Total Orders are both displayed prominently
- [x] Currency is formatted as $X,XXX,XXX and large numbers use separators
- [x] Values match the PRD's expected output (~$116,500 / 482 orders)

Commit: d914cff
Notes: clean. Re-verified independently against the real CSV: Total
Sales "$116,500", Total Orders "482" — exact match to the PRD.

### TASK-4: Sales trend chart
Add an interactive line chart showing sales over time.
- [x] Line chart plots sales by date (daily or monthly) with sales amount on the Y-axis
- [x] Tooltips show exact values on hover
- [x] Chart renders within 2 seconds of data load

Commit: ca26e16
Notes: clean. Re-verified sales_over_time against the real CSV: 12
monthly points, correctly summed and chronologically ordered. Tooltips
come from Plotly's default hover behavior (nothing in the code
suppresses it); render time is trivial at 482 rows.

### TASK-5: Category and region breakdowns
Add bar charts for sales by product category and by region.
- [x] Category bar chart shows all 5 categories, sorted highest to lowest, with tooltips
- [x] Region bar chart shows all 4 regions, sorted highest to lowest, with tooltips
- [x] Electronics appears as the top category, matching the PRD's expected output

Commit: 214cf12
Notes: clean. Re-verified against the real CSV: 5 categories sorted
descending with Electronics on top ($42,683.67), 4 regions (North, West,
East, South) sorted descending — exact match to the PRD.

### TASK-6: Testing and refinement
Verify the full dashboard against the PRD's acceptance criteria and clean up rough edges.
- [x] All 7 acceptance criteria in the PRD are checked off
- [x] Dashboard loads within 5 seconds with no errors or warnings
- [x] Layout and labels are polished enough for an executive presentation

Commit: 920c40c
Notes: This task's own acceptance criteria specifically require "no
errors or warnings" — the original TASK-6 commit (216db94) still had a
deprecated-Streamlit-kwarg warning on every chart render, only actually
fixed later in 920c40c during the final branch review. Using 920c40c as
the commit here since that's the one that makes this task's own criteria
true, not just the one that first touched app.py for it. Re-verified:
14/14 tests pass, live app loads in well under 5s with zero warnings in
the server log, page icon/title/caption/wide-layout polish all present
in app.py.
