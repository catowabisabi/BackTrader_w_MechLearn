import os
import json
import backtrader as bt
import yfinance as yf
import pandas as pd
from models.model_define.InceptionTime.train_class_inception_time_v2 import StockInceptionTime
#from strategies.inception_time_strategy import InceptionTimeStrategy
from strategies.golden_cross import GoldenCrossStrategy

def get_model_paths(models_folder):
    model_paths = []
    for root, dirs, files in os.walk(models_folder):
        for file in files:
            if file.endswith(".pth"):
                model_paths.append(os.path.join(root, file))
    return model_paths

def load_data(stock_list_file):
    stock_list = pd.read_csv(stock_list_file, header=None)
    data = {}
    for stock in stock_list[0]:
        data[stock] = yf.download(stock, start="2023-01-01", end="2023-06-12")
    return data

def load_params(param_file):
    with open(param_file, 'r') as f:
        params = json.load(f)
    return params






def backtest(model_path, data, params):
    cerebro = bt.Cerebro(runonce=False)
    cerebro.addstrategy(GoldenCrossStrategy)
    

    for stock, stock_data in data.items():
        feed = bt.feeds.PandasData(dataname=stock_data)
        cerebro.adddata(feed)

    cerebro.run()
    return cerebro.broker.getvalue()

def main():
    models_folder       = "models"
    stock_list_file     = "data/sectors/test.csv"
    param_file          = "config/hyperparameters.json"

    model_paths         = get_model_paths(models_folder)
    data                = load_data(stock_list_file)
    params              = load_params(param_file)

    results             = {}

    for model_path in model_paths:
        model_results = {}
        for stock, stock_data in data.items():
            result = backtest(model_path, {stock: stock_data}, params)
            model_results[stock] = result
        results[model_path] = model_results

    # 分析和總結回測結果
    
    # 打印回測結果
    for stock, result in results.items():
        print(f"Stock: {stock}, Final Portfolio Value: {result:.2f}")

if __name__ == "__main__":
    main()