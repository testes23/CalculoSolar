from django.urls import path
from clientes.views import clientes,cliente
from .views import cadastro_cliente,edit_cliente,upload_doc,remover_conta

urlpatterns = [
    path('clientes',clientes,name='clientes'),
    path('cliente/<int:cliente_id>/', cliente,name='cliente'),
    path('cadastro_cliente',cadastro_cliente,name='cadastro_cliente'),
    path('edit_cliente/<int:cliente_id>/', edit_cliente, name='edit_cliente'),
    path('upload_doc/<int:cliente_id>/',upload_doc,name='upload_doc'),
    path('remover_conta/<int:cliente_id>/',remover_conta,name='remover_conta')
] 