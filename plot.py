import matplotlib.pyplot as plt
import numpy as np

data = np.genfromtxt("simulated_data.txt",delimiter =','	)

plt.plot(data[0],data[1])
plt.savefig('plot_time_'+ str(1) +'.png')

for i in range(1,len(data)/100):
	plt.plot(data[0],data[i*100])
	plt.savefig('plot_time_'+ str(i*100) +'.png')

