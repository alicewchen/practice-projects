# Import required libraries
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()
launch_site_opt = [
    {"label": site, "value": site} for site in spacex_df["Launch Site"].unique()
]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        html.Div(
            dcc.Dropdown(
                id="site-dropdown",
                options=[{"label": "All Sites", "value": "ALL"}] + launch_site_opt,
                value="ALL",
                searchable=True,
                style={
                    "width": "50%",
                    "padding": "3px",
                    "font-size": "20px",
                    "text-align-last": "center",
                },
            )
        ),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart"), style={"display": "flex"}),
        # html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        html.Div(
            dcc.RangeSlider(
                id="payload-slider",
                min=0,
                max=10000,
                step=1000,
                value=[min_payload, max_payload],
            ),
            style={"width": "50%"},
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(
            dcc.Graph(id="success-payload-scatter-chart"), style={"display": "flex"}
        ),
    ]
)


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def create_pie_chart(site_dropdown):
    if site_dropdown == "ALL":
        # spacex_df['Class'==1]
        fig = px.pie(
            spacex_df[spacex_df["class"] == 1],
            values="class",
            names="Launch Site",
            title="Total Success Launches in All Sites",
        )
        return fig
    else:
        site_df = (
            spacex_df[spacex_df["Launch Site"] == site_dropdown]
            .groupby("class")
            .count()
        )
        site_df.reset_index(inplace=True)
        fig = px.pie(
            site_df,
            values="Launch Site",
            names="class",
            title="Success vs. Failed Launches By Site",
        )
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
    Input(component_id="payload-slider", component_property="value"),
)
def create_scatter_chart(site_dropdown, payload_slider):
    min_payload, max_payload = payload_slider
    if site_dropdown == "ALL":
        site_df = spacex_df.loc[
            (spacex_df["Payload Mass (kg)"] >= min_payload)
            & (spacex_df["Payload Mass (kg)"] <= max_payload)
        ]
        fig = px.scatter(
            site_df,
            x="Payload Mass (kg)",
            y="class",
            labels={"class": "Launch Success"},
            # color="Booster Version Category",
            title="Correlation Between Payload and Success for All Sites",
        )
        return fig
    else:
        site_df = spacex_df.loc[
            (spacex_df["Launch Site"] == site_dropdown)
            & (spacex_df["Payload Mass (kg)"] >= min_payload)
            & (spacex_df["Payload Mass (kg)"] <= max_payload)
        ]
        fig = px.scatter(
            site_df,
            x="Payload Mass (kg)",
            y="class",
            labels={"class": "Launch Success"},
            # color="Booster Version Category",
            title="Correlation Between Payload and Success for " + site_dropdown,
        )
        return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
