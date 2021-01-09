from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
import pyodbc
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,IntegerField

conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=LAPTOP-HCAE3FVL\MSSQLSERVER01;"
    "Database=STATIONERY_BUSINESS;"
    "Trusted_Connection=yes;"
)

class SupplierForm(Form):
    name = StringField('Tedarikçi İsmi',validators = [validators.length(max=50,message='Çok fazla karakter girdiniz!'), validators.DataRequired('Bu alan gerekli')])
    phoneNumber = IntegerField('Telefon Numarası')
    address = StringField('Adres')
    debt = IntegerField('Borç')

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


def insertSupplier(conn, name, phone, address, debt):
    cursor=conn.cursor()
    cursor.execute(
        'insert into SUPPLIER (SupplierName, PhoneNumber, Address, Debt) values (?,?,?,?)',
        (name, phone, address, debt)
    )
    conn.commit()
    print("Inserted")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/supplier", methods=["GET","POST"])
def supplier():
    form = SupplierForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        phoneNumber = form.phoneNumber.data
        address = form.address.data
        debt = form.debt.data
        insertSupplier(conn, name, phoneNumber, address, debt)
        return redirect("/")
    else:
        return render_template("supplier.html",form = form)

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

