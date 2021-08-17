from django.db import models
from datetime import date

ufs =   [('AC', 'AC'),('AL', 'AL'),('AM', 'AM'),('AP', 'AP'),('BA', 'BA'),('CE', 'CE'),('DF', 'DF'),('ES', 'ES'),
         ('GO', 'GO'),('MA', 'MA'),('MG', 'MG'),('MS', 'MS'),('MT', 'MT'),('PA', 'PA'),('PB', 'PB'),('PE', 'PE'),
         ('PI', 'PI'),('PR', 'PR'),('RJ', 'RJ'),('RN', 'RN'),('RO', 'RO'),('RR', 'RR'),('RS', 'RS'),('SC', 'SC'),
         ('SE', 'SE'),('SP', 'SP'),('TO', 'TO')]

# Create your models here.
class Empresas(models.Model):
    uf = models.CharField(max_length=2, choices=ufs)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    data_abertura = models.DateField()
    cnpj = models.CharField(max_length=14)
    atividades_secundarias = models.TextField()