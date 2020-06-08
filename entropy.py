import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def sampen(L, m, r):
    N = len(L)
    B = 0.0
    A = 0.0

    # Split time series and save all templates of length m
    xmi = np.array([L[i : i + m] for i in range(N - m)])
    xmj = np.array([L[i : i + m] for i in range(N - m + 1)])

    # Save all matches minus the self-match, compute B
    B = np.sum([np.sum(np.abs(xmii - xmj).max(axis=1) <= r) - 1 for xmii in xmi])

    # Similar for computing A
    m += 1
    xm = np.array([L[i : i + m] for i in range(N - m + 1)])

    A = [np.sum(np.abs(xmi - xm).max(axis=1) <= r) - 1 for xmi in xm]

    # Return SampEn
    a =  -np.log(A / B)
    a = np.nan_to_num(a, posinf=33333333)
    return a

data = pd.read_excel('test.xlsx', header=None)
data = data.dropna(axis=1, how='all')
data = data.values
data = data.T
data = data.flatten()
dataa = [i for i in data]
a = [i for i in sampen(dataa, 4, 0.2*np.std(data) ) ]

k = np.bincount(a).argmax()

aa = [(i, a[i], dataa[i]) for i in range(len(a))]
ab = [dataa[i] for i in range(len(a))]
anomalies = []
anomalies_index = []

print([i for i in aa if int(i[1]) != int(aa[k][1])])
exit()

for i in range(len(aa)):
    plt.clf()
    plt.scatter(anomalies_index, anomalies, color='red')
    plt.plot(range(i), ab[:i], '-o', color='green')
    if aa[i][1] != aa[k][1] and aa[i][1]!=33333333.0:
        anomalies_index.append(i)
        anomalies.append(aa[i][2])
        
        print(aa[i])

    plt.plot(anomalies_index, anomalies, marker='.', color='red')#, s=100)
    plt.pause(0.0005)
plt.show()