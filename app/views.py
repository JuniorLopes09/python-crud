from django.shortcuts import render, redirect
from app.forms import EmpresasForm
from app.models import Empresas
from django.core.paginator import Paginator
from django.db.models import Q
from requests import get
import json
# Create your views here.

def home(request):
    data = {}
    busca = request.GET.get('search')
    if busca:
        dados = Empresas.objects.filter(Q(uf__icontains=busca) | Q(nome__icontains=busca) | Q(email__icontains=busca) |
                                        Q(telefone__icontains=busca) | Q(cnpj__icontains=busca ) |
                                        Q(data_abertura__icontains=busca) | Q(atividades_secundarias__icontains=busca))
    else:
        dados = Empresas.objects.get_queryset().order_by('id')
    paginator = Paginator(dados, 5)
    page = request.GET.get('page')
    data['db'] = paginator.get_page(page)
    return render(request, 'index.html', data)


def form(request):
    data = {}
    data['form'] = EmpresasForm()
    print("-" * 40)
    print(form)
    print("-" * 40)
    return render(request, 'form.html', data)


def form1(request):
    data = {}
    data['form'] = EmpresasForm()
    data['mode'] = 'Criação'
    data['action'] = 'create'
    data['flags'] = ''
    return render(request, 'view.html', data)

def create(request):
     form = EmpresasForm(request.POST or None)
     if form.is_valid():
         form.save()
         return redirect('home')


def view(request, pk):
    data = {}
    data['db'] = Empresas.objects.get(pk=pk)
    data['form'] = EmpresasForm(instance=data['db'])
    data['mode'] = 'Visualização'
    data['flags'] = 'readonly disabled'
    for field in  data['form'].fields:
        data['form'].fields[field].widget.attrs['disabled'] = True
    return render(request, 'view.html', data)

def edit(request, pk):
    data = {}
    data['db'] = Empresas.objects.get(pk=pk)
    data['form'] = EmpresasForm(instance=data['db'])
    data['mode'] = 'Edição'
    data['action'] = 'update'
    data['flags'] = ''
    data['id'] = pk
    return render(request, 'view.html', data)

def update(request, pk):
    data = {}
    data['db'] = Empresas.objects.get(pk=pk)
    form = EmpresasForm(request.POST or None, instance=data['db'])
    if form.is_valid():
        form.save()
        return redirect('home')

def delete(request, pk):
    Empresas.objects.get(pk=pk).delete()
    return redirect('home')

def auto_form(request):
    return render(request, 'cadastro_automatico.html')

def auto_create(request):

    cnpjs = request.POST.get("cnpjs", "").split()
    for cnpj in cnpjs:
        data = json.loads(get(f'https://www.receitaws.com.br/v1/cnpj/{cnpj.strip()}').text)
        abertura = data['abertura'].split('/')
        f = EmpresasForm()
        empresa = f.save(commit=False)
        empresa.uf = data['uf']
        empresa.nome =  data['nome']
        empresa.email = data['email']
        empresa.telefone = data['telefone']
        empresa.cnpj = data['cnpj']
        empresa.data_abertura = f"{abertura[2]}-{abertura[1]}-{abertura[0]}"
        empresa.atividades_secundarias = '\n'.join([i['text'] for i in data['atividades_secundarias']])
        empresa.save()

    return redirect('home')
