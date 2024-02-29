import numpy as np
import matplotlib.pyplot as plt

X = np.arange(1, 100.1, 0.1)
Y = np.sin(X / 5) + np.cos(X * 5)
noise = np.random.uniform(-2, 2, size=X.shape)
Yn = Y + noise

plt.plot(X, Yn)
plt.show()
