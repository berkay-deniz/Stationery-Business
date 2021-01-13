from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField, DateField, SelectField, FloatField
from SqlServerConnection import *

class SupplierForm(Form):
    name = StringField('Tedarikçi İsmi', validators=[validators.length(
        max=50, message='Çok fazla karakter girdiniz!'), validators.DataRequired('Bu alanı boş bırakamazsınız')])
    phoneNumber = StringField('Telefon Numarası', validators=[validators.length(
        min=10, max=10, message='Geçersiz Telefon Numarası')])
    address = StringField('Adres')
    debt = FloatField('Borç')

class StaffForm(Form):
    tckn = StringField("TC Kimlik No", validators=[validators.length(
        min=11, max=11, message='Geçersiz TC kimlik no'), validators.DataRequired('Bu alanı boş bırakamazsınız')])
    fname = StringField('Ad', validators=[validators.length(
        max=25, message='Çok fazla karakter girdiniz!'), validators.DataRequired('Bu alanı boş bırakamazsınız')])
    lname = StringField('Soyad', validators=[validators.length(
        max=25, message='Çok fazla karakter girdiniz!'), validators.DataRequired('Bu alanı boş bırakamazsınız')])
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
    brand = StringField("Marka", validators = [validators.length(max = 25, message = 'Marka ismi en fazla 25 karakter içermelidir' ),validators.DataRequired('Bu alanı boş bırakamazsınız')])
    purchasePrice = FloatField("Alış fiyatı", validators = [validators.DataRequired('Bu alanı boş bırakamazsınız')])
    salePrice = FloatField("Satış fiyatı", validators = [validators.DataRequired('Bu alanı boş bırakamazsınız')])
    stock = IntegerField("Stok", validators = [validators.DataRequired('Bu alanı boş bırakamazsınız')])

class ProductTypeForm(Form):
    typeName=StringField("Ürün türü",validators=[validators.length (max = 25, message = 'Ürün türü en fazla 25 karakter içermelidir'),validators.DataRequired("Bu alanı boş bırakamazsınız")])

class salesReceiptForm(Form):

    receiptNumber = StringField("Fatura Numarası")
    customerType = SelectField("Müşteri Türü", choices=[
                               ('Company'), ('Person')])
    firstName = StringField("Ad", validators=[validators.length(
        max=25, message='Çok fazla karakter girdiniz!')])
    lastName = StringField("Soyad", validators=[validators.length(
        max=25, message='Çok fazla karakter girdiniz!')])
    companyName = StringField("Şirket Adı", validators=[validators.length(
        max=50, message='Çok fazla karakter girdiniz!')])
    date = StringField("Tarih",validators = [validators.DataRequired('Bu alanı boş bırakamazsınız')])


class PurchaseReceiptForm(Form):
    suppliers = []
    data = readSupplier(conn)
    for row in data:
        suppliers.append(row.get("SupplierName"))

    receiptNumber = StringField("Fatura Numarası", validators=[validators.length(
        min=8, max=8, message="Fatura Numarası 8 haneli olmalıdır"), validators.DataRequired('Bu alanı boş bırakamazsınız')])
    supplierName = SelectField("Tedarikçi adı", choices=suppliers)
    date = StringField("Tarih",validators = [validators.DataRequired('Bu alanı boş bırakamazsınız')])

class ProductPurchaseReceiptForm(Form):
    products = []
    productTypes = []
    productData = readProduct(conn)
    productTypes = dict()
    ptData = readProductType(conn)
    for pt in ptData:
        productTypes[pt.get("id")] = pt.get("TypeName")
    for product in productData:
        products.append(productTypes[product.get("ProductTypeId")] + ", " + product.get("Brand"))
    product = SelectField("Ürün", choices=products)
    unitPrice = FloatField("Birim Fiyat",validators = [validators.DataRequired('Bu alanı boş bırakamazsınız')])
    amount = FloatField("Alım Miktarı",validators = [validators.DataRequired('Bu alanı boş bırakamazsınız')])

class ProductSalesReceiptForm(Form):
    products = []
    productData = readProduct(conn)
    productTypes = dict()
    ptData = readProductType(conn)
    for pt in ptData:
        productTypes[pt.get("id")] = pt.get("TypeName")
    for product in productData:
        products.append(productTypes[product.get("ProductTypeId")] + ", " + product.get("Brand"))
    
    product = SelectField("Ürün", choices=products)
    unitPrice = FloatField("Birim Fiyat",validators = [validators.DataRequired('Bu alanı boş bırakamazsınız')])
    amount = FloatField("Alım Miktarı",validators = [validators.DataRequired('Bu alanı boş bırakamazsınız')])


