from django import forms
from calculosolar.models import CalculoIrradianciaSolar,CalculoSolar,AdicaoPotenciaKWHMes,CalcPotenciaAdicional,CalculoPotenciaGeracao

class CalculoSolarForm(forms.ModelForm):
    class Meta:    
        model = CalculoSolar
        fields = '__all__'
        labels = {
            'cliente':'Cliente',
            'cons_jan':'Janeiro',
            'cons_fev':'Fevereiro',
            'cons_mar':'Março',
            'cons_abr':'Abril',
            'cons_mai':'Maio',
            'cons_jun':'Junho',
            'cons_jul':'Julho',
            'cons_ago':'Agosto',
            'cons_set':'Setembro',
            'cons_out':'Outubro',
            'cons_nov':'Novembro',
            'cons_dez':'Dezembro',
        }
        widgets = {
            'cliente': forms.Select(attrs={'class':'form-control'}),
            'cons_jan':forms.NumberInput(attrs={'class':'form-control'}),
            'cons_fev':forms.NumberInput(attrs={'class':'form-control'}),
            'cons_mar':forms.NumberInput(attrs={'class':'form-control'}),
            'cons_abr':forms.NumberInput(attrs={'class':'form-control'}),
            'cons_mai':forms.NumberInput(attrs={'class':'form-control'}),
            'cons_jun':forms.NumberInput(attrs={'class':'form-control'}),
            'cons_jul':forms.NumberInput(attrs={'class':'form-control'}),
            'cons_ago':forms.NumberInput(attrs={'class':'form-control'}),
            'cons_set':forms.NumberInput(attrs={'class':'form-control'}),
            'cons_out':forms.NumberInput(attrs={'class':'form-control'}),
            'cons_nov':forms.NumberInput(attrs={'class':'form-control'}),
            'cons_dez':forms.NumberInput(attrs={'class':'form-control'}),
            }
    
class PotAdicionalForm(forms.ModelForm):
    class Meta:
        model = CalcPotenciaAdicional
        fields = '__all__'
        labels = {
            'cliente':'Cliente',
            'equipamento':'Eletrodoméstico',
            'pot':'Potencia (W)',
            'horas':'Horas de Uso/Dia',
            'minutos':'Minutos de Uso/Dia',
            'dias':'Nº Dias de uso no mês',

        }
        widgets = {
            'cliente': forms.Select(attrs={'class':'form-control'}),
            'equipamento':forms.TextInput(attrs={'class':'form-control'}),
            'pot':forms.NumberInput(attrs={'class':'form-control'}),
            'horas':forms.NumberInput(attrs={'class':'form-control'}),
            'minutos':forms.NumberInput(attrs={'class':'form-control'}),
            'dias':forms.NumberInput(attrs={'class':'form-control'}),
        }
    
class ConsAdicForm(forms.ModelForm):
    class Meta:
        model = AdicaoPotenciaKWHMes
        fields = '__all__'
        labels = {
            'cliente':'Cliente',
            'equipamento':'Eletrodoméstico',
            'consumo':'Consumo (kWh)',
            'horas':'Horas de Uso/Dia',
            'minutos':'Minutos de Uso/Dia',
            'dias':'Nº Dias de uso no mês',

        }
        widgets = {
            'cliente': forms.Select(attrs={'class':'form-control'}),
            'equipamento':forms.TextInput(attrs={'class':'form-control'}),
            'consumo':forms.NumberInput(attrs={'class':'form-control'}),
            'horas':forms.NumberInput(attrs={'class':'form-control'}),
            'minutos':forms.NumberInput(attrs={'class':'form-control'}),
            'dias':forms.NumberInput(attrs={'class':'form-control'}),
        }

class IrradForm(forms.ModelForm):
    class Meta:
        model = CalculoIrradianciaSolar
        fields = '__all__'
        labels = {
            'estado':'Estado',
            'cidade':'Cidade',
            'bairro':'Bairro',
            'irradi_jan':'Janeiro',
            'irradi_fev':'Fevereiro',
            'irradi_mar':'Março',
            'irradi_abr':'Abril',
            'irradi_mai':'Maio',
            'irradi_jun':'Junho',
            'irradi_jul':'Julho',
            'irradi_ago':'Agosto',
            'irradi_set':'Setembro',
            'irradi_out':'Outubro',
            'irradi_nov':'Novembro',
            'irradi_dez':'Dezembro',
        }

        widgets = {
            'estado':forms.TextInput(attrs={'class':'form-control'}),
            'cidade':forms.TextInput(attrs={'class':'form-control'}),
            'bairro':forms.TextInput(attrs={'class':'form-control'}),
            'irradi_jan':forms.NumberInput(attrs={'class':'form-control'}),
            'irradi_fev':forms.NumberInput(attrs={'class':'form-control'}),
            'irradi_mar':forms.NumberInput(attrs={'class':'form-control'}),
            'irradi_abr':forms.NumberInput(attrs={'class':'form-control'}),
            'irradi_mai':forms.NumberInput(attrs={'class':'form-control'}),
            'irradi_jun':forms.NumberInput(attrs={'class':'form-control'}),
            'irradi_jul':forms.NumberInput(attrs={'class':'form-control'}),
            'irradi_ago':forms.NumberInput(attrs={'class':'form-control'}),
            'irradi_set':forms.NumberInput(attrs={'class':'form-control'}),
            'irradi_out':forms.NumberInput(attrs={'class':'form-control'}),
            'irradi_nov':forms.NumberInput(attrs={'class':'form-control'}),
            'irradi_dez':forms.NumberInput(attrs={'class':'form-control'}),
        }

