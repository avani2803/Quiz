from Quiz.models import UserInfo

class DB:
    def saveUser(user):
        return user.save()

    def getUserByEmail(email):
        return UserInfo.objects.get(email=email)