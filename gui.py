import toy_data
import matplotlib.pyplot as plt

lmin = 500
lmax = 510
a = 1
mean = 505
sigma = 1

toy = toy_data.gaussian_noise(lmin, lmax, a, mean, sigma)
fig = plt.Figure()
plt.scatter(toy[0], toy[1])
plt.show()