from pathlib import Path

import duckdb

############
#Block A: Connect to DB
############
project_root = Path(__file__).resolve().parents[1]
db_path = project_root / "chess_dbt" / "dev.duckdb"
parquet_pattern = project_root / "data" / "games" / "date=*" / "*.parquet"

con = duckdb.connect(str(db_path))

############
#Block B: RAW Room
############
con.execute("CREATE SCHEMA IF NOT EXISTS raw")
con.execute("SET SCHEMA 'raw'")

############
#Block C: Magic Window with rules
############
con.execute("""
    CREATE OR REPLACE VIEW raw.games AS 
    SELECT * 
    FROM read_parquet(
        '{parquet_path}', 
        hive_partitioning=1, 
        union_by_name=True
    )
""".format(parquet_path=parquet_pattern.as_posix()))

print("Successfully created the 'raw.games' view with Hive Partitioning and Union-by-Name")
