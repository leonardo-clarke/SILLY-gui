import numpy as np
import pandas as pd

def gaussian_noise(lmin, lmax, a, mean, sigma, n_samples = 100):
    
    """ 
        generate gaussian with noise according to wavelength range, flux, sigma, mean
        - by default number of samples is set to 100 
    """

    x = np.linspace(lmin, lmax, n_samples)
    gauss = a*np.exp(-(x-mean)**2/(2*sigma**2))
    noise = np.random.normal(size=len(x))

    gauss_noise = gauss + 0.2*a*noise

    return x, gauss_noise


lmin = 500
lmax = 510
a = 1
mean = 505
sigma = 1

toy = gaussian_noise(lmin, lmax, a, mean, sigma)

dict = {'wavelength': toy[0], 'flux': toy[1]}

df = pd.DataFrame(dict)

df.to_csv('toy.csv')
