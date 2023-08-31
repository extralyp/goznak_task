import argparse
from keras.models import load_model
import numpy as np

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-p', '--file_path', type=str, help='path to meg file')
parser.add_argument('-s', '--save_path', type=str, help='path to save file')

args = parser.parse_args()


def get_window(meg):
    window_size = 80
    step_factor = 1
    step = int(window_size * step_factor)
    new_features = list()
    for i in range(0, meg.shape[0] - window_size + 1, step):
        new_features.append([meg[i:i + window_size, j] for j in range(meg.shape[1])])
    wind_feature = np.array(new_features)
    return wind_feature


def reverse_window(window_arr):
    last_arr = np.empty((0, 80))
    for arr in window_arr:
        last_arr = np.concatenate([last_arr, arr.T])
    return last_arr


def denoised(path_to_meg):
    model = load_model("models/denoise_autoencoder.h5")
    denoised_meg = reverse_window(model.predict(get_window(np.load(path_to_meg))))
    return denoised_meg


prediction = denoised(args.file_path)
np.save(args.save_path, prediction)
print('denoised file saved!')