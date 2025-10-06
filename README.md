# StockPrice_ETL
This project uses Apache Airflow to automatically fetch daily stock prices from the Alpha Vantage API and load them into Snowflake. It helps keep stock data updated every day for easy analysis and reporting.

# 📊 Stock Price ETL Pipeline (Airflow + Snowflake)

### 🚀 Overview
This project implements an **ETL pipeline** using **Apache Airflow** to extract daily stock prices from the **Alpha Vantage API** and load them into a **Snowflake** data warehouse.  

It automates data collection and storage for stock analytics, ensuring fresh and structured market data daily.

---

## ⚙️ Features
✅ Extracts stock price data (Open, High, Low, Close, Volume) using Alpha Vantage API  
✅ Loads clean data into a Snowflake table  
✅ Automatically scheduled via Airflow (daily at 2:30 AM UTC)  
✅ Built with modular, reusable Airflow tasks  

---

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
