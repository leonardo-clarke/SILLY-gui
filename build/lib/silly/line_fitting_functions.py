import numpy as np
from astropy.io import fits
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd

def gaussian(x, *params):
    """1D Gaussian profile for a spectral emission/absorption line.
    
    Args:
        x (float or array): An array of wavelengths.
        flux (float): The integrated flux of the spectral line.
        sig (float): The width of the line in wavelength units.
        mu (float): The wavelength of the line centroid.
        C (float): The continuum level around the line. 
        
    Returns:
        A numpy array containing the value of the best-fit gaussian function at each
          value of x.
    """

    if len(params) == 1:
        params = params[0]
    flux, sig, mu, C = params

    return flux * (1/np.sqrt(2*np.pi*sig**2)) * np.exp(-0.5 * ((x-mu)/sig)**2 ) + C

def create_wavelength_array(header):
    """Creates a wavelength array for a spectrum (data) assuming that data is a 1D array."""
    
    cRVAL = header['CRVAL1']
    cDELT = header['CDELT1']
    x = np.arange(header['NAXIS1'])

    return x*cDELT + cRVAL

def read_fits_spectrum(spec_file_path, header):
    """Reads in a spectrum from a fits file assuming that the wavelength dispersion 
    solution and flux density units are stored in the header."""

    spectrum = fits.getdata(spec_file_path)
    err_spec = fits.getdata(spec_file_path, ext=2)

    wavelengths = create_wavelength_array(header)

    return wavelengths, spectrum, err_spec


def wavelength_to_spectrum_index(wavelength, header):
    """Given a wavelength selected by the user, this function outputs the corresponding 
    index of the spectrum array."""

    cRVAL = header['CRVAL1']
    cDELT = header['CDELT1']

    index = int((wavelength - cRVAL) / cDELT)

    return index


def get_spectrum_wavelength_range_indices(low_wavelength, high_wavelength, header):
    """Selects the spectral data points that belong to the given wavelength range."""

    low_index = wavelength_to_spectrum_index(low_wavelength, header)
    high_index = wavelength_to_spectrum_index(high_wavelength, header)

    return low_index, high_index


def isolate_emission_line(low_wavelength, high_wavelength, spec_file_path):
    """Isolates the data belonging to the emission line of interest.
    
    Args:
        low_wavelength (float): The wavelength of the lower bound of the region over which the
          emission line is fit.
        high_wavelength (float): The wavelength of the upper bound of the region over which the
          emission line is fit.
        spec_file_path (string): The name of the path to the file containing the spectrum. Should
          be a FITS file.
          
    Returns:
        isolated_wavelengths (array): A numpy array of the wavelengths corresponding to the
          spectral feature that has been isolated.
        isolated_spectrum (array): A numpy array of the flux values corresponding to the
          spectral feature that has been isolated.
        isolated_err_spec (array): A numpy array of the error spectrum corresponding to the
          spectral feature that has been isolated.
    """

    header = fits.getheader(spec_file_path, ext=1)
    wavelengths, spectrum, err_spec = read_fits_spectrum(spec_file_path, header)

    low_index, high_index = get_spectrum_wavelength_range_indices(low_wavelength, high_wavelength, header)

    isolated_wavelengths = wavelengths[low_index:high_index]
    isolated_spectrum = spectrum[low_index:high_index]
    isolated_err_spec = err_spec[low_index:high_index]

    return isolated_wavelengths, isolated_spectrum, isolated_err_spec


def fit_emission_line_to_gaussian(low_wavelength, high_wavelength, spec_file_path):
    """Fits a spectrum to a Gaussian profile within a pre-defined wavelength range.
    
    Args:
        low_wavelength (float): The wavelength of the lower bound of the region over which the
          emission line is fit.
        high_wavelength (float): The wavelength of the upper bound of the region over which the
          emission line is fit.
        spec_file_path (string): The name of the path to the file containing the spectrum. Should
          be a FITS file.

    Returns:
        optimized_parameters (array):
            A 1D numpy array containing the optimized gaussian parameters
            in the following order: [line flux, line width (sigma), line centroid, continuum level flux]
        covariance_matrix (array):
            A 2D numpy array containing the covariance matrix describing the
            fit of the data to the gaussian model.
    """

    wavelengths, spectrum, err_spec = isolate_emission_line(low_wavelength, high_wavelength, spec_file_path)
    flux_guess = np.sum(spectrum) * (np.amax(wavelengths) - np.amin(wavelengths))
    sig_guess = (np.amax(wavelengths) - np.amin(wavelengths))/2
    mu_guess = (np.amax(wavelengths) + np.amin(wavelengths))/2
    C_guess = max(1e-18, np.amin(spectrum))
    guess_list = [flux_guess, sig_guess, mu_guess, C_guess]

    optimized_parameters, covariance_matrix = curve_fit(gaussian, wavelengths, spectrum, p0=guess_list, sigma=err_spec, maxfev=2000)
    print('optimized parameters are', optimized_parameters)
    return optimized_parameters, covariance_matrix, wavelengths, spectrum


#if __name__ == '__main__':
    # test_spectrum = '/Users/leonardoclarke/Research/CE_2021/all_1dspec/co2_deep.H.18812.ell.1d.fits'
    #test_range = np.array([17300, 17400])

    # params, covariance = fit_emission_line_to_gaussian(test_range[0], test_range[1], test_spectrum)
    # wavelengths, spectrum, err_spec = isolate_emission_line(test_range[0], test_range[1], test_spectrum)

    # plt.step(wavelengths, spectrum, where='mid')
    # plt.plot(wavelengths, gaussian(wavelengths, params))
    # plt.show()