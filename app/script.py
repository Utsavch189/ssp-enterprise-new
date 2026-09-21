import os
import random
import requests
from faker import Faker
from datetime import datetime,timedelta
import sys,os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db import get_con_cursor
from utility import hashs

fake = Faker()

def download_random_image(image_name, folder="media"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    image_urls = [
        "https://picsum.photos/200/300",
        "https://loremflickr.com/200/300",
    ]

    image_url = random.choice(image_urls)

    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(folder, image_name)
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return file_path
        else:
            print(f"Failed to download image from {image_url}")
            return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def seed_product(num_products=10):
    con, cur = get_con_cursor()

    try:
        for _ in range(num_products):
            product_id = fake.uuid4()[:8]
            name = fake.word()
            category = fake.word()
            desc = fake.sentence(nb_words=10)
            price = round(random.uniform(10, 1000), 2)
            image_name = f"{product_id}.jpg"
            
            image_path = download_random_image(image_name)
            
            if image_path:
                image = image_name
            else:
                image = None
                continue

            q = """
                INSERT INTO Products (id, name, image, price, desc,category)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cur.execute(q, (product_id, name, image, price, desc, category))

        con.commit()
        print(f"Successfully seeded {num_products} products.")
    except Exception as e:
        con.rollback()
        print(f"seed_product() | Error: {e}")
    finally:
        con.close()

def create_admin_user(name:str,email:str,password:str):
    con, cur = get_con_cursor()
    q="""
        INSERT INTO Users (name, email, password, role)
        VALUES (?, ?, ?, ?)
    """
    try:
        password=hashs(password)
        cur.execute(q, (name.upper(), email.lower(), password, 'admin'))
        con.commit()
    except Exception as e:
        con.close()
        print(f"create_admin_user() | {str(e)}")
    finally:
        con.close()

def seed_user_query(days:int=30):
    con, cur = get_con_cursor()
    q="Delete From UserQuery Where 1=1"
    cur.execute(q)
    con.commit()
    for i in range(days):
        day = (datetime.now() + timedelta(days=i+1)).strftime("%Y-%m-%d %H:%M:%S")
        q="""
            Insert Into UserQuery(name,subject,email,message,phone,file,gst_no,created_at) 
            Values(?, ?, ?, ?, ?, ?, ?, ?)
        """
        cur.execute(q,(fake.name(),fake.sentence(nb_words=10),fake.email(),fake.sentence(nb_words=50),fake.phone_number(),"abc.png","1234",day))
        con.commit()
    con.close()

if __name__=="__main__":
    seed_product(60)
    create_admin_user('SSP','enterprisessp007@gmail.com','ssp@2025')
    seed_user_query(120)
    pass