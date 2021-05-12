#!/usr/bin/env python3

import concurrent.futures
import os
import sys
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from LogEntry import Status
import plotly.express as px
import pandas as pd

from dash.dependencies import Input, Output
from LogFile import LogFile

# Dash setup
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Class Data
class Data:
    def __init__(self, logEntries, errorLogs, warningLogs):
        self.logEntries = logEntries
        self.errorLogs = errorLogs
        self.warningLogs = warningLogs

    def get_error_logs(self):
        return [self.logEntries[i] for i in self.errorLogs]

    def get_warning_logs(self):
        return [self.logEntries[i] for i in self.warningLogs]

    def __repr__(self):
        return f"{self.logEntries}, {self.get_warning_logs()}, {self.get_error_logs()}"


# Functions
def usage(exit_code=0):
    progname = os.path.basename(sys.argv[0])
    print(f'''Usage: {progname} [-c CORES] FILE.log...
    -c CORES    CPU Cores to use. Must be greater than
                or equal to number of files provided''')
    sys.exit(exit_code)


def logFileFactory(filename):
    tmp = LogFile(filename)
    logs, errors, warnings = tmp.monitor_file()
    return Data(logs, errors, warnings)


def main():
    arguments = sys.argv[1:]
    cores = 1
    files = []

    while len(arguments) > 0:
        arg = arguments[0]
        if arg == '-c':
            arguments.pop(0)
            cores = int(arguments[0])
        elif arg == '-h':
            usage(0)
        elif arg.startswith("-"):
            usage(1)
        elif arg.endswith(".log"):
            files.append(arg)
        else:
            usage(1)

        arguments.pop(0)

    if len(files) > cores:
        usage(1)

    with concurrent.futures.ProcessPoolExecutor(max_workers=cores) as executor:

        dataDict = {}
        store = [x for x in executor.map(logFileFactory, files)]
        for i in range(cores):
            dataDict[files[i]] = store[i]

    # Dash UI
    dropDownData = [{'label': x, 'value': x} for x in files]
    dropDownLog = [{'label': x.name, 'value': x.value} for x in Status]
    # print(dropDownData)
    # print(dropDownLog)
	
    title_style = {
		'text-align':'center',
		'color': '#191970',
		'font-family':'Courier'
	}

    subtitle_style = {
		'color': '#FFFFFF',
	}


    main_style = {
		'backgroundColor' : '#0077B6',
		'width':'2000px',
		'margin-left':'10%',
		'margin-right':'10%',
		'padding':'20px 20px'
	} 
		

    app.layout = dbc.Container(style=main_style, children=[
		dbc.Row([html.H1(children="IBM Preternship Project", style=title_style)]),	
            
		dbc.Row([html.H2(children="Log File Monitoring", style=title_style)]),

		html.Hr(),

		html.Label(children="This display shows the distribution between error and warning logs for a given file.", style=subtitle_style),

		html.Hr(),
        
        dbc.Row([html.H2(children='Choose a File:',style=subtitle_style)]),
		
		html.Label(children="All visualizations will be reflective of the logs in the file that you choose.", style=subtitle_style), 

		dbc.Row([
		    dcc.Dropdown(
                    id="file-choice",
                    options=dropDownData,
                    value=files[0],
					style={'width': '400px'}
            )
		]),
		
		html.Hr(),	
        
        dbc.Row([
			dbc.Col([
				html.H3(children='Bar Graph', style=subtitle_style), 

                dcc.Graph(id='log-file-data')
	
            ], md = 6),

            dbc.Col([
				    
                html.H3(children='Pie Chart', style=subtitle_style),

                dcc.Graph(id='log-pie-chart')   
				             
		    ], md = 6),

		]),

		html.Hr(),

		dbc.Row([html.H2('Choose a Log Status:', style=subtitle_style)]),

		dbc.Row([dcc.Dropdown(
                    id="log-choice",
                    options=dropDownLog,
                    value=Status.WARN.value,
					style={'width': '400px'}
			   )
		]),

		html.Hr(),

        dbc.Row([html.H3(children='Display Log Entries for a Given Status', style=subtitle_style)]),

		html.Label(children='The table shows the log entries for the chosen status along with its corresponding line number within the file', style=subtitle_style),

        dbc.Row([dash_table.DataTable(
            id='live-table',
            data=[],
            columns=[],
            style_cell={'textAlign': 'left',
                        'whiteSpace': 'normal',
                        'height': 'auto'},
            style_header={'minWidth': '50px'},
            page_size=15
        )]),
    ])

    @app.callback(
        Output('log-file-data', 'figure'),
        Input('file-choice', 'value'))
    def update_figure(selected_file):
        data = dataDict[selected_file]

        df = pd.DataFrame({
            "Log Status": ["Error", "Warning"],
            "# of Logs": [len(data.errorLogs),
                          len(data.warningLogs)],
            "Status": ["Error", "Warning"]
        })

        fig = px.bar(df,
                     title="Bar Graph Distribution of Error and Warning Logs",
                     x="Log Status",
                     y="# of Logs",
                     color="Status",
                     barmode="group")

        return fig

    @app.callback(
        Output('log-pie-chart', 'figure'),
        Input('file-choice', 'value'))
    def update_pie_chart(selected_file):
        data = dataDict[selected_file]

        df = pd.DataFrame({
            "Log Status": ["Error", "Warning"],
            "# of Logs": [len(data.errorLogs), len(data.warningLogs)]
        })

        fig = px.pie(df,
                     title="Pie Chart Distribution of Error and Warning Logs",
                     values="# of Logs",
                     names="Log Status")

        return fig

    @app.callback(
        Output("live-table", "data"),
        Output("live-table", "columns"),
        Output("live-table", "page_current"),
        Input('file-choice', 'value'),
        Input('log-choice', 'value')
    )
    def plot_table(selected_file, status):
        logs = [x for x in dataDict[selected_file].logEntries if x.status.value == status]

        data = pd.DataFrame({'Line #': [x.index for x in logs],
                             'Log': [x.data for x in logs]})

        return (data.to_dict('records'),
                [{'name': ix, 'id': ix} for ix in data.columns],
                0)
   

    app.run_server(debug=True)


# Main Execution
if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
