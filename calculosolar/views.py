from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from .forms import CalculoSolarForm,PotAdicionalForm,ConsAdicForm,IrradForm
from .models import CalculoSolar,CalculoPotenciaGeracao,AdicaoPotenciaKWHMes,CalcPotenciaAdicional,GeracaoPrevista,CalculoIrradianciaSolar
from clientes.views import upload_doc
from clientes.models import Cliente
from django.contrib import messages
from django.forms import modelformset_factory

def cadastro_consumo(request):

    if request.method == 'POST':

        form = CalculoSolarForm(request.POST)    
        formadc =  PotAdicionalForm(request.POST)
        formpot =  ConsAdicForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Consumo salvo com sucesso!')
            return redirect('cadastro_consumo')
        else:
            messages.error(request, 'Erro no formulário de Consumo!')    
            
        if formadc.is_valid():
            formadc.save()
            messages.success(request, 'Consumo Adicional salvo com sucesso!')
            return redirect('cadastro_consumo')
        else:
            messages.error(request, 'Erro no formulário de Consumo Adicional!')    
            
        if formpot.is_valid():
            formpot.save()
            messages.success(request, 'Consumo Adicional salvo com sucesso!')
            return redirect('cadastro_consumo')
        else:
            messages.error(request, 'Erro no formulário de Potência Adicional!')
    else:
        form = CalculoSolarForm()
        formadc = PotAdicionalForm()
        formpot = ConsAdicForm()

    return render(request, 'solar/cadastro_consumo.html',{'form':form,'formadc':formadc,'formpot':formpot,})


def cadastro_irradiacao(request):
    if request.method == 'POST':
        formirrad = IrradForm(request.POST)
        if formirrad.is_valid():
            formirrad.save()
            messages.success(request, 'Irradiação salva com sucesso!')
            return redirect('cadastro_irradiacao')
        else:
            messages.error(request, 'Erro no formulário!')
    else:
        formirrad = IrradForm()
    return render(request,'solar/cadastro_irradiacao.html',{'formirrad':formirrad,})



def edit_consumo(request,cliente_id):
    nome = get_object_or_404(Cliente,pk=cliente_id)
    consumo = get_object_or_404(CalculoSolar,cliente = nome)
    form = CalculoSolarForm(instance=consumo)
    

    if request.method == 'POST':
        form = CalculoSolarForm(request.POST,instance=consumo)
        if form.is_valid():
            form.save()
            messages.success(request,'Informações de Consumo Alteradas com Sucesso')
            return redirect('cliente',cliente_id=cliente_id)
    return render(request,'solar/edit_consumo.html',{'form':form,'cliente_id':cliente_id,'nome':nome})


def edit_consumo_ad_kwh(request,cliente_id):
    nome = get_object_or_404(Cliente,pk=cliente_id)
    consumo = get_object_or_404(CalculoSolar,cliente = nome)
    ConsumoFormSet = modelformset_factory(
        AdicaoPotenciaKWHMes,
        fields=('equipamento', 'consumo', 'horas', 'minutos', 'dias'),
        form=ConsAdicForm, 
        extra=1,
        can_delete=True
    )
    ConsumoFormSet1 = modelformset_factory(
        CalcPotenciaAdicional,
        fields=('equipamento', 'pot', 'horas', 'minutos', 'dias'),
        form=ConsAdicForm, 
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        formset = ConsumoFormSet(request.POST, queryset=AdicaoPotenciaKWHMes.objects.filter(cliente=consumo),prefix='consumo')
        formset1 = ConsumoFormSet1(request.POST, queryset=CalcPotenciaAdicional.objects.filter(cliente=consumo),prefix='consumo')
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.cliente = consumo 
                instance.save()
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, 'Dados atualizados!')
            return redirect('cliente', cliente_id=cliente_id)
        elif formset1.is_valid():
            instances1 = formset1.save(commit=False)
            for instance1 in instances1:
                instance1.cliente = consumo 
                instance1.save()
            for obj1 in formset1.deleted_objects:
                obj1.delete()
            messages.success(request, 'Dados atualizados!')
            return redirect('cliente', cliente_id=cliente_id)
    else:
        formset = ConsumoFormSet(
            queryset=AdicaoPotenciaKWHMes.objects.filter(cliente=consumo),
            prefix='consumo'
        )
        formset1 = ConsumoFormSet1(
            queryset=CalcPotenciaAdicional.objects.filter(cliente=consumo),
            prefix='consumo'
        )

    return render(request, 'solar/edit_cons_adic.html', {
        'formset': formset,
        'formset1': formset1,
        'cliente': consumo,
        'nome':nome,
        'cliente_id':cliente_id,
    })

def edit_irradi(request,cliente_id):
    nome = get_object_or_404(Cliente,pk=cliente_id)
    potger = CalculoPotenciaGeracao.objects.get_or_create(cliente=nome)
    
    if request.method == 'POST':
        form = IrradForm(request.POST)
        if form.is_valid():
            form.instance.bairro = nome.bairro
            form.instance.cidade = nome.city
            form.instance.estado = nome.state
            potger.irrad = form
            form.save()
            messages.success(request, 'Dados salvos com sucesso!')
            return redirect('cliente', cliente_id=cliente_id)
    else:
        form = IrradForm()

    return render(request,'solar/edit_irradi.html',{'formset':form,'cliente_id':cliente_id,'nome':nome})
