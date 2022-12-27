import plotly.graph_objs as go
from plotly.offline import plot

import numpy as np

def get_distribution(task):
    """Gets the distribution of each feature

    Args:
        task (dict): A task's dictionary

    Returns:
        list: A list containing the distribution's percentage of each feature

    """

    executions = task['task_kwargs']['executions']

    feature_vectors = get_feature_vectors(task, executions)

    qtde_features = len(feature_vectors[0])
    quantities = []

    for i in range(qtde_features):
        quantities.insert(i, 0)

    for feature_vector in feature_vectors:
        for chave, feature in enumerate(feature_vector):
            if feature:
                quantities[chave] += 1
    
    distributions = [(i/executions * 100) for i in quantities]

    return distributions

def get_feature_vectors(task, executions):
    """Gets the feature's vectors of each execution if there are

    Args:
        task (dict): A task's dictionary
        executions: The number of indepedent executions
    
    Returns:
        list: A list where each position is a feature vector
    """

    feature_vectors = []

    if executions == 1:
        feature_vectors.append(task['result']['best_features_vector'])

    else:
        for i in range(executions):
            name = "exec_" + str(i+1)
            feature_vectors.append(task['result'][name]['best_selected_features'])

    return feature_vectors

def plot_convergence(task):
    """Plots a graphic for fitness value over the iterations

    Args:
        task (dict): A task's dictionary

    Returns:
        plotly: An object plotly which contains a HTML version of the graphic
    """
    
    fitness_values = task['result']['fitness_values']

    # Create a list with the iterations
    iterations = list(range(1, len(fitness_values) + 1))
    
    name_opt = task['task_kwargs']['optimizer']

    # Set up the plot
    fig = go.Figure()
    scatter = go.Scatter(
        name = str(name_opt),
        x=iterations,
        y=fitness_values,
        mode='lines',
        opacity=0.8,
        marker_color='blue')
    fig.add_trace(scatter)
    fig.update_layout(
        title='Gráfico de Convergência',
        title_x=0.5,
        legend_title="Otimizador",
        template='simple_white',
        xaxis=dict(
            title='Iteração',
            showgrid=False,
            rangemode='tozero',
        ),
        yaxis=dict(
            title='Valor da Função',
            showgrid=False,
            tickformat='.4f',
            showexponent='all',
            exponentformat='e'
        ),
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
    """Plots a histogram for feature distribuitions

    Args:
        task (dict): A task's dictionary

    Returns:
        plotly: An object plotly which contains a HTML version of the histogram
    """

    distributions = get_distribution(task)

    name_opt = task['task_kwargs']['optimizer']

    number_of_features = list(range(1, len(distributions) + 1))

    fig = go.Figure()

    bar = go.Bar(
        name=str(name_opt),
        x = number_of_features,
        y = distributions,
        marker_color = 'blue',
        opacity=0.8,
    )

    fig.add_trace(bar)

    fig.update_layout(
        title='Gráfico de Distribuição de Frequências',
        legend_title="Otimizador",
        title_x=0.5,
        template='simple_white',
        xaxis=dict(
            title='Característica',
            showgrid=False,
            tickvals=number_of_features
        ),
        yaxis=dict(
            title='Porcentagem de Ocorrência',
            showgrid=False,
            tickformat='.2f',
            showexponent='all',
            exponentformat='e'
        ),
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
    

