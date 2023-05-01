# Dashboard Layout Generator Microservice

This project is a microservice that generates a dashboard for time-series visualization.
The datasets are available in the "data" directory, representing the flows (buy/sell) on the wholesale market in € and MWh (dataset2.csv) and the prices (prices.csv) in €/MWh.

The user can visualize the following set of data:

* Buy/Sell volumes
* Buy/Sell values
* Buy/Sell wholesale prices
* Balance

For each time-series, the user can also retrieve the following KPIs:

* Last_cumulated_value (yearly, monthly, or daily)
* Average_value (yearly, monthly, or daily)
* The relative difference between the last cumulated value and the previous one (yearly, monthly, or daily)


# Local Run

To run locally, follow these steps:

Install the required packages by running:

```bash
pip install -r requirements.txt
```

Start the Flask server by running:

```bash
flask run
```

In another terminal tab, run the following command to prepare the data for importing into the database:

```bash
python helper.py
```

This code allows you to get the _sorted.csv data files, which are ready to be imported into the database tables directly in PgAdmin:

prices.csv -> market_price
dataset2.csv -> trades


In PgAdmin, run the code to create the sql views calculated_trades_views.

Finally, run the tests using the following command:

```bash
pytest -s -v
```

# Still to do 
I wanted also to create an the sql view calculated_market_trades_view that allows to evaluate the (buy or sell)_price_spread, calculated
as the difference from the buy/sell wholesale price and the market price.
