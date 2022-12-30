import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot


def plot_convergence(task):
    # Name of the optimizer used in the execution
    optimizer = task['task_kwargs']['optimizer']['acronym']
    
    # Get list with fitness values
    fitness_values = task['result']['fitness_values']

    # Get stdev of fitness values
    stdev_fitness_values = task['result']['stdev_fitness_values']
    
    # Create a list with the iterations
    iterations = list(range(1, len(fitness_values) + 1))

    # Create figure
    fig = go.Figure()
    
    # Set up fitness values curve
    scatter = go.Scatter(
        name=optimizer,
        x=iterations,
        y=fitness_values,
        mode='lines',
        opacity=0.8,
        marker_color='blue',
        hovertemplate='(%{x}; %{y})'
    )
    
    # Add curve to the fig
    fig.add_traces(scatter)
    
    # If there's stdev for the fitness values
    if stdev_fitness_values:
        # Convert values and stdev to numpy arrays
        fitness_values = np.array(fitness_values)
        stdev_fitness_values = np.array(stdev_fitness_values)
        
        # Compute lower and upper fitness
        lower_fitness = (fitness_values - stdev_fitness_values).tolist()
        upper_fitness = (fitness_values + stdev_fitness_values).tolist()
        
        # Set the area for the stdev
        area_x = iterations + iterations[::-1]
        area_y = upper_fitness + lower_fitness[::-1]
        
        # Draw the stdev area above and down the curve
        stdev_scatter = go.Scatter(
            name='Desvio Padrão',
            x=area_x,
            y=area_y,
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=True
        )
        
        # Add stdev scatter to the fig
        fig.add_traces(stdev_scatter)
    
    # Update fig layout    
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
    
    # Return plot div
    return plot_div

def plot_bar(task):
    # Name of the optimizer used in the execution
    optimizer = task['task_kwargs']['optimizer']['acronym']
    
    # Distribution values for features
    distributions = get_distribution(task)
    
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
    
    # Initialize freq list
    freq = [0] * feature_count

    # Compute feature freq
    for vector in feature_vectors:
        for i, feature in enumerate(vector):
            if feature:
                freq[i] += 1
    
    # Get the number of executions
    executions = task['task_kwargs']['executions']
    
    # Compute distributions based on freq
    return [(x/executions * 100) for x in freq]

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

