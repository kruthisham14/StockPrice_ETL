from airflow import DAG 
from airflow.models import Variable
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

from datetime import timedelta
from datetime import datetime
import snowflake.connector
import requests

def return_snowflake_conn():
  hook = SnowflakeHook(snowflake_conn_id = 'snowflake_conn')

  conn = hook.get_conn()
  return conn.cursor()

@task
def extract(symbol = "GOOG"):
    try:
        alpha_vantage_api_key = Variable.get("alpha_vantage_api_key")
        #symbol = "GOOG" #SC Changes
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={alpha_vantage_api_key}'
        r = requests.get(url)
        data = r.json()

        results = []
        for d in data['Time Series (Daily)']:
            stock_info = data['Time Series (Daily)'][d]
            #stock_info["date"] = d #SC Changes
            #results.append(stock_info)
            results.append({
                "symbol": symbol,
                "date": d,
                "open": stock_info["1. open"],
                "high": stock_info["2. high"],
                "low": stock_info["3. low"],
                "close": stock_info["4. close"],
                "volume": stock_info["5. volume"]
            })
        return results
    except Exception as e:
       print(e)
       raise


@task
def load_to_snowflake(results, target_table):
   import datetime
   cur = return_snowflake_conn()
   try:
      cur.execute("BEGIN;")
      cur.execute(f"""
      CREATE TABLE IF NOT EXISTS {target_table} (
          SYMBOL VARCHAR(10) NOT NULL,
          DATE DATE NOT NULL,
          OPEN FLOAT NOT NULL,
          HIGH FLOAT NOT NULL,
          LOW FLOAT NOT NULL,
          CLOSE FLOAT NOT NULL,
          VOLUME FLOAT NOT NULL,
          PRIMARY KEY (SYMBOL, DATE)
      )
      """)

      cur.execute(f"DELETE FROM {target_table}")

      for r in results:
         #For debug purpose type conversion for snowflake
         date_val = datetime.datetime.strptime(r["date"], "%Y-%m-%d").date()
         open_val = float(r["open"])
         high_val = float(r["high"])
         low_val = float(r["low"])
         close_val = float(r["close"])
         vol_val = float(r["volume"])

         insert_sql = """
         INSERT INTO {target_table} (SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME)
         VALUES (%s, %s, %s, %s, %s, %s, %s)
         """.format(target_table=target_table)
         cur.execute(insert_sql, (
            r["symbol"], date_val, open_val, high_val,
            low_val, close_val, vol_val
         ))
      
      cur.execute("COMMIT;")
      print(f" Successfully inserted {len(results)} records into {target_table}")

   except Exception as e:
      cur.execute("ROLLBACK;")
      print("Error during Snowflake insert:", e)
      raise


with DAG(
    dag_id = 'StockPrice_ETL_v3',
    start_date = datetime(2025,10,1),
    catchup = False,
    tags = ['ETL', 'stocks'],
    schedule = '30 2 * * *'
) as dag:
  
    target_table = "Raw.stock_table"

    extracted_data = extract("GOOG")
    load_to_snowflake(extracted_data, target_table)


  # Dependencies
  #raw_data >> transformed_data >> load(transformed_data, target_table)