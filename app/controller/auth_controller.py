from app.db import get_con_cursor

def get_a_user(email:str):
    data=()
    con, cur = get_con_cursor()
    try:
        q = "SELECT * FROM Users WHERE email = ?"
        cur.execute(q, (email,))
        data = cur.fetchone()
    except Exception as e:
        print(e)
    finally:
        con.close()
        return data

def add_session_token(token,user_id,role,expires_at):
    con, cur = get_con_cursor()
    try:
        con,cur = get_con_cursor()
        q="INSERT INTO SessionToken(token,user_id,role,expires_at) VALUES(? ,?, ?, ?)"
        cur.execute(q,(token,user_id,role,expires_at))
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
    finally:
        con.close()

def delete_session_token(token:str):
    status=True
    con, cur = get_con_cursor()
    try:
        q="Delete From SessionToken Where token = ?"
        con,cur = get_con_cursor()
        cur.execute(q,(token,))
        con.commit()
    except Exception as e:
        status=False
        con.rollback()
        print(e)
    finally:
        con.close()
        return status

def change_password(user_id:str,new_password:str):
    con, cur = get_con_cursor()
    try:
        con,cur = get_con_cursor()
        q = "UPDATE Users SET password = ? WHERE id = ?"
        cur.execute(q, (new_password, user_id))
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
    finally:
        con.close()