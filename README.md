# plotly-dash-boilerplate

> Update

Cliccare questo link per provare e modicare la dashboard 
[![Run on Repl.it](https://repl.it/badge/github/visiont3lab/plotly-dash-boilerplate)](https://repl.it/github/visiont3lab/plotly-dash-boilerplate)

**Importante** 
> Per generare grafic è possibile utilizzare [Chart Studio Plotly](https://plotly.com/chart-studio/) (Tool Web Grafico per creare figure senza riga di codice). Le figure poi possono essere importate facilmente nell'applicazione in quanto dash usa json per scambiare file tra frontend e backend.

Una dashorboad più complessa basata su questo esempio è la [covid19-dash-plotly](https://github.com/visiont3lab/covid19-dash-plotly)

## Spiegazione 
Dash  è un react (frontend) , Dash (flask based python) framework che permette di costruire dashboard interattive principalmente usando codice python e la libreria plotly.

Questo repositorio permette di creare una dashboard utilizzando l'editor online [repl.it](https://repl.it/)


## Data
I Dataset utilizzati sono disponibili ai seguenti link:

* [Dati COVID-19 Italia](https://github.com/pcm-dpc/COVID-19)
  * [Dati andamento nazionale csv](https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv)
  * [Dati andamento regionale csv](https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv)
  * [Dati andamento provinciale csv](https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv)
  
* [Covid World Data](https://github.com/open-covid-19/data)


## Sviluppo Local (Local Development)

```
pip install -r requirements.txt
python app.py
```

## Link Utili (References)
* [Dash Documentation](https://dash.plotly.com/)
* [Dash Gallery examples](https://dash-gallery.plotly.host/Portal/)
* [Plotly Express](https://plotly.com/python/plotly-express/)
* [Plotly](https://plotly.com/python/)
* [Chart Studio Plotly](https://plotly.com/chart-studio/)
