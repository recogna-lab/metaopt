import plotly.graph_objs as go
from plotly.offline import plot


def plot_convergence(error_values):
    # Create a list with the iterations
    iterations = list(range(1, len(error_values) + 1))
    
    # Set up the plot
    fig = go.Figure()
    scatter = go.Scatter(
        x=iterations,
        y=error_values,
        mode='lines',
        opacity=0.8,
        marker_color='blue')
    fig.add_trace(scatter)
    fig.update_layout(
        title='Gráfico de Convergência',
        title_x=0.5,
        template='simple_white',
        xaxis=dict(
            title='Iteração',
            showgrid=False,
            rangemode='tozero',
        ),
        yaxis=dict(
            title='Valor da função',
            showgrid=False,
            tickformat='.2e',
        ),
        margin=dict(
            l=0, 
            r=0, 
            t=30, 
            b=30
        ),
    )
    
    # Generate a div element with the plot
    plot_div = plot(fig, output_type='div', config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['resetScale']
    })
    
    return plot_div