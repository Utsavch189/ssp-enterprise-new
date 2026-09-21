from flask import Blueprint,render_template,send_from_directory,request,redirect
from app.service.crm_service import contact_us_service,submit_query_service,download_query_service
from urllib.parse import unquote

crm_bp = Blueprint('crm_bp',__name__)

@crm_bp.route("/",methods=['GET'])
def home():
    return render_template('home.html')

@crm_bp.route("/internal-error",methods=['GET'])
def internal_error():
    return render_template('internal_server_error.html')

@crm_bp.route("/about",methods=['GET'])
def about():
    return render_template('about.html')

@crm_bp.route("/contact",methods=['POST'])
def contact():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    contact_us_service(
        name=name,
        email=email,
        message=message
    )
    return redirect("/")

@crm_bp.route("/submit-query",methods=['POST'])
def submit_query():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    phone = data.get('contact_no')
    gst_no = data.get('gst_no')
    referral_mobile = data.get('referral_mobile')
    file = request.files.get('q_file')

    submit_query_service(
        name=name,
        email=email,
        message=message,
        phone=phone,
        file=file,
        gst_no=gst_no,
        referral_mobile=referral_mobile
    )
    return redirect("/")

@crm_bp.route("/download-query",methods=['POST'])
def download_query():
    data = request.json
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    response = download_query_service(start_date,end_date)
    return response

@crm_bp.route('/media/<path:filename>')
def media_serve(filename):
    return send_from_directory('media', filename)

@crm_bp.route('/query-file/<path:filename>')
def query_file_serve(filename):
    return send_from_directory('media/userQuery', unquote(filename))