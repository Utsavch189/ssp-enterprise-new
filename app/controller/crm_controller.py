from app.db import get_con_cursor
from datetime import datetime
import pytz

def save_contact_hist(name:str,message:str,subject:str,sender_email:str,receiver_email:str):
    con,cur = get_con_cursor()
    try:
        q="""
            Insert Into ContactHistory(name,subject,sender_email,receiver_email,message) 
            Values(?, ?, ?, ?, ?)
        """
        cur.execute(q,(name,subject,sender_email,receiver_email,message))
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
    finally:
        con.close()

def save_user_query(name:str,message:str,subject:str,email:str,phone:str,file=None,gst_no=None,referral_mobile=None):
    con,cur = get_con_cursor()
    try:
        q="""
            Insert Into UserQuery(name,subject,email,message,phone,file,gst_no,referral_mobile) 
            Values(?, ?, ?, ?, ?, ?, ?, ?)
        """
        cur.execute(q,(name,subject,email,message,phone,file if file!=None else 'NULL',gst_no if gst_no!=None else 'NULL',referral_mobile if referral_mobile!=None else 'NULL'))
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
    finally:
        con.close()

def get_user_queries(start_date,end_date):
    con,cur = get_con_cursor()
    data = {}
    try:
        kolkata_tz = pytz.timezone("Asia/Kolkata")
        utc_tz = pytz.utc

        q="""
            Select * From UserQuery Where created_at Between ? AND ? Order By created_at
        """
        cur.execute(q,(start_date,end_date))
        res = cur.fetchall()

        name = []
        subject = []
        email = []
        phone = []
        message = []
        gst_no = []
        referral_mobile = []
        file = []
        submitted_at = []

        if res:
            for r in res:
                name.append(r[1] if r[1] else "N/A")
                subject.append(r[2] if r[2] else "N/A")
                email.append(r[3] if r[3] else "N/A")
                phone.append(r[4] if r[4] else "N/A")
                message.append(r[5] if r[5] else "N/A")
                gst_no.append(r[6] if r[6] else "N/A")
                referral_mobile.append(r[7] if r[7] else "N/A")
                file.append("http://sspenterprise.in"+"/query-file/"+r[8] if r[8] else "N/A")
                submitted_at.append(((datetime.strptime(r[9], "%Y-%m-%d %H:%M:%S").replace(tzinfo=utc_tz)).astimezone(kolkata_tz)).strftime("%Y-%m-%d %H:%M:%S") if r[9] else "N/A")
            data = {
                    "name":name,
                    "subject" : subject,
                    "email": email,
                    "phone": phone,
                    "message" : message,
                    "gst_no" : gst_no,
                    "referral_mobile" : referral_mobile,
                    "file" : file,
                    "submitted_at" : submitted_at
                }
    except Exception as e:
        print(e)
    finally:
        con.close()
        return data