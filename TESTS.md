***

## Tests

### Overview

The project uses **pytest** for automated testing:

- Logic & data tests (DuckDB + YAML + answers).
- Streamlit UI tests with `streamlit.testing.AppTest`. [docs.streamlit](https://docs.streamlit.io/develop/concepts/app-testing/get-started)

Run all tests:

```bash
uv run pytest
```

***

### 1. Logic / data tests

**File:** `tests/test_exercises_data.py`

These tests verify that your exercise configuration, DuckDB schema, and answer queries are internally consistent.

- `test_all_yaml_exercises_have_answer_files`  
  - Loads `src/srs_sql/config/exercises.yml`.  
  - Extracts every `name` from the `exercises` list.  
  - Asserts that a matching `answers/{name}.sql` file exists for each exercise.

- `test_all_answers_execute_successfully`  
  - Creates a fresh DuckDB connection with `get_connection()`.  
  - Calls `init_base_tables(con)` and `init_exercises(con)` to seed all tables and the `exercises` table.  
  - Iterates over all `*.sql` files in `src/srs_sql/answers/`.  
  - For each file:
    - Reads the query.  
    - Executes it against DuckDB.  
    - Asserts that it returns a `pandas.DataFrame` (i.e. the query is valid and runs without error).

These tests guarantee that:

- Every exercise in YAML has a solution file.  
- Every solution query is executable against the initialized database.

***

### 2. Streamlit UI tests

**File:** `tests/test_app_ui.py`  
(Using `streamlit.testing.v1.AppTest`.)

These tests simulate user interactions with the Streamlit app in-process, without a real browser. [docs.streamlit](https://docs.streamlit.io/develop/concepts/app-testing/get-started)

- `test_app_starts`  
  - Loads `src/srs_sql/app.py` with `AppTest.from_file`.  
  - Runs the app once.  
  - Asserts that the main title (“SRS SQL”) appears in the rendered markdown.

- `test_by_last_review_mode_loads_exercise`  
  - Sets `session_state["review_mode"] = "By last review date"`.  
  - Runs the app.  
  - Asserts that at least one `st.dataframe` is rendered (exercise tables / expected result).  
  - Asserts that an exercise brief (`st.subheader`) is shown.

- `test_by_difficulty_mode_all_themes_selectable`  
  - Sets `session_state["review_mode"] = "By difficulty"`.  
  - Runs the app.  
  - Locates the selectbox labeled “What would you like to review?”.  
  - Iterates over all theme options:
    - Sets the selectbox to each theme.  
    - Runs the app.  
    - Asserts that an exercise brief (`st.subheader`) and at least one `st.dataframe` are rendered for each theme.

- `test_solution_path_is_accepted_for_one_exercise`  
  - Sets `session_state["review_mode"] = "By difficulty"`.  
  - Runs the app.  
  - Chooses the first theme from the theme selectbox.  
  - Reads the solution SQL displayed via `st.text` (last `at.text` value).  
  - Pastes that SQL into the main text area (user query).  
  - Runs the app again.  
  - Asserts that the success message `"You found the right solution."` appears in the markdown output (from `st.write`).

These UI tests ensure that:

- The app renders correctly.  
- Both review modes behave as expected.  
- Each theme can be selected without breaking the app.  
- At least one exercise’s full “solution path” (solution SQL → user input → success feedback) works end-to-end.

***

### How to run tests” 

```bash
# Run everything
uv run pytest

# Only logic/data tests
uv run pytest tests/test_exercises_data.py

# Only UI tests
uv run pytest tests/test_app_ui.py
```