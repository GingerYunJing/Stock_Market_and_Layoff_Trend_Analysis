# DSCI 550 Final Project

## Name of the Project

Stock Market and Layoff Trend Analysis

## Team Members

Ming Shan Lee, Yun Jing Chang, Takaaki Morita, Hasti Sodavadia

## Instructions on how to redirect the repository before running project

Before running any code, please redirect your repository to `src`

### Usage

```bash
cd src
```

## Instructions on how to reproduce the work in one run

`main.py` would automatically run everything, which is `get_data.py`, `clean_data.py`, `run_analysis.py`, and `visualize_results.py` and doesn't require user to input any parameter. 

### Usage

```bash
python main.py
```

## Instructions on how to reproduce the work separately

Every script in this project are designed to be able to run individually. Follow the instructions in the following sections to do so.

## Instructions on how to download the data

In this project, we would be scraping data from the yahoo finance webpage and also using the yahoo finance python package. By running `get_data.py`, we would be scraping stock prices of the listing companies (ticker) from January 2019 to April 2024 and fetching the financial data from yfianance package:

- Meta (META)
- Amazon (AMZN)
- Apple (AAPL)
- Netflix (NFLX)
- Google (GOOGL)

### Usage

```bash
python get_data.py ticker
```
Replace `ticker` to any valid company ticker. `ticker` should be one ticker at a time.

After running this code, the terminal will output some snippet of the data and then save the data into the data\raw folder.

## Instructions on how to clean the data

`clean_data.py` would be converting time attribute to datetime using python datetime package, dropping missing values, removing comma separators, converting data types, sorting data to ensure it's in chronological order, resetting index, and at last, dropping values that is 0, which indicates that the market was not open. 

### Usage

Run this when cleaning stock price data:
```bash
python clean_data.py --stock_data stock_data_path
```
Replace `stock_data_path` with your path to stock data.

Run this when cleaning financial price data:
```bash
python clean_data.py --financial_data financial_data_path
```
Replace `financial_data_path` with your path to financial data.

After running this code, the terminal will output some snippet of the data and then save the data into the data\processed folder.

## Instrucions on how to run analysis code

`run_analysis.py` would be outputting analyses including statistical analysis of the financial data. We've tried to present the financial health of the companies, but due to lack of data, we were unable to do so.

### Usage

```bash
python run_analysis.py financial_data_path
```
Replace `financial_data_path` with your path to financial data.

After running this code, the terminal will output some snippet of the analysis and a new folder `analysis` will be created if not already exists. The statistical analyses will be saved here.

## Instructions on how to create visualizations

`visualize_results.py` would be outputting the heatmap of the stock prices data. In addition, we will also present the visualizations of the layoff barchart with stock price, and visualizations of the machine learning model that predicts future stock prices. To see more visulizations like simple moving average, exponential moving average, volatility, please refer to `FInal_project _550.ipynb` in the `results` folder.

### Usage
```bash
python visualize_results.py stock_data_path layoff_data_path
```
Replace `stock_data_path` and `layoff_data_path` with your paths to stock data and layoff data.

After running this code, the terminall will first output the heatmap of the stock price data. Then, output some snippet of the data used in training and testing, the visualization of the machine learning model, the visualization of the layoff barchart with stock price, and the metrics of the model. All figures will be saved into a new folder `visualizations`.