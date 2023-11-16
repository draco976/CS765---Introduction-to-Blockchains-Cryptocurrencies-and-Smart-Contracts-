import matplotlib.pyplot as plt
import numpy as np

hf = [10,20,30,40]
y_25 = [0.53666667,0.75337302,0.77348485,0.88332905]
y_50 = [0.66257576,0.74420635,0.87087191,0.91630519]
y_75 = [0.68939394,0.84428571,0.88642136,0.92581637]

plt.plot(hf, y_25, label='tau=25%', marker="x", markerfacecolor="None")
plt.plot(hf, y_50, label='tau=50%', marker="o", markerfacecolor="None")
plt.plot(hf, y_75, label='tau=75%', marker="^", markerfacecolor="None")
plt.xlabel('hashing percentage')
plt.ylabel('MPU adversary')
plt.title('Comparison for different tau')

plt.legend(loc='upper left')
plt.savefig('mpu_adv.png')
