# pylint: disable=missing-module-docstring
import duckdb
import pandas as pd
import streamlit as st

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ANSWERS_DIR = BASE_DIR / "answers"

class Exercise:
    """
    Represents the current exercise being worked on.
    """

    def __init__(self, con: duckdb.DuckDBPyConnection):
        self._con = con
        self.name = ""
        self.tables_names: list[str] = []
        self.solution_query = ""
        self.solution_df: pd.DataFrame = pd.DataFrame()
        self.instruction = ""

    def load_from_theme(self, theme_selected: str | None, review_mode: str) -> None:
        """
        Load current exercise based on:
        - review_mode:
            "By last review date": ignore theme, pick oldest last_reviewed globally
            "By difficulty": within a theme, easiest + least reviewed
        - theme_selected: only used when review_mode == "By difficulty"
        """

        params = []

        if review_mode == "By last review date":
            # Pure SRS: oldest last_reviewed in the whole table
            query = """
                SELECT *
                FROM exercises
                ORDER BY last_reviewed ASC, difficulty ASC
            """
        else:
            # By difficulty: if a theme is selected, restrict to it
            if theme_selected:
                query = """
                    SELECT *
                    FROM exercises
                    WHERE theme = ?
                    ORDER BY difficulty ASC, last_reviewed ASC
                """
                params.append(theme_selected)
            else:
                # No theme selected yet: nothing to load
                self.name = ""
                return

        df = self._con.execute(query, params).df()
        if df.empty:
            self.name = ""
            return

        current = df.iloc[0]

        self.name = current["name"]
        self.tables_names = current["tables_names"]
        self.instruction = current.get("instruction", "")

        answer_path = ANSWERS_DIR / f"{self.name}.sql"
        if not answer_path.exists():
            st.write(f"Missing answer file: {answer_path}")
            self.solution_query = ""
            self.solution_df = pd.DataFrame()
            return

        with answer_path.open("r", encoding="utf-8") as f:
            self.solution_query = f.read()

        self.solution_df = self._con.execute(self.solution_query).df()
        
    # -------- display helpers --------

    def show_tables(self) -> None:
        """
        Display the tables for the current exercise.
        """
        for table in self.tables_names:
            st.write(f"table: {table}")
            df_table = self._con.execute(f'SELECT * FROM "{table}"').df()
            st.dataframe(df_table)

    def show_expected(self) -> None:
        """
        Display the expected result (solution_df).
        """
        if not self.solution_df.empty:
            st.write("expected:")
            st.dataframe(self.solution_df)

    def show_solution(self) -> None:
        """
        Display the solution SQL.
        """
        if self.solution_query:
            st.text(self.solution_query)

    def check_user_solution(self, user_query: str) -> None:
        """
        Execute and compare user SQL to the solution.
        """
        if not user_query:
            return

        try:
            input_df = self._con.execute(user_query).df()
            st.dataframe(input_df)

            if self.solution_df.empty:
                st.write("No solution loaded for comparison.")
                return

            nb_lines_difference = self.solution_df.shape[0] - input_df.shape[0]
            if nb_lines_difference != 0:
                if nb_lines_difference > 0:
                    st.write(f"The solution has {nb_lines_difference} lines more.")
                else:
                    st.write(f"The solution has {-nb_lines_difference} lines less.")

            try:
                input_df = input_df[self.solution_df.columns]
                comparison_result = input_df.compare(self.solution_df)
                if comparison_result.empty:
                    st.write("You found the right solution.")
                    st.balloons()
                else:
                    st.write("Not yet, here are the differences :")
                    st.dataframe(comparison_result)
            except KeyError:
                st.write("Some columns are missing or different.")
            except ValueError as e:
                st.write(f"{e}")

        except duckdb.ParserException as e:  # <- change here
            st.write("incorrect input sent, not an SQL command")
            st.write(f"{e}")
        except duckdb.CatalogException as e:  # <- and here
            st.write(f"{e}")
            
    def srs_buttons(self) -> None:
        """
        Spaced Repetition buttons: update last_reviewed.
        """
        from datetime import date, timedelta

        for n_days in [2, 7, 21]:
            if st.button(f"Review in {n_days} days"):
                next_review = date.today() + timedelta(days=n_days)
                self._con.execute(
                    "UPDATE exercises "
                    "SET last_reviewed = ? "
                    "WHERE name = ?",
                    [str(next_review), self.name],
                )
                st.rerun()

        if st.button("Reset"):
            self._con.execute("UPDATE exercises SET last_reviewed = '1970-01-01'")
            st.rerun()