class PersonForm(Form):
    staff = readStaff(conn)
    staffNames = []
    staffNames.append(None)
    for s in staff:
        name = s.get("FirstName") + " " + s.get("LastName")
        staffNames.append(name)
    firstName = StringField("Müşteri Adı", validators=[validators.length(
        max=25, message='Müşteri Adı en fazla 25 karakter içermelidir!'),validators.DataRequired("Bu alanı boş bırakamazsınız")])
    lastName = StringField("Müşteri Soyadı", validators=[validators.length(
        max=25, message='Müşteri Soyadı en fazla 25 karakter içermelidir!'),validators.DataRequired("Bu alanı boş bırakamazsınız")])
    phone = StringField("Telefon Numarası",validators=[validators.length(
        min=10, max=10, message='Geçersiz Telefon Numarası')])
    address = StringField("Adres")
    receivable =StringField("Alacak")
    resStaff = SelectField("İlgilenen Çalışan", choices=staffNames)


class CompanyForm(Form):
    staff = readStaff(conn)
    staffNames = []
    staffNames.append(None)
    for s in staff:
        name = s.get("FirstName") + " " + s.get("LastName")
        staffNames.append(name)
    companyName = StringField("Şirket Adı", validators=[validators.length(
        max=50, message='Şirket Adı en fazla 50 karakter içermelidir!'),validators.DataRequired("Bu alanı boş bırakamazsınız")])
    taxNumber = StringField("Vergi Numarası",validators=[validators.length(
        min=8, max=8, message='Geçersiz Vergi Numarası'),validators.DataRequired("Bu alanı boş bırakamazsınız")])
    phone = StringField("Telefon Numarası",validators=[validators.length(
        min=10, max=10, message='Geçersiz Telefon Numarası')])
    address = StringField("Adres")
    receivable =StringField("Alacak")
    resStaff = SelectField("İlgilenen Çalışan", choices=staffNames)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/productType", methods=["GET", "POST"])
def productType():
    form = ProductTypeForm(request.form)
    productTypeData=readProductType(conn)
    if request.method == "POST" and form.validate():
        typeName = form.typeName.data

        insertProductType(conn,typeName)
        flash("Ürün çeşidi başarıyla eklendi!","success")
        return redirect("/productType")
    else:
        return render_template("productType.html", form=form,productTypeData=productTypeData)



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
        flash("Ürün başarıyla eklendi!","success")              
        return redirect("/product")
    else:
        productTypes = dict()
        for typeRow in productTypeData:
            productTypes[typeRow.get('id')] = typeRow.get('TypeName')
                

        return render_template("product.html", form=form,productData=productData, productTypes = productTypes)


@app.route("/person", methods=["GET", "POST"])
def person():
    customerData = readCustomer(conn)
    staffData = readStaff(conn)
    form = PersonForm(request.form)

    if request.method == "POST" and form.validate():
        firstName = form.firstName.data
        lastName = form.lastName.data
        phone = form.phone.data
        receivable = form.receivable.data
        address = form.address.data
        resStaffId=None
        for row in staffData:
            if row.get("FirstName") + " " + row.get("LastName") == form.resStaff.data:
                resStaffId = row.get("id")
                break

                    
        insertPersonCustomer(conn, firstName, lastName, phone, address, receivable, resStaffId )
        flash("Bireysel müşteri başarıyla eklendi!","success")
        return redirect("/person")

    else:
        personCustomers = []
        for customer in customerData:
            if customer.get("CustomerType") == "Person":
                personCustomers.append(customer)

        staffNames = dict()
        for staff in staffData:
            staffNames[staff.get("id")] = staff.get("FirstName") + " " + staff.get("LastName")


        return render_template("person.html", form=form, personData = personCustomers, staffNames = staffNames)



