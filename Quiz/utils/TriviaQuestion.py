from dataclasses import dataclass
from typing import List, Any, TypeVar, Callable, Type
from Quiz.models import QuestionAnswer
from Quiz.utils.helper import *
import requests

T = TypeVar("T")

def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]

@dataclass
class TriviaQuestion:
    category: str
    type: str
    difficulty: str
    question: str
    correct_answer: str
    incorrect_answers: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'TriviaQuestion':
        assert isinstance(obj, dict)
        category = from_str(obj.get("category"))
        type = from_str(obj.get("type"))
        difficulty = from_str(obj.get("difficulty"))
        question = from_str(obj.get("question"))
        correct_answer = from_str(obj.get("correct_answer"))
        incorrect_answers = from_list(from_str, obj.get("incorrect_answers"))
        return TriviaQuestion(category, type, difficulty, question, correct_answer, incorrect_answers)

    @staticmethod
    def convertListDictToTrivaQuestion(objs):
        triviaQuestion = []
        for obj in objs:
            question = TriviaQuestion.from_dict(obj)
            triviaQuestion.append(question)
        return triviaQuestion

    @staticmethod
    def convertTrivaQuestionToQuestion(trivaQuestions):
        htmlCodes = (
            ("'", '&#39;'),
            ("'", '&#039;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
        questionAnswers = [] 
        for trivaQuestion in trivaQuestions:
            if(trivaQuestion.type=="multiple"):
                questionAnswer = QuestionAnswer(question = trivaQuestion.question, category = trivaQuestions[0].category,
                answer = trivaQuestion.correct_answer, wrongAnswer1=trivaQuestion.incorrect_answers[0], wrongAnswer2=trivaQuestion.incorrect_answers[1],
                wrongAnswer3=trivaQuestion.incorrect_answers[2])
                for code in htmlCodes:
                    questionAnswer.question = questionAnswer.question.replace(code[1], code[0])                
            questionAnswer.save()
            questionAnswers.append(questionAnswer)            
        return questionAnswers

    @staticmethod
    def getQuestionForCategory(quizCategory):
        quizMap = {"21": 'Sports', "22": "Geography", "30": "Science: Gadgets" }
        questionAnswers = QuestionAnswer.objects.filter(category=quizMap.get(quizCategory))
        if questionAnswers.exists()==0:
            questionAnswers = TriviaQuestion.convertTrivaQuestionToQuestion(TriviaQuestionClient.getTriviaQuestion(quizCategory))
        return questionAnswers

class TriviaQuestionClient:
    def getTriviaQuestion(category):
        url = "http://opentdb.com/api.php"
        respone = requests.get(url,params={'amount':'10','category':category,'type':'multiple'})
        res = respone.json()
        triviaQuestion = TriviaQuestion.convertListDictToTrivaQuestion(res['results'])
        return triviaQuestion