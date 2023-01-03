import mysql.connector
import json
import requests
import time
from datetime import date
from datetime import timedelta

def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='mars')
    return conn
def create_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS mars (id INT PRIMARY KEY auto_increment,photo_id varchar(3000), url varchar(3000), date DATE); ''')
    return
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor
def add_new_picture(cursor, mars):
    # extract all required columns
    photo_id_num = mars['id']
    img_src = mars['img_src']
    date = mars["earth_date"]
    query = cursor.execute("INSERT INTO mars( photo_id, url, date) VALUES(%s,%s,%s)", (photo_id_num, img_src, date))
    # https://stackoverflow.com/questions/20818155/not-all-parameters-were-used-in-the-sql-statement-python-mysql/20818201#20818201
    return query_sql(cursor, query)
def check_if_picture_exists(cursor, mars):
    photo_id = mars['id']
    query = "SELECT * FROM mars WHERE photo_id = \"%s\"" % photo_id
    return query_sql(cursor, query)
def delete_picture(cursor, mars):
    photo_id = mars['id']
    query = "DELETE * FROM mars WHERE photo_id = \"%s\"" % photo_id
    return query_sql(cursor, query)
def fetch_new_pictures():
    today = date.today()
    threedays = today - timedelta(days=3)
    params = {"earth_date": threedays, "api_key": "ekzhH2EN2c076XH54seXButHeyXM8MPAMXj2NahP"}
    f = r"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?"
    data = requests.get(f, params=params)
    a = json.loads(data.text)

    return a['photos']

def picturehunt(cursor):
    marspage = fetch_new_pictures()
    add_or_delete_picture( marspage, cursor)
def add_or_delete_picture( marspage, cursor):
    # Add your code here to parse the job page
    for mars in  marspage:  # EXTRACTS EACH Player from list
        # Add in your code here to check if the player already exists in the DB
        check_if_picture_exists(cursor, mars)
        is_picture_found = len(cursor.fetchall()) > 0  # https://stackoverflow.com/questions/2511679/python-number-of-rows-affected-by-cursor-executeselect
        if is_picture_found:
            print("Picture is found: " + mars['img_src'])
        else:
            print("Picture is found: " + mars['img_src'])
            add_new_picture(cursor, mars)
def main():
    # Important, rest are supporting functions
    # Connect to SQL and get cursor
    conn = connect_to_sql()
    cursor = conn.cursor()
    create_tables(cursor)

    # Load text file and store arguments into dictionary
    while(1):  # Infinite Loops. Only way to kill it is to crash or manually crash it. We did this as a background process/passive scraper
        picturehunt( cursor)  # arg_dict is argument dictionary,
        time.sleep(3600)  # Sleep for 1h, this is ran every hour because API or web interfaces have request limits. Your reqest will get blocked.
# Sleep does a rough cycle count, system is not entirely accurate
# If you want to test if script works change time.sleep() to 10 seconds and delete your table in MySQL
if __name__ == '__main__':
    main()