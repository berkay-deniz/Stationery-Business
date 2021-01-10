from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField, DateField, SelectField, FloatField
from SqlServerConnection import *

class SupplierForm(Form):
    name = StringField('Tedarikçi İsmi', validators=[validators.length(
        max=50, message='Çok fazla karakter girdiniz!'), validators.DataRequired('Bu alan gerekli')])
    phoneNumber = StringField('Telefon Numarası', validators=[validators.length(
        min=10, max=10, message='Geçersiz Telefon Numarası')])
    address = StringField('Adres')
    debt = FloatField('Borç')

class StaffForm(Form):
    tckn = StringField("TC Kimlik No", validators=[validators.length(
        min=11, max=11, message='Geçersiz TC kimlik no'), validators.DataRequired('Bu alan gerekli!')])
    fname = StringField('Ad', validators=[validators.length(
        max=25, message='Çok fazla karakter girdiniz!'), validators.DataRequired('Bu alan gerekli')])
    lname = StringField('Soyad', validators=[validators.length(
        max=25, message='Çok fazla karakter girdiniz!'), validators.DataRequired('Bu alan gerekli')])
    phoneNumber = StringField('Telefon Numarası', validators=[validators.length(
        min=10, max=10, message='Geçersiz Telefon Numarası')])
    address = StringField('Adres')
    bdate = StringField('Doğum Tarihi')
    wage = FloatField('Maaş')
    rest = IntegerField('İzin günü')


class ProductForm(Form):
    types = []
    data = readProductType(conn)
    for row in data:
        types.append(row.get("TypeName"))

    typeName = SelectField("Ürün çeşidi", choices=types)
    brand = StringField("Marka")
    purchasePrice = FloatField("Alış fiyatı")
    salePrice = FloatField("Satış fiyatı")
    stock = IntegerField("Stok")

class ProductTypeForm(Form):
    typeName=StringField("Ürün türü",validators=[validators.DataRequired("Bu alan gerekli")])

class salesReceiptForm(Form):

    receiptNumber = StringField("Fatura Numarası")
    customerType = SelectField("Müşteri Türü", choices=[
                               ('Company'), ('Person')])
    firstName = StringField("Ad")
    lastName = StringField("Soyad")
    companyName = StringField("Şirket Adı")
    date = StringField("Tarih")


class PurchaseReceiptForm(Form):
    suppliers = []
    data = readSupplier(conn)
    for row in data:
        suppliers.append(row.get("SupplierName"))

    receiptNumber = StringField("Fatura numarası", validators=[validators.length(
        min=8, max=8, message="Fatura numarası 8 haneli olmalıdır")])
    supplierName = SelectField("Tedarikçi adı", choices=suppliers)
    date = StringField("Tarih")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/productType", methods=["GET", "POST"])
def productType():
    form = ProductTypeForm(request.form)

    if request.method == "POST" and form.validate():
        typeName = form.typeName.data

        insertProductType(conn,typeName)
        return redirect("/")
    else:
        return render_template("product type.html", form=form)



@app.route("/product", methods=["GET", "POST"])
def product():
    form = ProductForm(request.form)

    if request.method == "POST" and form.validate():
        typeName = form.typeName.data
        brand = form.brand.data
        purchasePrice = form.purchasePrice.data
        salePrice = form.salePrice.data
        stock = form.stock.data

        data = readProductType(conn)
        for row in data:
            if row.get("TypeName") == typeName:
                productTypeId = row.get("id")
                break

        insertProduct(conn, productTypeId, brand,
                      purchasePrice, salePrice, stock)
        return redirect("/")
    else:
        return render_template("product.html", form=form)



@app.route("/salesReceipt", methods=["GET", "POST"])
def salesReceipt():
    form = salesReceiptForm(request.form)

    if request.method == "POST" and form.validate():
        receiptNumber = form.receiptNumber.data
        customerType = form.customerType.data
        firstName = form.firstName.data
        lastName = form.lastName.data
        companyName = form.companyName.data
        date = form.date.data

        data = readCustomer(conn)
        for row in data:

            if row.get("CustomerType") == 'Company' and row.get("CompanyName") == companyName:
                customerId = row.get("id")
                break
            elif row.get("CustomerType") == 'Person' and row.get("FirstName") == firstName:
                customerId = row.get("id")
                break
        insertSalesReceipt(conn, receiptNumber, customerId, date)
        return redirect("/")
    else:
        return render_template("sales receipt.html", form=form)




@app.route("/supplier", methods=["GET", "POST"])
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
        return render_template("supplier.html", form=form)




@app.route("/staff", methods=["GET", "POST"])
def staff():
    staffData = readStaff(conn)
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
        insertStaff(conn, tckn, fname, lname, phone,
                    address, bdate, wage, rest)
        return redirect('/staff')

    else:
        return render_template("staff.html", form=form, staffData=staffData)

@app.route("/staff/info/<string:staffId>", methods=["GET", "POST"])
def staffInfo(staffId):
    staffData = readStaff(conn)
    form = StaffForm(request.form)
    id =int(staffId)

    if request.method == "POST" and form.validate():
        tckn = form.tckn.data
        fname = form.fname.data
        lname = form.lname.data
        phone = form.phoneNumber.data
        address = form.address.data
        bdate = form.bdate.data
        wage = form.wage.data
        rest = form.rest.data
        updateStaff(conn,id, tckn, fname, lname, phone,
                    address, bdate, wage, rest)
        return redirect('/staff')
    else:
        for row in staffData:
            if row.get("id") == id:
                staff = row
                break
        form.tckn.data = staff.get("Tckn")
        form.fname.data = staff.get("FirstName")
        form.lname.data = staff.get("LastName")
        form.phoneNumber.data = staff.get("PhoneNumber")
        form.address.data = staff.get("Address")
        form.bdate.data = staff.get("BirthDate")
        form.wage.data = staff.get("Wage")
        form.rest.data = staff.get("DaysOfRest")
        return render_template("staffInfo.html",id=id, staff = staff, form = form)

    


@app.route("/purchaseReceipt", methods=["GET", "POST"])
def purchaseReceipt():
    form = PurchaseReceiptForm(request.form)

    if request.method == "POST" and form.validate():
        receiptNumber = form.receiptNumber.data
        supplierName = form.supplierName.data
        date = form.date.data

        data = readSupplier(conn)
        for row in data:
            if row.get("SupplierName") == supplierName:
                supplierId = row.get("id")
                break

        insertPurchaseReceipt(conn, receiptNumber, supplierId, date)
        return redirect("/")
    else:
        return render_template("purchaseReceipt.html", form=form)


@app.route('/deleteStaff/<int:id>', methods=['POST'])
def removeStaff(id):
    deleteStaff(conn,id)
    return redirect("/staff")


if __name__ == "__main__":
    app.run(debug=True)


conn.close()
