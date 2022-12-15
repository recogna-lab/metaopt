from django import forms

from .models import Function, Optimizer


class OptimizationForm(forms.Form):
    
    optimizer = forms.ModelChoiceField(
        label='Otimizador',
        queryset=Optimizer.objects.all(),
        to_field_name='acronym',
        empty_label=None
    )
    
    function = forms.ModelChoiceField(
        label='Função',
        queryset=Function.objects.all(),
        to_field_name='short_name',
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