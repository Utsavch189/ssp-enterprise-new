from flask import request,redirect
from app.db import get_con_cursor
import json

def session_data():
    setattr(request,"session_data",None)
    session_id = request.cookies.get('session_id')
    if session_id:
        try:
            con,cur = get_con_cursor()
            q="SELECT * from SessionToken where token = ?"
            cur.execute(q,(session_id,))
            data = cur.fetchone()
            con.close()
            setattr(request,"session_data",json.dumps({
                "user_id":data[2],
                "role" : data[3],
                "expires_at" : data[4],
                "session_token" : session_id
            }))
        except Exception as e:
            response = redirect("/login")
            response.delete_cookie("session_id")
            return response