@app.route("/company", methods=["GET", "POST"])
def company():
    customerData = readCustomer(conn)
    staffData = readStaff(conn)
    form = CompanyForm(request.form)

    if request.method == "POST" and form.validate():
        companyName = form.companyName.data
        taxNumber = form.taxNumber.data
        phone = form.phone.data
        receivable = form.receivable.data
        address = form.address.data
        resStaffId=None
        for row in staffData:
            if row.get("FirstName") + " " + row.get("LastName") == form.resStaff.data:
                resStaffId = row.get("id")
                break

        insertCompanyCustomer(conn, companyName, taxNumber, phone, address, receivable, resStaffId )
        flash("Müşteri şirket başarıyla eklendi!","success")
        return redirect("/company")

    else:
        companyCustomers = []
        for customer in customerData:
            if customer.get("CustomerType") == "Company":
                companyCustomers.append(customer)

        staffNames = dict()
        for staff in staffData:
            staffNames[staff.get("id")] = staff.get("FirstName") + " " + staff.get("LastName")


        return render_template("company.html", form=form, companyData = companyCustomers, staffNames = staffNames)



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
        flash("Satış faturası başarıyla eklendi!","success")
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
        flash("Tedarikçi başarıyla eklendi!","success")
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
        flash("Personel başarıyla eklendi","success")            
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
        flash("Personel bilgileri başarıyla güncellendi!","success")           
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



@app.route("/person/info/<int:id>", methods=["GET", "POST"])
def personInfo(id):
    customerData = readCustomer(conn)
    staffData = readStaff(conn)
    form = PersonForm(request.form)

    if request.method == "POST" and form.validate():
        firstName = form.firstName.data
        lastName = form.lastName.data
        phone = form.phone.data
        receivable = form.receivable.data
        address = form.address.data
        resStaffId=None
        for row in staffData:
            if row.get("FirstName") + " " + row.get("LastName") == form.resStaff.data:
                resStaffId = row.get("id")
                break

        updatePersonCustomer(conn, id, firstName, lastName, phone, address, receivable, resStaffId)
        flash("Bireysel müşterinin bilgileri başarıyla güncellendi!","success")
        return redirect('/person')

    else:
        for row in customerData:
            if row.get("id") == id:
                customer = row
                break
        form.firstName.data = customer.get("FirstName")
        form.lastName.data = customer.get("LastName")
        form.phone.data = customer.get("PhoneNumber")
        form.address.data = customer.get("Address")
        form.receivable.data = customer.get("Receivable")
        form.resStaff.data=None
        for row in staffData:
            if row.get("id") == customer.get("ResponsibleStaffId"):
                staff = row
                break
        if form.resStaff.data is not None:    
            form.resStaff.data = staff.get("FirstName") + " " + staff.get("LastName")

        return render_template("personInfo.html",customer = customer, form = form)


@app.route("/company/info/<int:id>", methods=["GET", "POST"])
def companyInfo(id):
    customerData = readCustomer(conn)
    staffData = readStaff(conn)
    form = CompanyForm(request.form)

    if request.method == "POST" and form.validate():
        companyName = form.companyName.data
        taxNumber = form.taxNumber.data
        phone = form.phone.data
        receivable = form.receivable.data
        address = form.address.data
        resStaffId=None
        for row in staffData:
            if row.get("FirstName") + " " + row.get("LastName") == form.resStaff.data:
                resStaffId = row.get("id")
                break

        UpdateCompanyCustomer(conn, id, companyName, taxNumber, phone, address, receivable, resStaffId)
        flash("Müşteri şirketin bilgileri başarıyla güncellendi!","success")    
        return redirect('/company')

    else:
        for row in customerData:
            if row.get("id") == id:
                customer = row
                break
        form.companyName.data = customer.get("CompanyName")
        form.taxNumber.data = customer.get("TaxNumber")
        form.phone.data = customer.get("PhoneNumber")
        form.address.data = customer.get("Address")
        form.receivable.data = customer.get("Receivable")
        form.resStaff.data = None
        for row in staffData:
            if row.get("id") == customer.get("ResponsibleStaffId"):
                staff = row
                break
        if form.resStaff.data is not None:    
            form.resStaff.data = staff.get("FirstName") + " " + staff.get("LastName")

        return render_template("companyInfo.html",customer = customer, form = form)


