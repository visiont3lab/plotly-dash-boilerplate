# https://stackoverflow.com/questions/53622518/launch-a-dash-app-in-a-google-colab-notebook
### Save file with Dash app on the Google Colab machine

# Deployment https://dash.plotly.com/deployment

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
import time

def get_nomi_regioni(df):
    nomi_regioni = list(df["denominazione_regione"].unique())
    nomi_regioni.sort()
    return nomi_regioni

def get_nomi_province(df, regione=None):
    
    # Nomi delle prime num provincie per numero di casi 
    ultima_data_aggiornamento = list(df.tail(1)["data"])[0]
    # Dataframe regione scelta e ultima data aggiornamento
    el = 'In fase di definizione/aggiornamento'
    if regione==None:
        temp = df[(df["data"]==ultima_data_aggiornamento) & (df["denominazione_provincia"]!=el)] 
    else:
        temp = df[(df["denominazione_regione"]==regione) & (df["data"]==ultima_data_aggiornamento) & (df["denominazione_provincia"]!=el)]
    # Ordina dal più grande al più piccolo
    temp.sort_values(by="totale_casi",ascending=False, inplace=True)
    nomi_province = list(temp["denominazione_provincia"]) #[0:num])

    # Nomi pronvicie 
    #nomi_province = list(df["denominazione_provincia"].unique())
    return nomi_province

def get_data_provincia(df, provincia="Bologna", regione="Emilia-Romagna"):
    # Estrai i dati relativi alla regione=regione e provincia=pronvincia
    df_choice = df[ (df["denominazione_regione"]==regione) & (df["denominazione_provincia"]==provincia)]
    df_fin = df_choice[["data", "denominazione_regione","denominazione_provincia","lat","long","totale_casi"]]
    return df_fin

def get_info_data(df):
    # Usiamo dataset andamento nazionale
    totale_positivi  = df.tail(1)["totale_positivi"].values[0]
    dimessi_guariti  = df.tail(1)["dimessi_guariti"].values[0]
    deceduti  = df.tail(1)["deceduti"].values[0]
    nuovi_positivi  = df.tail(1)["nuovi_positivi"].values[0]
    totale_casi  = df.tail(1)["totale_casi"].values[0]
    return totale_positivi,dimessi_guariti,deceduti,nuovi_positivi,totale_casi
    
