from flask import Blueprint,request,render_template,make_response,jsonify
import json
from app.utility import is_authorize,hashs
from app.service.auth_service import logins,logouts,change_password_service

auth_bp = Blueprint("auth_bp",__name__)

@auth_bp.route("/login", methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        data = request.form
        email = data.get('email')
        password = data.get('password')
        response = logins(email,password)
        return response

@auth_bp.route("/logout", methods=['GET'])
@is_authorize(redirect_url="/")
def logout(session_data):
    session_id = request.cookies.get('session_id')
    response = logouts(session_id)
    return response

@auth_bp.route("/session-data",methods=['GET'])
def get_session_data():
    try:
        return make_response(jsonify({"data":json.loads(request.session_data) if request.session_data!=None else None,"status":200}),200)
    except Exception as e:
        return make_response(jsonify({"data":None,"status":500}),500)

@auth_bp.route("/change-password", methods=['POST'])
@is_authorize("/")
def change_password(session_data):
    data = request.form
    user_id = session_data.get('user_id')
    new_password = hashs(data.get('new_password'))
    session_id = request.cookies.get('session_id')
    response = change_password_service(
        user_id=user_id,
        new_password=new_password,
        session_id=session_id
    )
    return response