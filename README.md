# SRS SQL – Spaced Repetition System for SQL

SRS SQL is a small Streamlit app that lets you **practice SQL with a Spaced Repetition System (SRS)** on top of a local DuckDB database.

You pick how to review (oldest exercises first, or by difficulty), solve business‑style SQL questions, and the app tracks when each exercise was last reviewed.

***

## Features

- **Local, fast SQL practice** with DuckDB.
- **Spaced Repetition System**:
  - “Review in 2 / 7 / 21 days” buttons per exercise.
  - Exercises ordered by `last_reviewed` or by `difficulty`.
- **Progressive difficulty**:
  - Basics (`SELECT`, filtering).
  - Aggregations & joins.
  - Window functions.
  - DDL & “procedural style” CTEs.
- **Business‑style instructions** for each exercise (not just “write a query”).
- **Automatic checking**:
  - Compare your query result to the reference solution.
  - Row count hints and value differences.
- **Config-driven metadata** via a YAML file (`exercises.yml`).

***

## Project structure

```text
.
├─ pyproject.toml
├─ README.md
├─ data/
│  └─ sql_exercises.duckdb        # created at runtime
└─ src/
   └─ srs_sql/
      ├─ __init__.py
      ├─ app.py                   # Streamlit UI
      ├─ db.py                    # DuckDB connection + initialization
      ├─ models.py                # Exercise model + SRS logic
      ├─ config/
      │  └─ exercises.yml         # Exercise metadata (theme, difficulty, instructions)
      └─ answers/
         └─ *.sql                 # Reference solutions for each exercise
```

***

## Installation

This project uses **uv** for dependency and project management. [docs.astral](https://docs.astral.sh/uv/concepts/projects/config/)

1. Install uv (if not already):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repo:

```bash
git clone https://github.com/<your-username>/SRS_SQL.git
cd SRS_SQL
```

3. Install dependencies and create the virtual env:

```bash
uv sync
```

***

## Running the app

From the project root:

```bash
uv run streamlit run src/srs_sql/app.py
```

This will:

- Ensure `data/sql_exercises.duckdb` exists.
- Seed base tables (`employees`, `orders`, `customers`, `sales`, etc.).
- Load all exercises from `src/srs_sql/config/exercises.yml` into DuckDB.
- Start the Streamlit app in your browser (by default at `http://localhost:8501`). [discuss.streamlit](https://discuss.streamlit.io/t/specify-requirements-txt/48291)

***

## How it works

### Exercises & difficulty

Exercises are defined in **YAML** (`src/srs_sql/config/exercises.yml`) as a list of entries:

```yaml
exercises:
  - name: employees_basic_select
    theme: select_basics
    difficulty: 1
    tables:
      - employees
    instruction: >
      HR wants a simple list of all employees with their department and salary.
  # ...
```

Each exercise has:

- `name`: unique id, also used as `answers/{name}.sql`.
- `theme`: conceptual group (e.g. `window_functions`).
- `difficulty`: integer (1 = easy, higher = harder).
- `tables`: tables used in the exercise.
- `instruction`: business-style description of the problem.

On startup, `db.py` reads this YAML, builds a `pandas` DataFrame, and creates a DuckDB table `exercises` with:

- `theme`
- `name`
- `tables_names` (list of table names)
- `difficulty`
- `last_reviewed`
- `instruction`

### Review modes

In the sidebar you can choose a **review mode**:

- **By last review date**:
  - Ignores theme.
  - Selects the exercise with the **oldest `last_reviewed`**, breaking ties by `difficulty`.
  - Ideal for pure SRS reviewing.

- **By difficulty**:
  - First lets you pick a **theme**.
  - Within that theme, picks the **easiest** (`difficulty ASC`) exercise, breaking ties by `last_reviewed`.
  - Good for focused practice on a concept.

### Spaced Repetition buttons

For the current exercise:

- “Review in 2 days”
- “Review in 7 days”
- “Review in 21 days”

Each button sets `last_reviewed` for the current exercise to `today + N days` and reruns the app so the next exercise becomes due.

A **“Reset”** button sets `last_reviewed` to `1970-01-01` for all exercises, so you can restart the cycle.

### Solutions and automatic checking

For each exercise:

- The app loads `answers/{exercise_name}.sql`.
- Executes it to compute the **expected result**.
- When you run your own SQL, the app:
  - Executes it against the same DuckDB database.
  - Shows your result.
  - Compares row counts and column values against the expected result.
  - Highlights differences, or celebrates success with `st.balloons()` if they match.

***

## Adding a new exercise

1. **Add metadata** in `config/exercises.yml`:

```yaml
  - name: customers_without_orders
    theme: joins
    difficulty: 2
    tables:
      - customers
      - orders
    instruction: >
      Find all customers with no orders.
```

2. **Create the solution** in `answers/customers_without_orders.sql`:

```sql
SELECT c.*
FROM customers c
LEFT JOIN orders o
  ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL
ORDER BY c.customer_id;
```

3. Restart the app (or let it rerun); the new exercise will be picked up automatically on init.

***

## Roadmap / ideas

- **User accounts / progress tracking**:
  - Simple username login.
  - Store success / failure counts per exercise in DuckDB.
  - Show per-theme progress and mastery.

- **More exercise metadata**:
  - Tags (`joins`, `GROUP BY`, `window`, etc.).
  - Estimated difficulty/time.
  - Hints and step-by-step unlocks.

- **Exportable progress**:
  - Download progress as CSV or JSON.
  - Sync with a remote DuckDB / MotherDuck instance.

***

## Development

Install dev tools:

```bash
uv sync --group dev
```

Run linting:

```bash
uv run ruff check src
uv run ruff format src
```

Run tests (when added):

```bash
uv run pytest
```

***

