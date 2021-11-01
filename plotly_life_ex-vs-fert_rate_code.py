import io
import numpy as np
import pandas as pd
from base64 import b64encode
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

df_lifeexp = pd.read_excel("~/gapminder_lifeexpectancy.xlsx")
df_fert = pd.read_csv('~/gapminder_total_fertility.csv', index_col=0)
df_life = pd.read_excel('~/gapminder_lifeexpectancy.xlsx', index_col=0)

df_fert.columns = df_fert.columns.astype(int)
df_fert.index.name = 'country'
df_fert.reset_index(inplace=True) 
df_fert = df_fert.melt(id_vars='country', var_name='year', value_name='fertility_rate')

df_life.index.name = 'country'
df_life.reset_index(inplace=True) 
df_life = df_life.melt(id_vars='country', var_name='year', value_name='life_expectancy')

df_pop = pd.read_excel('~/spiced/random-forest-fennel-student-code/week_01/data/gapminder_population.xlsx', index_col=0)
df_pop.index.name = 'country'
df_pop.reset_index(inplace=True)
df_pop = df_pop.melt(id_vars='country', var_name='year', value_name='population')

df = df_fert.merge(df_pop)
df = df.merge(df_life)

df_cont = pd.read_csv('~/spiced/random-forest-fennel-student-code/week_01/data/continents.csv', index_col=0, sep=';')
df_cont = df_cont.reset_index()

df_total = pd.merge(df, df_cont, on='country', how='left')
df_total.dropna(inplace=True)

buffer = io.StringIO()

app = dash.Dash(__name__)

fig = px.scatter(df_total, x="life_expectancy", y="fertility_rate", animation_frame='year', animation_group='country',
                 size="population", color="continent", hover_name="country",
                 log_x=False, size_max=60, range_x=[30,90], range_y=[0,10], template='plotly_dark')
fig.write_html(buffer)

html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()

app.layout = html.Div([
    dcc.Graph(
        id='fert-rate-vs-life-exp',
        figure=fig
    ),
    html.A(
    html.Button("Download HTML"), 
    id="download",
    href="data:text/html;base64," + encoded,
    download="plotly_life_ex-vs-fert_rate.html"
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port=3000)

