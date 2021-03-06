import numpy as np
import pandas as pd
import random
from datetime import datetime
import scipy.linalg as la
import scipy.io
import pickle
import sys
import os 
dir_path = os.path.dirname(os.path.realpath(__file__)) 

def backtest(ticker="JNUG"):
	"""
	Using training and testing data,
	develop a model to predict the
	stock market and test that model
	
	Params:
		ticker: The ticker to backtest

	Returns:
		P: Portfolio gain over test data 
			(but as a multiplying
			factor, not a percentage)
		A: Portfolio gain every day for 
			the test data
	
	"""
	with open(dir_path + f'/data/{ticker}_test_train.p', 'rb') as handle:
		model_dict = pickle.load(handle)
	with open(dir_path + f"/models/{ticker}_model.p", 'rb') as fp:
		m = pickle.load(fp)

	T = model_dict["T"]
	Q = model_dict["Q"]

	# Guess how much the stock value will increase
	model_gain_predictions = np.matmul(T, m)
	model_perc_predictions = model_gain_predictions - 1

	# Determine how much money to invest / short on the stock
	def allocate_portfolio(est_perc_increase):
		if est_perc_increase > 0:
			return 1
		else:
			return -1

	allocate_portfolio_vec = np.vectorize(allocate_portfolio)
	model_portfolio_allocations = allocate_portfolio_vec(model_perc_predictions)

	# Compare portfolio holdings to actual stock gains
	day_gains = model_portfolio_allocations * (Q - 1) + 1
	total_percentage_increase = np.prod(day_gains)

	return day_gains, total_percentage_increase




def train_model(ticker):
	"""
	Train a model and save it to the models folder
	
	"""
	with open(dir_path + f'/data/{ticker}_test_train.p', 'rb') as handle:
		model_dict = pickle.load(handle)
	Y = np.array(model_dict.get("Y"))
	C = np.array(model_dict.get("C"))
	Yt = Y.transpose()
	YtY = np.dot(Yt, Y)
	YtC = np.dot(Yt, C)
	# Both solutions yield the same answer
	# m = np.linalg.solve(YtY, YtC)
	m, _, _, _ = np.linalg.lstsq(Y, C, rcond= None)
	
	with open(dir_path + f"/models/{ticker}_model.p", 'wb') as fp:
		pickle.dump(m, fp)
	print(m)
	return m
	

def est_perc_increase(ticker, last_10_days=None, opening_price=None, date=datetime.today()):
	"""
	Given a stock and its opening price, predict the percentage
	increase from opening price to closing price.
	A value of 1 means the stock means no change.

	Params:
		ticker: the stock ticker
		opening_price: the opening price / current price
		date: the day of the transaction
	
	Returns:
		the percentage increase of the day
	"""
	with open(dir_path + f"/models/{ticker}_model.p", 'rb') as fp:
		m = pickle.load(fp)

	if opening_price is not None:
		# This part of the algorithm is not run
		with open(dir_path + f'/data/{ticker}_test_train.p', 'rb') as handle:
			model_dict = pickle.load(handle)
		T = np.array(model_dict.get("T"))
		T_size = np.size(T, 0)
		T = T[T_size-1,:]
		T = T.flatten()
		T_size = np.size(T, 0)
		np.put(T, T_size-1, opening_price)
		T = np.divide(T,T[0])
		print("T Shape", T.shape)
		print("T:", T)
	else:
		T = last_10_days
	G = np.matmul(T, m)
	print(m)
	print(G)
	return G
	'''
	# hack fix to get MATLAB data for stock predictions
	# change this when Python analyses are working
	try:
		ticker_model = scipy.io.loadmat(f"../models/{ticker}_predict.mat")
		m = np.array(ticker_model["m"]).flatten()
		
		historical_data = pd.read_csv(f"../data/{ticker}.csv")
		last_2_weeks_data = historical_data.tail(10)
		last_2_weeks_data = last_2_weeks_data.loc[:,["Open", "High", "Low", "Close"]]

		previous_intraday_data = last_2_weeks_data.values.flatten()
		all_previous_data = np.append(previous_intraday_data, opening_price / previous_intraday_data[0])

		perc_increase = np.prod(m * all_previous_data)
		return perc_increase

	except Exception as e:
		print(e)

	return random.uniform(0.95, 1.05)
	'''
if __name__ == "__main__":
	# Assign the ticker
	if len(sys.argv) >= 2:
		ticker = sys.argv[1]
	else:
		ticker = input("What stock do you want to test? ")
		# opening_price = input("What is the opening price? ")
	train_model(ticker)
	# est_perc_increase(ticker, opening_price)