{{ config(
    materialized='external', 
    location='output/netflix_top_shows.csv', 
    format='csv'
 )}}

-- SQL GOES HERE


{{ config(
    materialized='external',
    location='output/netflix_top_shows.csv',
    format='csv'
)}}

SELECT
    "As of" as date_label,
    Rank,
    Title,
    Type
FROM
    's3://uvasds-systems/data/netflix_daily_top_10.parquet'
WHERE
    Rank = 1
ORDER BY
    date_label