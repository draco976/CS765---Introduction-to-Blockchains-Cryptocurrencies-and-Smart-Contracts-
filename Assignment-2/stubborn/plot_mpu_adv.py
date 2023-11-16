import matplotlib.pyplot as plt
import numpy as np

hf = [10,20,30,40]
y_25 = [0.52666667,0.50694444,0.60015152,0.65448017]
y_50 = [0.55833333,0.58944444,0.62611111,0.65394231]
y_75 = [0.71809524,0.66218254,0.70397436,0.91752798]

plt.plot(hf, y_25, label='tau=25%', marker="x", markerfacecolor="None")
plt.plot(hf, y_50, label='tau=50%', marker="o", markerfacecolor="None")
plt.plot(hf, y_75, label='tau=75%', marker="^", markerfacecolor="None")
plt.xlabel('hashing percentage')
plt.ylabel('MPU adversary')
plt.title('Comparison for different tau')

plt.legend(loc='upper left')
plt.savefig('mpu_adv.png')
