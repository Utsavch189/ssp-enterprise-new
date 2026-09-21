import sys,os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db import get_con_cursor

def create_user_table():
    con,cur=get_con_cursor()
    try:
        q="""
            Create table if not exists Users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        """
        cur.execute(q)
        con.commit()
    except Exception as e:
        con.rollback()
        print(f"create_user_table() | {str(e)}")

def create_session_table():
    con,cur=get_con_cursor()
    try:
        q="""
            Create table if not exists SessionToken(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token VARCHAR(255) unique NOT NULL,
                user_id INTEGER NOT NULL,
                role VARCHAR(255) NOT NULL,
                expires_at DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        cur.execute(q)
        con.commit()
    except Exception as e:
        con.rollback()
        print(f"create_session_table() | {str(e)}")

def create_product_table():
    con,cur=get_con_cursor()
    try:
        q="""
            Create table if not exists Products(
                id VARCHAR(255) PRIMARY KEY,
                type VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                image VARCHAR(255),
                price DECIMAL(10, 2) NOT NULL,
                desc TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                price_gst_included BOOLEAN DEFAULT FALSE,
                category_id VARCHAR(255) NOT NULL,
                subcategory_id VARCHAR(255),
                qnt_unit VARCHAR(255) NOT NULL
            )
        """
        cur.execute(q)
        con.commit()
    except Exception as e:
        con.rollback()
        print(f"create_product_table() | {str(e)}")

def create_sector_table():
    con, cur = get_con_cursor()
    try:
        q = """
            CREATE TABLE IF NOT EXISTS ProductSector (
                id VARCHAR(255) PRIMARY KEY,
                sector_name VARCHAR(255) NOT NULL UNIQUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        """
        cur.execute(q)
        con.commit()
    except Exception as e:
        con.rollback()
        print(f"create_sector_table() | {str(e)}")

def create_category_table():
    con, cur = get_con_cursor()
    try:
        q = """
            CREATE TABLE IF NOT EXISTS ProductCategory (
                id VARCHAR(255) PRIMARY KEY,
                category_name VARCHAR(255) NOT NULL UNIQUE,
                parent_category_id VARCHAR(255) DEFAULT NULL,
                sector_id VARCHAR(255),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (parent_category_id) REFERENCES ProductCategory(id) ON DELETE CASCADE,
                FOREIGN KEY (sector_id) REFERENCES ProductSector(id) ON DELETE CASCADE
            )
        """
        cur.execute(q)
        con.commit()
    except Exception as e:
        con.rollback()
        print(f"create_category_table() | {str(e)}")

def create_contact_hist_table():
    con,cur=get_con_cursor()
    try:
        q="""
            Create table if not exists ContactHistory(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                subject VARCHAR(255) NOT NULL,
                sender_email VARCHAR(255) NOT NULL,
                receiver_email VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        cur.execute(q)
        con.commit()
    except Exception as e:
        con.rollback()
        print(f"create_contact_hist_table() | {str(e)}")

def create_userquery_hist_table():
    con,cur=get_con_cursor()
    try:
        q="""
            Create table if not exists UserQuery(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                subject VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(15) NOT NULL,
                message TEXT NOT NULL,
                gst_no VARCHAR(50),
                referral_mobile VARCHAR(15),
                file VARCHAR(255),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        cur.execute(q)
        con.commit()
    except Exception as e:
        con.rollback()
        print(f"create_userquery_hist_table() | {str(e)}")

def create_tables():
    create_user_table()
    create_session_table()
    create_product_table()
    create_sector_table()
    create_category_table()
    create_contact_hist_table()
    create_userquery_hist_table()


if __name__=="__main__":
    create_tables()