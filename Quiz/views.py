from Quiz.utils.helper import *
from Quiz.models import QuizDetail, UserInfo
from Quiz.utils.DB import *
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
def home(request):
    user = Helper.checkSession(request) 
    if user == None:
        return render(request, 'Quiz/Index.html')
    print(user.name + " ", user.email)
    return render(request, 'Quiz/quizHome.html')

def register(request):
    if request.method=="POST":
        user = UserInfo(name=request.POST.get('name'),email=request.POST.get('email'),password=request.POST.get('password'))
        response = HttpResponse(DB.saveUser(user))
        request.session['email'] = user.email
        request.session['password'] = user.password
        return render(request, 'Quiz/quizHome.html')
    return render(request, 'Quiz/Register.html')

def login(request):
    if request.method == "POST":
        try:
            user = DB.getUserByEmail(request.POST.get('email'))
            if user.password == request.POST.get('password'):
                request.session['email'] = user.email
                request.session['password'] = user.password
                return render(request, 'Quiz/quizHome.html')
            return HttpResponseForbidden("User does not exists!!!")
        except UserInfo.DoesNotExist:
            return HttpResponseForbidden("User does not exists!!!")
    return render(request,"Quiz/Error404.html")

def Logout(request):
    request.session['email'] = ""
    request.session['password'] = ""
    return render(request, 'Quiz/Index.html')

def startQuiz(request):
    quizMap = {"21": 'Sports', "22": "Geography", "30": "Science: Gadgets" }
    if request.method == "POST":
        user = Helper.checkSession(request) 
        if user == None:
            return render(request, 'Quiz/Index.html')
        quizCategory= request.POST.get('quiz')
        triviaQuestions = TriviaQuestion.getQuestionForCategory(quizCategory)
        quizID = QuizDetail.genrateID(user)
        for triviaQuestion in triviaQuestions:
            quizDetail  = QuizDetail(quizID = quizID, question= triviaQuestion,userID=user.id)
            quizDetail.save()
        quizs = QuizDetail.objects.filter(quizID=quizID)
        dict = {}
        i = 1
        for quiz in quizs:
            dict['quizs' +str(i)]= quiz
            i=i+1
        dict["QuizID"] = quizID
        print(dict)
        return render(request,"Quiz/quiz.html",dict)
    return render(request,"Quiz/Error404.html")

def submitQuiz(request):
    quizid = request.POST.get('QuizID')
    time = request.POST.get('time')
    print("time: "+str(time))
    quizDetails = QuizDetail.objects.filter(quizID = quizid)
    correctAns = 0
    for quizDetail in quizDetails:
        quizDetail.givenAnswer = request.POST.get(str(quizDetail.question.id))
        print(quizDetail.givenAnswer)
        print(quizDetail.question.answer)
        if quizDetail.givenAnswer == quizDetail.question.answer:
            quizDetail.correct = True
            correctAns= correctAns+1
        else:
            quizDetail.correct = False
    msg =""
    if correctAns>8:
        msg="Congratulations you have scored a great number!!!!!"
    elif correctAns >6:
        msg="Congratulations you have scored a good number!!!!!"
    else:
        msg="Your score is too low"
    dict={"score":correctAns,"msg":msg}
    return render(request,"Quiz/Result.html",dict)

def about(request):
    return render(request, "Quiz/AboutUs.html")