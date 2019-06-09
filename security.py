from werkzeug.security import safe_str_cmp
from resources.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    print('identity payload', payload)
    user_id = payload['identity']
    print('userid', user_id)
    return UserModel.find_by_id(user_id)
