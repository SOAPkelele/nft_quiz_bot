from typing import Dict, List


class DatabaseBase:
    @staticmethod
    def _insert_args(table: str, column_values: Dict):
        """INSERT INTO {table} ({column}) VALUES ({$1})"""

        columns = ', '.join(column_values.keys())
        placeholders = ", ".join(f"${n}" for n in range(1, len(column_values) + 1))
        query = "INSERT INTO {} ({}) VALUES ({})".format(table, columns, placeholders)

        return query, tuple(column_values.values())

    @staticmethod
    def _select_args(table: str, columns: List[str]):
        """SELECT {column} FROM {table}"""

        columns = ', '.join(columns)
        query = "SELECT {} FROM {}".format(columns, table)
        return query

    @staticmethod
    def _select_where_args(table: str, columns: List[str], conditions: Dict):
        """SELECT {column} FROM {table} WHERE cond_1=val_1 AND ..."""

        columns = ', '.join(columns)
        placeholders = " AND ".join(f"{item} = ${num + 1}" for num, item in enumerate(conditions))
        query = "SELECT {} FROM {} WHERE {}".format(columns, table, placeholders)

        return query, tuple(conditions.values())

    @staticmethod
    def _update_args(table: str, values: Dict, conditions: Dict):
        """UPDATE {table} SET attr_1=val_1, attr_2=val_2... WHERE cond_1=val_1"""
        attributes = ', '.join(f"{key} = {values[key]}" for key in values.keys())
        placeholders = " AND ".join(f"{item} = ${num + 1}" for num, item in enumerate(conditions))
        query = "UPDATE {} SET {} WHERE {}".format(table, attributes, placeholders)

        return query, tuple(conditions.values())
