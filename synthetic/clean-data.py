import os
import duckdb

input_file = "https://s3.amazonaws.com/uvasds-systems/data/synthdata.parquet"

def clean_parquet():

    con = None

    try:
        # Connect to local DuckDB
        con = duckdb.connect(database='synthdata.duckdb', read_only=False)

        # Clear and ipmort
        con.execute(f"""
            -- SQL goes here
            DROP TABLE IF EXISTS synthdata;
            CREATE TABLE synthdata
                AS
            SELECT * FROM read_parquet('{input_file}');
        """)
        
        con.execute("""
            ALTER TABLE synthdata
            ADD COLUMN age INTEGER;
            UPDATE synthdata
                SET age = date_diff('year', 'birth_date', CURRENT_DATE)
        """)

        con.execute("""
            DELETE FROM synthdata
            WHERE score IS NULL;
        """)
        
        con.execute("""
            CREATE TABLE synthdata_clean AS
            SELECT DISTINCT * FROM synthdata;
            
            DROP TABLE synthdata;
            ALTER TABLE synthdata_clean RENAME TO synthdata;
        """)
        
        maxage = con.execute("""
            SELECT MAX(age) FROM synthdata;
        """)

        minage = con.execute("""
            SELECT MIN(age) FROM synthdata;
        """)
        
        too_old = con.execute("""
            SELECT COUNT(*) FROM synthdata
            WHERE age > 100;
        """)
        
        count = con.execute("""
            SELECT COUNT(*) FROM synthdata;
        """)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    clean_parquet()

