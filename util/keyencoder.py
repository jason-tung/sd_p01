def decode(apiname):
	with open(apiname + ".txt") as f:
		k = f.read()

	for i in range(len(k)):
		try:
			t = int(k[i])
			if t >= 5:
				k[i] = str(t - 5)
			else:
				k[i] = str(t + 5)
		except:
			k[i] = k[i].toupper()