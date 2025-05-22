from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import elementary_charge, k, h, c
from constants import *
from glob import glob

# ============================= Handwavy numbers ============================= #
# range of wavelength studied [nm]
lowest_lambd_studied = 200
highest_lambd_studied = 2600

# number of datapoints contained in average in the calibration measurements and in the photocurrent measurements
nb_values = {
    'low':706,
    'mid':627,
    'high':1093,
    'photocurrent':1872
}

# =============================== Data classes =============================== #
@dataclass
class IV:
    filename: str
    I: np.ndarray[float]
    V: np.ndarray[float]
    temperature: ufloat

@dataclass
class Calibration:
    sensor: str
    filter: int
    min_lambda: float
    max_lambda: float
    lambd: np.ndarray[float]
    E: np.ndarray[float]
    intensity: np.ndarray[float]

@dataclass
class SensorResponse:
    sensor: str
    min_lambda: float
    max_lambda: float
    lambd: np.ndarray[float]
    response: np.ndarray[float]

@dataclass
class Photocurrent:
    min_lambda: float
    max_lambda: float
    lambd: np.ndarray[float]
    intensity: np.ndarray[float]
    E: np.ndarray[float]


# ======================== auxiliary loading functions ======================= #
def load_IV(path: str) -> list[IV]:
    data_files = glob(f'../data/{path}/*.tsv')
    data_files.sort()
    data = []
    for i, file in enumerate(data_files):

        # V [V], I [mA]
        V, I = np.loadtxt(file, delimiter='\t', unpack=True, converters=lambda s: s.replace(',', '.'))

        # Extract temperature (Ohm)
        ohm_lower, ohm_upper, *_ = map(float, file.split("/")[-1][:-4].split('-'))
        T = (resistance_to_temperature(ohm_lower) + resistance_to_temperature(ohm_upper)) / 2
        err_T = abs(resistance_to_temperature(ohm_lower) - resistance_to_temperature(ohm_upper)) / 2

        # Instantiate IV object
        data.append(
            IV(
                filename=file,
                I=I[V>0],
                V=V[V>0],
                temperature=ufloat(T,err_T)
            )
        )
    return data

def load_calibration(path: str) -> list[Calibration]:
    """
    From a path containing total calibration spectrums (.tsv) returns a list of Calibration objects.
    The calibration spectrum is extended with zeros (before and after its range) to cover the entire length of a photocurrent measurement.
    """
    data_files = glob(f'../data/{path}/*.tsv')
    data_files.sort()
    dataset: list[Calibration] = []

    for i, file in enumerate(data_files):
        _, t, signal, _ = np.loadtxt(file, unpack=True, delimiter="\t", converters=lambda s: s.replace(',', '.'))
        sensor, filterr, lower, upper = file.split('/')[-1][:-4].split('-')
        lower = int(lower)
        upper = int(upper)
        lambd_values = np.linspace(lower, upper, len(t), endpoint=True)
        filterr = int(filterr)

        signal[signal < 0] = 0  # negative values begone

        # Fill the rest of the spectrum with zeros
        # if (sensor=='low'):
        #     lambda_section_after = np.linspace(upper, highest_lambd_studied, num=(nb_values['photocurrent'] - lambd_values.size))
        #     signal_section_after = np.zeros(nb_values['photocurrent'] - lambd_values.size)
        #     lambd_values = np.concat((lambd_values, lambda_section_after))
        #     signal = np.concat((signal, signal_section_after))
        # elif (sensor=='mid'):

        # else:
        #     print("WARNING: MID and HIGH sensors not implemented")
        # Maximum response should be 1

        lambd_values, signal = fill_spectrum(lambd_values, signal, lowest_lambd_studied, highest_lambd_studied, nb_values['photocurrent'])
        signal /= np.max(signal)

        # convert wavelengths to energies [eV]
        E_values = h * c / (lambd_values*1e-9) * EV_PER_JOULE # [eV]

        data = Calibration(
            sensor=sensor, filter=filterr, min_lambda=lower, max_lambda=upper,
            lambd=lambd_values, E = E_values,
            intensity=signal
        )

        dataset.append(data)
    return dataset

