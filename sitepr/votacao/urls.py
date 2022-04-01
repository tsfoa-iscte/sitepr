from django.urls import path
from . import views
app_name = 'votacao'
urlpatterns = [
    # ex: votacao/
    path("", views.index, name='index'),
    # ex: votacao/1
    path("<int:questao_id>", views.detalhe,
        name='detalhe'),
    # ex: votacao/3/resultados
    path('<int:questao_id>/resultados', views.resultados,
        name='resultados'),
    # ex: votacao/5/voto
    path('<int:questao_id>/voto', views.voto,
        name='voto'),
    path('criarquestao', views.criarquestao, name='criarquestao'),
    path('sendquest', views.sendquest, name='sendquest'),
    path('<int:questao_id>/criaropcao',views.criaropcao, name='criaropcao'),
    path('<int:questao_id>/novaopcao', views.novaopcao, name= 'novaopcao'),
    #path('votacao/opcaocriada', views.opcriada, name='opcaocriada')
    path('<int:questao_id>/apagarquestao', views.deletequestao, name='deletequestao'),
    path('<int:questao_id>/apagaropcao', views.deleteopcao, name='deleteopcao'),
    path('registar',views.registar,name='registar'),
    path('registo',views.registo,name='registo'),
    path('loginview',views.loginview,name='loginview'),
    path('logoutview', views.logoutview, name='logoutview'),
    path('perfil', views.perfil, name='perfil'),
]