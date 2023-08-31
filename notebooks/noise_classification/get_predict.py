import argparse
import numpy as np
import pickle

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-p', '--file_path', type=str, help='path to meg file')
args = parser.parse_args()


def get_predict(meg, clf):
    window_size = 80
    step_factor = 1
    data = np.load(meg)

    step = int(window_size * step_factor)
    new_features = list()
    for i in range(0, data.shape[0] - window_size + 1, step):
        new_features.append([data[i:i + window_size, j] for j in range(data.shape[1])])
    wind_feature = np.array(new_features)

    test = wind_feature.reshape(wind_feature.shape[0], wind_feature.shape[1] * wind_feature.shape[2])

    predict_wind = []
    for wind in test:
        predict_wind.append(clf.predict(wind.reshape(1, -1)))

    if np.mean(predict_wind) > 0.5:
        return 1
    else:
        return 0


rnd_for = pickle.load(open('models/rnd_for.pkl', 'rb'))


prediction = get_predict(args.file_path, rnd_for)
if prediction == 0:
    print("This spectrogramm is clean")
elif prediction == 1:
    print("This spectrogramm is noisy")
