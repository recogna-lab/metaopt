from django import forms

from utils.django_forms import add_attr

from .models import Function, Optimizer, Dataset, TransferFunction

class TaskForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields['optimizer'], 'class', 'form-select')
        add_attr(self.fields['agents'], 'class', 'form-control')
        add_attr(self.fields['iterations'], 'class', 'form-control')

    optimizer = forms.ModelChoiceField(
        label='Otimizador',
        queryset=Optimizer.objects.all(),
        to_field_name='acronym',
        empty_label=None
    )

    agents = forms.IntegerField(
        label='Número de Agentes',
        initial=10,
        min_value=10, 
        max_value=50, 
        step_size=5
    )

    iterations = forms.IntegerField(
        label='Número de Iterações',
        initial=100,
        min_value=10, 
        max_value=500, 
        step_size=10
    )

class OptimizationForm(TaskForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.name = 'optimization_form'
        
        add_attr(self.fields['function'], 'class', 'form-select')
        
    function = forms.ModelChoiceField(
        label='Função',
        queryset=Function.objects.all(),
        to_field_name='short_name',
        empty_label=None
    )

    field_order = ['optimizer', 'function', 'agents', 'iterations']
    

class FeatureSelectionForm(TaskForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.name = 'feature_selection_form'

        add_attr(self.fields['dataset'], 'class', 'form-select')
        add_attr(self.fields['transfer_function'], 'class', 'form-select')

    dataset = forms.ModelChoiceField(
        label='Base de Dados',
        queryset=Dataset.objects.all(),
        to_field_name='file_name',
        empty_label=None
    )

    transfer_function = forms.ModelChoiceField(
        label='Função de Transferência',
        queryset=TransferFunction.objects.all(),
        to_field_name='name',
        empty_label=None
    )

    field_order = ['optimizer', 'dataset', 'transfer_function', 'agents', 'iterations']
    
