# MACD-strategy

This repository contains a simple yet effective backtesting tool for the MACD (Moving Average Convergence Divergence) trading strategy using Python. It downloads historical stock data, calculates MACD signals, executes a basic long-only strategy, and evaluates performance metrics such as Sharpe Ratio and Max Drawdown.

# Features: 

- Fetches historical stock data using yfinance
- Computes MACD and Signal Line
- Generates Buy/Sell signals based on MACD crossovers
- Backtests the strategy vs. buy-and-hold
  
# Calculates:
- Total Market Return
- Total Strategy Return
- Sharpe Ratio
- Maximum Drawdown
- Plots Buy/Sell signals on price chart

# Dependencies:

- yfinance
- numpy
- pandas
- matplotlib

# How to Use

from macd_backtester import MACDBacktester

### Initialize backtester
macd = MACDBacktester(symbol='AAPL', start='2020-01-01', end='2024-01-01')

### Run full backtest
performance = macd.run()

### View results
print(performance)

### Optional: Plot Buy/Sell signals
macd.plot_signals()

# Strategy Logic

- Buy Signal: When MACD crosses above the Signal Line.
- Sell Signal: When MACD crosses below the Signal Line.
- Position: Fully invested on buy, exited on sell.
- Returns: Strategy return is calculated only when in position.

# License

This project is licensed under the MIT License.






