import dash
from dash import html, dcc
import plotly.graph_objs as go
import pandas as pd
import configparser
import openai
import os

# Directory setup
masterdir = os.getcwd()
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

# Reading configuration for API key
config = configparser.ConfigParser()
config.read(os.path.join(masterdir, '03-config', 'pw-config.ini'))
chat_api = config.get('chatanalyst', 'api_key')

# Read the CSV/Excel File
file_path = os.path.join(masterdir, '01-data', 'Sample.xlsx')
data_frame = pd.read_excel(file_path)

# Function to get analysis from OpenAI using the chat model
def get_openai_analysis():
    openai.api_key = chat_api
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Analyze the following stock data: " + data_frame.to_string()}
            ]
        )
        return response.choices[0].message['content'] if response else "No response from the model."
    except Exception as e:
        return f"An error occurred: {e}"

analysis = get_openai_analysis()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Stock Data Dashboard", style={'textAlign': 'center'}),

    dcc.Graph(
        id='aapl-graph',
        figure={
            'data': [
                go.Scatter(
                    x=data_frame[data_frame['ticker'] == 'AAPL']['Date'],
                    y=data_frame[data_frame['ticker'] == 'AAPL']['Open'],
                    mode='lines',
                    name='AAPL Open'
                ),
                go.Scatter(
                    x=data_frame[data_frame['ticker'] == 'AAPL']['Date'],
                    y=data_frame[data_frame['ticker'] == 'AAPL']['Close'],
                    mode='lines',
                    name='AAPL Close'
                )
            ],
            'layout': go.Layout(title='AAPL Stock Prices', xaxis={'title': 'Date'}, yaxis={'title': 'Price'})
        },
        style={'width': '50%', 'display': 'inline-block'}
    ),

    dcc.Graph(
        id='msft-graph',
        figure={
            'data': [
                go.Scatter(
                    x=data_frame[data_frame['ticker'] == 'MSFT']['Date'],
                    y=data_frame[data_frame['ticker'] == 'MSFT']['Open'],
                    mode='lines',
                    name='MSFT Open'
                ),
                go.Scatter(
                    x=data_frame[data_frame['ticker'] == 'MSFT']['Date'],
                    y=data_frame[data_frame['ticker'] == 'MSFT']['Close'],
                    mode='lines',
                    name='MSFT Close'
                )
            ],
            'layout': go.Layout(title='MSFT Stock Prices', xaxis={'title': 'Date'}, yaxis={'title': 'Price'})
        },
        style={'width': '50%', 'display': 'inline-block'}
    ),

    html.Div([
        html.H2("Analysis", style={'textAlign': 'left'}),
        html.Div([
            html.Div(line.strip(), style={'marginBottom': '15px', 'textAlign': 'left'})
            for line in analysis.split('\n') if line.strip()
        ], style={'marginTop': '20px', 'marginLeft': '20px', 'marginRight': '20px', 'textAlign': 'left'})
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

app.run_server(debug=True, port=8080)