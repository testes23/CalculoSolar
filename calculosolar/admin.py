from django.contrib import admin
from calculosolar.models import GeracaoPrevista, CalculoSolar, CalculoIrradianciaSolar, CalculoPotenciaGeracao, QntPaineis,AdicaoPotenciaKWHMes,CalcPotenciaAdicional,CalculoPotenciaGeracao

class CalculoPotAdicional(admin.TabularInline):
    model = AdicaoPotenciaKWHMes
    extra = 1

class CalculokWhAdicional(admin.TabularInline):
    model = CalcPotenciaAdicional
    extra = 1

class CalculoPotenciaGeracaoInLine(admin.TabularInline):
    model = CalculoPotenciaGeracao
    extra = 0

@admin.register(CalculoIrradianciaSolar)
class CalculoIrradianciaAdmin(admin.ModelAdmin):
     
    list_display = ('estado', 'cidade', 'bairro', 'media_irradiancia')
    readonly_fields = ('media_irradiancia',)
    fieldsets = (
        ('Bairro', {
            'fields': (
                ('estado', 'cidade', 'bairro',),
                       )
        }),
        ('Irradiância Mensal', {
            'fields': (
                ('irradi_jan', 'irradi_fev', 'irradi_mar'),
                ('irradi_abr', 'irradi_mai', 'irradi_jun'),
                ('irradi_jul', 'irradi_ago', 'irradi_set'),
                ('irradi_out', 'irradi_nov', 'irradi_dez')
            )
        }),
        ('Resultados', {
            'fields': ('media_irradiancia',)
        }),
    )
    
    inlines = [CalculoPotenciaGeracaoInLine]

    def media_irradiancia(self, obj):
        return f"{obj.media_irradiancia:.2f} kWh/m².dia"
    media_irradiancia.short_description = 'Média Mensal'

@admin.register(CalculoSolar)
class CalculoSolarAdmin(admin.ModelAdmin):
     
    list_display = ('cliente', 'media_consumo','soma_total','cons_total')
    readonly_fields = ('media_consumo', 'soma_potencia_adicional_display','soma_pot_w_display','soma_total','cons_total')
    fieldsets = (
        ('Cliente', {
            'fields': ('cliente',)
        }),
        ('Consumo Mensal (kWh)', {
            'fields': (
                ('cons_jan', 'cons_fev', 'cons_mar'),
                ('cons_abr', 'cons_mai', 'cons_jun'),
                ('cons_jul', 'cons_ago', 'cons_set'),
                ('cons_out', 'cons_nov', 'cons_dez')
            )
        }),
    
        ('Resultados', {
            'fields': ('media_consumo', 'soma_potencia_adicional_display','soma_pot_w_display',)
        }),
        ('Resultados Totais',{
            'fields':('soma_total','cons_total',),
        })
    )
    inlines = [CalculoPotAdicional, CalculokWhAdicional]


    def media_consumo(self, obj):
        return f"{obj.media_consumo:.2f} kWh/mês"
    media_consumo.short_description = 'Média Mensal'

    def soma_potencia_adicional_display(self, obj):
        return f"{obj.soma_potencia_adicional:.2f} kWh/mês"
    soma_potencia_adicional_display.short_description = "Consumo Adicional por kWh/mês"

    def soma_pot_w_display(self,obj):
        return f'{obj.soma_consumo_kwh_adicional:.2f} kWh/mês'
    soma_pot_w_display.short_description = 'Consumo Adicional pela Potência'

    def soma_total(self,obj):
        return f'{obj.consumo_adicional_total:.2f} kWh/mês'
    soma_total.short_description = 'Consumo Adicional Total'

    def cons_total(self,obj):
        return f'{obj.cons_total:.2f} kWh/mês'
    cons_total.short_description = 'Consumo Total Calculado'

@admin.register(CalculoPotenciaGeracao)
class CalculoPotGeracaoAdmin(admin.ModelAdmin):
     
    list_display = ('cliente', 'calculogeracao')
    readonly_fields = ('calculogeracao',)
    fieldsets = (
        ('Cliente', {
            'fields': ('cliente',)
        }),
        ('Potência de Geração Necessária (kWp)', {
            'fields': (('consumo', 'irradi', 'rendimento'),)
        }),
        ('Resultados', {
            'fields': ('calculogeracao',)
        }),
    )

    def calculogeracao(self, obj):
        return f"{obj.calculogeracao:.2f} kWp"
    calculogeracao.short_description = 'Potência de Geração Necessária'

@admin.register(QntPaineis)
class QntPaineisAdmin(admin.ModelAdmin):
     
    list_display = ('cliente', 'calculopainel', 'potenciasistema')
    readonly_fields = ('calculopainel', 'potenciasistema')
    fieldsets = (
        ('Cliente', {
            'fields': ('cliente',)
        }),
        ('Quantidade de Painéis Necessária', {
            'fields': (('potgeracao', 'potpainel'),)
        }),
        ('Resultados', {
            'fields': ('calculopainel', 'potenciasistema')
        }),
    )

    def calculopainel(self, obj):
        return f"{obj.calculopainel} painéis"
    calculopainel.short_description = 'Quantidade Mínima de Painéis'

    def potenciasistema(self, obj):
        return f"{obj.potenciasistema} kWp"
    potenciasistema.short_description = 'Potência Calculada do Sistema'

@admin.register(GeracaoPrevista)
class GeracaoPrevistaAdmin(admin.ModelAdmin):
     
    list_display = ('cliente', 'get_irradiacao', 'get_rendimento', 'geracao_formatada')
    readonly_fields = ('geracao_formatada',)
    fieldsets = (
        ('Cliente', {
            'fields': ('cliente', 'rend','irrad')
        }),
        ('Número de Painéis', {
            'fields': (('potsist', 'paineisdesejados',),)
        }),
        ('Resultados', {
            'fields': ('geracao_formatada',)
        }),
    )

    def geracao_formatada(self, obj):
        return "\n".join([f"{mes}: {valor:.2f}" for mes, valor in obj.gercaoesperada])
    geracao_formatada.short_description = "Geração Esperada (kWh)"

    @admin.display(description='Irradiação Média')
    def get_irradiacao(self, obj):
        return f"{obj.irrad.media_irradiancia:.2f} kWh/m²"
    
    @admin.display(description='Rendimento (%)')
    def get_rendimento(self, obj):
        return f"{obj.rend.rendimento}%"
    
