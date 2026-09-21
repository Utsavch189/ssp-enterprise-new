import json
from app.controller.product_controller import get_product,search_product,similar_products,get_products,create_product,update_product,delete_product
from flask import redirect,make_response,jsonify,render_template,request
from app.utility import generate_unique_id,insert_data_from_xl
import os
import time

def get_products_service(page:int,page_size:int,session_data,category_id=None,subcategory_id=None):
    try:
        offset = (page - 1) * page_size
        products = get_products(
            page_size=page_size,
            offset=offset,
            role=json.loads(session_data).get('role')  if session_data else 'guest',
            category_id = category_id,
            subcategory_id = subcategory_id
        )
        return {"products": products.get('products'),"total_products":products.get('total_products')}, 200
    except Exception as e:
        print(e)
        return {"message": str(e)}, 500

def search_product_service(keyword:str,session_data,category_id=None,subcategory_id=None):
    try:
        products = search_product(
            keyword=keyword,
            role=json.loads(session_data).get('role')  if session_data else 'guest',
            category_id=category_id,
            subcategory_id=subcategory_id
        )
        if products.get('products'):
            return {"products": products.get('products')}, 200
        else:
            return {"message": "No products found matching the keyword"}, 404
    except Exception as e:
        return {"message": str(e)}, 500

def product_service(product_id:str,session_data):
    try:
        product = get_product(
            p_id=product_id,
            role=json.loads(session_data).get('role')  if session_data else 'guest'
        )
        if product:
            category_name = product['category_name']
            category_name = category_name.split(" ")
            category_name = category_name[1:]
            category_name = " ".join(category_name)
            product['category_name'] = category_name
            return render_template('product_details.html',product=product)
        return {"message": "Product not found"}, 404
    except Exception as e:
        return redirect("/internal-error")

def get_product_service(product_id:str,session_data):
    try:
        product = get_product(
            p_id=product_id,
            role=json.loads(session_data).get('role')  if session_data else 'guest'
        )
        if product:
            return {"product":product}, 200
        return {"message": "Product not found"}, 404
    except Exception as e:
        return {"message": str(e)}, 500

def get_similar_products_service(p_id,p_name,p_type,page,page_size,session_data):
    try:
        offset = (page - 1) * page_size
        products = similar_products(
            p_id=p_id,
            p_name=p_name,
            p_type=p_type,
            offset=offset,
            page_size=page_size,
            role=json.loads(session_data).get('role')  if session_data else 'guest'
        )
        return {"similar_products": products.get('products',[]),"total_products": products.get('total_products')}, 200
    except Exception as e:
        return {"message": str(e)}, 500

def create_product_service(name,price,image,types,desc,unit,category_id=None,subcategory_id=None,importedExcel=None):
    try:
        product_id = generate_unique_id()

        if not importedExcel:
            image_name = product_id+image.filename
            create_product(
                product_id=product_id,
                name=name,
                image_name=image_name,
                price=price,
                types=types,
                desc=desc,
                unit=unit,
                category_id=category_id,
                subcategory_id=subcategory_id
            )
            image.save(f"app/media/{image_name}")
            return redirect("/product-catalog")
        else:
            excel_name = str(int(time.time() * 1000))+importedExcel.filename
            excel_path = f"app/media/importedExcels/{excel_name}"
            importedExcel.save(excel_path)
            status=insert_data_from_xl(excel_file=excel_path)
            if not status:
                return make_response(jsonify({"error":"data seeding is failed!"}),500)
            return make_response(jsonify({"message":"data seeding is completed!"}),200)
    except Exception as e:
        print(e)
        if importedExcel:
            return make_response(jsonify({"error":"data seeding is failed!"}),500)
        else:
            return redirect("/internal-error")

def update_product_service(product_id,name,price,image,types,desc,unit,visibilty,redirectPath):
    try:
        product = get_product(
            p_id=product_id
        )
        image_name = product.get('image')
        if image:
            os.remove(f"app/media/{image_name}")
            image.save(f"app/media/{image.filename}")
            image = image.filename
        else:
            image = image_name

        update_product(
            product_id=product_id,
            name=name,
            image_name=image,
            price=price,
            types=types,
            desc=desc,
            unit=unit,
            visibilty=1 if visibilty!=None else 0
        )
        return redirect(redirectPath)
    except Exception as e:
        print(e)
        return redirect("/internal-error")

def delete_product_service(product_id:str):
    try:
        product = get_product(
            p_id=product_id
        )
        image_name = product.get('image')
        if image_name:
            os.remove(f"app/media/{image_name}")
        delete_product(
            product_id=product_id
        )
        return make_response(jsonify({"message":"Successfully Deleted!","status":200}),200)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message":"Internal server error!","status":500}),500)