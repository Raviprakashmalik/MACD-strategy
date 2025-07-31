import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MACDBacktester:
    def __init__(self, symbol, start, end, EMA_1=12, EMA_2=26, signal_line=9):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.EMA_1 = EMA_1
        self.EMA_2 = EMA_2
        self.signal_line = signal_line
        self.results = None
        self.get_data()

    def get_data(self):
        data = yf.download(self.symbol, start=self.start, end=self.end)
        data = data[['Close']]
        data.columns = ['Close']
        data['EMA_1'] = data['Close'].ewm(span=self.EMA_1, adjust=False).mean()
        data['EMA_2'] = data['Close'].ewm(span=self.EMA_2, adjust=False).mean()
        data['MACD'] = data['EMA_1'] - data['EMA_2']
        data['Signal'] = data['MACD'].ewm(span=self.signal_line, adjust=False).mean()
        self.data = data.dropna()

    def generate_signals(self):
        df = self.data.copy()
        df['Buy Signal'] = (df['MACD'] > df['Signal']) & (df['MACD'].shift(1) <= df['Signal'].shift(1))
        df['Sell Signal'] = (df['MACD'] < df['Signal']) & (df['MACD'].shift(1) >= df['Signal'].shift(1))

        df['Position'] = 0
        df.loc[df['Buy Signal'], 'Position'] = 1
        df.loc[df['Sell Signal'], 'Position'] = 0
        df['Position'] = df['Position'].ffill().fillna(0)

        self.data = df

    def backtest(self):
        df = self.data.copy()
        df['Market Return'] = df['Close'].pct_change()
        df['Strategy Return'] = df['Market Return'] * df['Position'].shift(1)
        df.dropna(inplace=True)
        self.results = df

    def evaluate_performance(self):
        data = self.results.copy()
        total_market_return = np.exp(np.log1p(data['Market Return']).sum()) - 1
        total_strategy_return = np.exp(np.log1p(data['Strategy Return']).sum()) - 1

        excess_returns = data['Strategy Return'] - 0.0001  # assume small daily risk-free rate
        sharpe = np.sqrt(252) * excess_returns.mean() / excess_returns.std()

        cumulative = (1 + data['Strategy Return']).cumprod()
        rolling_max = cumulative.cummax()
        drawdown = (cumulative - rolling_max) / rolling_max
        max_drawdown = drawdown.min()

        return {
            'Total Market Return': round(total_market_return * 100, 2),
            'Total Strategy Return': round(total_strategy_return * 100, 2),
            'Sharpe Ratio': round(sharpe, 3),
            'Max Drawdown': round(max_drawdown * 100, 2)
        }

    def plot_signals(self):
        df = self.data.copy()
        plt.figure(figsize=(14, 7))
        plt.plot(df['Close'], label='Price', alpha=0.5)
        plt.plot(df.loc[df['Buy Signal']].index, df['Close'][df['Buy Signal']], '^', color='green', label='Buy Signal', markersize=10)
        plt.plot(df.loc[df['Sell Signal']].index, df['Close'][df['Sell Signal']], 'v', color='red', label='Sell Signal', markersize=10)
        plt.title(f'{self.symbol} - Buy/Sell Signals')
        plt.legend()
        plt.show()

    def run(self):
        self.generate_signals()
        self.backtest()
        return self.evaluate_performance()

