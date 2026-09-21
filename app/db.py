import sqlite3

# import mysql.connector

# def get_con_cursor_mysql():
#     connection = mysql.connector.connect(
#         host="37.27.71.198",
#         user="oblkniia_ssp",
#         password="ssp@2025",
#         database="oblkniia_sspdb"
#     )
#     cursor = connection.cursor()
#     return connection, cursor


def get_con_cursor_sqllite():
    connection = sqlite3.connect('ssp_enterprise.db')
    cusror = connection.cursor()
    return connection,cusror

def get_con_cursor():
    try:
        return get_con_cursor_sqllite()
    except Exception as e:
        print(e)
        return None,None