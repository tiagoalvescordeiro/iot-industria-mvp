def test_sql_has_create_table():
    sql = open("db/create_tables.sql", "r", encoding="utf-8").read().lower()
    assert "create table" in sql and "readings" in sql, "SQL must create table readings"
