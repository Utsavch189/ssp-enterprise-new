from app.db import get_con_cursor

def get_products(page_size:int,offset:int,role:str='admin',category_id=None,subcategory_id=None):
    data={}
    con, cur = get_con_cursor()
    try:
        if role=='admin':
            if category_id and subcategory_id:
                q1 = "SELECT * FROM Products Where category_id = ? AND subcategory_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?"
                q2 = "SELECT COUNT(*) FROM Products Where category_id = ? AND subcategory_id = ?"
            elif category_id:
                q1 = "SELECT * FROM Products Where category_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?"
                q2 = "SELECT COUNT(*) FROM Products Where category_id = ?"
            elif subcategory_id:
                q1 = "SELECT * FROM Products Where subcategory_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?"
                q2 = "SELECT COUNT(*) FROM Products Where subcategory_id = ?"
            else:
                q1 = "SELECT * FROM Products ORDER BY created_at DESC LIMIT ? OFFSET ?"
                q2 = "SELECT COUNT(*) FROM Products"
        else:
            if category_id and subcategory_id:
                q1 = "SELECT * FROM Products Where category_id = ? AND subcategory_id = ? AND is_active = 1 ORDER BY created_at DESC LIMIT ? OFFSET ?"
                q2 = "SELECT COUNT(*) FROM Products Where category_id = ? AND subcategory_id = ? AND is_active = 1"
            elif category_id:
                q1 = "SELECT * FROM Products Where category_id = ? AND is_active = 1 ORDER BY created_at DESC LIMIT ? OFFSET ?"
                q2 = "SELECT COUNT(*) FROM Products Where category_id = ? AND is_active = 1"
            elif subcategory_id:
                q1 = "SELECT * FROM Products Where subcategory_id = ? AND is_active = 1 ORDER BY created_at DESC LIMIT ? OFFSET ?"
                q2 = "SELECT COUNT(*) FROM Products Where subcategory_id = ? AND is_active = 1"
            else:
                q1 = "SELECT * FROM Products Where is_active = 1 ORDER BY created_at DESC LIMIT ? OFFSET ?"
                q2 = "SELECT COUNT(*) FROM Products Where is_active = 1"
        
        if category_id and subcategory_id:
            cur.execute(q1, (category_id,subcategory_id,page_size, offset))
        elif category_id:
            cur.execute(q1, (category_id,page_size, offset))
        elif subcategory_id:
            cur.execute(q1, (subcategory_id,page_size, offset))
        else:
            cur.execute(q1, (page_size, offset))

        products = cur.fetchall()
        data['products'] = []
        if products:
            for p in products:
                data['products'].append({
                    "id":p[0],
                    "name":p[2],
                    "type":p[1],
                    "image":p[3],
                    "price":p[4],
                    "desc":p[5],
                    "created_at":p[6],
                    "is_active":p[7],
                    "price_gst_included":p[8],
                    "category_id":p[9],
                    "subcategory_id":p[10],
                    "qnt_unit":p[11]
                })
        if category_id and subcategory_id:
            cur.execute(q2, (category_id,subcategory_id))
        elif category_id:
            cur.execute(q2, (category_id,))
        elif subcategory_id:
            cur.execute(q2, (subcategory_id,))
        else:
            cur.execute(q2)
        data['total_products'] = cur.fetchone()[0]
    except Exception as e:
        print(e)
    finally:
        con.close()
        return data

def search_product(keyword:str,role:str='admin',category_id=None,subcategory_id=None):
    data={}
    con, cur = get_con_cursor()
    try:
        if role=='admin':
            if category_id and subcategory_id:
                q = """
                    SELECT * FROM Products 
                    WHERE name LIKE ? AND category_id = ? AND subcategory_id = ?
                """
            elif category_id:
                q = """
                    SELECT * FROM Products 
                    WHERE name LIKE ? AND category_id = ?
                """
            elif subcategory_id:
                q = """
                    SELECT * FROM Products 
                    WHERE name LIKE ? AND subcategory_id = ?
                """
            else:
                q = """
                    SELECT * FROM Products 
                    WHERE name LIKE ?
                """
        else:
            if category_id and subcategory_id:
                q = """
                    SELECT * FROM Products 
                    WHERE name LIKE ? AND is_active=1 AND category_id = ? AND subcategory_id = ?
                """
            elif category_id:
                q = """
                    SELECT * FROM Products 
                    WHERE name LIKE ? AND is_active=1 AND category_id = ?
                """
            elif subcategory_id:
                q = """
                    SELECT * FROM Products 
                    WHERE name LIKE ? AND is_active=1 AND subcategory_id = ?
                """
            else:
                q = """
                    SELECT * FROM Products 
                    WHERE name LIKE ? AND is_active=1
                """
        if category_id and subcategory_id:
            cur.execute(q, (f"%{keyword}%",category_id,subcategory_id))
        elif category_id:
            cur.execute(q, (f"%{keyword}%",category_id))
        elif subcategory_id:
            cur.execute(q, (f"%{keyword}%",subcategory_id))
        else:
            cur.execute(q, (f"%{keyword}%",))
        products = cur.fetchall()
        data['products'] = []
        if products:
            for p in products:
                data['products'].append({
                    "id":p[0],
                    "name":p[2],
                    "type":p[1],
                    "image":p[3],
                    "price":p[4],
                    "desc":p[5],
                    "created_at":p[6],
                    "is_active":p[7],
                    "price_gst_included":p[8],
                    "category_id":p[9],
                    "subcategory_id":p[10],
                    "qnt_unit":p[11]
                })
    except Exception as e:
        print(e)
    finally:
        con.close()
        return data

