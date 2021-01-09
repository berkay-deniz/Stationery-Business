from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
import pyodbc

from wtforms import Form,StringField,TextAreaField,PasswordField,validators,IntegerField,DateField,SelectField
#LAPTOP-HCAE3FVL\MSSQLSERVER01;
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

def readProductType(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PRODUCT_TYPE')
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))
   
    return data
    
def readSupplier(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM SUPPLIER')
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))
   
    return data


class StaffForm(Form):
    tckn = StringField("TC Kimlik No",validators=[validators.length(min=11,max=11,message='Geçersiz TC kimlik no'), validators.DataRequired('Bu alan gerekli!')])
    fname = StringField('Ad', validators = [validators.length(max=25,message='Çok fazla karakter girdiniz!'), validators.DataRequired('Bu alan gerekli')])
    lname = StringField('Soyad', validators = [validators.length(max=25,message='Çok fazla karakter girdiniz!'), validators.DataRequired('Bu alan gerekli')])
    phoneNumber = StringField('Telefon Numarası', validators=[validators.length(min=10, max=10, message='Geçersiz Telefon Numarası')])
    address = StringField('Adres')
    bdate = StringField('Doğum Tarihi')
    wage = IntegerField('Maaş')
    rest = IntegerField('İzin günü')

class ProductForm(Form):
    types = []
    data = readProductType(conn)
    for row in data:
        types.append(row.get("TypeName")) 

    typeName = SelectField("Ürün çeşidi",choices=types)
    brand = StringField("Marka")
    purchasePrice = IntegerField("Alış fiyatı")
    salePrice = IntegerField("Satış fiyatı")
    stock = IntegerField("Stok")

class PurchaseReceiptForm(Form):
    suppliers = []
    data = readSupplier(conn)
    for row in data:
        suppliers.append(row.get("SupplierName")) 

    receiptNumber = StringField("Fatura numarası",validators=[validators.length(min = 8, max = 8, message="Fatura numarası 8 haneli olmalıdır")])
    supplierName = SelectField("Tedarikçi adı", choices=suppliers)
    date = StringField("Tarih")



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

def insertProduct(conn, productTypeId, brand, purchasePrice, salePrice, stock):
    cursor=conn.cursor()
    cursor.execute(
        'insert into PRODUCT (ProductTypeId, Brand, PurchasePrice, SalePrice, Stock) values(?,?,?,?,?)',
        (productTypeId, brand, purchasePrice, salePrice, stock)
    )
    conn.commit()
    print("inserted")

def insertPurchaseReceipt(conn, receiptNumber, supplierId, date):
    cursor=conn.cursor()
    cursor.execute(
        'insert into PURCHASE_RECEIPT (ReceiptNumber, SupplierId, Date) values(?,?,?)',
        (receiptNumber, supplierId, date)
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

@app.route("/product", methods=["GET","POST"])
def product():
    form = ProductForm(request.form)

    if request.method == "POST" and form.validate():
        typeName = form.typeName.data
        brand = form.brand.data
        purchasePrice = form.purchasePrice.data
        salePrice = form.salePrice.data
        stock = form.stock.data 
        
        data=readProductType(conn)
        for row in data:
            if row.get("TypeName") == typeName:
                productTypeId = row.get("id")
                break

        insertProduct(conn, productTypeId, brand, purchasePrice, salePrice, stock)
        return redirect("/")   
    else:
        return render_template("product.html", form = form)      

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

@app.route("/purchaseReceipt", methods=["GET","POST"])
def purchaseReceipt():
    form = PurchaseReceiptForm(request.form)

    if request.method == "POST" and form.validate():
        receiptNumber = form.receiptNumber.data
        supplierName = form.supplierName.data
        date = form.date.data
        
        data=readSupplier(conn)
        for row in data:
            if row.get("SupplierName") == supplierName:
                supplierId = row.get("id")
                break

        insertPurchaseReceipt(conn, receiptNumber, supplierId, date)
        return redirect("/")   
    else:
        return render_template("purchaseReceipt.html", form = form)


if __name__ ==  "__main__":
    app.run(debug=True)



#readProductType(conn)
#insertProductType(conn, "test 2")
#updateProductType(conn, 33, 'New Test')





conn.close()

