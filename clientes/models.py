from django.db import models
from datetime import datetime
from django.utils.html import format_html
from django.core.validators import FileExtensionValidator
from clientes.validators import validate_file_mimetype,validate_file_size

class Cliente(models.Model):
    TYPE = (
        ('PJ','Pessoa Jurídica'),
        ('PF','Pessoa Fisica')
        )
    
    name = models.CharField(max_length=100,null=False,blank=False,verbose_name='Cliente')
    doc = models.CharField(max_length=14,unique=True,verbose_name='CPF/CNPJ')
    type_pf_pj = models.CharField(max_length=2, choices=TYPE, null=False,blank=False, default='PF',verbose_name='Tipo de Cliente')
    email = models.EmailField(max_length=200,blank=False,null=False,verbose_name='Email')
    phone1 = models.CharField(max_length=11,null=False,blank=False,verbose_name='Contato 1')
    phone2 = models.CharField(max_length=11,null=True,blank=True,verbose_name='Contato 2')
    coord_s = models.CharField(default='', max_length=11, verbose_name='Coordenada Sul', null=True, blank=True)
    coord_w = models.CharField(default='', max_length=11, verbose_name='Coordenada Oeste', null=True, blank=True)
    street = models.CharField(max_length=100,blank=False,null=False,verbose_name='Logradouro',default='-')
    street_number = models.CharField(max_length=100,blank=False,null=False,verbose_name='Numero',default='-')
    city = models.CharField(max_length=100,blank=True,null=True,verbose_name='Cidade')
    state = models.CharField(max_length=100,blank=True,null=True,verbose_name='Estado')
    postal_code = models.CharField(max_length=8,blank=False,null=False,verbose_name='CEP',default='-')
    bairro = models.CharField(max_length=100,blank=True,null=True,verbose_name='Bairro')
    register_date = models.DateField(default=datetime.now,blank=False,verbose_name='Data de Cadastro')

    class Meta:
        verbose_name_plural='Clientes'

    def __str__(self):
        return self.name
    
    def format_phone(self, number):
        if not number:
            return ""
        digits = ''.join(filter(str.isdigit, number))
        if len(digits) == 11:
            return format_html('({}) {}-{}', digits[:2], digits[2:7], digits[7:])
        return number
    
    def format_doc(self,number):
        if self.type_pf_pj == 'PF':
            if not number:
                return ""
            digits = ''.join(filter(str.isdigit,number))
            if len(digits) == 11:
                return format_html('{}.{}.{}-{}',digits[:3],digits[3:6],digits[6:9],digits[9:])
            return number
        else:
            if not number:
                return ""
            digits = ''.join(filter(str.isdigit,number))
            if len(digits) == 14:
                return format_html('{}.{}.{}/{}-{}',digits[:2],digits[2:5],digits[5:8],digits[8:12],digits[12:])
            return number

    def format_postal(self,number):
        if not number:
            return ''
        digits = ''.join(filter(str.isdigit,number))
        if len(digits) == 8:
            return format_html('{}-{}',digits[:5],digits[5:])
        return number
    
    def format_coord(self):
        return f'{self.coord_s}S {self.coord_w}O'

    def format_endereco(self):
        return f'{self.street}, {self.street_number} - {self.bairro}, {self.city} - {self.state}, {self.format_postal(self.postal_code)}'
        
    
def get_upload_path(instance,filename):
    data_atual = datetime.now().strftime("%Y/%m/%d")
    return f"uploads/{instance.client.type_pf_pj}/{data_atual}/{filename}"

class ContaClienteFile(models.Model):
    client = models.ForeignKey(Cliente, on_delete=models.CASCADE,related_name='files')
    archives = models.FileField(
        upload_to=get_upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'gif']),
            validate_file_mimetype,
            validate_file_size
        ],
        verbose_name="Arquivo (PDF ou imagem)"
    )
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conta - {self.client.name} [Upload: {self.data_upload.date()}]"
    