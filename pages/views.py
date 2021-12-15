from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from pages.forms import QuizForm
from pages.models import QuestionModel, ResultsModel
from random import randint
import random



# Create your views here.

def index(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user_qs = authenticate(username = username, password = password)

        if user_qs is not None:
            messages.success(request,"Hesabınıza uğurla daxil oldundu")
            login(request,user_qs)

            return redirect("pages:quiz")

        else:
            messages.info(request,"İstifadəçi adı və ya şifrə yalnışdır")

    return render(request,"login.html")

def register_user(request):
    
    if request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            try:
                neWUser = User.objects.create_user(username = username,first_name = name, email = email, password = password)
                neWUser.save()
                login(request,neWUser)
                messages.success(request,"Hesabınız uğurla yaradıldı.")

            except:
                messages.info(request,"Bu istifadəçi adından mövcuddur")
                return redirect("pages:register")

        else:
            messages.info(request,"Şifrələr eyni deyil!")
            return redirect("pages:register")
        
        return redirect('pages:quiz')

    return render(request,"register.html")

def logout_user(request):

    logout(request)
    messages.success(request,"Hesabınızdan uğurla çıxıldı")

    return redirect("pages:index")


@login_required(login_url='pages:index')
def quiz(request):
    

    questions = QuestionModel.objects.order_by("?")[:20]

    if request.method == "POST":
        questions = QuestionModel.objects.all()
        correct = 0
        wrong = 0
        score = ""
        wrong_list = []
        answer_l = []
        answer_list = []

        for q in questions:
            
            if q.answer == request.POST.get(q.name):
                correct += 1
            
            elif request.POST.get(q.name) == None:
                pass

            else:
                wrong += 1
                wrong_list.append(q.id)
                answer_l.append(request.POST.get(q.name))

        if correct <= 4:
            score += str("E")

        elif 9 >= correct >=4:
            score += str("D")
            
        elif 13 >= correct >=9 :
            score += str("C")

        elif 17 >= correct >=13:
            score += str("B")

        else:
            score += str("A")
        

        for answer in answer_l:
            if answer != None:
                answer_list.append(answer)
        
        wrong_questions = QuestionModel.objects.filter(id__in =wrong_list )

        all = zip(wrong_questions,answer_list)

        result = ResultsModel.objects.create(user = request.user, wrong = wrong, correct = correct, score = score)
        result.save()

        extends = {
            "correct":correct,
            "wrong":wrong,
            "score":score,
            "list":wrong_list,
            "wrong_questions":wrong_questions,
            "answer_list":answer_list,
            "all":all,
        }




        return render(request, "wrong_questions.html", extends)       

    extends = {
        'questions':questions,
    }
    
    return render(request,"quiz.html",extends)

@login_required(login_url='pages:index')
def my_questions(request):
    user = request.user
    questions = QuestionModel.objects.filter(user = user)

    extends = {
        'questions':questions,
    }

    return render(request, "myquestions.html",extends)

@login_required(login_url='pages:index')
def add_quiz(request):

    form = QuizForm()
    user = request.user

    if request.method == "POST":
        
        form = QuizForm(request.POST)

        if form.is_valid():
    
            
            quest = form.save(commit = False)
            quest.user = user
            quest.save()

            messages.success(request,"Sualınız uğurla əlavə edildi.")
            return redirect("pages:my_questions")


    extends = {
        'form':form,
    }
    
    return render(request, "addquiz.html",extends)

@login_required(login_url='pages:index')
def delete_quiz(request,id):
    user = request.user

    question = get_object_or_404(QuestionModel,user = user, id = id)
    question.delete()

    messages.success(request,"Sualınız uğurla silindi")    

    return redirect("pages:my_questions")

@login_required(login_url='pages:index')
def update_quiz(request,id):
    user = request.user
    question = get_object_or_404(QuestionModel, id = id,user = user)
    form = QuizForm(request.POST or None,instance=question)
    
    if form.is_valid():
        question = form.save(commit=False)
        question.user = request.user
        question.save()
            
        messages.success(request,"Sualınız uğurla yeniləndi")
        return redirect("pages:my_questions")

    extends = {
        "form":form,
    }    
    return render(request,"quizupdate.html",extends)

@login_required(login_url='pages:index')
def results(request):

    user = request.user

    results = ResultsModel.objects.filter(user = user)

    extends = {
        "results":results,
    }

    return render(request,"results.html",extends)


def deleteresult(request,id):

    user = request.user
    result = get_object_or_404(ResultsModel,id = id, user =user)
    
    result.delete()
    
    return redirect("pages:myresults")

