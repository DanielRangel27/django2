from django.shortcuts import render
from .forms import ContatoForm, ProdutoModelForm
from django.contrib import messages
from django.shortcuts import redirect
from .models import Produto

def index(reguest):
    context = {
        'produtos': Produto.objects.all()
    }
    return render(reguest, 'index.html', context)

def contato(reguest):
    form = ContatoForm(reguest.POST or None)

    if str(reguest.method) == 'POST':
        if form.is_valid():
            form.send_mail()
            #nome = form.cleaned_data['nome']
            #email = form.cleaned_data['email']
            #assunto = form.cleaned_data['assunto']
            #menssagem = form.cleaned_data['menssagem']

            #print('menssagem enviada')
            #print(f'Nome: {nome}')
            #print(f'E-mail: {email}')
            ##print(f'Assunto: {assunto}')
            #print(f'Menssagem: {menssagem}')

            messages.success(reguest, 'E-mail enviado com sucesso!')
            form = ContatoForm()
        else:
            messages.error(reguest, ' Erro ao enviar email')
    context = {
        'form': form
    }
    return render(reguest, 'contato.html', context)

def produto(reguest):
    if str(reguest.user) != 'AnonymousUser':
        if str(reguest.method) == 'POST':
            form = ProdutoModelForm(reguest.POST, reguest.FILES)
            if form.is_valid():
                form.save()

                messages.success(reguest, 'produto salvo com sucesso')
                form = ProdutoModelForm()
            else:
                messages.error(reguest, 'Erro ao salvar produto')
        else:
            form = ProdutoModelForm()
        context = {
            'form': form
        }

        return  render(reguest, 'produto.html', context)
    else:
        return redirect('index')