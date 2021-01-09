from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
import pyodbc
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,IntegerField,DateField
#VG DESKTOP-CPMCPBA
#AFY DESKTOP-ISHU912
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=DESKTOP-CPMCPBA;"
    "Database=STATIONERY_BUSINESS;"
    "Trusted_Connection=yes;"
)

class SupplierForm(Form):
    name = StringField('Tedarikçi İsmi',validators = [validators.length(max=50,message='Çok fazla karakter girdiniz!'), validators.DataRequired('Bu alan gerekli')])
    phoneNumber = StringField('Telefon Numarası', validators=[validators.length(min=10, max=10,message='Geçersiz Telefon Numarası')])
    address = StringField('Adres')
    debt = IntegerField('Borç')


class StaffForm(Form):
    tckn = StringField("TC Kimlik No",validators=[validators.length(min=11,max=11,message='Geçersiz TC kimlik no'), validators.DataRequired('Bu alan gerekli!')])
    fname = StringField('Ad', validators = [validators.length(max=25,message='Çok fazla karakter girdiniz!'), validators.DataRequired('Bu alan gerekli')])
    lname = StringField('Soyad', validators = [validators.length(max=25,message='Çok fazla karakter girdiniz!'), validators.DataRequired('Bu alan gerekli')])
    phoneNumber = StringField('Telefon Numarası', validators=[validators.length(min=10, max=10, message='Geçersiz Telefon Numarası')])
    address = StringField('Adres')
    bdate = StringField('Doğum Tarihi')
    wage = IntegerField('Maaş')
    rest = IntegerField('İzin günü')


def readProductType(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PRODUCT_TYPE')
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))
   
    return data
    

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


def insertStaff(conn, tckn, fname, lname, phone, address, bdate, wage, rest):
    cursor=conn.cursor()
    cursor.execute(
        'insert into STAFF (Tckn, FirstName, LastName, PhoneNumber, Address, BirthDate, Wage, DaysOfRest) values (?,?,?,?,?,?,?,?)',
        (tckn, fname, lname, phone, address, bdate, wage, rest)
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

@app.route("/staff", methods=["GET","POST"])
def staff():
    form = StaffForm(request.form)

    if request.method == "POST" and form.validate():
        tckn = form.tckn.data
        fname = form.fname.data
        lname = form.lname.data
        phone = form.phoneNumber.data
        address = form.address.data
        bdate = form.bdate.data
        wage = form.wage.data
        rest = form.rest.data
        insertStaff(conn, tckn, fname, lname, phone, address, bdate, wage, rest)
        return redirect('/')

    else:
        return render_template("staff.html",form = form)

if __name__ ==  "__main__":
    app.run(debug=True)



#readProductType(conn)
#insertProductType(conn, "test 2")
#updateProductType(conn, 33, 'New Test')





conn.close()

