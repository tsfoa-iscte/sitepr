from datetime import datetime
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Questao, Opcao, Aluno
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout

def email_check(user):
    return user.email.endswith('@iscte-iul.pt')

def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {'latest_question_list':latest_question_list}
    return render(request, 'votacao/index.html',context)

def login_check(request):
    username = request.POST['username']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('votacao:index',))
    else:
        return render(request, 'votacao/index.html')

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

@login_required(login_url='/votacao/')
def criarquestao(request):
    if request.method == 'POST':
        try:
            questao = request.POST["questao"]
        except KeyError:
            HttpResponseRedirect(reverse('votacao:index'))
        if questao:
            q = Questao(questao_texto = str(questao), pub_data=datetime.now())
            q.save()
            return HttpResponseRedirect(reverse('votacao:index'))
        else:
            return HttpResponseRedirect(reverse('votacao:index'))
    else:
        return render(request,'votacao/criarquestao.html')

"""def criaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request ,'votacao/novaopcao.html', {'questao': questao})
, login_url='/votacao/registo_invalido/'
def novaopcao(request,questao_id):
    if request.method == 'POST':
        opcao = request.POST["opcao"]
        questao = get_object_or_404(Questao, pk=questao_id)
        newopcao=Opcao(questao=questao , opcao_texto=str(opcao))
        newopcao.save()
        return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))"""

@login_required(login_url='/votacao/')
def novaopcao(request,questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    if request.method == 'POST':
        try:
            opcao = request.POST["opcao"]
        except KeyError:
            return render(request, 'votacao/novaopcao.html', {'questao': questao})
        if opcao:
            newopcao = Opcao(questao=questao, opcao_texto=str(opcao))
            newopcao.save()
            return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
        else:
            return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
    else:
        return render(request, 'votacao/novaopcao.html', {'questao': questao})

@login_required(login_url='/votacao/')
def deletequestao(request, questao_id):
    questao = Questao.objects.get(id=questao_id)
    questao.delete()
    return HttpResponseRedirect(reverse('votacao:index'))

@login_required(login_url='/votacao/')
def deleteopcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        return render(request, 'votacao/detalhe.html',
                      {'questao': questao, 'error_message': "Não escolheu uma opção", })
    else:
        opcao_seleccionada.delete()
    return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))

def loginview(request):
    username = request.POST['username']
    password = request.POST['pass']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('votacao:index',))
    else:
        return render(request, 'votacao/index.html')


def registar(request):
    return render(request, 'votacao/registar.html')

def registo(request):
    username = request.POST['username']
    password = request.POST['pass']
    email = request.POST.get('email')
    curso = request.POST['curso']
    user= User.objects.create_user(username , email, password)
    user.save()

    if bool(request.FILES.get('myfile',False)):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        file = uploaded_file_url[1:]
        print(file)
        aluno =Aluno(user=user, curso=curso, file=file)
    else:
        aluno = Aluno(user=user, curso=curso)
    aluno.save()
    return render(request, 'votacao/usercriado.html')

def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:index', ))

@login_required(login_url='/votacao/')
def perfil(request):
    return render(request, 'votacao/perfil.html')

