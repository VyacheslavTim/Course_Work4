import calendar

from constants import JWT_SECRET, JWT_ALGORITHM
from service.user import UserService
import datetime
import jwt


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def created_token(self, email, password, is_refresh=False):
        user = self.user_service.get_by_email(email)

        if user is None:
            raise Exception()

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                raise Exception()

        data = {
            "username": user.email,
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
        email = data.get("email")

        user = self.user_service.get_by_email(email)

        if user is None:
            raise Exception()
        return self.created_token(email, user.password, is_refresh=True)

    def valid_token(self, access_token, refresh_token):
        for tok in [access_token, refresh_token]:
            try:
                jwt.decode(jwt=tok, keys=JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except Exception as e:
                return False
            return True



