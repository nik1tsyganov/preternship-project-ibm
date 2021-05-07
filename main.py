#!/usr/bin/env python3

import concurrent.futures
import os
import time
import sys
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import pandas as pd

from dash.dependencies import Input, Output
from LogFile import LogFile

# Dash setup
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


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


def callback(logs, errors, warnings, filename):
    print(f"Saving {len(logs)} logs to {filename}")
    curr = Data(logs, errors, warnings)
    return curr


def logFileFactory(filename):
    tmp = LogFile(filename)
    logs, errors, warnings = tmp.monitor_file(callback)
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

    # Dash stuff
    time.sleep(3)

    dropDownData = [{'label': x, 'value': x} for x in files]
    app.layout = html.Div(children=[
        html.H1(children='Log Graphing'),

        html.Label('Files'),
        dcc.Dropdown(
            id="file-choice",
            options=dropDownData,
            value=files[0]
        ),

        html.P(children='''
            Testing how logs are being graphed.
        '''),

        dcc.Graph(id='log-file-data'),

        html.P(children='''
            Pie Chart
        '''),

        dcc.Graph(id='log-pie-chart'),

        html.P(children='''
            Display table of error and warning logs.
        '''),

        dash_table.DataTable(
            id='table-virtualization',
            data=[],
            page_action='none'
        )
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
    def update_figure(selected_file):
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
        [Output("table-virtualization", "data")],
        [Input('file-choice', 'value')])
    def updateTable(selected_file):

        dataError = [{"id": index, "log": log.data} for index, log in enumerate(dataDict[files[0]].get_error_logs())]
        # dataWarning = [{"id": index, "log": log.data} for index, log in enumerate(dataDict[files[0]].get_warning_logs())]
        # data = [dataError, dataWarning]
        tblrows = dataError.to_dict('columns'),
        tblcols = [{'name': i, 'id': i} for i in data.columns],

        table = dct.DataTable(
            id='live-table',
            data=tblrows,
            columns=tblcols,
            style_cell={'textAlign': 'center', 'min-width': '50px'}
        )

    app.run_server(debug=True)


# Main Execution
if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