def get_product(p_id:str,role:str='admin'):
    con, cur = get_con_cursor()
    data={}
    try:
        if role=='admin':
            q = """SELECT 
                        p.id, p.type, p.name, p.image, p.price, p.desc, 
                        p.created_at, p.is_active, p.price_gst_included,
                        p.category_id, p.subcategory_id,
                        c.category_name AS category_name,
                        s.category_name AS subcategory_name,
                        p.qnt_unit AS qnt_unit
                    FROM Products p
                    JOIN ProductCategory c 
                        ON p.category_id = c.id 
                        AND c.parent_category_id IS NULL
                    LEFT JOIN ProductCategory s 
                        ON p.subcategory_id = s.id 
                        AND s.parent_category_id = p.category_id
                    WHERE p.id = ?;"""
        else:
            q = """SELECT 
                        p.id, p.type, p.name, p.image, p.price, p.desc, 
                        p.created_at, p.is_active, p.price_gst_included,
                        p.category_id, p.subcategory_id,
                        c.category_name AS category_name,
                        s.category_name AS subcategory_name,
                        p.qnt_unit AS qnt_unit
                    FROM Products p
                    JOIN ProductCategory c 
                        ON p.category_id = c.id 
                        AND c.parent_category_id IS NULL
                    LEFT JOIN ProductCategory s 
                        ON p.subcategory_id = s.id 
                        AND s.parent_category_id = p.category_id
                    WHERE p.id = ?;"""
        cur.execute(q, (p_id,))
        product = cur.fetchone()
        if product:
            data = {
                    "id":product[0],
                    "name":product[2],
                    "type":product[1],
                    "image":product[3],
                    "price":product[4],
                    "desc":product[5],
                    "created_at":product[6],
                    "is_active":product[7],
                    "price_gst_included":product[8],
                    "category_id":product[9],
                    "subcategory_id":product[10],
                    "category_name":product[11],
                    "subcategory_name":product[12],
                    "qnt_unit":product[13]
                }
    except Exception as e:
        print(e)
    finally:
        con.close()
        return data

def similar_products(p_id,p_name,p_type,offset,page_size,role:str='admin'):
    con, cur = get_con_cursor()
    data={}
    try:
        if role=='admin':
            q1 = "SELECT * FROM Products WHERE id != ? AND (name LIKE ? OR type LIKE ?) LIMIT ? OFFSET ?"
            q2 = "SELECT COUNT(*) FROM Products WHERE id != ? AND (name LIKE ? OR type LIKE ?)"
        else:
            q1 = "SELECT * FROM Products WHERE id != ? AND is_active=1 AND (name LIKE ? OR type LIKE ?) LIMIT ? OFFSET ?"
            q2 = "SELECT COUNT(*) FROM Products WHERE id != ? AND is_active=1 AND (name LIKE ? OR type LIKE ?)"
        
        cur.execute(q1, (p_id,f"%{p_name}%",p_type,page_size,offset))
        products = cur.fetchall()
        data['products'] = []
        if products:
            for p in products:
                data['products'].append({
                    "id":p[0],
                    "name":p[2],
                    "type":p[1],
                    "image":p[3],
                    "price":p[4],
                    "desc":p[5],
                    "created_at":p[6],
                    "is_active":p[7],
                    "price_gst_included":p[8],
                    "category_id":p[9],
                    "subcategory_id":p[10],
                    "qnt_unit":p[11]
                })
        cur.execute(q2,(p_id,f"%{p_name}%",f"%{p_type}%"))
        data['total_products'] = cur.fetchone()[0]
    except Exception as e:
        print(e)
    finally:
        con.close()
        return data

