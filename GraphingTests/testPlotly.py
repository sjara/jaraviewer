from plotly.offline import plot 
import plotly.graph_objs as go
import random
import numpy as np

#xVals = random.sample(range(100), 10)
#yVals = random.sample(range(100), 10)

#print(xVals)
#print(yVals)
#plot([Scatter(x = xVals, y = yVals)])
trace1 = go.Scatter(
    x= random.sample(range(10000), 1000),
    y= random.sample(range(10000), 1000)
)
trace2 = go.Scatter(
    x= random.sample(range(10000), 1000),
    y= random.sample(range(10000), 1000),
    xaxis='x2',
    yaxis='y'
)
trace3 = go.Scatter(
    x=random.sample(range(10000), 1000),
    y=random.sample(range(10000), 1000),
    xaxis='x',
    yaxis='y3'
)
trace4 = go.Scatter(
    x=random.sample(range(10000), 1000),
    y=random.sample(range(10000), 1000),
    xaxis='x4',
    yaxis='y4'
)
#currently not working
#trace5 = go.Box(y = np.random.randn(50), showlegend=False)
data = [trace1, trace2, trace3, trace4]
layout = go.Layout(
    xaxis=dict(
        domain=[0, 0.45]
    ),
    yaxis=dict(
        domain=[0, 0.45]
    ),
    xaxis2=dict(
        domain=[0.55, 1]
    ),
    xaxis4=dict(
        domain=[0.55, 1],
        anchor='y4'
    ),
    yaxis3=dict(
        domain=[0.55, 1]
    ),
    yaxis4=dict(
        domain=[0.55, 1],
        anchor='x4'
    )
)
fig = go.Figure(data=data, layout=layout)
plot(fig, filename = 'testPlotly.html')

