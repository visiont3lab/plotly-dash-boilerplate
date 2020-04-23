import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
import time
import seaborn as sns
import os
import plotly.express as px

# Info 
# https://dash.plotly.com/dash-core-components/tab

directory = "assets/images/"
if not os.path.exists(directory):
    os.makedirs(directory)

# Input
df_nazionale = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
df_nazionale["data"] = pd.to_datetime(df_nazionale["data"]).dt.date
lista = ["data","ricoverati_con_sintomi","terapia_intensiva","totale_ospedalizzati","isolamento_domiciliare"]
input_lista = list(df_nazionale.columns)[2:12]

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

def plotly_andamento_italia(df, lista=["ricoverati_con_sintomi","totale_casi","deceduti"]):
    fig = go.Figure()
    for nome in lista:
        #print(nome.replace("_"," "))
        fig.add_trace(go.Scatter(x=df["data"], y=df[nome],mode='lines+markers', name=nome.replace("_"," ")))
    
    fig.update_layout(
        hovermode = "x",
        paper_bgcolor = "rgb(0,0,0)" ,
        plot_bgcolor = "rgb(10,10,10)" , 
        #title=dict(
        #    text = "Andamento Italia",
        #    x = 0.5,
        #    font=dict(
        #        color =  "rgb(0,255,0)",
        #    )
        #)
    )
    return fig

def plotly_express_andamento_italia(df, lista=None):
    if lista ==None:
        df = df.drop(columns=["stato", "note_it", "note_en"])
        df_tidy = df.melt('data', var_name='cols',  value_name='vals')
    else:
        if "data" not in lista:
            lista.append("data")
        df_temp = df[lista]
        df_tidy = df_temp.melt('data', var_name='cols',  value_name='vals')

    fig = px.line(df_tidy, x="data", y="vals",  color="cols", template="plotly_dark",hover_name="cols", line_group="cols") # marginal_y="box", marginal_x="violin"
    fig.update_layout(
        hovermode = "x", 
    )
    return fig

fig_seaborn = plot_andamento_nazionale_seaborn(df_nazionale)
#fig_plotly = plot_andamento_nazionale_plotly(df_nazionale)
fig_plotly = plotly_andamento_italia(df_nazionale,input_lista)
fig_ploty_express = plotly_express_andamento_italia(df_nazionale, input_lista)

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
            dcc.Markdown(
                write,
            highlight_config=dict(theme="dark")),
        ], className="pretty_container"),
    
        html.Div([
          html.Img(src='/assets/images/fig_seaborn.png', className="center", id="fig-seaborn"),
        ], className="pretty_container"),

        html.Div([
            html.H3("Analisi Nazionale"),
            html.P("Analisi Nazionale basata sul dataset covid19 fornito dalla protezione civile"),
        ], className="four_modified1 columns  pretty_container"),


        html.Div([
            html.H3("fdfsd", className="myh3"),
            html.P("o dalla protezione civile"),
        ], className="pretty_container"),

        html.Div([
            html.H1("Mio titolo",className="myh3" ),
            dcc.Markdown('''
            # Titolo
            *fdfd*

            1. fdfd
            2. t45t4
            3. fdfdf

            **This text will be bold**

            __This will also be bold__

            _You **can** combine them_


            [Nome del link](https://www.youtube.com/?hl=it&gl=IT)

            ```python
            import 
            ```

            ''', highlight_config=dict(theme='light')),
        ], className="pretty_container"),
        
        html.Div([
            html.H1("Andamento Covid italia",className="myh3" ),
            dcc.Markdown('''
            Il covid è un virus, blabla
            Ha i seguinti punti

                * ds
                * ds
                *  sd

            Da notare
            
            > jdisajd djskldj sdjs

            La fifgura reappressenta xxzzzzzzzzzzzz
            xzxxxxxxxxxx
            xzxzxxxxxxxx

            Ê stata realizzata con il seguente blocco di codice
            
            ```python
            def plotly_andamento_italia(df, lista=["ricoverati_con_sintomi","totale_casi","deceduti"]):
                fig = go.Figure()
                for nome in lista:
                    #print(nome.replace("_"," "))
                    fig.add_trace(go.Scatter(x=df["data"], y=dt[nome],mode='lines+markers', name=nome.replace("_"," ")))
                
                fig.update_layout(
                    hovermode = "x",
                    paper_bgcolor = "rgb(0,0,0)" ,
                    plot_bgcolor = "rgb(10,10,10)" , 
                    title=dict(
                        text = "Andamento Italia",
                        x = 0.5,
                        font=dict(
                            color =  "rgb(0,255,0)",
                        )
                    )
                )
                return fig

            input_lista = list(df_nazionale.columns)[2:12]
            fig = plotly_andamento_italia(df_nazionale,input_lista)
            fig.show()
            ```
            ''', highlight_config=dict(theme="dark")),
            dcc.Graph(id="fig-plotly", figure=fig_plotly),
        ], className="pretty_container"),

        html.Div([
            dcc.Graph(id="fig-plotly-express", figure=fig_ploty_express)      
        ],className="pretty_container")
    
    ],id="main")


if __name__ == '__main__':
    app.run_server(host="0.0.0.0",debug=True) # host="0.0.0.0", port=8800)
