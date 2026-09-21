from flask import Blueprint,render_template,request
from app.utility import is_authorize
from app.service.product_service import get_product_service,get_products_service,get_similar_products_service,search_product_service,create_product_service,delete_product_service,update_product_service,product_service
from app.controller.product_controller import get_categories,get_all_sectors

product_bp = Blueprint('product_bp',__name__)

@product_bp.route("/product-catalog",methods=['GET'])
def product_catalog():
    return render_template('catalog.html')

@product_bp.route("/get-products/<int:page>/<int:page_size>", methods=['GET'])
def get_products(page, page_size):
    category_id = request.args.get('category-id')
    subcategory_id = request.args.get('subcategory-id')

    session_data = request.session_data
    response = get_products_service(
        page=page,
        page_size=page_size,
        session_data=session_data,
        category_id = category_id,
        subcategory_id = subcategory_id
    )
    return response

@product_bp.route("/search-product/<string:keyword>", methods=['GET'])
def search_product(keyword):
    category_id = request.args.get('category-id')
    subcategory_id = request.args.get('subcategory-id')

    session_data = request.session_data
    response = search_product_service(
        keyword=keyword,
        session_data=session_data,
        category_id=category_id,
        subcategory_id=subcategory_id
    )
    return response

@product_bp.route("/product/<string:p_id>", methods=['GET'])
def product(p_id):
    session_data = request.session_data
    response = product_service(
        product_id=p_id,
        session_data=session_data
    )
    return response

@product_bp.route("/get-product/<string:p_id>", methods=['GET'])
def get_product(p_id):
    session_data = request.session_data
    response = get_product_service(
        product_id=p_id,
        session_data=session_data
    )
    return response

@product_bp.route("/get-similar-products/<string:p_id>/<string:p_name>/<string:p_type>/<int:page>/<int:page_size>", methods=['GET'])
def get_similar_products(p_id,p_name,p_type,page,page_size):
    session_data = request.session_data
    response = get_similar_products_service(
        p_id=p_id,
        p_name=p_name,
        p_type=p_type,
        page=page,
        page_size=page_size,
        session_data=session_data
    )
    return response

@product_bp.route('/create-product', methods=['POST'])
@is_authorize(role='admin')
def create_product(session_data):
    data = request.form
    name = data.get('addName')
    price = data.get('addPrice')
    image = request.files.get('addImage')
    types = data.get('addType')
    desc = data.get('addDesc')
    category_id = data.get('addCategory')
    subcategory_id = data.get('addSubcategory')
    importExcel = request.files.get('importExcel')
    unit = data.get('addUnit')
    response = create_product_service(
        name=name,
        price=price,
        image=image,
        types=types,
        desc=desc,
        unit=unit,
        importedExcel=importExcel,
        category_id=category_id,
        subcategory_id=subcategory_id
    )
    return response



@product_bp.route('/update-product',methods=['POST'])
@is_authorize(role='admin')
def update_product(session_data):
    data = request.form
    id = data.get('editProductid')
    name = data.get('editName')
    price = data.get('editPrice')
    image = request.files.get('editImage')
    types = data.get('editType')
    desc = data.get('editDesc')
    visibilty = data.get('editVisibility')
    redirectPath = data.get('redirectPath')
    unit = data.get('editUnit')

    response = update_product_service(
        product_id=id,
        name=name,
        price=price,
        image=image,
        types=types,
        desc=desc,
        unit=unit,
        visibilty=visibilty,
        redirectPath=redirectPath
    )
    return response

@product_bp.route('/delete-product',methods=['POST'])
@is_authorize(json_response=True,role='admin')
def delete_product(session_data):
    data = request.json
    id = data.get('id')

    response = delete_product_service(
        product_id=id
    )
    return response

@product_bp.route('/categories',methods=['GET'])
def categories():
    return render_template('categories.html')

@product_bp.route('/get-categories',methods=['GET'])
def get_all_categories():
    sector_id = request.args.get('sector-id')
    sector_name = request.args.get('sector-name')
    return get_categories(sector_id,sector_name)

@product_bp.route('/get-sectors',methods=['GET'])
def get_all_sector():
    return get_all_sectors()