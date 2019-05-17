import matplotlib.pyplot as plt
import pandas as pd

coarse = False

if coarse:
	n = 'coarse_histo'
else:
	n = 'fine_histo'

data = pd.read_csv(n + '.csv', sep=',',header=None, index_col =0)

data.plot(kind='bar')
plt.ylabel('Frequency')
plt.xlabel('Class')

if coarse:
	plt.title('Coarse-grained classification histogram')
else:
	plt.title('Fine-grained classification histogram')
plt.tight_layout()

plt.savefig(n + '.svg')