def load_photocurrent(path:str) -> list[Photocurrent]:
    """
    From a path containing photocurrent measurements (.tsv) returns a list of Photocurrent objects.
    The data is cut in order to fit the (arbitrary) canonical length of the measurements.
    """
    data_files = glob(f'../data/{path}/*.tsv')
    data_files.sort()
    dataset: list[Calibration] = []
    for i, file in enumerate(data_files):
        _, t, signal, _ = np.loadtxt(file, unpack=True, delimiter="\t", converters=lambda s: s.replace(',', '.'))
        lambd = np.linspace(lowest_lambd_studied, highest_lambd_studied, len(t), endpoint=True) # [nm]
        E = h * c / (lambd*1e-9) * EV_PER_JOULE # [eV]

        dataset.append(Photocurrent(lowest_lambd_studied, highest_lambd_studied, lambd[:nb_values['photocurrent']], signal[:nb_values['photocurrent']], E[:nb_values['photocurrent']]))
    return dataset

def load_sensor_response(path:str) -> list[SensorResponse]:
    """
    From a path containing optical sensor response curves (.tsv) returns a list of SensorResponse objects.
    The original curve is resized by interpolation so that its response values correspond to the wavelength values of the calibration curves, 
    then extended with zeros in order to cover the full photocurrent measurement spectrum.
    """
    data_files = glob(f'../data/{path}/*.tsv')
    data_files.sort()
    dataset: list[SensorResponse] = []
    for i, file in enumerate(data_files):
        true_lambd, true_response = np.loadtxt(file, unpack=True, delimiter='\t')
        sensor, lower, upper = file.split('/')[-1][:-4].split('-')
        lower = int(lower)
        upper = int(upper)

        true_response /= np.max(true_response)

        new_lambd = np.linspace(lower, upper, nb_values[sensor])
        interp_response = np.interp(new_lambd, true_lambd, true_response)

        new_lambd, interp_response = fill_spectrum(new_lambd, interp_response, lowest_lambd_studied, highest_lambd_studied, nb_values['photocurrent'])
        dataset.append(SensorResponse(sensor, lower, upper, new_lambd, interp_response))

    return dataset
    
def fill_spectrum(old_lambd:np.ndarray[float], old_signal:np.ndarray[float], lowest:int, highest:int, nb_total_values:int):
    """
    Extends a spectrum with zeros to cover the full length between 'lowest' and 'highest', knowing it must contain a number 'nb_total_values' of datapoints
    """
    new_lambd = np.linspace(lowest, highest, nb_total_values, endpoint=True)
    start_idx = (np.abs(new_lambd - np.min(old_lambd))).argmin()
    new_signal = np.zeros(nb_total_values)

    if start_idx != 0: start_idx-=1
    new_signal[start_idx:start_idx+np.size(old_signal)] = old_signal
    return new_lambd, new_signal

def remove_sensor_response(calibration_dataset: list[Calibration], sensor_dataset: list[SensorResponse]) -> list[Calibration]:
    updated_calibration_dataset = calibration_dataset
    for calibration in updated_calibration_dataset:
        for sensor in sensor_dataset:
            if calibration.sensor == sensor.sensor:
                with np.errstate(divide='ignore'):
                    calibration.intensity /= sensor.response
                    # calibration.intensity /= np.max(calibration.intensity)
    return updated_calibration_dataset


def resistance_to_temperature(ohm: float) -> float:
    return ohm * RESISTANCE_SLOPE + RESISTANCE_OFFSET

def wavelength_nm_to_energy(wavelength: float) -> float:
    return h * c / (wavelength * 1e-9) * EV_PER_JOULE

def curve_IV(I: np.ndarray[float], T, I_s, n, R) -> np.ndarray[float]:
    return (n*k*T / elementary_charge) * np.log(I/I_s + 1) + R*I

if __name__ == '__main__':
    print(resistance_to_temperature(109) - 273.15)