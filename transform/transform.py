import os
import duckdb

input_file = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet"


    """_summary_
    0. set up a duckdb connection
    1. drop table if it exists
    2. read the parquet in as a new table
    3. count the number of records
    4. save the new table as a local parquet file
    5. push the table to a remote RDS instance
    """


def duckdb_read_parquet(input_file):

    con = None

    try:
        # Connect to local DuckDB instance
        con = duckdb.connect(database='transform.duckdb', read_only=False)

        
        con.execute(f"""
            DROP TABLE IF EXISTS yellow_tripdata_202501;
        """)
        print("Table has been dropped")
        
        con.execute(f"""
            CREATE TABLE yellow_tripdata_202501 AS SELECT * FROM read_parquet('{input_file}');
        """)
        
        con.execute(f"""
            SELECT COUNT(*) FROM yellow_tripdata_202501;
        """)
        
        con.execute(f"""
            CREATE TABLE yellow_tripdata_202501_clean AS
            SELECT DISTINCT * FROM yellow_tripdata_202501;
            
            DROP TABLE yellow_tripdata_202501;
            ALTER TABLE yellow_tripdata_202501_clean RENAME TO yellow_tripdata_202501;
        """)
        
        con.execute(f"""
            COPY yellow_tripdata_202501 TO '{local_parquet}' {FORMAT PARQUET};
        """)
        
        con.execute(f"""
            ATTACH '' AS rds (TYPE MYSQL, SECRET rds);
        """)
        
        con.execute(f"""
            DROP TABLE IF EXISTS rds.yellow_tripdata_202501;
            CREATE TABLE rds.yellow_tripdata_202501 
                AS 
            SELECT * FROM transform.yellow_tripdata_202501 LIMIT 100000;
        """)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    duckdb_read_parquet(input_file)