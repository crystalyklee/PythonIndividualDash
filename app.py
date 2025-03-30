import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load datasets
df_annual = pd.read_csv("annual.csv", engine='python')
df_generic = pd.read_csv("generic.csv", engine='python')
df_province = pd.read_csv("province.csv", engine='python')
df_therapy = pd.read_csv("therapy.csv", engine='python')

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server
app.title = "Insurance Claims Dashboard"

# App layout
app.layout = html.Div([
    html.H1("Insurance Claims Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.H3("Select Insurer for Cost Trends"),
        dcc.Dropdown(
            id='insurer-select',
            options=[{'label': i, 'value': i} for i in df_annual['Insurer'].unique()],
            value=df_annual['Insurer'].unique()[0],
            multi=False
        ),
        dcc.Graph(id='cost-over-time')
    ], style={"margin": "40px"}),

    html.Div([
        html.H3("Total Claimants and Costs by Insurer"),
        dcc.Graph(id='bar-insurer', figure=px.bar(
            df_annual.groupby("Insurer")["Claimants"].sum().reset_index(),
            x="Insurer", y="Claimants", color="Insurer",
            title="Total Claimants by Insurer",
            color_discrete_sequence=px.colors.qualitative.Set3
        )),
        dcc.Graph(id='cost-insurer', figure=px.bar(
            df_annual.groupby("Insurer")["Cost"].sum().reset_index(),
            x="Insurer", y="Cost", color="Insurer",
            title="Total Cost by Insurer",
            color_discrete_sequence=px.colors.qualitative.Set3
        ))
    ], style={"margin": "40px"}),

    html.Div([
        html.H3("Correlation Heatmap (Annual Data)"),
        dcc.Graph(id='correlation-heatmap', style={'width': '100%'}, figure=px.imshow(
            df_annual[["Claimants", "Cost", "Volumes"]].corr(),
            text_auto=True,
            title="Correlation Heatmap",
            aspect="auto",
            color_continuous_scale='Pinkyl'
        ))
    ], style={"margin": "40px"}),

    html.Div([
        html.H3("Claimants vs Cost by Province"),
        dcc.Graph(id='scatter-province', figure=px.scatter(
            df_province, x="Claimants", y="Cost", color="Province",
            title="Claimants vs Cost by Province",
            color_discrete_sequence=px.colors.qualitative.Pastel
        ))
    ], style={"margin": "40px"})

], style={
    "fontFamily": "'Poppins', 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif",
    "padding": "20px",
    "backgroundColor": "#fdf6f9"
})

# Callback for cost over time per insurer
@app.callback(
    Output('cost-over-time', 'figure'),
    Input('insurer-select', 'value')
)
def update_cost_graph(insurer):
    df_filtered = df_annual[df_annual['Insurer'] == insurer]
    fig = px.line(
        df_filtered, x='Year', y='Cost',
        title=f"Cost Over Time for {insurer}",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
