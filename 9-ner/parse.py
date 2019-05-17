import xml.etree.ElementTree as ET
from collections import Counter
import os

coarse = True
select_top50 = False
select_10 = False
baseforms = False

histogram = True
bar = False

ne = Counter()
tokens = 0

dirname = 'out2'

if coarse:
	dirname = 'out_top9'


for filename in os.listdir(dirname):
	tree = ET.parse(os.path.join(dirname, filename))
	root = tree.getroot()

	# [{(chan, 1): full}, ...]

	for chunk in root:
		for sentence in chunk:
			found = {}  # (chan, no) : 'phrase'
			real = {}
			for tok in sentence:
				word = ''
				base = ''
				tokens += 1
				for a in tok:
					if a.tag == 'orth':
						word = a.text
					elif a.tag == 'lex':
						base = a[0].text
						tag = a[1].text
					elif a.tag == 'ann':
						name = a.attrib['chan']
						number = int(a.text)
						if number > 0:
							#print(name, number, base)

							key = "{}:{}".format(name, number)
							if key in found.keys():
								found[key] += ' ' + base
								real[key] += ' ' + word
							else:
								found[key] = base
								real[key] = word

			if baseforms:
				for f in found.items():
					key = f[0].split(':')[0]
					new_key = (key, f[1])
					ne[new_key] += 1
			else:
				for f in real.items():
					key = f[0].split(':')[0]
					new_key = (key, f[1])
					ne[new_key] += 1

if select_10 and coarse:
	top10 = {}
	ne_sorted = ne.most_common(len(ne))
	for n in ne_sorted:
		cat = n[0][0]
		count = str(n[1])
		phrase = n[0][1]
	
		if cat in top10:
			if len(top10[cat]) < 10:
				top10[cat] += [(phrase, count)]
		else:
			top10[cat] = [(phrase, count)]
	
	for k in top10.keys():
		print k
		for l in top10[k]:
			record = u', '.join((l[0], l[1])).encode('utf-8').strip()
			print record 
		
	
if select_top50:
	top50 = ne.most_common(50)

	for n in top50:
		record = u', '.join((n[0][1], n[0][0], str(n[1]))).encode('utf-8').strip()
		print record


if bar:
	categories = Counter()
	for n in ne.most_common(len(ne)):
		cat = n[0][0].encode('utf-8')
		count = n[1]
		categories[cat] += count

	for c in categories.most_common(len(categories)):
		record = u', '.join((c[0], str(c[1]))).encode('utf-8').strip()
		print record


if histogram:
	for n in ne.most_common(len(ne)):
		record = u'!'.join((n[0][1], str(n[1]), n[0][0])).encode('utf-8').strip()
		print record

