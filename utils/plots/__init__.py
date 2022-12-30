import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot


def plot_convergence(task):
    # Name of the optimizer used in the execution
    optimizer = task['task_kwargs']['optimizer']['acronym']
    
    # Get list with fitness values
    fitness_values = task['result']['fitness_values']

    # Create a list with the iterations
    iterations = list(range(1, len(fitness_values) + 1))

    # Set up the plot
    fig = go.Figure()
    scatter = go.Scatter(
        name=optimizer,
        x=iterations,
        y=fitness_values,
        mode='lines',
        opacity=0.8,
        marker_color='blue',
        hovertemplate='(%{x}; %{y})'
    )
    fig.add_trace(scatter)
    fig.update_layout(
        legend_title='Otimizador',
        title_x=0.5,
        template='simple_white',
        xaxis=dict(
            title='Iteração',
            showgrid=False,
            rangemode='tozero',
        ),
        yaxis=dict(
            title='Valor da Função',
            showgrid=False,
            tickformat='.3f',
            showexponent='all',
            exponentformat='e'
        ),
        separators=',',
        margin=dict(l=0, r=0, t=30, b=30),
        showlegend=True
    )
    
    # Generate a div element with the plot
    plot_div = plot(fig, output_type='div', config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['resetScale']
    })
    
    return plot_div

def plot_bar(task):
    # Name of the optimizer used in the execution
    optimizer = task['task_kwargs']['optimizer']['acronym']
    
    executions = task['task_kwargs']['executions']

    # Distribution values for features
    distributions, stdev = get_distribution(task)
    
    # List with number of features in the distributions
    features = list(range(1, len(distributions) + 1))
    
    # Set up the plot
    fig = go.Figure()
    bar = go.Bar(
        name=optimizer,
        x=features,
        y=distributions,
        marker_color = 'blue',
        opacity=0.8,
        hovertemplate='(%{x}; %{y})'
    )

    if executions > 1:
      bar.error_y = go.bar.ErrorY(
        type='data',
        array=stdev
      )   
        
    fig.add_trace(bar)
    fig.update_layout(
        legend_title='Otimizador',
        title_x=0.5,
        template='simple_white',
        xaxis=dict(
            title='Característica',
            showgrid=False,
            tickvals=features
        ),
        yaxis=dict(
            title='Porcentagem de Ocorrência',
            showgrid=False,
            tickformat='.2f',
            showexponent='all',
            exponentformat='e'
        ),
        separators=',',
        margin=dict(l=0, r=0, t=30, b=30),
        showlegend=True
    )

    # Generate a div element with the plot
    plot_div = plot(fig, output_type='div', config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['resetScale']
    })
    
    return plot_div


# Helper function to get features distribution
def get_distribution(task):
    # Get list with features vector
    feature_vectors = get_feature_vectors(task)

    # Get number of features in a vector
    feature_count = len(feature_vectors[0])

    new_feature_vectors = []

    for vector in feature_vectors:
        new_feature_vectors.append(list(map(int, vector)))

    new_feature_vectors = np.array(new_feature_vectors)

    freq = (np.mean(np.array(new_feature_vectors), axis=0)*100).tolist()
    stdev = np.std(np.array(new_feature_vectors), axis=0).tolist()
    
    # Compute distributions based on freq
    return freq, stdev

# Helper function to get feature vectors
def get_feature_vectors(task):
    # Get number of executions
    executions = task['task_kwargs']['executions']
    
    # If there's only one execution, return the best features
    # vector in a list 
    if executions == 1:
        return [task['result']['best_features_vector']]

    # Create a list to hold features vector 
    feature_vectors = []
    
    # Access data from all executions and extract
    # the features vectors
    for i in range(executions):
        exec = "exec_" + str(i+1)
        
        feature_vectors.append(
            task['result'][exec]['best_selected_features']
        )
    
    # Return the list with feature vectors
    return feature_vectors

