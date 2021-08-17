from django.forms import ModelForm
from django import forms
from app.models import Empresas


class EmpresasForm(ModelForm):


    class Meta:
        model = Empresas
        fields = ['uf', 'nome', 'email', 'telefone', 'data_abertura', 'cnpj', 'atividades_secundarias']