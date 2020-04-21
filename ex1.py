import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
import time
import seaborn as sns
import os
directory = "assets/images/"
if not os.path.exists(directory):
    os.makedirs(directory)

# Input
df_nazionale = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
df_nazionale["data"] = pd.to_datetime(df_nazionale["data"]).dt.date
lista = ["data","ricoverati_con_sintomi","terapia_intensiva","totale_ospedalizzati","isolamento_domiciliare"]

# Funzioni
def plot_andamento_nazionale(df_nazionale, lista=None):
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

fig_seaborn = plot_andamento_nazionale(df_nazionale)

write = '''
# La nostra prima dashboard
## Realizzata con saeborn e dash

1. Importante
2. Balal
3. test

> Molto bella

```
x=5
```
'''

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout =  html.Div([
        html.Div([
            dcc.Markdown(
                write,
            ),
        ], className="row pretty_container"),
        html.Div([
          html.Img(src='/assets/images/fig_seaborn.png'),
        ], className="row pretty_container"),
    ],id="main")


if __name__ == '__main__':
    app.run_server(host="0.0.0.0") #debug=True, host="0.0.0.0", port=8800)
