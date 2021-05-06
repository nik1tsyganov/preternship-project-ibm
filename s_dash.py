import plotly.graph_objects as go
import plotly.offline as pyo
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

firstrow = dbc.Row(
    [
        dbc.Col(
            dcc.Dropdown(
                options = [{'label': 1, 'value': 1}, {'label': 2, 'value': 2}]
            ),
            md = 2
        ),
        dbc.Col(
            html.H2('log entry text goes here'),
            md = 10
        )
    ]
)

secondrow = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(),
            md = 6
        ),
        dbc.Col(
            dcc.Graph(),
            md = 6
        )
    ]
)


app = dash.Dash()

app.layout = html.Div(
    [
        html.H1('Title Goes Here'),
        firstrow,
        secondrow
    ]
)

if __name__ == '__main__':
    app.run_server()
