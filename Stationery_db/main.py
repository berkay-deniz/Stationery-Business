from flask import Flask,render_template
import pyodbc

conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=LAPTOP-HCAE3FVL\MSSQLSERVER01;"
    "Database=STATIONERY_BUSINESS;"
    "Trusted_Connection=yes;"
)

def readProductType(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PRODUCT_TYPE')
    for row in cursor:
        print(f'{row}')
    

def insertProductType(conn, product_type):
    cursor=conn.cursor()
    cursor.execute(
        'insert into PRODUCT_TYPE (TypeName) values (?)',
        (product_type)
    )
    conn.commit()
    print("Inserted")


def updateProductType(conn, id, type_name):
    cursor=conn.cursor()
    cursor.execute(
        'Update PRODUCT_TYPE set TypeName = ? Where id = ?',(type_name,id)
    )
    conn.commit()
    print('Updated')



app = Flask(__name__)

@app.route("/")
def index():
    #readProductType(conn)
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/about/afy")
def afy():
    return "AFY hakkında"

@app.route("/about/VG")
def VG():
    return "VG hakkında"

if __name__ ==  "__main__":
    app.run(debug=True)



#readProductType(conn)
#insertProductType(conn, "test 2")
#updateProductType(conn, 33, 'New Test')





conn.close()

