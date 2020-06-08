import numpy as np
import pandas as pd
import time
import os
from tqdm import tqdm

data = pd.read_excel('test_str.xlsx', header=None)
data = data.values
data = data
# Each window is of size (10, 60) and has data of 300s i.e. 5 minutes, on the other hand each row contains data worth 30s.
# Now the train case only contains the normal scenario, we have to implement something which is able to understand and 
# label anomalies in the test dataset

# In statistics, an approximate entropy (ApEn) is a technique used to quantify the amount of regularity and the 
# unpredictability of fluctuations over time-series data.
mean_all = 0
median_all = 0
mean_absolute_deviation_all = 0
median_absolute_deviation_all = 0
alpha = 0.9
first = True
th = 1
n = 20
window = np.array([data[n*i:(i+1)*n] for i in range(data.shape[0]//n)])
c = 0
train_index = 5
for index, time_step in enumerate(window):
	c += n
	mean_per_30 = np.mean(time_step)
	median_per_30 = np.median(time_step)
	mean_absolute_deviation = np.mean(np.absolute(time_step - mean_per_30))
	median_absolute_deviation = np.mean(np.absolute(time_step - median_per_30))
	z_score_median = (time_step - median_per_30)/median_absolute_deviation
	z_score_mean = (time_step - mean_per_30)/mean_absolute_deviation
	if first:
		first = False
		mean_all = mean_per_30
		median_all = median_per_30
		mean_absolute_deviation_all = mean_absolute_deviation
		median_absolute_deviation_all = median_absolute_deviation
		z_score_median_all = (time_step - median_all)/median_absolute_deviation_all
		z_score_mean_all = (time_step - mean_all)/mean_absolute_deviation_all
		mean_prev = mean_per_30
		median_prev = median_per_30
		mean_absolute_deviation_prev = mean_absolute_deviation
		median_absolute_deviation_prev = median_absolute_deviation
		z_score_median_prev = (time_step - median_prev)/median_absolute_deviation_prev
		z_score_mean_prev = (time_step - mean_prev)/mean_absolute_deviation_prev
	else:
		mean_prev = mean_all
		median_prev = median_all
		mean_absolute_deviation_prev = mean_absolute_deviation_all
		median_absolute_deviation_prev = median_absolute_deviation_all
		z_score_median_prev = (time_step - median_all)/median_absolute_deviation_all
		z_score_mean_prev = (time_step - mean_all)/mean_absolute_deviation_all
		mean_all = (mean_all*alpha + mean_per_30)/(1+alpha)
		median_all = (median_all*alpha + median_per_30)/(1+alpha)
		mean_absolute_deviation_all = (mean_absolute_deviation_all*alpha + mean_absolute_deviation)/(1+alpha)
		median_absolute_deviation_all = (median_absolute_deviation_all*alpha + median_absolute_deviation)/(1+alpha)
		z_score_median_all = (time_step - median_all)/median_absolute_deviation_all
		z_score_mean_all = (time_step - mean_all)/mean_absolute_deviation_all
	anomaly_score = np.mean(z_score_mean_all - z_score_mean)

	if int(mean_per_30) > 50000:
		print(mean_per_30, anomaly_score)
	

	if anomaly_score > th and index>train_index:
		mean_all = mean_prev
		median_all = median_prev
		mean_absolute_deviation_all = mean_absolute_deviation_prev
		median_absolute_deviation_all = median_absolute_deviation_prev
		z_score_median_all = (time_step - median_prev)/median_absolute_deviation_prev
		z_score_mean_all = (time_step - mean_prev)/mean_absolute_deviation_prev
		print(int(mean_per_30), anomaly_score, c)
		