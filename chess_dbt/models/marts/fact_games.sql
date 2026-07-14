{{
    config(
        materialized='incremental',
        unique_key='url'
    )
}}

SELECT 
    url,
    game_type,
    time_control,
    white_player_name,
    white_rating,
    white_result,
    black_player_name,
    black_rating,
    black_result,
    pgn,
    
    -- New logic to determine the game winner
    CASE 
        WHEN white_result = 'win' THEN 'White'
        WHEN black_result = 'win' THEN 'Black'
        ELSE 'Draw'
    END AS winner
    
FROM {{ ref('stg_raw_games') }}

{% if is_incremental() %}
    WHERE url NOT IN (SELECT url FROM {{ this }})
{% endif %}