from app.models import User
from app.pydantic_models import Regist_Model, Login_Model
from app.pydantic_models import ResponseMessage
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, current_user
import datetime
from flask_openapi3.models import Tag
from app.views.blueprint import BlueprintApi
from flask import jsonify
from app.logger import logger

# Set up Bluerints
SECURITY = [{"jwt": []}]
TAG = Tag(name="Auth", description="Basic auth")
api_auth = BlueprintApi("/auth", __name__, abp_tags=[TAG], abp_security=SECURITY)


@api_auth.get('/register')
def register_get():
    return {'Register form': 'Sign up'}, 200


@api_auth.post('/register')
@logger.catch
def register_post(body: Regist_Model):
    if User.query.filter(User.email == body.email).first():
        logger.info(f'Email "{body.email}" already in use')
        return ResponseMessage(success=False, description=f'User with email: {body.email} already exist').json()

    if User.query.filter(User.username == body.username).first():
        logger.info(f'Username "{body.username}" already in use')
        return ResponseMessage(success=False, description=f'User with username: {body.username} already exist').json()

    user = User(username=body.username, email=body.email, password=body.password)
    user.save()
    return ResponseMessage(success=True, description='Registration successful.').json()


@api_auth.get('/login')
def login_get():
    return {'Login form': 'Please log in'}, 200


@api_auth.post('/login')
@logger.catch
def login_post(body: Login_Model):

    user = User.query.filter(User.username == body.username).first()

    if user is None:
        logger.info(f'User "{body.username}" does not exist. Please, sign up.')
        return ResponseMessage(
            success=False,
            description=f'User "{body.username}" does not exist. Please, sign up.'
        ).json(), 409

    if not check_password_hash(user.password, body.password):
        logger.info(f'User with email "{body.email}" entered wrong password')
        return ResponseMessage(success=False, description='Wrong password').json(), 409

    expires = datetime.timedelta(minutes=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)
    headers = {'Authorization': f'Bearer {access_token}'}
    print(jsonify(headers=headers))

    return ResponseMessage(success=True, description="Logged in").json(), 200, headers


@api_auth.get("/logout")
@jwt_required()
def logout_get():

    return {"Logout form": f"Logout {current_user}"}, 302
