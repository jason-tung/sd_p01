def decode(apiname):
	with open(apiname + ".txt") as f:
		k = f.read()

	for i in range(len(k)):
		try:
			t = int(k[i])
			k[i] = str((t + 5) % 10)
		except:
			k[i] = k[i].toupper()