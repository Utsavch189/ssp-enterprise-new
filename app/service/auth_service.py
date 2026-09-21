from app.controller.auth_controller import get_a_user,add_session_token,delete_session_token,change_password
from flask import render_template,make_response,redirect
from app.utility import verify_hash,hashs,generate_unique_id
from datetime import datetime,timedelta
import os
from dotenv import load_dotenv

load_dotenv()

def logins(email:str,password):
    try:
        user=get_a_user(email=email)
        if not user:
            response = render_template('login.html',message="wrong credentials!",level="error")
            return response
        if not verify_hash(password,user[3]):
            response = render_template('login.html',message="wrong credentials!",level="error")
            return response
        
        session_id = generate_unique_id()
        add_session_token(
            token=session_id,
            user_id=user[0],
            role=user[4],
            expires_at=datetime.now()+timedelta(minutes=int(os.getenv('SESSION_EXPIRY')))
        )

        response = make_response(redirect('/'))
        response.set_cookie('session_id',session_id,max_age=int(os.getenv('SESSION_EXPIRY'))*60)
        return response

    except Exception as e:
        print(e)
        response = render_template('login.html',message="something is wrong!",level="error")
        return response

def logouts(session_token:str):
    try:
        delete_session_token(session_token)
        response = make_response(redirect('/'))
        response.delete_cookie('session_id')
        return response
    except Exception as e:
        print(e)
        return redirect("/internal-error")

def change_password_service(user_id:str,new_password:str,session_id:str):
    try:
        change_password(
            user_id=user_id,
            new_password=new_password
        )
        response = redirect("/login")
        response.delete_cookie('session_id')
        delete_session_token(
            token=session_id
        )
        return response
    except Exception as e:
        return redirect("/internal-error")