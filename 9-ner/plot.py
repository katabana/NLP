import matplotlib.pyplot as plt
import pandas as pd

coarse = False

if coarse:
	n = 'coarse'
else:
	n = 'fine'

data = pd.read_csv(n + '.csv', sep=',', header=None, index_col=0)

data.plot(kind='bar', legend=False)
plt.ylabel('Frequency')
plt.xlabel('Class')

if coarse:
	plt.title('Coarse-grained classification')
else:
	plt.title('Fine-grained classification')
plt.tight_layout()

plt.savefig(n + '.svg')
