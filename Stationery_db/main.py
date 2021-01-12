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

    receiptNumber = StringField("Fatura Numarası", validators=[validators.length(
        min=8, max=8, message="Fatura Numarası 8 haneli olmalıdır")])
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
    productData=readProduct(conn)
    productTypeData = readProductType(conn)
    form = ProductForm(request.form)

    if request.method == "POST" and form.validate():
        typeName = form.typeName.data
        brand = form.brand.data
        purchasePrice = form.purchasePrice.data
        salePrice = form.salePrice.data
        stock = form.stock.data

        for row in productTypeData:
            if row.get("TypeName") == typeName:
                productTypeId = row.get("id")
                break

        insertProduct(conn, productTypeId, brand,
                      purchasePrice, salePrice, stock)
        return redirect("/product")
    else:
        productTypes = dict()
        for typeRow in productTypeData:
            productTypes[typeRow.get('id')] = typeRow.get('TypeName')
                

        return render_template("product.html", form=form,productData=productData, productTypes = productTypes)



@app.route("/salesReceipt", methods=["GET", "POST"])
def salesReceipt():
    form = salesReceiptForm(request.form)
    receiptData = readSalesReceipt(conn)
    customerData = readCustomer(conn)

    if request.method == "POST" and form.validate():
        receiptNumber = form.receiptNumber.data
        customerType = form.customerType.data
        firstName = form.firstName.data
        lastName = form.lastName.data
        companyName = form.companyName.data
        date = form.date.data

        customerData = readCustomer(conn)
        for row in customerData:

            if row.get("CustomerType") == 'Company' and row.get("CompanyName") == companyName:
                customerId = row.get("id")
                break
            elif row.get("CustomerType") == 'Person' and row.get("FirstName") == firstName:
                customerId = row.get("id")
                break
        insertSalesReceipt(conn, receiptNumber, customerId, date)
        return redirect("/")
    else:
        customersWithId = dict()
        for customer in customerData:
            if customer.get("CustomerType") == "Person":
                customersWithId[customer.get("id")] = "" + customer.get("FirstName") + " " + customer.get("LastName")
            else:
                customersWithId[customer.get("id")] = customer.get("CompanyName")
        return render_template("salesReceipt.html", form=form, receiptData = receiptData,customers = customersWithId )




@app.route("/supplier", methods=["GET", "POST"])
def supplier():
    supplierData=readSupplier(conn)
    form = SupplierForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        phoneNumber = form.phoneNumber.data
        address = form.address.data
        debt = form.debt.data
        insertSupplier(conn, name, phoneNumber, address, debt)
        return redirect("/supplier")
    else:
        return render_template("supplier.html", form=form,supplierData=supplierData)




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



@app.route("/purchaseReceipt/info/<int:id>", methods=["GET", "POST"])
def purchaseReceiptInfo(id):
    receiptData = readPurchaseReceipt(conn)
    form = PurchaseReceiptForm(request.form)


    if request.method == "POST" and form.validate():
        receiptNumber = form.receiptNumber.data
        date = form.date.data
        suppliers = readSupplier(conn)
        for supplier in suppliers:
            if supplier.get("SupplierName") == form.supplierName.data:
                supplierId = supplier.get("id")
                break
        updatePurchaseReceipt(conn, id, receiptNumber, supplierId, date)
        return redirect('/purchaseReceipt')
    else:
        for row in receiptData:
            if row.get("id") == id:
                receipt = row
                break
        suppliers = readSupplier(conn)
        for supplier in suppliers:
            if supplier.get("id") == receipt.get("SupplierId"):
                s = supplier
                break
        form.supplierName.data = s.get("SupplierName")
        form.receiptNumber.data = receipt.get("ReceiptNumber")
        form.date.data = receipt.get("Date")
        return render_template("purchaseReceiptInfo.html",form = form, receipt = receipt)



