import matplotlib.pyplot as plt
import numpy as np

hf = [10,20,30,40]
y_25 = [0.08080573,0.12605521,0.32368241,0.51870742]
y_50 = [0.08759398,0.16312673,0.33114201,0.59670494]
y_75 = [0.1345048,0.17970951,0.34636221,0.71132004]

plt.plot(hf, y_25, label='tau=25%', marker="x", markerfacecolor="None")
plt.plot(hf, y_50, label='tau=50%', marker="o", markerfacecolor="None")
plt.plot(hf, y_75, label='tau=75%', marker="^", markerfacecolor="None")
plt.xlabel('hashing percentage')
plt.ylabel('Fraction in longest chain')
plt.title('Comparison for different tau')
plt.ylim(0,0.8)
plt.legend(loc='upper left')
plt.savefig('frac_blocks.png')
