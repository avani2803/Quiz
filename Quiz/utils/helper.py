from Quiz.utils.TriviaQuestion import TriviaQuestion
from Quiz.utils.DB import *

class Helper:
    def checkSession(request):
        if request.session.has_key('email'):
            emailID = request.session['email']
            try:
                user =  DB.getUserByEmail(request.session['email'])
                return user
            except UserInfo.DoesNotExist:
                return None
        return None      