@app.route("/purchaseReceipt/info/<int:id>", methods=["GET", "POST"])
def purchaseReceiptInfo(id):
    receiptData = readPurchaseReceipt(conn)
    form = PurchaseReceiptForm(request.form)
    formProduct = ProductPurchaseReceiptForm(request.form)
    prp = readPurchaseReceiptProduct(conn)
    
    if request.method == "POST" and form.validate():
        receiptNumber = form.receiptNumber.data
        date = form.date.data
        suppliers = readSupplier(conn)
        for supplier in suppliers:
            if supplier.get("SupplierName") == form.supplierName.data:
                supplierId = supplier.get("id")
                break
        updatePurchaseReceipt(conn, id, receiptNumber, supplierId, date)
        flash("Alış faturası başarıyla güncellendi!","success")
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

        products = dict()
        productParts = []
        productTypes = dict()
        ptData = readProductType(conn)
        for pt in ptData:
            productTypes[pt.get("id")] = pt.get("TypeName")
        for product in productData:
            products[product.get("id")] = productTypes[product.get("ProductTypeId")] + " (" + product.get("Brand") + ")" 
        for productPart in prp:
            if productPart.get("ReceiptId") == receipt.get("id"):
                productParts.append(productPart)
            
        return render_template("purchaseReceiptInfo.html",formProduct = formProduct, form = form, receipt = receipt, products = products, productParts = productParts)



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
        flash("Satış faturası başarıyla güncellendi!","success")
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
        flash("Tedarikçi bilgileri başarıyla güncellendi!","success")
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
        flash("Ürün bilgileri başarıyla güncellendi!","success")
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

@app.route("/productType/info/<string:productTypeId>", methods=["GET", "POST"])
def productTypeInfo(productTypeId):
    productTypeData = readProductType(conn)
    form = ProductTypeForm(request.form)
    id =int(productTypeId)

    if request.method == "POST" and form.validate():
        typeName = form.typeName.data

        updateProductType(conn,id,typeName)
        flash("Ürün çeşidi başarıyla güncellendi!","success")
        return redirect('/productType')
    else:
        for row in productTypeData:
            if row.get("id") == id:
               productType = row
               break
        form.typeName.data = productType.get("TypeName")
        return render_template("productTypeInfo.html",id=id, productType = productType, form = form)


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
        flash("Alış faturası başarıyla eklendi!","success")
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
    flash("Personel silindi!","success")
    return redirect("/staff")


@app.route('/deletePerson/<int:id>', methods=['POST'])
def removePerson(id):
    deletePerson(conn,id)
    flash("Kişisel müşteri silindi!","success")
    return redirect("/person")


@app.route('/deleteCompany/<int:id>', methods=['POST'])
def removeCompany(id):
    deleteCompany(conn,id)
    flash("Müşteri şirket silindi!","success")
    return redirect("/company")

@app.route('/deleteSalesReceipt/<int:id>', methods=['POST'])
def removeSalesReceipt(id):
    deleteSalesReceipt(conn,id)
    flash("Satış faturası silindi!","success")
    return redirect("/salesReceipt")

@app.route('/deletePurchaseReceipt/<int:id>', methods=['POST'])
def removePurchaseReceipt(id):
    deletePurchaseReceipt(conn, id)
    flash("Alış faturası silindi!","success")
    return redirect("/purchaseReceipt")

@app.route('/deleteSupplier/<int:id>', methods=['POST'])
def removeSupplier(id):
    deleteSupplier(conn,id)
    flash("Tedarikçi silindi!","success")
    return redirect("/supplier")

@app.route('/deleteProduct/<int:id>', methods=['POST'])
def removeProduct(id):
    deleteProduct(conn,id)
    flash("Ürün silindi!","success")
    return redirect("/product")

@app.route('/deleteProductType/<int:id>', methods=['POST'])
def removeProductType(id):
    deleteProductType(conn,id)
    flash("Ürün çeşidi silindi!","success")
    return redirect("/productType")

@app.route('/addProductToPurchaseReceipt/<int:id>', methods=['POST'])
def addProductToPurchaseReceipt(id):
    
    form = ProductPurchaseReceiptForm(request.form)
    unitPrice = form.unitPrice.data
    amount = form.amount.data
    productFullName = form.product.data.split(", ")
    typeName = productFullName[0]
    brand = productFullName[1]
    ptData = readProductType(conn)
    for pt in ptData:
        if pt.get("TypeName") == typeName:
            typeId = pt.get("id")
            break
    productData = readProduct(conn)
    for prod in productData:
        if prod.get("ProductTypeId") == typeId and prod.get("Brand") == brand:
            productId = prod.get("id")
            break
    
    insertPurchaseReceiptProduct(conn, id, productId, unitPrice, amount)
    flash("Ürün alış faturası eklendi!","success")

    return redirect(url_for('purchaseReceiptInfo', id=id))


if __name__ == "__main__":
    app.run(debug=True)


conn.close()