@app.route("/salesReceipt/info/<int:id>", methods=["GET", "POST"])
def salesReceiptInfo(id):
    receiptData = readSalesReceipt(conn)
    form = salesReceiptForm(request.form)

    if request.method == "POST" and form.validate():
        receiptNumber = form.receiptNumber.data
        customerType = form.customerType.data
        firstName = form.firstName.data
        lastName = form.lastName.data
        companyName = form.companyName.data
        date = form.date.data
        customers = readCustomer(conn)
        for customer in customers:
            if customerType == "Person" and customer.get("FirstName") == firstName and customer.get("LastName") == lastName:
                customerId = customer.get("id")
                break
            elif customerType == "Company" and customer.get("CompanyName") == companyName:
                customerId = customer.get("id")
                break
        updateSalesReceipt(conn, id, receiptNumber, customerId, date)
        return redirect('/salesReceipt')
    else:
        for row in receiptData:
            if row.get("id") == id:
                receipt = row
                break
        customers = readCustomer(conn)
        for customer in customers:
            if customer.get("id") == receipt.get("CustomerId"):
                c = customer
                break
        form.receiptNumber.data = receipt.get("ReceiptNumber")
        form.customerType.data = c.get("CustomerType")
        form.date.data = receipt.get("Date")
        if c.get("CustomerType") == "Person":
            form.companyName.data = None
            form.firstName.data = c.get("FirstName")
            form.lastName.data = c.get("LastName")
        else:
            form.firstName.data = None
            form.lastName.data = None
            form.companyName.data = c.get("CompanyName")
        return render_template("salesReceiptInfo.html",form = form, receipt = receipt)

@app.route("/supplier/info/<string:supplierId>", methods=["GET", "POST"])
def supplierInfo(supplierId):
    supplierData = readSupplier(conn)
    form = SupplierForm(request.form)
    id =int(supplierId)

    if request.method == "POST" and form.validate():
        name = form.name.data
        phone = form.phoneNumber.data
        address = form.address.data
        debt = form.debt.data
        updateSupplier(conn,id,name,phone,address,debt)
        return redirect('/supplier')
    else:
        for row in supplierData:
            if row.get("id") == id:
               supplier = row
               break
        form.name.data = supplier.get("SupplierName")
        form.phoneNumber.data = supplier.get("PhoneNumber")
        form.address.data = supplier.get("Address")
        form.debt.data = supplier.get("Debt")
        return render_template("supplierInfo.html",id=id, supplier = supplier, form = form)

#product
@app.route("/product/info/<string:productId>", methods=["GET", "POST"])
def productInfo(productId):
    productData = readProduct(conn)
    form = ProductForm(request.form)
    id =int(productId)
    if request.method == "POST" and form.validate():
        typeName = form.typeName.data
        brand = form.brand.data
        purchasePrice = form.purchasePrice.data
        salePrice = form.salePrice.data
        stock = form.stock.data
        typeId = readProductType(conn)
        for row in typeId:
            if row.get("TypeName") == typeName:
                productTypeId = row.get("id")
                break
        updateProduct(conn,id,productTypeId,brand,purchasePrice,salePrice,stock,)
        return redirect('/product')
    else:
        for row in productData:
            if row.get("id") == id:
               product = row
               break
        form.brand.data = product.get("Brand")
        form.purchasePrice.data = product.get("PurchasePrice")
        form.salePrice.data = product.get("SalePrice")
        form.stock.data = product.get("Stock")
        return render_template("productInfo.html",id=id, product = product, form = form)   



@app.route("/purchaseReceipt", methods=["GET", "POST"])
def purchaseReceipt():
    receiptData = readPurchaseReceipt(conn)
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
        return redirect("/purchaseReceipt")
    else:
        suppliersWithId = dict()
        supplierData = readSupplier(conn)
        for s in supplierData:
            suppliersWithId[s.get("id")] = s.get("SupplierName")
        return render_template("purchaseReceipt.html", form=form, receiptData = receiptData, suppliers = suppliersWithId)


@app.route('/deleteStaff/<int:id>', methods=['POST'])
def removeStaff(id):
    deleteStaff(conn,id)
    return redirect("/staff")

@app.route('/deleteSalesReceipt/<int:id>', methods=['POST'])
def removeSalesReceipt(id):
    deleteSalesReceipt(conn,id)
    return redirect("/salesReceipt")

@app.route('/deletePurchaseReceipt/<int:id>', methods=['POST'])
def removePurchaseReceipt(id):
    deletePurchaseReceipt(conn, id)
    return redirect("/purchaseReceipt")

@app.route('/deleteSupplier/<int:id>', methods=['POST'])
def removeSupplier(id):
    deleteSupplier(conn,id)
    return redirect("/supplier")

@app.route('/deleteProduct/<int:id>', methods=['POST'])
def removeProduct(id):
    deleteProduct(conn,id)
    return redirect("/product")



if __name__ == "__main__":
    app.run(debug=True)


conn.close()
