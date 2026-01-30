# SRS SQL – Functional Specification

A concise functional spec for the **SRS SQL** Streamlit app, suitable for `docs/functional_spec.md` in a GitHub repo. Structure is inspired by common SRS/FS templates. 

***

## 1. Overview

**SRS SQL** is a Streamlit app that lets users practice SQL against a local DuckDB database using a **Spaced Repetition System (SRS)**.  
Users pick a theme (e.g. joins, window functions), see example tables, write SQL, and get immediate feedback against a reference solution, with review scheduling based on success. 

### 1.1 Goals

- Provide a lightweight, local web UI to practice SQL.
- Cover progressive difficulty: basic `SELECT` → joins → window functions → DDL → CTE “procedural” patterns.
- Use SRS-style scheduling (`last_reviewed`) to repeat exercises at spaced intervals.

### 1.2 Non-goals

- No authentication or multi-user management.
- No remote database connections (only local DuckDB file).
- No exercise authoring UI (exercises added via code + `.sql` files).

***

## 2. User stories

- **As a learner**, I want to pick a theme (e.g. window functions) and get an exercise so I can focus on a concept.  
- **As a learner**, I want to see the underlying tables and expected result so I understand the target.  
- **As a learner**, I want to run my SQL and see if it matches the expected result, with clear differences if not.  
- **As a learner**, I want SRS buttons that schedule the next review so I don’t have to track it manually.  
- **As a maintainer**, I want to add new exercises and solutions without changing the app logic.

***

## 3. Core features

### 3.1 Exercise catalog & themes

- Exercises stored in DuckDB table `exercises` with:
  - `theme`: text, e.g. `cross_joins`, `window_functions`.
  - `name`: text, unique per exercise, used as filename key.
  - `tables_names`: list/array of table names used by the exercise.
  - `last_reviewed`: date used for SRS ordering.

**Checklist**

- [ ] `exercises` table is created on init with all exercises seeded.  
- [ ] `theme` values include at least: `cross_joins`, `select_basics`, `filtering`, `aggregations`, `joins`, `window_functions`, `ddl`, `procedural_style`.  
- [ ] Every `name` has a corresponding `answers/{name}.sql` file.

### 3.2 Theme selection & exercise pick

- Sidebar `selectbox` lists all distinct themes from `exercises`.
- When a theme is selected:
  - App queries `exercises WHERE theme = :theme ORDER BY last_reviewed ASC`.
  - First row becomes the current exercise.
- If no theme is selected:
  - App uses all exercises ordered by `last_reviewed` and picks the first.

**Checklist**

- [ ] Theme dropdown populated from `SELECT DISTINCT theme FROM exercises`.  
- [ ] Current exercise is always the row with smallest `last_reviewed` in the selected scope.  
- [ ] Selected exercise’s data is visible in the UI (name, theme, last_reviewed).

***

## 4. Exercise details & solution

### 4.1 Tables display

- For the current exercise, app reads `tables_names` (list).
- For each table:
  - Runs `SELECT * FROM "{table}"`.
  - Displays it in the “Tables” tab (column layout).

**Checklist**

- [ ] Every table in `tables_names` is displayed with a title `table: {name}`.  
- [ ] Errors for missing tables are caught and shown as user-facing messages.  

### 4.2 Expected result display

- The app loads solution SQL from `answers/{exercise_name}.sql`.
- Runs the solution query against DuckDB.
- Displays the resulting DataFrame as “expected” in the “Tables” tab.

**Checklist**

- [ ] If the `.sql` file is missing, a clear message is shown instead of crashing.  
- [ ] Solution result is computed once per exercise selection (not on every keystroke).  

### 4.3 Solution SQL display

- “Solution” tab shows the full solution SQL as plain text.

**Checklist**

- [ ] Solution SQL is rendered as monospaced text preserving formatting.  
- [ ] A missing `.sql` file does not break the app (graceful fallback).

***

## 5. User query & auto-checking

### 5.1 Input & execution

- Main body has a text area labeled “your SQL code here”.
- On change/submit, app:
  - Executes the user query via DuckDB.
  - Displays the resulting DataFrame.

**Checklist**

- [ ] User query is executed against the same DuckDB connection as the solution.  
- [ ] DuckDB syntax errors and missing-table errors are caught and displayed.  

### 5.2 Comparison with expected result

- If a solution is loaded:
  - App compares number of rows.
  - Reorders user result columns to match `solution_df.columns`.
  - Uses `DataFrame.compare()` to find differences.
  - If no differences:
    - Shows success message “You found the right solution.”
    - Triggers Streamlit `st.balloons()`.

**Checklist**

- [ ] Row count difference is computed and displayed (more/less lines).  
- [ ] If columns differ, user sees a “Some columns are missing or different.” message.  
- [ ] On exact match (rows & values), app shows success + balloons.  

***

## 6. SRS (Spaced Repetition) behavior

### 6.1 Review scheduling buttons

- Buttons for the current exercise:
  - “Review in 2 days”
  - “Review in 7 days”
  - “Review in 21 days”
- On click:
  - Compute `next_review = today + N days`.
  - Update `exercises.last_reviewed` for the current `name`.
  - Call `st.rerun()` to reload and pick the next due exercise.

**Checklist**

- [ ] `last_reviewed` is updated correctly in DuckDB for the current exercise only.  
- [ ] After rerun, the next exercise due surfaces as the first in the list.  

### 6.2 Reset

- “Reset” button:
  - Sets all `last_reviewed` values to `'1970-01-01'`.
  - Calls `st.rerun()`.

**Checklist**

- [ ] Reset sets every row’s `last_reviewed` uniformly.  
- [ ] After reset, the first exercise is deterministic (e.g. by seed order).

***

## 7. Initialization & data model

### 7.1 Database file & connection

- On app start:
  - Ensure `data/` directory exists.
  - Ensure `data/sql_exercises.duckdb` exists.
- Open a single read/write DuckDB connection shared across app components.

**Checklist**

- [ ] Creating `data` folder is idempotent (`exist_ok=True`).  
- [ ] If DB file is missing, initialization creates it and seeds all tables.  

### 7.2 Seeding exercises and tables

- Initialization function:
  - Creates `EXERCISES` DataFrame with all exercise metadata.
  - Loads CSV-like sample data into pandas and upserts to DuckDB tables:
    - `beverages`, `food_items`, `sizes`, `trademarks`,
    - `employees`, `orders`, `customers`,
    - `sales`, `products`.
  - Drops/recreates `exercises` and each base table.

**Checklist**

- [ ] Running init multiple times yields the same database state.  
- [ ] All exercises in `EXERCISES` refer to existing DuckDB tables.  

***

## 8. Non-functional constraints

- **Performance**:  
  - Execution and comparison for typical exercises should complete within a few seconds. 
- **Reliability**:  
  - User SQL errors must not crash the app; they are handled and shown.
- **Extensibility**:  
  - Adding a new exercise requires:
    - Adding a row to `EXERCISES` (init code).
    - Providing `answers/{exercise_name}.sql`.
  - No changes in the main Streamlit app logic.

***
