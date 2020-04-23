import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
import time
import seaborn as sns
import os

# Info 
# https://dash.plotly.com/dash-core-components/tab

directory = "assets/images/"
if not os.path.exists(directory):
    os.makedirs(directory)

# Input
df_nazionale = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
df_nazionale["data"] = pd.to_datetime(df_nazionale["data"]).dt.date
lista = ["data","ricoverati_con_sintomi","terapia_intensiva","totale_ospedalizzati","isolamento_domiciliare"]

# Funzioni
def plot_andamento_nazionale_plotly(df):
    # lista_input è una lista che contiene i nomi delle regioni da plottare
    # plot_number numero di grafici da plottare All o 10

    fig = go.Figure()
    my_dict={}
    my_dict["data"] = df["data"].unique()
    lista_keys_to_plot = list(df.keys()[2:-2])
    not_visible = ["variazione_totale_positivi","tamponi", "nuovi_positivi", "casi_testati"]

    for nome_key_to_plot in lista_keys_to_plot:
        my_dict[nome_key_to_plot] = list(df[nome_key_to_plot])

        visible_str=True
        if (nome_key_to_plot in not_visible):
            visible_str="legendonly"

        xx = my_dict["data"]
        yy = my_dict[nome_key_to_plot]

        fig.add_trace(go.Scatter(
                x = xx,
                y = yy,
                #legendgroup=nome_regione,
                name=nome_key_to_plot,
                mode="lines+markers",
                showlegend=True,
                visible=visible_str,
                marker=dict(
                    symbol="circle",
                    size=4,
                ),
                hoverlabel=dict(namelength=-1),
                #fill="tozeroy", # tonexty
                line=dict(
                    width=1,
                    #color="rgb(0,255,0)",
                    #dash="longdashdot"
                )
            ),
        )
        
    fig.update_layout(
        #title=dict(
        #    text ="Analisi Regionale" ,
            #y = 0.9,
            #x = 0.1, # 0.5 center
            #xanchor = "left",
            #yanchor = "top",
        #),
        legend=dict(
            orientation="v",
            #y = 1.1,
            #x = 0,
        ),
        xaxis = dict(
            title="data",
            gridcolor="cyan",
            #gridwidth=5,
            #color="red"
            #linecolor="red",
            zeroline=False,
        ),
        yaxis = dict(
            title="numero",
            gridcolor="cyan",
            #gridwidth=5,
            #linecolor = "red",
            zeroline=False,
            #zerolinecolor="cyan",
        ),
        font=dict(
        #    family="Courier New, monospace",
        #    size=20,
            color="white", #"#7f7f7f", 
        ),
        hovermode='x',  #['x unified', 'y', 'closest', False]
        plot_bgcolor = "rgb(44,44,44)",
        paper_bgcolor="rgb(33, 33, 33)",
        margin={"t":50, "b": 10}
        #transition = dict(
        #    duration=500,
        #    easing='cubic-in-out',
        #),
    )

    return fig

def plot_andamento_nazionale_seaborn(df_nazionale, lista=None):
    df_ridotto  = []
    if lista==None:
        df_ridotto = df_nazionale.drop(columns=["stato", "note_it", "note_en"])  
    else:
        df_ridotto = df_nazionale[lista]
    df_ridotto_tidy =  df_ridotto.melt('data', var_name='cols',  value_name='vals')
    # display(df_ridotto_tidy.head())
    fig_seaborn = sns.relplot(x="data", y="vals", hue="cols" ,data=df_ridotto_tidy, kind="line", aspect=3)
    #fig_seaborn.savefig("image.png")
    fig_seaborn.savefig("assets/images/fig_seaborn.png") #, transparent=True )
    return fig_seaborn

fig_seaborn = plot_andamento_nazionale_seaborn(df_nazionale)
fig_plotly = plot_andamento_nazionale_plotly(df_nazionale)


write = '''
# La nostra prima dashboard
## Realizzata con saeborn e dash

1. Importante
2. Balal
3. test

> Molto bella

```python
import pandas as pd
path ="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
df_nazionale = pd.read_csv(path)
df_nazionale["data"] = pd.to_datetime(df_nazionale["data"]).dt.date
lista = ["data","ricoverati_con_sintomi","terapia_intensiva","totale_ospedalizzati","isolamento_domiciliare"]
```
'''

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout =  html.Div([
        html.Div([
            
            html.Div([
                dcc.Markdown(
                    write,
                highlight_config=dict(theme="dark")),
            ], className="four_modified columns pretty_container"), #className="four columns pretty_container"),
            
            html.Div([
                html.H3("Analisi Nazionale"),
                html.P("Analisi Nazionale basata sul dataset covid19 fornito dalla protezione civile"),
            ], className="four_modified1 columns  pretty_container"),

            html.Div([
                html.H3("Analisi Nazionale"),
                html.P("Analisi Nazionale basata sul dataset covid19 fornito dalla protezione civile"),
            ], className="four_modified1 columns  pretty_container"),
        
            html.Div([
                html.H3("Analisi Nazionale"),
                html.P("Analisi Nazionale basata sul dataset covid19 fornito dalla protezione civile"),
                html.Img(src='/assets/images/fig_seaborn.png', className="center", id="fig-seaborn"),
            ], className="eigth_modified columns pretty_container"), # className="eight columns pretty_container"),
     
        ],className="row"),
        
        html.Div([
            
            html.Div([
                html.H3("Analisi Nazionale"),
                html.P("Analisi Nazionale basata sul dataset covid19 fornito dalla protezione civile"),
            ], className="four_modified columns pretty_container"),
            
            html.Div([
                dcc.Graph(id='fig-plotly', figure=fig_plotly)
            ], className="eigth_modified columns pretty_container"),
        
        ]),

    ],id="main")


if __name__ == '__main__':
    app.run_server(host="0.0.0.0",debug=True) # host="0.0.0.0", port=8800)
