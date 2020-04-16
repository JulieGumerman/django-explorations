from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question


# Create your views here.
from django.http import HttpResponse
#####################ONE WAY TO WRITE INDEX#######################
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

#######################REFACTORED INDEX FUNCTION####################
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


################ detail function, first way ###########################
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})

#     #return HttpResponse("You're looking at question %s." % question_id)


################### detail function, second way ########################
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


################### REFACTORED DETAIL VIEW ############################
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


####################results, first way ###############################
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


#################### RESULTS, REFACTORED ###########################
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You did not select a choice, silly hooman.',
        })

    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        #HttpResponseRedirect is what bumps you along to the results page when you submit your result