'''
Make a plot save as SVG.
'''

import matplotlib.pyplot as plt
import numpy as np

x=np.random.randn(1000)
plt.plot(x,'-')
plt.xlabel('Time')
plt.ylabel('Amplitude')

plt.savefig('./figtest.svg')

