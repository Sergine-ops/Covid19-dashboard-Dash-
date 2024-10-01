from dash import Dash,dcc,Input,Output,html
import pandas as pd
import plotly.express as px

df = pd.read_csv('data/covid_data.csv')
df = df.melt(id_vars=['Province/State','Country/Region','Lat','Long'],var_name='date',value_name='cases')
df.rename(columns={'Country/Region':'country','date':'date'},inplace=True)
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y') 


app= Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css'])

app.layout = html.Div([
    html.H1("Covid 19 Data Dashboard",style={'text-align':'center','color':'#4A2574','font-family':'Arial','font-weight':'bolder'}),
    dcc.Dropdown(id='country-dp',
    options=[{'label':country,'value':country} for country in df['country'].unique()],
    value='Albania',
    style={'width':'45%','margin':'auto','padding':'8px','font-size':'18px','font-weight':'bold','color':'#0F0529'}
    ),
    dcc.Graph(id="line-chart"),
],style={'background-color':'#f4f4f9','padding':'20px','font-family':'Arial'})

@app.callback(
    Output('line-chart','figure'),
    Input('country-dp','value')
)

def update(selected_country):
    filtered_df = df[df['country'] == selected_country]
    fig = px.line(filtered_df,x='date',y='cases',title=f'Cases in {selected_country}',
    template='plotly_dark')

    fig.update_layout(
        title={'x':0.5,'xanchor':'center','font':{'size':28,'color':'#4A2574','weight':700}},
        xaxis_title='Date',
        yaxis_title='Number of Cases',
        font=dict(family='Arial',size=14,color='azure'),
        xaxis=dict(showgrid=True, gridcolor='#4A2574'),
        yaxis=dict(showgrid=True, gridcolor='#4A2574')
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)    
