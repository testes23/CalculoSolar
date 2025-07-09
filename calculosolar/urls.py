from django.urls import path
from .views import cadastro_consumo,cadastro_irradiacao,edit_consumo,edit_consumo_ad_kwh,edit_irradi

urlpatterns = [
    path('cadastro_consumo',cadastro_consumo,name='cadastro_consumo'),
    path('cadastro_irradiacao',cadastro_irradiacao,name='cadastro_irradiacao'),
    path('edit_consumo/<int:cliente_id>/',edit_consumo,name='edit_consumo'),
    path('edit_cons_adic/<int:cliente_id>/',edit_consumo_ad_kwh,name='edit_consumo_ad_kwh'),
    path('edit_irradi/<int:cliente_id>/',edit_irradi,name='edit_irradi'),
    
]