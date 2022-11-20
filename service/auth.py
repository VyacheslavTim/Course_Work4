import calendar

from constants import JWT_SECRET, JWT_ALGORITHM
from service.user import UserService
import datetime
import jwt


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def formation_by_token(self, username, password, is_refresh=False):
        user = self.user_service.get_by_user(username)

        if user is None:
            raise Exception()

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                raise Exception()

        data = {
            "username": user.username,
            "aim": user.aim
        }

        access_token_duration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["num"] = calendar.timegm(access_token_duration.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        refresh_token_duration = datetime.datetime.utcnow() + datetime.timedelta(days=200)
        data["num"] = calendar.timegm(refresh_token_duration.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def check_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = data.get("username")

        user = self.user_service.get_by_user(username)

        if user is None:
            raise Exception()
        return self.formation_by_token(username, user.password, is_refresh=True)
