import numpy as np
import pandas as pd

data = pd.read_excel('train.xlsx', header=None)
data = data.dropna(axis=1, how='all')
data = data.values
data = data.T

windows = np.array([data[10*i:10*(i+1)] for i in range(data.shape[0]//10)])
print("Shape of data\t",windows.shape)

# Each window is of size (10, 60) and has data of 300s i.e. 5 minutes, on the other hand each row contains data worth 30s.
# Now the train case only contains the normal scenario, we have to implement something which is able to understand and 
# label anomalies in the test dataset

