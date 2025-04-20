
import plotly.graph_objects as go

def create_donut_chart(df, value):
    if value not in ["Frequency","Topic_Percentage","Class_Percentage"]:
        raise ValueError(f"{value} is not a discrete column from the df in parameter")

    fig = go.Figure(data=[go.Pie(labels=df['Name'], 
                                 values=df[value], 
                                 hole=.6,
                                #  marker=dict(colors=palette), 
                                # default:['#1f77b4',  '#ff7f0e',  '#2ca02c',  '#d62728',  '#9467bd',  '#8c564b',  '#e377c2',  '#7f7f7f',  '#bcbd22',  '#17becf']
                                 hovertemplate='%{label}: %{value}<extra></extra>'
                                )
                    ])
    
    fig.update_layout(
        legend_title_text='Topics',
        title={'text': "Topics' Repartition",
               'y':0.9,'x':0.5,
               'xanchor': 'center','yanchor': 'top'},
        title_font=dict(size=20,
                        color='rgb(107, 107, 107)'),
        autosize=False,
        width=800,
        height=500
    )

    return fig