from cmath import nan
from tempfile import SpooledTemporaryFile
from turtle import width
import dash
from dash import Dash, html, dcc, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import utilities as ut
import numpy as np
import os
import re

# Dash-App erstellen
app = Dash(__name__)

list_of_subjects = []
subj_numbers = []
number_of_subjects = 0

folder_current = os.path.dirname(__file__) 
print(folder_current)
folder_input_data = os.path.join(folder_current, "input_data")
for file in os.listdir(folder_input_data):
    
    if file.endswith(".csv"):
        number_of_subjects += 1
        file_name = os.path.join(folder_input_data, file)
        print(file_name)
        list_of_subjects.append(ut.Subject(file_name))


df = list_of_subjects[0].subject_data

# Reset CSS für Website
path = os.path.join(folder_current, "assets")
path = os.path.join(path, "static")
path = os.path.join(path, "reset.css")

app.css.append_css({'external_url': path})
app.server.static_folder = 'static'


for i in range(number_of_subjects):
    subj_numbers.append(list_of_subjects[i].subject_id)

data_names = ["SpO2 (%)", "Blood Flow (ml/s)","Temp (C)"]
algorithm_names = ['Min','Max']
blood_flow_functions = ['CMA','SMA','Limits']


fig0= go.Figure()
fig1= go.Figure()
fig2= go.Figure()
fig3= go.Figure()

fig0 = px.line(df, x="Time (s)", y = "SpO2 (%)")
fig1 = px.line(df, x="Time (s)", y = "Blood Flow (ml/s)")
fig2 = px.line(df, x="Time (s)", y = "Temp (C)")
fig3 = px.line(df, x="Time (s)", y = "Blood Flow (ml/s)")

#--App Layout--> TO DO: Farben, Schatten und Auswahl bzw. Filterleiste überarbeiten
app.layout = html.Div([
    
    # Überschrift mit Umrandung
    html.Div(children=[
        html.H1(children='Cardiopulmonary Bypass Dashboard', 
            style={'textAlign': 'center',
            "font-family": "Arial, Helvetica, sans-serif",
            "color": "white",
            'background-color': "rgb(70, 70, 70)",
            "height": "10%",
            "margin-left": "1%",
            "margin-right": "1%",
            "padding": "2%",
            "border-radius": "10px"
            })
        ]
    ),

    # Auswahl und Filter
    html.Div(children=[

        # Label für Dropdown:
        html.Div([
            html.Label("Select a subject:")
        ], style={"color": "white",
            "font-family": "Arial, Helvetica, sans-serif",
            "display": "inline-block",
            "float": "left",
            "margin-right": "0.5%"}),

        # Dropdown zur Auswahl
        html.Div([
            dcc.Dropdown(options = subj_numbers, value='1', id='subject-dropdown'),
            html.Div(id='dd-output-container')
        ], style={"display": "inline-block",
            "width": "5%",
            "margin-right": "2%"}),

        # Label für Checklisten:
        html.Div([
            html.Label("Select filters:")
        ], style={"color": "white",
            "font-family": "Arial, Helvetica, sans-serif",
            "display": "inline-block"}),

        # Checkliste mit min und max
        dcc.Checklist(
            id= 'checklist-algo',
            options=algorithm_names,

            style={'display': 'inline-block'}, # Damit Checklisten nebeneinander 
            labelStyle={"font-family": "Arial, Helvetica, sans-serif",
                "color": "white",
                'display': 'inline-block'},
            inputStyle={"margin-right": "7.5px", "margin-left": "15px"}
        ),

        # Checkliste mit 
        dcc.Checklist(
            id= 'checklist-bloodflow',
            options=blood_flow_functions,

            style={'display': 'inline-block'}, # Damit Checklisten nebeneinander 
            labelStyle={"font-family": "Arial, Helvetica, sans-serif",
                "color": "white",
                'display': 'inline-block'},
            inputStyle={"margin-right": "7.5px", "margin-left": "15px"}
        )

    ], style={"margin-left": "1%",
        "margin-right": "1%",
        "margin-top": "1%",
        "padding": "1%",
        "height": "10%",
        "background-color": "rgb(70, 70, 70)",
        "border-radius": "10px",
        "display": "flex",                  
        "align-items": "center"}), # Damit Elemente vertikal in der Mitte

    # Vier Plots in Raster-Ansicht
    html.Div([

        # Zwei Plots nebeneinander
        html.Div([
            html.Div([
                dcc.Graph(
                    id='dash-graph0',
                    figure=fig0,
                    style={"border": "solid",
                        "border-width": "10px",
                        "border-color": "white",
                        "border-radius": "10px"}
                )
            ], style={"width": "49.5%",
                "display": "inline-block",
                "float": "left"}),

            html.Div([
                dcc.Graph(
                    id='dash-graph1',
                    figure=fig1,
                    style={"border": "solid",
                        "border-width": "10px",
                        "border-color": "white",
                        "border-radius": "10px"}
                )
            ], style={"width": "49.5%",
                "display": "inline-block",
                "margin-left": "1%"})

        ], style={"margin-bottom": "0.75%"}),

        # Zwei Plots nebeneinander
        html.Div([
            html.Div([
                dcc.Graph(
                    id='dash-graph2',
                    figure=fig2,
                    style={"border": "solid",
                        "border-width": "10px",
                        "border-color": "white",
                        "border-radius": "10px"}
                ),
            ], style={"width": "49.5%",
                "display": "inline-block",
                "float": "left"}),

            html.Div([
                dcc.Graph(
                    id='dash-graph3',
                    figure=fig3,
                    style={"border": "solid",
                        "border-width": "10px",
                        "border-color": "white",
                        "border-radius": "10px"}
                )
            ], style={"width": "49.5%",
                "display": "inline-block",
                "margin-left": "1%"})

        ]),
        
    ], style={"margin": "1%"})

])

### Callback Functions ###
## Graph Update Callback
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph0', 'figure'),
    Output('dash-graph1', 'figure'),
    Output('dash-graph2', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-algo','value')
)
def update_figure(value, algorithm_checkmarks):
    print("Current Subject: ",value)
    print("current checked checkmarks are: ", algorithm_checkmarks)
    ts = list_of_subjects[int(value)-1].subject_data
    #SpO2
    fig0 = px.line(ts, x="Time (s)", y = data_names[0])
    # Blood Flow
    fig1 = px.line(ts, x="Time (s)", y = data_names[1])
    # Blood Temperature
    fig2 = px.line(ts, x="Time (s)", y = data_names[2])
    
    ### Aufgabe 2: Min / Max ###

    return fig0, fig1, fig2 


## Blodflow Simple Moving Average Update
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph3', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-bloodflow','value')
)
def bloodflow_figure(value, bloodflow_checkmarks):
    
    ## Calculate Moving Average: Aufgabe 2
    print(bloodflow_checkmarks)
    bf = list_of_subjects[int(value)-1].subject_data
    fig3 = px.line(bf, x="Time (s)", y="Blood Flow (ml/s)")


    return fig3

if __name__ == '__main__':
    app.run_server(debug=True)