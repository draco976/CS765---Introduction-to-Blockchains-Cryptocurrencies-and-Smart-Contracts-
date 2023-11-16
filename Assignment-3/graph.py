import numpy as np
import matplotlib.pyplot as plt

x = np.arange(100, 1001, 100)
# y1 = [0.96, 0.94, 0.98, 0.98, 0.92, 0.92, 0.91, 0.87, 0.91, 0.92]
y1 = [0.96, 0.94, 0.98, 0.98, 0.92, 0.92, 0.91, 0.87, 0.86, 0.86]
# y2 = [0.4, 0.32, 0.36, 0.31, 0.31, 0.21, 0.28, 0.36, 0.33, 0.22]
y2 = [0.4, 0.32, 0.36, 0.31, 0.31, 0.21, 0.28, 0.27, 0.23, 0.22]

plt.plot(x,y1, label='m=2')
plt.plot(x,y2, label='m=1')
plt.legend()
plt.title('Success Ratio for every 100 transactions')
plt.xlabel('transaction horizon')
plt.ylabel('Success Ratio')
plt.savefig('plot.png')

