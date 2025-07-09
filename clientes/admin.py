from django.contrib import admin
from clientes.models import Cliente,ContaClienteFile
from calculosolar.models import CalculoSolar

class ContaClienteFileInLine(admin.TabularInline):
    model = ContaClienteFile
    extra = 1
    verbose_name_plural = 'Contas do Cliente'
    verbose_name = 'Conta do Cliente'

class CalculoSolarAdminInLine(admin.TabularInline):
    model = CalculoSolar
    extra = 0

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id','name','type_pf_pj','email','get_doc_formatted','get_phone1_formatted','get_phone2_formatted','get_formatted_postal')
    list_display_links = ('id','name','email',)
    list_per_page = 20
    search_fields = ('name','type_pf_pj',)
    inlines = [ContaClienteFileInLine,CalculoSolarAdminInLine]

    fieldsets = (
        ('Cliente',{
            'fields':(
                'type_pf_pj',
                ('name','doc',),
                ('email','phone1','phone2',),
                ('street','street_number','bairro',),
                ('city','state','postal_code',),
                ('coord_s','coord_w'),
                'register_date',
                
                )
        }),
    )


    @admin.display(description='CEP')
    def get_formatted_postal(self,obj):
        return obj.format_postal(obj.postal_code)

    @admin.display(description="CPF/CNPJ")
    def get_doc_formatted(self, obj):
        return obj.format_doc(obj.doc)

    @admin.display(description="Contato 1")
    def get_phone1_formatted(self, obj):
        return obj.format_phone(obj.phone1)
    
    @admin.display(description="Contato 2")
    def get_phone2_formatted(self, obj):
        return obj.format_phone(obj.phone2)