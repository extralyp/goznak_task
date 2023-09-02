import base64
import io
import pickle
from sklearn import metrics
import rigis_html
import numpy as np
import warnings
import dash
from keras.models import load_model

from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px

warnings.filterwarnings('ignore')
# os.getenv('DEBUG')
DEVSTAT = 1
# prod or debug

if DEVSTAT == 1:  # debug
    DP_PORT = 8200
    VFM_PORT = 8201
elif DEVSTAT == 0:  # prod
    DP_PORT = 8200
    VFM_PORT = 8201

# CYBORG
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])

color_cards = '#1f1f1f'
color_text = '#ffffff'
plot_bgcolor = '#ffffff'
paper_bgcolor = '#1f1f1f'
table_header_color = 'rgb(30, 30, 30)'
table_back_color = 'rgb(50, 50, 50)'
table_grid_color = '1px solid #494949'

style_cell = ({
    'overflow': 'hidden',
    'textOverflow': 'ellipsis',
    'maxWidth': '100%',
    'textAlign': 'left'
})
style_table = ({
    'maxHeight': '100%',
    'maxWidth': '98%',
})
style_header = ({
    'backgroundColor': table_header_color,
    'color': 'white',
    'border': table_grid_color
})
style_data = ({
    'backgroundColor': table_back_color,
    'color': 'white',
    'border': table_grid_color,
    'whiteSpace': 'normal',
    'height': 'auto'
})

app.layout = html.Div([

    dbc.Row([
        dbc.Col(
            html.H1('NeuroSound', style={'color': 'white'}, ), width=10
        ),
    ]),
    html.Br(),
    html.Div(rigis_html.cards_rigis)
], style={'width': '99.5%'})


def get_predict(meg, clf):
    window_size = 80
    step_factor = 1
    step = int(window_size * step_factor)
    new_features = list()
    for i in range(0, meg.shape[0] - window_size + 1, step):
        new_features.append([meg[i:i + window_size, j] for j in range(meg.shape[1])])
    wind_feature = np.array(new_features)

    test = wind_feature.reshape(wind_feature.shape[0], wind_feature.shape[1] * wind_feature.shape[2])

    predict_wind = []
    for wind in test:
        predict_wind.append(clf.predict(wind.reshape(1, -1)))

    if np.mean(predict_wind) > 0.5:
        return 1
    else:
        return 0
@app.callback(
    [
        Output(component_id='npy-file-class', component_property='children'),
        Output(component_id='npy-file-name', component_property='children'),
    ],

    [
        Input(component_id="upload-data-las", component_property="contents"),
        Input(component_id='upload-data-las', component_property='filename'),
    ], prevent_initial_call=True
)
def classification(npy_file, npy_name):
    content_type, content_string = npy_file.split(',')
    decoded = base64.b64decode(content_string)
    arr = np.load(io.BytesIO(decoded))

    rnd_for = pickle.load(open('assets/model/rnd_for.pkl', 'rb'))

    predict = get_predict(arr, rnd_for)
    if predict == 0:
        predict_string = 'Файл не зашумлен'
    else:
        predict_string = 'Файл зашумлен'

    return [predict_string, npy_name]

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


def denoised(meg):
    model = load_model("assets/model/denoise_autoencoder.h5")
    denoised_meg = reverse_window(model.predict(get_window(meg)))
    return denoised_meg

@app.callback(
    [
        Output(component_id='noised-mse', component_property='children'),
        Output(component_id='denoised-mse', component_property='children'),

        Output(component_id='clear-chart', component_property='figure'),
        Output(component_id='noiesd-chart', component_property='figure'),
        Output(component_id='denoiesd-chart', component_property='figure'),
    ],
    [
        Input(component_id='submit-val', component_property='n_clicks')
    ],
    [
        State(component_id="upload-data-noised", component_property="contents"),
        State(component_id='upload-data-noised', component_property='filename'),

        State(component_id="upload-data-clear", component_property="contents"),
        State(component_id='upload-data-clear', component_property='filename'),

    ], prevent_initial_call=True
)
def denoising(n, npy_file, npy_name, npy_file_clear, npy_name_clear):

    content_type, content_string = npy_file.split(',')
    decoded = base64.b64decode(content_string)
    arr = np.load(io.BytesIO(decoded))

    content_type_clear, content_string_clear = npy_file_clear.split(',')
    decoded_clear = base64.b64decode(content_string_clear)
    arr_clear = np.load(io.BytesIO(decoded_clear))

    clear_window = get_window(arr_clear)
    clear_signal_reverse = reverse_window(clear_window)

    noised_window = get_window(arr)
    noised_signal_reverse = reverse_window(noised_window)
    denoised_arr = denoised(arr)

    fig_clear = px.imshow(clear_signal_reverse.T, title='Чистая спетрограмма')
    fig_noised = px.imshow(noised_signal_reverse.T, title='Зашумленная спетрограмма')
    fig_denoised = px.imshow(denoised_arr.T, title='Очищенная спетрограмма')

    denoised_mse = metrics.mean_squared_error(denoised_arr, clear_signal_reverse)
    noised_mse = metrics.mean_squared_error(noised_signal_reverse, clear_signal_reverse)


    return [noised_mse, denoised_mse, fig_clear, fig_noised, fig_denoised]

if __name__ == "__main__":
    if DEVSTAT == 1:
        app.run(debug=True)
    elif DEVSTAT == 0:
        app.run(debug=False, host='0.0.0.0', port=VFM_PORT)
