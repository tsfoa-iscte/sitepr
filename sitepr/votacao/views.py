from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Questao, Opcao

def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list':latest_question_list}
    return render(request, 'votacao/index.html',context)

def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})

def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})

def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist): # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html', {'questao': questao, 'error_message': "Não escolheu uma opção",})
    else:
        opcao_seleccionada.votos += 1
        opcao_seleccionada.save()
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior.
    return HttpResponseRedirect(reverse('votacao:resultados', args=(questao.id,)))

def criarquestao(request):
    return render(request, 'votacao/criarquestao.html')

def sendquest(request):
    if request.method == 'POST':
        questao = request.POST["questao"]
        q= Questao(questao_texto=str(questao), pub_data=datetime.now())
        q.save()
        return HttpResponseRedirect(reverse('votacao:index'))

def criaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request ,'votacao/novaopcao.html', {'questao': questao})

def novaopcao(request,questao_id):
    if request.method == 'POST':
        opcao = request.POST["opcao"]
        questao = get_object_or_404(Questao, pk=questao_id)
        newopcao=Opcao(questao=questao , opcao_texto=str(opcao))
        newopcao.save()
        return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))




