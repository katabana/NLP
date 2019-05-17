import matplotlib.pyplot as plt
import pandas as pd

coarse = True

if coarse:
	n = 'coarse_histogram'
else:
	n = 'fine_histogram'

data = pd.read_csv(n + '.csv', sep='!',header=None, index_col =0)

data.plot(kind='hist')
plt.ylabel('Frequency')
plt.xlabel('Class')

if coarse:
	plt.title('Coarse-grained classification histogram')
else:
	plt.title('Fine-grained classification histogram')

plt.savefig(n + '.svg')
