from app.utility import push_email
import os
from dotenv import load_dotenv
from datetime import datetime,timedelta
from app.controller.crm_controller import save_contact_hist,save_user_query,get_user_queries
from app.utility import generate_unique_id
import base64
import pandas as pd
import io
from flask import send_file
import tempfile

load_dotenv()

SMTP_RECEIVER = os.getenv('SMTP_RECEIVER')

def contact_us_service(name:str,email:str,message:str):
    try:
        template = 'email_templates/contact_us.html'
        context = {
            "user_name" : name,
            "user_email" : email,
            "user_message" : message,
            "current_year" : datetime.now().year
        }
        subject = f"New Contact Request From {name}"
        save_contact_hist(
            name=name,
            message=message,
            subject=subject,
            sender_email=email,
            receiver_email=SMTP_RECEIVER
        )
        push_email(
            template_addr=template,
            receiver_email=[SMTP_RECEIVER],
            subject=subject,
            context=context
        )
    except Exception as e:
        print(e)

def submit_query_service(name:str,email:str,message:str,phone:str,file=None,gst_no=None,referral_mobile=None):
    try:
        attachment=None
        file_name=None
        if file:
            file_name = generate_unique_id()+file.filename
            file.save(f"app/media/userQuery/{file_name}")
            with open(f"app/media/userQuery/{file_name}","rb") as f:
                attachment = {
                    "content": base64.b64encode(f.read()).decode('utf-8'),
                    "name": file.filename
                } 
        
        subject = f"New Query From {name}"

        save_user_query(
            name=name,
            message=message,
            subject=subject,
            email=email,
            phone=phone,
            file=file_name,
            gst_no=gst_no,
            referral_mobile=referral_mobile
        )

        template = 'email_templates/submit_query_template.html'
        context = {
            "user_name" : name,
            "user_email" : email,
            "user_message" : message,
            "user_contact" : phone,
            "gst_no" : gst_no,
            "referral_mobile" : referral_mobile,
            "current_year" : datetime.now().year
        }

        push_email(
            template_addr=template,
            receiver_email=[SMTP_RECEIVER],
            subject=subject,
            context=context,
            attachment=attachment
        )
    except Exception as e:
        print(e)

def download_query_service(start_date=None, end_date=None):
    if start_date and end_date:
        start_date_sql = datetime.strptime(start_date, "%m/%d/%Y").strftime("%Y-%m-%d %H:%M:%S")
        end_date_sql = (datetime.strptime(end_date, "%m/%d/%Y") + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    else:
        end_date_sql = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_date_sql = (datetime.now() - timedelta(days=31)).strftime("%Y-%m-%d %H:%M:%S")

    queries = get_user_queries(start_date_sql, end_date_sql)

    df = pd.DataFrame.from_dict(queries) if queries else pd.DataFrame(columns=[
        "Name", "Subject", "Email", "Phone", "Message", 
        "Gst No", "Referral Mobile", "File", "Submitted At"
    ])

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        with pd.ExcelWriter(temp_file.name, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")

    return send_file(
        temp_file.name,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=f"{start_date_sql}_{end_date_sql}.xlsx"
    )