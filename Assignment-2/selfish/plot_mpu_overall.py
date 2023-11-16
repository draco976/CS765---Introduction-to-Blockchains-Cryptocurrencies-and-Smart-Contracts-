import matplotlib.pyplot as plt
import numpy as np

hf = [10,20,30,40]
y_25 = [0.0100465,0.01002925,0.01003091,0.0105794]
y_50 = [0.01001994,0.01004295,0.01017963,0.01123922]
y_75 = [0.01011881,0.01015156,0.01013172,0.01104778]

plt.plot(hf, y_25, label='tau=25%', marker="x", markerfacecolor="None")
plt.plot(hf, y_50, label='tau=50%', marker="o", markerfacecolor="None")
plt.plot(hf, y_75, label='tau=75%', marker="^", markerfacecolor="None")
plt.xlabel('hashing percentage')
plt.ylabel('MPU overall')
plt.title('Comparison for different tau')

plt.legend(loc='upper left')
plt.savefig('mpu_overall.png')
