from django import forms
from .models import Cliente,ContaClienteFile

class ClienteForms(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ['register_date']
        labels={
            'type_pf_pj':'Tipo de Cliente',
            'name':'Nome',
            'doc':'CPF/CNPJ',
            'email':'Email',
            'phone1':'Contato 1',
            'phone2':'Contato 2',
            'coord_s':'Coordenada Sul',
            'coord_w':'Coordenada Oeste',
            'street':'Logradouro',
            'street_number':'Número',
            'city':'Cidade',
            'state':'Estado',
            'postal_code':'CEP',
            'bairro':'Bairro',
        }

        widgets = {
            'type_pf_pj':forms.Select(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'doc':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'phone1':forms.TextInput(attrs={'class':'form-control'}),
            'phone2':forms.TextInput(attrs={'class':'form-control'}),
            'coord_s':forms.TextInput(attrs={'class':'form-control'}),
            'coord_w':forms.TextInput(attrs={'class':'form-control'}),
            'street':forms.TextInput(attrs={'class':'form-control'}),
            'street_number':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.TextInput(attrs={'class':'form-control'}),
            'postal_code':forms.TextInput(attrs={'class':'form-control'}),
            'bairro':forms.TextInput(attrs={'class':'form-control'}),
        }

class DocUploadForm(forms.ModelForm):
    class Meta:
        model = ContaClienteFile
        fields = ['archives',]
        labels = {
            'archives':'Conta',
        }
        widgets={
            'archives':forms.FileInput(attrs={'class':'form-control'}),
        }
