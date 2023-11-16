import matplotlib.pyplot as plt
import numpy as np

hf = [10,20,30,40]
y_25 = [0.0945173,0.22517395,0.33355505,0.54179919]
y_50 = [0.11625423,0.24928634,0.39103179,0.57799603]
y_75 = [0.13321405,0.2659527,0.43892926,0.61780604]

plt.plot(hf, y_25, label='tau=25%', marker="x", markerfacecolor="None")
plt.plot(hf, y_50, label='tau=50%', marker="o", markerfacecolor="None")
plt.plot(hf, y_75, label='tau=75%', marker="^", markerfacecolor="None")
plt.xlabel('hashing percentage')
plt.ylabel('Fraction in longest chain')
plt.title('Comparison for different tau')
plt.ylim(0,0.8)

plt.legend(loc='upper left')
plt.savefig('frac_blocks.png')
