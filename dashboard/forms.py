from django import forms

from utils.django.forms import add_attr

from .models import Dataset, Function, Optimizer, TransferFunction


class _TaskForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['optimizer'], 'class', 'form-select')
        add_attr(self.fields['agents'], 'class', 'form-control')
        add_attr(self.fields['iterations'], 'class', 'form-control')
        add_attr(self.fields['executions'], 'class', 'form-control')
    
    optimizer = forms.ModelChoiceField(
        label='Otimizador',
        queryset=Optimizer.objects.all(),
        to_field_name='acronym',
        empty_label='Selecione um otimizador',
        help_text=(
            'Escolha uma das meta-heurísticas de otimização.'
        )
    )

    agents = forms.IntegerField(
        label='Número de Agentes',
        initial=10,
        min_value=5,
        max_value=50,
        step_size=5,
        help_text=(
            'Escolha de 5 a 50 agentes para o otimizador.'
        )
    )

    iterations = forms.IntegerField(
        label='Número de Iterações',
        initial=50,
        min_value=10,
        max_value=500,
        step_size=10,
        help_text=(
            'Escolha de 10 a 500 iterações para a '
            'execução do otimizador.'
        )
    )
    
    executions = forms.IntegerField(
        label='Número de Execuções',
        initial=1,
        min_value=1,
        max_value=30,
        help_text=(
            'Escolha de 1 a 30 execuções para a tarefa.'
        )
    )

class OptimizationForm(_TaskForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.name = 'optimization_form'
        
        add_attr(self.fields['function'], 'class', 'form-select')
        
        for field in self.fields.values():
            # Add tooltips
            add_attr(field, 'data-bs-toggle', 'tooltip')
            add_attr(field, 'data-bs-title', field.help_text)
    
    function = forms.ModelChoiceField(
        label='Função de Teste',
        queryset=Function.objects.all(),
        to_field_name='latex_expression',
        empty_label='Selecione uma função de benchmark',
        help_text=(
            'Escolha uma das funções de teste para a tarefa de otimização.'
        )
    )

    field_order = ['optimizer', 'function', 'agents', 'iterations']

class FeatureSelectionForm(_TaskForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.name = 'feature_selection_form'

        add_attr(self.fields['dataset'], 'class', 'form-select')
        add_attr(self.fields['transfer_function'], 'class', 'form-select')
        
        for field in self.fields.values():
            # Add tooltips
            add_attr(field, 'data-bs-toggle', 'tooltip')
            add_attr(field, 'data-bs-title', field.help_text)

    dataset = forms.ModelChoiceField(
        label='Base de Dados',
        queryset=Dataset.objects.all(),
        to_field_name='features',
        empty_label='Selecione uma base de dados',
        help_text=(
            'Escolha uma das bases para a tarefa de '
            'seleção de características.'
        )
    )

    transfer_function = forms.ModelChoiceField(
        label='Função de Transferência',
        queryset=TransferFunction.objects.all(),
        to_field_name='latex_expression',
        empty_label='Selecione uma função de transferência',
        help_text=(
            'Escolha uma das funções de transferências para '
            'extrair as características presentes na base.'
        )
    )
    
    field_order = [
        'optimizer',
        'dataset',
        'transfer_function',
        'agents',
        'iterations'
    ]

   