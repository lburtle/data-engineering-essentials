import os
import duckdb

input_file = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet"
local_parquet = "yellow_cab_202501.parquet"

"""
- 0. set up DB connection
- 1. drop table if it exists
- 2. create new table from parquet file
- 3. count # of records in imported table
- 4. do some basic cleaning
- 5. save table as local parquet file
6. export/push data to MySQL RDS instance
"""

def duckdb_read_parquet():

    con = None

    try:
        # Connect to local DuckDB instance
        con = duckdb.connect(database='transform.duckdb', read_only=False)
        print("DuckDB connection established")

        con.execute(f"""
            -- SQL goes here
            DROP TABLE IF EXISTS yellow_tripdata_202501;
        """)
        print("Dropped table if exists")

        con.execute(f"""
            CREATE TABLE yellow_tripdata_202501
                AS
            SELECT * FROM read_parquet('{input_file}');
        """)
        print("Imported parquet file to DuckDB table")

        count = con.execute(f"""
            SELECT COUNT(*) FROM yellow_tripdata_202501;
        """)
        print(f"Number of records in table: {count.fetchone()[0]}")

        con.execute(f"""
            -- Create a new table with unique rows
            CREATE TABLE yellow_tripdata_202501_clean AS 
            SELECT DISTINCT * FROM yellow_tripdata_202501;

            -- Drop original and rename
            DROP TABLE yellow_tripdata_202501;
            ALTER TABLE yellow_tripdata_202501_clean RENAME TO yellow_tripdata_202501;
        """)
        print("Deduped the data set")

        con.execute(f"""
            -- Save as parquet
            COPY yellow_tripdata_202501 TO '{local_parquet}' (FORMAT PARQUET);
        """)
        print("Saved as local parquet")

        con.execute(f"""
            -- Attach to remote RDS instance using secret
            ATTACH '' AS rds (TYPE MYSQL, SECRET rds);
        """)
        print("Attached to RDS instance")

        con.execute(f"""
            -- Drop table
            DROP TABLE IF EXISTS yellow_tripdata_202501;
        """)

        con.execute(f"""                    
            -- Export table into remote RDS
            CREATE TABLE rds.yellow_tripdata_202501
                AS
            SELECT * FROM yellow_tripdata_202501 LIMIT 100000;
        """)
        print("Exported into RDS table")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    duckdb_read_parquet()