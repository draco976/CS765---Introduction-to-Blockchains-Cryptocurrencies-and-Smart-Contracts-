import matplotlib.pyplot as plt
import numpy as np

hf = [10,20,30,40]
y_25 = [0.00998729,0.0101247,0.01068191,0.0112663]
y_50 = [0.0100915,0.01013516,0.01054225,0.01107432]
y_75 = [0.01009238,0.01003355,0.01066897,0.01246273]

plt.plot(hf, y_25, label='tau=25%', marker="x", markerfacecolor="None")
plt.plot(hf, y_50, label='tau=50%', marker="o", markerfacecolor="None")
plt.plot(hf, y_75, label='tau=75%', marker="^", markerfacecolor="None")
plt.xlabel('hashing percentage')
plt.ylabel('MPU overall')
plt.title('Comparison for different tau')

plt.legend(loc='upper left')
plt.savefig('mpu_overall.png')
