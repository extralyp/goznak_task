import warnings
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

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

text_size = 21

load_data_las = dcc.Upload(
    id='upload-data-las',
    children=([
        'Перетащите .npy файл или ',
        html.B('Выберите файл')
    ]),
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    },
    multiple=False
)


load_data_noise_meg = dcc.Upload(
    id='upload-data-noised',
    children=([
        'Перетащите зашумленный .npy файл или ',
        html.B('Выберите файл')
    ]),
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    },
    multiple=False
)

load_data_clear_meg = dcc.Upload(
    id='upload-data-clear',
    children=([
        'Перетащите НЕ зашумленный .npy файл или ',
        html.B('Выберите файл')
    ]),
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    },
    multiple=False
)

button = dbc.Button('Применить',
                    id='submit-val',
                    color='success',
                    n_clicks=0,
                    style={'marginTop': '10px'}
                    )

cards_rigis = [
    dbc.Row([
        dbc.Col(
            dbc.Card([

                dbc.CardBody([
                    html.B('Классификация спектрограмм', style={'font-size': 18,
                                                          'color': color_text}),
                    html.Div(load_data_las, style={'width': '500px'}),

                ], style={'padding-top': '0px', 'padding-bottom': '0px'}),
            ], color=color_cards, style={'height': '150px', 'border-radius': '0', 'padding': '0px'}),
            style={'padding-right': '5px', 'padding-left': '0px', 'padding-bottom': '0px'}
        ),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.B('Имя файла:',
                                      style={'font-size': 18, 'color': color_text}),
                    html.Div(id='npy-file-name'),
                ]),
                dbc.CardBody([
                    html.B('Предсказание:', style={'font-size': 18,
                                                   'color': color_text}),
                    html.Div(id='npy-file-class'),
                ])
            ], color=color_cards, style={'height': '150px', 'border-radius': '0', 'padding': '0px', 'width': '1250px'})
        ], style={'margin-top': '0px', 'margin-right': '0px', 'margin-left': '10px', 'margin-bottom': '0px',
                  'padding': '0px'}
        ),
    ], style={'margin-top': '10px', 'margin-right': '10px', 'margin-left': '10px', 'margin-bottom': '10px',
              'padding': '0px'}),


dbc.Row([
        dbc.Col(
            dbc.Card([

                dbc.CardBody([
                    html.B('Очистка спектрограмм', style={'font-size': 18,
                                                          'color': color_text}),
                    html.Div(load_data_noise_meg, style={'width': '500px'}),

                    html.Div(load_data_clear_meg, style={'width': '500px'}),

                    html.Div(button),


                    html.B('MSE зашумленной спектрограммы:', style={'font-size': 18,
                                                          'color': color_text}),
                    html.Div(id='noised-mse'),
                    html.B('MSE очищенной спектрограммы:', style={'font-size': 18,
                                                          'color': color_text}),
                    html.Div(id='denoised-mse'),

                ], style={'padding-top': '0px', 'padding-bottom': '0px'}),
            ], color=color_cards, style={'height': '1500px', 'border-radius': '0', 'padding': '0px'}),
            style={'padding-right': '5px', 'padding-left': '0px', 'padding-bottom': '0px'}
        ),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.B('Спектрограммы:',
                                      style={'font-size': 18, 'color': color_text}),
                    dcc.Graph(id="clear-chart"),
                    dcc.Graph(id="noiesd-chart"),
                    dcc.Graph(id="denoiesd-chart"),

                ]),


            ], color=color_cards, style={'height': '1500px', 'border-radius': '0', 'padding': '0px', 'width': '1250px'})
        ], style={'margin-top': '0px', 'margin-right': '0px', 'margin-left': '10px', 'margin-bottom': '0px',
                  'padding': '0px'}
        ),
    ], style={'margin-top': '10px', 'margin-right': '10px', 'margin-left': '10px', 'margin-bottom': '10px',
              'padding': '0px'}),

]