def plot_regioni(df,lista_regioni_to_plot,lista_keys_to_plot=None, plot_style=None ):
    # lista_input è una lista che contiene i nomi delle regioni da plottare
    # plot_number numero di grafici da plottare All o 10

    if plot_style=="area_plot":
        plot_style_string = "tozeroy"
    else: 
        plot_style_string = "none"

    lista = []
    if isinstance(lista_regioni_to_plot, list)==False:
        lista.append(lista_regioni_to_plot)
    else:
        lista = lista_regioni_to_plot   

    if lista_keys_to_plot==None:
        lista_keys_to_plot = ['deceduti', 'variazione_totale_positivi','terapia_intensiva'] # list(df.keys()[6:-2]) 
 
    fig_reg = go.Figure()
    my_dict={}
    my_dict["data"] = df["data"].unique()
    for nome_regione in lista:
        for nome_key_to_plot in lista_keys_to_plot:
            my_dict[nome_key_to_plot] = list(df[df["denominazione_regione"]==nome_regione][nome_key_to_plot])

            xx = my_dict["data"]
            yy = my_dict[nome_key_to_plot]
    
            fig_reg.add_trace(go.Scatter(
                    x = xx,
                    y = yy,
                    #legendgroup=nome_regione,
                    name=nome_regione + " (" +nome_key_to_plot + ")",
                    mode="lines", #+markers",
                    showlegend=True,
                    #marker=dict(
                    #    symbol="circle-dot",
                    #    size=6,
                    #),
                    hoverlabel=dict(namelength=-1),
                    fill=plot_style_string, # tonexty
                    line=dict(
                        width=2,
                        #color="rgb(0,255,0)",
                        #dash="longdashdot"
                    )
                ),
            )
        
    fig_reg.update_layout(
        #title=dict(
        #    text ="Analisi Regionale" ,
            #y = 0.9,
            #x = 0.1, # 0.5 center
            #xanchor = "left",
            #yanchor = "top",
        #),
        legend=dict(
            orientation="v",
            #traceorder="grouped",
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
        margin={"t":50, "b": 10},
        #transition = dict(
        #    duration=500,
        #    easing='cubic-in-out',
        #),
    )
    return fig_reg

def plot_nazionale(df):
    # lista_input è una lista che contiene i nomi delle regioni da plottare
    # plot_number numero di grafici da plottare All o 10

    fig = go.Figure()
    my_dict={}
    my_dict["data"] = df["data"].unique()
    lista_keys_to_plot = list(df.keys()[2:-2])
    not_visible = ["variazione_totale_positivi","tamponi", "nuovi_positivi"]

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

def plot_variazione_nazionale(df):
    # lista_input è una lista che contiene i nomi delle regioni da plottare
    # plot_number numero di grafici da plottare All o 10

    fig = go.Figure()
    my_dict={}
    my_dict["data"] = df["data"].unique()
    lista_keys_to_plot = ["variazione_totale_positivi", "nuovi_positivi"]

    for nome_key_to_plot in lista_keys_to_plot:
        my_dict[nome_key_to_plot] = list(df[nome_key_to_plot])

        xx = my_dict["data"]
        yy = my_dict[nome_key_to_plot]

        fig.add_trace(go.Scatter(
                x = xx,
                y = yy,
                #legendgroup=nome_regione,
                name=nome_key_to_plot,
                mode="lines+markers",
                showlegend=True,
                marker=dict(
                    symbol="circle",
                    size=6,
                ),
                hoverlabel=dict(namelength=-1),
                fill="tozeroy", # tonexty
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
            orientation="h",
            y = 1.1,
            x = 0,
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

regione ="Emilia-Romagna"
provincia = "Bologna"

# Dati per provincia
df_nazionale = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
df_nazionale["data"] = pd.to_datetime(df_nazionale["data"]).dt.date
fig_naz = plot_nazionale(df_nazionale)
fig_var_naz = plot_variazione_nazionale(df_nazionale)
totale_positivi,dimessi_guariti,deceduti,nuovi_positivi,totale_casi = get_info_data(df_nazionale)


# Dati per provincia
df_regioni = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv")
df_regioni["data"] = pd.to_datetime(df_regioni["data"]).dt.date
fig_reg = plot_regioni(df_regioni, regione)

df = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv")
df["data"] = pd.to_datetime(df["data"]).dt.date
lista_date = (df["data"].unique())
ultima_data = lista_date[-1].strftime("%A %d %b  %Y")
dict_date={}
for c in range(0,len(lista_date),3):
    # https://www.guru99.com/date-time-and-datetime-classes-in-python.html
    dict_date[c] = {"label": lista_date[c].strftime("%b %d")} 

nomi_regioni_province = ["Tutte"] +  get_nomi_regioni(df) + get_nomi_province(df)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout =  html.Div([
        html.Div([
            html.H3("Analisi Nazionale"),
            dcc.Graph(id='fig-naz', figure=fig_naz)
        ], className="pretty_container"),
        html.Div([
            html.H3("Variazione Nazionale Totale Positivi"),
            dcc.Graph(id='fig-var-naz', figure=fig_var_naz)
        ], className="pretty_container"),
        html.Div([
            html.H3("Analisi Regionale"),
            dcc.Dropdown(
                id="dropdown-regioni",
                options=[{'label':nome, 'value':nome} for nome in get_nomi_regioni(df)],
                value=regione,
                searchable=True,
                multi=True
            ), 
            dcc.RadioItems(
                id = "radio-buttom-plot-style",
                options=[
                    {'label': 'line plot', 'value': 'line_plot'},
                    {'label': 'area plot', 'value': 'area_plot'},
                ],
                value='area_plot',
                labelStyle={'display': 'inline-block'}
            ),   
            dcc.Graph(id='fig-reg', figure=fig_reg),
            dcc.Checklist(
                id="checklist",
                options=[{'label':  nome.replace("_"," "), 'value': nome} for nome in list(df_regioni.keys()[6:-2])],
                value=['deceduti', 'variazione_totale_positivi','terapia_intensiva'],
                labelStyle={'display': 'inline-block'}
            ),  
        ],className="pretty_container"),
    ],id="main")


@app.callback(dash.dependencies.Output('fig-reg', 'figure'),
    [dash.dependencies.Input('checklist', 'value'),
    dash.dependencies.Input('radio-buttom-plot-style', 'value'),
    dash.dependencies.Input('dropdown-regioni', 'value')])
def update_fig_reg(checklist_value, plot_style_value, dropdown_regioni_value):
    #print(checklist_value)
    fig_reg = plot_regioni(df_regioni, dropdown_regioni_value, checklist_value,plot_style_value)
    return fig_reg


if __name__ == '__main__':
    app.run_server(host="0.0.0.0") #debug=True, host="0.0.0.0", port=8800)