SELECT 
    url, -- Kept exclusively as the Primary Key for the incremental model
    
    CASE 
        WHEN rated THEN 'Rated Game'
        WHEN NOT rated THEN 'Casual Game'
        ELSE 'Unknown'
    END AS game_type,
    
    time_control,
    pgn,
    
    -- Flattening the nested JSON objects
    white->>'username' AS white_player_name,
    CAST(white->>'rating' AS INTEGER) AS white_rating,
    white->>'result' AS white_result,
    
    black->>'username' AS black_player_name,
    CAST(black->>'rating' AS INTEGER) AS black_rating,
    black->>'result' AS black_result

FROM raw.games