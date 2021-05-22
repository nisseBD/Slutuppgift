import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as HTML
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Gör hemsidan pch ger tillgång till bootstrap
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Färger
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# genererar mockup data
regiontotaldata = pd.read_csv(
    "Regional_Totals_Data.csv", encoding="UTF-8", header=0)
genderdata = pd.read_csv("Gender_Data.csv", encoding="ISO-8859-1", header=0)
dagligadöda = pd.read_csv("National_Daily_Deaths.csv",
                          encoding="ISO-8859-1", header=0)
åldersgrupp = pd.read_csv("National_Total_Deaths_by_Age_Group.csv")

# Skapar Figs
figDagligadöda = px.line(
    dagligadöda, x="Date", y="National_Daily_Deaths", title="Coronastatistik för avlidna dagligen")

# Uppdaterar layouen (ger färg) för den statiska grafen
figDagligadöda.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

# Hemsidans layout
app.layout = dbc.Container(style={"backgroundColor": "black"}, children=[

    # Titel
    HTML.H1("Nils Coronagrafer"),

    # Gör en dropdown till första grafen där man kan mata in olika values
    dcc.Dropdown(
        id="drop1",
        options=[dict(label="Totala fall", value="Total_Cases"), dict(
            label="Akuta jukvårdsbesök", value="Total_ICU_Admissions"), dict(
            label="Totala dödsfall", value="Total_Deaths"), dict(
            label="Fall per Hundratusen", value="Cases_per_100k_Pop")],
        value="Total_Cases"

    ),

    # Grafens position
    dcc.Graph(
        id="graph1"
    ),

    # En till dropdown för båda pie chartsen
    dcc.Dropdown(
        id="drop2",
        options=[dict(label="Totala fall", value="Total_Cases"), dict(
            label="Akuta sjukvårdsbesök", value="Total_ICU_Admissions"), dict(
            label="Totala dödsfall", value="Total_Deaths")],
        value="Total_Cases"
    ),

    # Gör så att pie chartsen är bredvid varandra med två colummner
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id="graph2",
                )),

            dbc.Col(
                dcc.Graph(
                    id="graph4",
                )),
        ]),

    # Sista Grafens position
    dcc.Graph(
        id="graph3",
        figure=figDagligadöda
    ),

])

# Kallar tillbaka på den informationen man får från htmln


@ app.callback(
    # Den den plottar som "graph1"
    Output("graph1", "figure"),
    # Den informationen man får från dropdownen med idt "drop1" och tar dens value
    [Input("drop1", "value")]
)
# Uppdaterar grafen beroende på den value man valde i dropdown
def update_figure(value):
    # Plottar grafen
    fig = px.bar(regiontotaldata, x="Region", y=value,
                 title="Coronastatistik mellan regionerna")
    # Tiden som den tar att ändra graf när man ändrar value samt färg
    fig.update_layout(transition_duration=500,
                      plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text']),
    # Gör så att man kan se lite enklare på grafen hur många som har t.ex dött så att man slipper hålla med musen
    fig.update_traces(
        texttemplate='%{value:.2s}', textposition='outside')
    return fig


@ app.callback(
    Output("graph2", "figure"),
    [Input("drop2", "value")]
)
def update_figure(value):
    fig = px.pie(genderdata, names="Gender", values=value,
                 title="Coronastatistik mellan könen")
    fig.update_layout(transition_duration=500,
                      plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
    return fig


@ app.callback(
    Output("graph4", "figure"),
    [Input("drop2", "value")]
)
def update_figure(value):
    fig = px.pie(åldersgrupp, names="Age_Group", values=value,
                 title="Coronastatistik mellan åldersgrupperna")
    fig.update_layout(transition_duration=500,
                      plot_bgcolor=colors['background'], paper_bgcolor=colors['background'], font_color=colors['text'])
    return fig


# Startar servern
if __name__ == "__main__":
    app.run_server(debug=True)
