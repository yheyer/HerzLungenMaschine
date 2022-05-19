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

# Pfad für Ordner input_data
folder_current = os.path.dirname(__file__) 
print(folder_current)
folder_input_data = os.path.join(folder_current, "input_data")

# .csv Dateien durchgehen und Daten in Objekt Subject speichern
for file in os.listdir(folder_input_data):
    if file.endswith(".csv"):
        number_of_subjects += 1
        file_name = os.path.join(folder_input_data, file)
        print(file_name)
        list_of_subjects.append(ut.Subject(file_name))

# Default Werte für Graphen setzen
df = list_of_subjects[0].subject_data

# Array mit Subject-IDs
for i in range(number_of_subjects):
    subj_numbers.append(list_of_subjects[i].subject_id)

#------------

# Listen mit Labels für Graph und Checklisten
data_names = ["SpO2 (%)", "Blood Flow (ml/s)","Temp (C)"]
algorithm_names = ['Min','Max']
blood_flow_functions = ['CMA','SMA','Limits']

fig0= go.Figure()
fig1= go.Figure()
fig2= go.Figure()
fig3= go.Figure()

# Graphen mit default Werten und beschrifteten Achsen erstellen
fig0 = px.line(df, x="Time (s)", y = data_names[0])
fig1 = px.line(df, x="Time (s)", y = data_names[1])
fig2 = px.line(df, x="Time (s)", y = data_names[2])
fig3 = px.line(df, x="Time (s)", y = data_names[1])

#------------

# App Layout: HTML und CSS wird hier erstellt und dann in wirkliche HTML Datei mit CSS umgewandelt
# CSS Styling teilweise in style.css ausgelagert
app.layout = html.Div([
    
    # Überschrift mit Umrandung
    html.Div(children=[
        html.H1(children='Cardiopulmonary Bypass Dashboard')
        ]
    ),

    # Auswahl und Filter
    html.Div(children=[

        # Label für Dropdown:
        html.Div([
            html.Label("Select a subject:")
        ]),

        # Dropdown zur Auswahl
        html.Div([
            dcc.Dropdown(options = subj_numbers, value='1', id='subject-dropdown'),
            html.Div(id='dd-output-container')
        ], className="div-dropdown"),

        # Label für Checklisten:
        html.Div([
            html.Label("Select filters:")
        ]),

        # Checkliste mit min und max
        dcc.Checklist(
            id= 'checklist-algo',
            options=algorithm_names,

            # CSS Attribute für Checklisten wegen label und input nicht in style.css ausgelagert
            style={'display': 'inline'}, 
            labelStyle={"font-family": "Arial, Helvetica, sans-serif",
                "color": "white",
                'display': 'inline'},
            inputStyle={"margin-right": "7.5px", "margin-left": "15px"}
        ),

        # Checkliste mit CMA SMA und Limits
        dcc.Checklist(
            id= 'checklist-bloodflow',
            options=blood_flow_functions,

            # CSS Attribute für Checklisten wegen label und input nicht in style.css ausgelagert
            style={'display': 'inline'},
            labelStyle={"font-family": "Arial, Helvetica, sans-serif",
                "color": "white",
                'display': 'inline'},
            inputStyle={"margin-right": "7.5px", "margin-left": "15px"}
        )

    ], className="div-dropdown-checklist"),

    # Vier Plots in Raster-Ansicht
    html.Div([

        # Zwei Plots nebeneinander
        html.Div([
            html.Div([
                dcc.Graph(
                    id='dash-graph0',
                    figure=fig0,
                    className="graph"
                )
            ], className="div-graph-left"),

            html.Div([
                dcc.Graph(
                    id='dash-graph1',
                    figure=fig1,
                    className="graph"
                )
            ], className="div-graph-right")

        ], style={"margin-bottom": "0.75%"}),

        # Zwei Plots nebeneinander
        html.Div([
            html.Div([
                dcc.Graph(
                    id='dash-graph2',
                    figure=fig2,
                    className="graph"
                ),
            ], className="div-graph-left"),

            html.Div([
                dcc.Graph(
                    id='dash-graph3',
                    figure=fig3,
                    className="graph"
                )
            ], className="div-graph-right")

        ]),
        
    ], style={"margin": "1%",
        "margin-bottom": "0.5%"})

])


#-----Callback Functions------------------

# Callback handelt als Input die Checkliste für CMA SMA Limits und Output Graph 3
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph0', 'figure'),
    Output('dash-graph1', 'figure'),
    Output('dash-graph2', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-algo','value')
)

# Hier werden 3 von 4 (bis auf letze Bloodflow) verändert
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


# Callback handelt als Input die Checkliste für CMA SMA Limits und Output Graph 3
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph3', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-bloodflow','value')
)

# Hier wird nur der letze Graph mit Bloodflow verändert
def bloodflow_figure(value, bloodflow_checkmarks):
    
    ## Calculate Moving Average: Aufgabe 2
    print(bloodflow_checkmarks)
    bf = list_of_subjects[int(value)-1].subject_data
    fig3 = px.line(bf, x="Time (s)", y="Blood Flow (ml/s)")


    return fig3

if __name__ == '__main__':
    app.run_server(debug=True)