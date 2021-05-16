"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question,Choice,User
from django.template import loader
from django.core.urlresolvers import reverse
from app.forms import QuestionForm, ChoiceForm,UserForm, QuestionFilter
from django.shortcuts import redirect
import json


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Autor de la web',
            'message':'Datos de contacto',
            'year':datetime.now().year,
        })

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
def index(request):
    
    
    if request.method == "POST": 
        form = QuestionFilter(request.POST)
        if form.is_valid():
            categ = form.cleaned_data['category']
            latest_question_list = Question.objects.filter(category=categ).order_by('-pub_date')
            template = loader.get_template('polls/index.html')
           
    else:
        form = QuestionFilter()
        latest_question_list = Question.objects.order_by('-pub_date')

    context = {
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': latest_question_list,
                'form':form,
              }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
     question = get_object_or_404(Question, pk=question_id)
     return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:','question': question})

def results(request, question_id , correct):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:','question': question, 'correct':correct})

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else: 
       
        selected_choice.votes += 1
        selected_choice.save()
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form.  Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:','question': question, 'correct':selected_choice.correct})


def question_new(request):
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.pub_date = datetime.now()
                question.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html',
                #{'title':'Respuestas posibles','question': question})
        else:
            form = QuestionForm()
        return render(request, 'polls/question_new.html', {'form': form})

def choice_add(request, question_id):
        #Lista de opciones
        choices = Choice.objects.filter(question_id=question_id)
        cont = choices.count()
        question = Question.objects.get(id = question_id)
        if request.method == 'POST':
            form = ChoiceForm(request.POST)
            if form.is_valid():    
                
                choice = form.save(commit = False)
               
                #Si ya hay una opcion correcta
                if (choices.filter(correct ='True').count() == 1 and choice.correct):
                   return render(request, 'polls/choice_new.html', {'title':'Pregunta:' + question.question_text,'form': form,'cont':cont, 'allIncorrect':'No puede haber 2 respuestas correctas'})
                #Si se han introducido 3 opciones incorrectas
                if (Choice.objects.filter(question_id=question_id).filter(correct ='False').count() == 3 and not choice.correct):
                   return render(request, 'polls/choice_new.html', {'title':'Pregunta:' + question.question_text,'form': form,'cont':cont, 'allIncorrect':'La respuesta tiene que ser correcta'})
                print(choice.correct)
                choice.question = question
                choice.vote = 0
                choice.save()
                cont+=1
                #form.save()
        else: 
            
            form = ChoiceForm()
           
        #return render_to_response ('choice_new.html', {'form': form,
        #'poll_id': poll_id,}, context_instance = RequestContext(request),)
        if (choices.count() < 2):
            return render(request, 'polls/choice_new.html', {'title':'Pregunta:' + question.question_text,'form': form,'cont':cont, 'allIncorrect':'Tiene que haber al menos 2 respuestas'})
        if cont >= 4:
            return render(request, 'polls/choice_new.html', {'title':'Pregunta:' + question.question_text,'form': form, 'mtf':'Ya hay mas de 4 posibles respuestas'})
        return render(request, 'polls/choice_new.html', {'title':'Pregunta:' + question.question_text,'form': form, 'cont':cont})

def chart(request, question_id):
    q = Question.objects.get(id = question_id)
    qs = Choice.objects.filter(question=q)
    choices = [obj.choice_text for obj in qs]
    counts = [obj.votes for obj in qs]
    context = {
        'choices': json.dumps(choices),
        'counts': json.dumps(counts),
    }

    return render(request, 'polls/grafico.html', context)

def user_new(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html',
                #{'title':'Respuestas posibles','question': question})
        else:
            form = UserForm()
        return render(request, 'polls/user_new.html', {'form': form})

def users_detail(request):
    latest_user_list = User.objects.order_by('email')
    template = loader.get_template('polls/users.html')
    context = {
                'title':'Lista de usuarios',
                'latest_user_list': latest_user_list,
              }
    return render(request, 'polls/users.html', context)

def correctono(request):
    p = get_object_or_404(Question, pk=request.POST['question'])
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/respuestaAJAX.html', {'error': "ERROR: No se ha seleccionado una opcion",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return render(request, 'polls/respuestaAJAX.html', {'correct':selected_choice.correct,})
