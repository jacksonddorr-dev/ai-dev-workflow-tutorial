# Tasks

This file tracks all work for the ShopSmart sales dashboard (see [prd/ecommerce-analytics.md](prd/ecommerce-analytics.md)).

## Definition of Done

A milestone can only move to Done when:

- Its acceptance criteria (below) are all met
- The app runs locally with `streamlit run app.py` with no errors or warnings
- Changes are committed with the milestone ID (e.g. `TASK-1`) in the commit message

## To Do

### TASK-3: KPI cards implementation
Display the Total Sales and Total Orders KPIs at the top of the dashboard.
- [ ] Total Sales and Total Orders are both displayed prominently
- [ ] Currency is formatted as $X,XXX,XXX and large numbers use separators
- [ ] Values match the PRD's expected output (~$116,500 / 482 orders)

Commit:

### TASK-4: Sales trend chart
Add an interactive line chart showing sales over time.
- [ ] Line chart plots sales by date (daily or monthly) with sales amount on the Y-axis
- [ ] Tooltips show exact values on hover
- [ ] Chart renders within 2 seconds of data load

Commit:

### TASK-5: Category and region breakdowns
Add bar charts for sales by product category and by region.
- [ ] Category bar chart shows all 5 categories, sorted highest to lowest, with tooltips
- [ ] Region bar chart shows all 4 regions, sorted highest to lowest, with tooltips
- [ ] Electronics appears as the top category, matching the PRD's expected output

Commit:

### TASK-6: Testing and refinement
Verify the full dashboard against the PRD's acceptance criteria and clean up rough edges.
- [ ] All 7 acceptance criteria in the PRD are checked off
- [ ] Dashboard loads within 5 seconds with no errors or warnings
- [ ] Layout and labels are polished enough for an executive presentation

Commit:

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the finished dashboard and confirm it's publicly reachable.
- [ ] App is deployed to Streamlit Community Cloud
- [ ] Public URL loads the dashboard correctly for a stakeholder with no local setup
- [ ] Deployed version matches the tested local version (same data, same charts)

Commit:

## In Progress

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
