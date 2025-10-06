## StockPrice_ETL
This project uses Apache Airflow to automatically fetch daily stock prices from the Alpha Vantage API and load them into Snowflake. It helps keep stock data updated every day for easy analysis and reporting.

## Stock Price ETL DAG
This Airflow Directed Acyclic Graph (DAG) extracts daily stock pricing data using the Alpha Vantage API and loads it into a Snowflake table. It's designed to automate the process of fetching stock market data, making it available for analysis, reporting, or other data-driven applications.

## Prerequisites
Before running this DAG, ensure you have the following configured in your Airflow environment:

Snowflake Connection: A connection named snowflake_conn must be set up in Airflow with your Snowflake account credentials.

Alpha Vantage API Key: An API key from Alpha Vantage is required to fetch stock data. This key should be stored as an Airflow Variable with the key alpha_vantage_api_key.

Required Python Libraries: The following libraries must be installed in your Airflow environment:

apache-airflow-providers-snowflake

requests

snowflake-connector-python

## DAG Description
The DAG, named StockPrice_ETL_v3, is scheduled to run daily at 2:30 AM. It consists of two main tasks:

extract
This task uses the Alpha Vantage API to fetch daily stock price data for a specified symbol. By default, it retrieves data for GOOG (Google). It handles the API call, parses the JSON response, and returns a list of dictionaries, where each dictionary represents a day's stock information (open, high, low, close, and volume prices).

load_to_snowflake
This task takes the extracted data and performs a series of operations to load it into a Snowflake table.

Table Creation: It first ensures the target table (Raw.stock_table by default) exists with the correct schema.

Data Insertion: It iterates through the list of stock data and inserts each record into the table.

Transaction Management: It uses SQL transactions (BEGIN; and COMMIT;) to ensure data integrity. If any error occurs during the insertion process, it executes a ROLLBACK; to prevent partial data loads.

## Customization
You can easily modify this DAG to suit your needs:

Change the Stock Symbol: In the DAG definition, you can change the stock symbol passed to the extract task to fetch data for a different company.

Python

extracted_data = extract("MSFT") # e.g., to get Microsoft stock data
Change the Target Table: You can modify the target_table variable to specify a different table in your Snowflake warehouse.

Adjust Schedule: The schedule parameter in the DAG definition can be modified to change the frequency of the data extraction. For example, schedule='0 9 * * 1-5' would run the DAG at 9 AM on weekdays.

## 🧱 Architecture

      +----------------------+
      |  Alpha Vantage API   |
      +----------+-----------+
                 |
                 v
      +----------------------+
      |   Airflow DAG (ETL)  |
      |  - Extract Task      |
      |  - Load Task         |
      +----------+-----------+
                 |
                 v
      +----------------------+
      |  Snowflake Database  |
      |  Table: RAW.STOCK_TABLE |
      +----------------------+
