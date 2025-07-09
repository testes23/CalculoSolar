from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Cliente,ContaClienteFile
from calculosolar.models import QntPaineis,CalculoSolar,CalculoPotenciaGeracao,CalculoIrradianciaSolar,AdicaoPotenciaKWHMes,CalcPotenciaAdicional,GeracaoPrevista
from .forms import ClienteForms,DocUploadForm



def clientes(request):
    clientes = Cliente.objects.order_by('name')
    pger = {
        calculo.cliente_id: calculo for calculo in CalculoPotenciaGeracao.objects.select_related('cliente')
    }
    return render(request,'clientes/clientes.html',{'cards':clientes,'pger':pger})

def cliente(request,cliente_id):
    nome = get_object_or_404(Cliente,pk=cliente_id)
    try:
        try:
            conta = ContaClienteFile.objects.filter(client=nome)
        except:
            conta = None
        try:
            consumo = CalculoSolar.objects.filter(cliente=nome).get()
        except CalculoSolar.DoesNotExist:
            consumo = None
        try:
            irrad = CalculoIrradianciaSolar.objects.filter(bairro = nome.bairro).get()
        except CalculoIrradianciaSolar.DoesNotExist:
            irrad = None
        try:
            gerprev = GeracaoPrevista.objects.filter(cliente=nome).get()
        except GeracaoPrevista.DoesNotExist:
            gerprev = None
        try:
            pger = CalculoPotenciaGeracao.objects.filter(cliente=nome).get()
        except CalculoPotenciaGeracao.DoesNotExist:
            pger = None
        try:
            paineis = QntPaineis.objects.filter(cliente=nome).get()
        except:
            paineis = None
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            if request.method == 'POST':
                form_up = DocUploadForm(request.POST,request.FILES)
                if form_up.is_valid():
                    conta = form_up.save(commit=False)
                    conta.client = cliente
                    conta.save()
                    messages.success(request,'Conta enviada com Sucesso')
                    return redirect('cliente',cliente_id=cliente_id)
            else:    
                form_up = DocUploadForm()
        except:
            cliente = None

        conskwhm = AdicaoPotenciaKWHMes.objects.filter(cliente=consumo)
        potw = CalcPotenciaAdicional.objects.filter(cliente = consumo)
    except ( CalculoIrradianciaSolar.DoesNotExist, GeracaoPrevista.DoesNotExist):
        return redirect('cliente_novo',cliente_id=cliente_id)

    return render(request,'clientes/cliente.html',{'conta':conta,'nome':nome,'consumo':consumo,'irrad':irrad,'potadic':potw,'consadic':conskwhm,'gerprev':gerprev,'pger':pger,'paineis':paineis,'form_up':form_up,'cliente':cliente})

def cadastro_cliente(request):
    if request.method == 'POST':    
        clienteform = ClienteForms(request.POST)
        if clienteform.is_valid():
            clienteform.save()
            messages.success(request, 'Cliente salvo com sucesso!')
            return redirect('cadastro_cliente')
        else:
            print(clienteform.errors)
            messages.error(request, 'Erro no formulário!')

    else:
        clienteform = ClienteForms()
    return render(request,'clientes/cadastro_cliente.html',{'clienteform':clienteform,})

def edit_cliente(request,cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    form = ClienteForms(instance=cliente)

    if request.method == 'POST':
        form = ClienteForms(request.POST,instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request,'Informações do Cliente Alteradas com Sucesso')
            return redirect('cliente',cliente_id=cliente_id)
    return render(request,'clientes/edit_cliente.html',{'form':form,'cliente_id':cliente_id})

def upload_doc(request,cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)

    if request.method == 'POST':
        form_up = DocUploadForm(request.POST,request.FILES)
        if form_up.is_valid():
            conta = form_up.save(commit=False)
            conta.client = cliente
            conta.save()
            messages.success(request,'Conta enviada com Sucesso')
            return redirect('cliente',cliente_id=cliente_id)
    else:    
        form_up = DocUploadForm()
    return render(request,'clientes/partials/upload_doc.html',{'form_up':form_up,'cliente_id':cliente_id,'cliente':cliente})

def remover_conta(request, cliente_id):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=cliente_id)
        contas_ids = request.POST.getlist('contas_ids')  # IDs dos checkboxes
        
        # Converte strings para inteiros
        contas_ids_int = [int(id_str) for id_str in contas_ids]
        
        # Deleta os arquivos do cliente com os IDs recebidos
        ContaClienteFile.objects.filter(
            id__in=contas_ids_int, 
            client=cliente
        ).delete()
        
        messages.success(request, 'Arquivos deletados!')
        return redirect('cliente', cliente_id=cliente_id)
    
    return redirect('cliente', cliente_id=cliente_id)