def create_product(product_id:str,name:str,image_name:str,price:float,types:str,desc:str,unit:str,category_id:str,subcategory_id:str):
    con, cur = get_con_cursor()
    try:
        q = """
                INSERT INTO Products (id, name, image, price, desc,type,category_id,subcategory_id,qnt_unit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        cur.execute(q, (product_id, name, image_name, price, desc, types,category_id,subcategory_id,unit))
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
    finally:
        con.close()

def update_product(product_id:str,name:str,image_name:str,price:float,types:str,desc:str,unit:str,visibilty):
    con, cur = get_con_cursor()
    try:
        q="Update Products Set name = ?, price = ?, image = ?, type = ?, desc = ?, is_active = ?, qnt_unit = ? Where id = ?"
        cur.execute(q,(name,price,image_name,types,desc,visibilty,unit,product_id))
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
    finally:
        con.close()

def delete_product(product_id:str):
    con, cur = get_con_cursor()
    try:
        q="Delete From Products Where id = ?"
        cur.execute(q,(product_id,))
        con.commit()
    except Exception as e:
        con.rollback()
        print(e)
    finally:
        con.close()

def get_category(id:str):
    con, cur = get_con_cursor()
    data={}
    try:
        q="""
            SELECT 
                main.id AS main_category_id,
                main.category_name AS main_category_name,
                sub.id AS subcategory_id,
                sub.category_name AS subcategory_name
            FROM ProductCategory AS main
            LEFT JOIN ProductCategory AS sub 
                ON main.id = sub.parent_category_id
            WHERE main.id = ? AND main.parent_category_id IS NULL
            ORDER BY main.category_name, sub.category_name;
        """
        cur.execute(q,(id,))
        category = cur.fetchone()
        if category:
            data['category']={
                "category_id" : category[0],
                "category_name" : category[1],
                "subcategory_id" : category[2],
                "subcategory_name" : category[3]
            }
    except Exception as e:
        print(e)
    finally:
        con.close()
        return data

def get_categories(sector_id=None,sector_name=None):
    con, cur = get_con_cursor()
    categories_map = {}
    
    try:

        if sector_name:
            q = "Select id From ProductSector Where sector_name like ?"
            cur.execute(q,(sector_name,))
            res = cur.fetchone()
            if not res:
                return []
            sector_id = res[0]

            q = """
            SELECT 
                main.id AS main_category_id,
                main.category_name AS main_category_name,
                sub.id AS subcategory_id,
                sub.category_name AS subcategory_name
            FROM ProductCategory AS main
            LEFT JOIN ProductCategory AS sub 
                ON main.id = sub.parent_category_id
            WHERE main.parent_category_id IS NULL AND main.sector_id = ?
            ORDER BY CAST(main.category_name AS INT) ASC;
            """
            cur.execute(q,(sector_id,))
        
        elif sector_id:
            q = """
            SELECT 
                main.id AS main_category_id,
                main.category_name AS main_category_name,
                sub.id AS subcategory_id,
                sub.category_name AS subcategory_name
            FROM ProductCategory AS main
            LEFT JOIN ProductCategory AS sub 
                ON main.id = sub.parent_category_id
            WHERE main.parent_category_id IS NULL AND main.sector_id = ?
            ORDER BY CAST(main.category_name AS INT) ASC;
            """
            cur.execute(q,(sector_id,))
        
        else:
            q = """
                SELECT 
                    main.id AS main_category_id,
                    main.category_name AS main_category_name,
                    sub.id AS subcategory_id,
                    sub.category_name AS subcategory_name
                FROM ProductCategory AS main
                LEFT JOIN ProductCategory AS sub 
                    ON main.id = sub.parent_category_id
                WHERE main.parent_category_id IS NULL
                ORDER BY CAST(main.category_name AS INT) ASC;
            """
            cur.execute(q)

        categories = cur.fetchall()

        for category in categories:
            category_id = category[0]
            category_name = category[1]
            subcategory_id = category[2]
            subcategory_name = category[3]

            # If category is not yet in the map, add it
            if category_id not in categories_map:
                categories_map[category_id] = {
                    "category_id": category_id,
                    "category_name": category_name,
                    "subcategories": []
                }

            # If there's a subcategory, add it to the subcategories list
            if subcategory_id:
                categories_map[category_id]["subcategories"].append({
                    "subcategory_id": subcategory_id,
                    "subcategory_name": subcategory_name
                })

    except Exception as e:
        print(e)
    finally:
        con.close()

    return list(categories_map.values())

def get_all_sectors():
    con, cur = get_con_cursor()
    data = []
    try:
        q= """
            Select * from ProductSector 
        """
        cur.execute(q)
        res = cur.fetchall()

        if res:
            for r in res:
                data.append({
                    "id":r[0],
                    "name":r[1]
                })
                
    except Exception as e:
        print(e)
    finally:
        con.close()
        return data