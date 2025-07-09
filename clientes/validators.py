import re
from validate_docbr import CPF,CNPJ
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_file_size(value):
    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError("O arquivo não pode exceder 5MB.")

def validate_file_mimetype(value):
    allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'gif']
    ext = value.name.split('.')[-1].lower()
    
    if ext not in allowed_extensions:
        raise ValidationError("Extensão inválida. Use apenas PDF, JPG, PNG ou GIF.")

def nome_invalido(nome):
    return not nome.isalpa()
