CREATE VIEW calculated_trades_view AS 
SELECT id, timestamp ,buy_value - sell_value AS balance_value,
buy_volume - sell_volume AS balance_volume,
ABS(buy_value / buy_volume) AS buy_price,
ABS(sell_value / sell_volume) AS sell_price
FROM trades;

--This query is not working, 
CREATE VIEW calculated_market_trades_view AS

SELECT timestamp,

CASE
            WHEN diff IS null
            THEN LAG(diff,1) OVER(ORDER BY id)
            ELSE diff
            END


FROM (
	SELECT t1.id, t1.buy_price - t2.price AS diff, t1.timestamp AS timestamp
	FROM calculated_trades_view t1
	LEFT JOIN market_price t2 ON DATE(t1.timestamp) = DATE(t2.timestamp) AND 
	EXTRACT(HOUR FROM t2.timestamp) = EXTRACT(HOUR FROM t1.timestamp)) AS subquery;

SELECT * FROM calculated_market_trades_view