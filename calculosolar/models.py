from django.db import models
from django.forms import ValidationError
import math
from clientes.models import Cliente

class CalculoSolar(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cons_jan = models.IntegerField(default=0,verbose_name='Consumo (kWh) Janeiro',null=False,blank=False)
    cons_fev = models.IntegerField(default=0,verbose_name='Consumo (kWh) Fevereiro',null=False,blank=False)
    cons_mar = models.IntegerField(default=0,verbose_name='Consumo (kWh) Março',null=False,blank=False)
    cons_abr = models.IntegerField(default=0,verbose_name='Consumo (kWh) Abril',null=False,blank=False)
    cons_mai = models.IntegerField(default=0,verbose_name='Consumo (kWh) Maio',null=False,blank=False)
    cons_jun = models.IntegerField(default=0,verbose_name='Consumo (kWh) Junho',null=False,blank=False)
    cons_jul = models.IntegerField(default=0,verbose_name='Consumo (kWh) Julho',null=False,blank=False)
    cons_ago = models.IntegerField(default=0,verbose_name='Consumo (kWh) Agosto',null=False,blank=False)
    cons_set = models.IntegerField(default=0,verbose_name='Consumo (kWh) Setembro',null=False,blank=False)
    cons_out = models.IntegerField(default=0,verbose_name='Consumo (kWh) Outubro',null=False,blank=False)
    cons_nov = models.IntegerField(default=0,verbose_name='Consumo (kWh) Novembro',null=False,blank=False)
    cons_dez = models.IntegerField(default=0,verbose_name='Consumo (kWh) Dezembro',null=False,blank=False)

    @property
    def soma_potencia_adicional(self):
        return sum(item.calculopotadicional for item in self.adicaopotenciakwhmes_set.all())

    @property
    def soma_consumo_kwh_adicional(self):
        return sum(item.calculokwh for item in self.calcpotenciaadicional_set.all())

    @property
    def consumo_adicional_total(self):
        soma1 = self.soma_potencia_adicional
        soma2 = self.soma_consumo_kwh_adicional

        return (soma1 + soma2)
    
    @property
    def cons_total(self):
        soma3 = self.consumo_adicional_total
        soma4 = self.media_consumo
        return (soma4 + soma3)

    @property
    def media_consumo(self):
        meses = [
            self.cons_jan,self.cons_fev,self.cons_mar,
            self.cons_abr,self.cons_mai,self.cons_jun,
            self.cons_jul,self.cons_ago,self.cons_set,
            self.cons_out,self.cons_nov,self.cons_dez
        ]
        return sum(meses)/12 if all(meses) else 0

    def clean(self):
        if any(valor < 0 for valor in [
            self.cons_jan, self.cons_fev, self.cons_mar,
            self.cons_abr, self.cons_mai, self.cons_jun,
            self.cons_jul, self.cons_ago, self.cons_set,
            self.cons_out, self.cons_nov, self.cons_dez
        ]):
            raise ValidationError("Os valores de consumo não podem ser negativos")
        
    def __str__(self):
        return f'Media de consumo para {self.cliente.name} - Média: {self.media_consumo:.2f} kWh/mês'

    class Meta:
        verbose_name = 'Consumo Médio'
        verbose_name_plural = 'Consumos Médios'

class CalculoIrradianciaSolar(models.Model):
    estado = models.CharField(default='',max_length=200,null=False,blank=False)
    cidade = models.CharField(default='',max_length=200,null=False,blank=False)
    bairro = models.CharField(default='',max_length=200,null=False,blank=False)
    irradi_jan = models.FloatField(default=0,verbose_name='Irradiancia Janeiro',null=False,blank=False)
    irradi_fev = models.FloatField(default=0,verbose_name='Irradiancia Fevereiro',null=False,blank=False)
    irradi_mar = models.FloatField(default=0,verbose_name='Irradiancia Março',null=False,blank=False)
    irradi_abr = models.FloatField(default=0,verbose_name='Irradiancia Abril',null=False,blank=False)
    irradi_mai = models.FloatField(default=0,verbose_name='Irradiancia Maio',null=False,blank=False)
    irradi_jun = models.FloatField(default=0,verbose_name='Irradiancia Junho',null=False,blank=False)
    irradi_jul = models.FloatField(default=0,verbose_name='Irradiancia Julho',null=False,blank=False)
    irradi_ago = models.FloatField(default=0,verbose_name='Irradiancia Agosto',null=False,blank=False)
    irradi_set = models.FloatField(default=0,verbose_name='Irradiancia Setembro',null=False,blank=False)
    irradi_out = models.FloatField(default=0,verbose_name='Irradiancia Outubro',null=False,blank=False)
    irradi_nov = models.FloatField(default=0,verbose_name='Irradiancia Novembro',null=False,blank=False)
    irradi_dez = models.FloatField(default=0,verbose_name='Irradiancia Dezembro',null=False,blank=False)

    @property
    def media_irradiancia(self):
        meses = [
            self.irradi_jan,self.irradi_fev,self.irradi_mar,
            self.irradi_abr,self.irradi_mai,self.irradi_jun,
            self.irradi_jul,self.irradi_ago,self.irradi_set,
            self.irradi_out,self.irradi_nov,self.irradi_dez
        ]
        return sum(meses)/12 if all(meses) else 0

    def clean(self):
        if any(valor < 0 for valor in [
            self.irradi_jan, self.irradi_fev, self.irradi_mar,
            self.irradi_abr, self.irradi_mai, self.irradi_jun,
            self.irradi_jul, self.irradi_ago, self.irradi_set,
            self.irradi_out, self.irradi_nov, self.irradi_dez
        ]):
            raise ValidationError("Os valores de Irradiancia não podem ser negativos")
        
    def __str__(self):
        return f'{self.media_irradiancia:.2f} kWh/m^(2).dia'

    class Meta:
        verbose_name = 'Irradiancia Média'
        verbose_name_plural = 'Irradiancias Médias'

class AdicaoPotenciaKWHMes(models.Model): #adiciona a potencia ao consumo médio
    cliente = models.ForeignKey(CalculoSolar,on_delete=models.CASCADE)
    equipamento = models.CharField(verbose_name='Equipamento',default='',null=True,blank=True,max_length=100)
    consumo = models.FloatField(verbose_name='Consumo (kWh/mes)',null=True,blank=True)
    horas = models.FloatField(verbose_name='Horas de Uso por dia',null=True,blank=True)
    minutos = models.FloatField(verbose_name='Minutos de Uso por dia',null=True,blank=True)
    dias = models.FloatField(verbose_name='Dias uso mês',null=True,blank=True)

    def clean(self):
        super().clean()
        if self.equipamento.strip() != '':
            campos_fixos = {
                'consumo': 'Consumo é obrigatório quando Equipamento é preenchido.',
                'dias': 'Dias são obrigatórios quando Equipamento é preenchido.'
            }
            
        for campo, mensagem in campos_fixos.items():
            if getattr(self, campo) is None:
                raise ValidationError({campo: mensagem})
        
        if self.horas is None and self.minutos is None:
            raise ValidationError({
                'horas': 'Preencha horas ou minutos.',
                'minutos': 'Preencha horas ou minutos.'
            })
        elif self.horas is None:
            if self.minutos is None:
                raise ValidationError({'minutos': 'Minutos é obrigatório se horas não for preenchido.'})
        elif self.minutos is None:
            pass  

    @property
    def calculopotadicional(self):
        if None in (self.consumo, self.dias):
            return 0
        elif self.horas == None:
            potadicional = self.consumo*(self.dias/30)*(self.minutos/60)
            return potadicional
        elif self.minutos == None:
            potadicional = self.consumo*(self.dias/30)*(self.horas)
            return potadicional
        else:
            potadicional = self.consumo*(self.dias/30)*(self.horas+(self.minutos/60))
            return potadicional
    
    def __str__(self):
        return f'Consumo de {self.equipamento}: {self.calculopotadicional:.2f} kWh/mês'

    class Meta:
        verbose_name = 'Adição de consumo por kWh/mes do equipamento'
        verbose_name_plural = 'Adições de consumo por kWh/mes dos equipamentos'

class CalcPotenciaAdicional(models.Model): # Faz o calculo de Consumo do Aparelho a Partir da Potencia INSTÂNTANEA
    cliente = models.ForeignKey(CalculoSolar, on_delete=models.CASCADE)
    equipamento = models.CharField(max_length=100, null=True,blank=True, default='',verbose_name='Equipamento')
    pot =  models.FloatField(max_length=100, null=True,blank=True,verbose_name='Potência do equipamento (Watts)')
    horas = models.FloatField(verbose_name='Horas de Uso por dia',null=True,blank=True)
    minutos = models.FloatField(verbose_name='Minutos de Uso por dia',null=True,blank=True)
    dias = models.FloatField(verbose_name='Dias uso mês',null=True,blank=True)

    def clean(self):
        super().clean()
        if self.equipamento.strip() != '':
            campos_fixos = {
                'pot': 'Potência é obrigatória quando Equipamento é preenchido.',
                'dias': 'Dias são obrigatórios quando Equipamento é preenchido.'
            }
            
        for campo, mensagem in campos_fixos.items():
            if getattr(self, campo) is None:
                raise ValidationError({campo: mensagem})
        
        if self.horas is None and self.minutos is None:
            raise ValidationError({
                'horas': 'Preencha horas ou minutos.',
                'minutos': 'Preencha horas ou minutos.'
            })
        elif self.horas is None:
            if self.minutos is None:
                raise ValidationError({'minutos': 'Minutos é obrigatório se horas não for preenchido.'})
        elif self.minutos is None:
            pass  

    @property
    def calculokwh(self):
        if None in (self.pot,self.dias):
            return 0
        elif self.horas == None:
            self.horas = 0
            potadicional = (self.pot/1000)*self.dias*(self.horas+(self.minutos/60))
            return potadicional
        elif self.minutos == None:
            self.minutos = 0
            potadicional = (self.pot/1000)*self.dias*(self.horas+(self.minutos/60))
            return potadicional
        else:
            potadicional = (self.pot/1000)*self.dias*(self.horas+(self.minutos/60))
            return potadicional
    
    def __str__(self):
        return f'Consumo de {self.equipamento}: {self.calculokwh:.2f} kWh/mês'

    class Meta:
        verbose_name = 'Adição de consumo pela Potência do equipamento'
        verbose_name_plural = 'Adições de consumo pela Potência dos equipamentos'

class CalculoPotenciaGeracao(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    consumo = models.ForeignKey(CalculoSolar,on_delete=models.CASCADE, verbose_name='Consumo Base')
    irradi = models.ForeignKey(CalculoIrradianciaSolar,on_delete=models.CASCADE,verbose_name='Irradiação Solar')
    rendimento = models.IntegerField(default=100,null=False,blank=False,verbose_name='Eficiência do Sistema %')
    
    @property
    def calculogeracao(self):
        pger = ((self.consumo.media_consumo) + (self.consumo.soma_potencia_adicional))*1/(30*(self.irradi.media_irradiancia)*(self.rendimento/100)) 
        return pger
    
    def __str__(self):
        return f'Potencia do Sistema: {round(self.calculogeracao,3)} kWp'
    
    class Meta:
        verbose_name = 'Potência de Geração Necessária '
        verbose_name_plural = 'Potências de Geração Necessárias'

class QntPaineis(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    potgeracao = models.ForeignKey(CalculoPotenciaGeracao, on_delete=models.CASCADE,verbose_name='Potência de Geração')
    potpainel = models.IntegerField(default=0,null=False,blank=False,verbose_name='Potencia do Painel (W)')

    @property
    def calculopainel(self):
        n_painel = math.ceil(self.potgeracao.calculogeracao/(self.potpainel/1000))
        return n_painel
    
    @property
    def potenciasistema(self):
        potsis = self.calculopainel*(self.potpainel/1000)
        return potsis

    def __str__(self):
        return f'{self.calculopainel}'

    class Meta:
        verbose_name = 'Quantdade de Painel Necessário '
        verbose_name_plural = 'Quantdade de Painéis Necessários'
        ordering = ['-id']

class GeracaoPrevista(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    potsist = models.ForeignKey(QntPaineis, on_delete=models.CASCADE,verbose_name='Numero ideal de Painéis no Sistema')
    paineisdesejados = models.IntegerField(null=True,blank=True,verbose_name='Quantidade de Painéis Desejada')
    irrad = models.ForeignKey(CalculoIrradianciaSolar, on_delete=models.CASCADE,verbose_name='Irradiância Local')
    rend = models.ForeignKey(CalculoPotenciaGeracao, on_delete=models.CASCADE, verbose_name='Eficiência')
    
    
    @property
    def gercaoesperada(self):
        
        irradiancias = [
            float(self.irrad.irradi_jan),float(self.irrad.irradi_fev),float(self.irrad.irradi_mar),
            float(self.irrad.irradi_abr),float(self.irrad.irradi_mai),float(self.irrad.irradi_jun),
            float(self.irrad.irradi_jul),float(self.irrad.irradi_ago),float(self.irrad.irradi_set),
            float(self.irrad.irradi_out),float(self.irrad.irradi_nov),float(self.irrad.irradi_dez),
        ]

        dias_no_mes = [
            31, 28, 31,
            30, 31, 30, 
            31, 31, 30, 
            31, 30, 31
            ]

        meses = [
            'Janeiro','Fevereiro','Março',
            'Abril','Maio','Junho',
            'Julho','Agosto','Setembro',
            'Outubro','Novembro','Dezembro'
        ]

        geracao_mensal = []

        for mes,irradiancia,dia in zip(meses, irradiancias, dias_no_mes):
            if self.paineisdesejados:    
                pot_sistema = float(self.paineisdesejados)
            else:
                pot_sistema = float(self.potsist.potenciasistema)
            rendimento = float(self.rend.rendimento)            
            geracao = (irradiancia*dia*pot_sistema*rendimento)/100
            geracao_mensal.append((mes,geracao))

        return geracao_mensal
    
    def __str__(self):
        return f"Geracao Prevista para {self.cliente}"

    @property
    def rendimento_do_sistema(self):
        return self.rend.rendimento  # Acessa o rendimento diretamente

    @property
    def irradiacao_media(self):
        return self.rend.irradi.media_irradiancia
      