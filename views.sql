CREATE VIEW calculated_trades_view AS 
SELECT id, timestamp ,
buy_value - sell_value AS balance_value,
buy_volume - sell_volume AS balance_volume,
ABS(buy_value / buy_volume) AS buy_price,
ABS(sell_value / sell_volume) AS sell_price
FROM trades;

