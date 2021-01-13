import pyodbc
# Server Owner           Server Name
# -----------------------------------------------------
# Berkay DENİZ           LAPTOP-HCAE3FVL\MSSQLSERVER01;
# Vahap GÖZENELİOĞLU     DESKTOP-CPMCPBA
# Ahmet Faruk YILMAZ     DESKTOP-ISHU912
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=LAPTOP-HCAE3FVL\MSSQLSERVER01;"
    "Database=STATIONERY_BUSINESS;"
    "Trusted_Connection=yes;"
)

def readSalesReceipt(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM SALES_RECEIPT')
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))

    return data


def readPurchaseReceipt(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PURCHASE_RECEIPT')
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))

    return data


def readProductType(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PRODUCT_TYPE')
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))

    return data


def readCustomer(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM CUSTOMER')
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))

    return data

def readProduct(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PRODUCT')
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


def readStaff(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM STAFF')
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))

    return data

def readPurchaseReceiptProduct(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PURCHASE_RECEIPT_PRODUCT')
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))

    return data

def readSalesReceiptProduct(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM SALES_RECEIPT_PRODUCT')
    columns = [column[0] for column in cursor.description]
    data = []
    for row in cursor.fetchall():
        data.append(dict(zip(columns, row)))

    return data


def insertSalesReceipt(conn, receiptNumber, customerId, date):
    cursor = conn.cursor()
    cursor.execute(
        'exec dbo.createSaleReceipt ?,?,?',
        (receiptNumber, customerId, date)

    )
    conn.commit()
    print("Sale receipt created")


def insertPurchaseReceipt(conn, receiptNumber, supplierId, date):
    cursor = conn.cursor()
    cursor.execute(
        'exec dbo.createPurchaseReceipt ?,?,?',
        (receiptNumber, supplierId, date)
    )
    conn.commit()
    print("Inserted")


def insertProductType(conn, product_type):
    cursor = conn.cursor()
    cursor.execute(
        'insert into PRODUCT_TYPE (TypeName) values (?)',
        (product_type)
    )
    conn.commit()
    print("Inserted")


def insertSupplier(conn, name, phone, address, debt):
    cursor = conn.cursor()
    cursor.execute(
        'exec dbo.addSupplier ?,?,?,?',
        (name, phone, address, debt)
    )
    conn.commit()
    print("Inserted")



def insertPersonCustomer(conn, firstName, lastName, phone, address, receivable, resStaffId):
    cursor = conn.cursor()
    cursor.execute(
        'insert into Customer (CustomerType, FirstName, LastName, PhoneNumber, Address, Receivable, ResponsibleStaffId) values (?,?,?,?,?,?,?)',
        ("Person",firstName, lastName, phone, address, receivable, resStaffId)
    )
    conn.commit()
    print("Inserted")


def insertCompanyCustomer(conn, companyName, taxNumber, phone, address, receivable, resStaffId):
    cursor = conn.cursor()
    cursor.execute(
        'insert into Customer (CustomerType, CompanyName, TaxNumber, PhoneNumber, Address, Receivable, ResponsibleStaffId) values (?,?,?,?,?,?,?)',
        ("Company", companyName, taxNumber, phone, address, receivable, resStaffId)
    )
    conn.commit()
    print("Inserted")


def insertStaff(conn, tckn, fname, lname, phone, address, bdate, wage, rest):
    cursor = conn.cursor()
    cursor.execute(
        'insert into STAFF (Tckn, FirstName, LastName, PhoneNumber, Address, BirthDate, Wage, DaysOfRest) values (?,?,?,?,?,?,?,?)',
        (tckn, fname, lname, phone, address, bdate, wage, rest)
    )
    conn.commit()
    print("Inserted")


def insertProduct(conn, productTypeId, brand, purchasePrice, salePrice, stock):
    cursor = conn.cursor()
    cursor.execute(
        'insert into PRODUCT (ProductTypeId, Brand, PurchasePrice, SalePrice, Stock) values(?,?,?,?,?)',
        (productTypeId, brand, purchasePrice, salePrice, stock)
    )
    conn.commit()
    print("inserted")



def insertPurchaseReceiptProduct(conn, ReceiptId, ProductId, PurchaseUnitPrice, PurchaseAmount):
    cursor = conn.cursor()
    cursor.execute(
        'insert into PURCHASE_RECEIPT_PRODUCT (ReceiptId, ProductId, PurchaseUnitPrice, PurchaseAmount) values(?, ?, ?, ?)',
        (ReceiptId, ProductId, PurchaseUnitPrice, PurchaseAmount)
    )
    conn.commit()
    print("inserted")



def insertSalesReceiptProduct(conn, ReceiptId, ProductId, SaleUnitPrice, SaleAmount):
    cursor = conn.cursor()
    cursor.execute(
        'insert into SALES_RECEIPT_PRODUCT (ReceiptId, ProductId, SaleUnitPrice, SaleAmount) values(?, ?, ?, ?)',
        (ReceiptId, ProductId, SaleUnitPrice, SaleAmount)
    )
    conn.commit()
    print("inserted")


def updateProductType(conn, id, type_name):
    cursor = conn.cursor()
    cursor.execute(
        'Update PRODUCT_TYPE set TypeName = ? Where id = ?', (type_name, id)
    )
    conn.commit()
    print('Updated')


def updateStaff(conn, id, tckn, fname, lname, phone,
                address, bdate, wage, rest):
    cursor = conn.cursor()
    cursor.execute(
        '''Update STAFF set 
                         Tckn = ?,
                         FirstName = ?,
                         LastName = ?,
                         PhoneNumber = ?,
                         Address = ?,
                         Birthdate = ?,
                         Wage = ?,
                         DaysOfRest = ?
                         Where id = ?''',
        (tckn, fname, lname, phone,
         address, bdate, wage, rest, id)
    )
    conn.commit()
    print('Updated')

def updateSupplier(conn, id, supplierName, phoneNumber, address, debt):

    cursor = conn.cursor()
    cursor.execute(

        'Update SUPPLIER Set supplierName = ? , phoneNumber=?,address=?,debt= ? where id = ? ', (
            supplierName, phoneNumber, address, debt, id)

    )

    conn.commit()
    print("Updated")



def updateProduct(conn, id,ProductTypeId,Brand,PurchasePrice,SalePrice,Stock):

    cursor = conn.cursor()
    cursor.execute(

        'Update PRODUCT Set ProductTypeId = ? , Brand=?,PurchasePrice=?,SalePrice= ?,Stock= ?  where id = ? ', (
            ProductTypeId, Brand, PurchasePrice, SalePrice,Stock, id)

    )

    conn.commit()
    print("Updated")    

def updatePurchaseReceipt(conn, id, ReceiptNumber, SupplierId, Date):

    cursor = conn.cursor()
    cursor.execute(

        'Update PURCHASE_RECEIPT Set ReceiptNumber = ?, SupplierId = ?, Date = ? where id = ? ', (
            ReceiptNumber, SupplierId, Date, id)

    )

    conn.commit()
    print("Updated")    



def updatePersonCustomer(conn, id, firstName, lastName, phone, address, receivable, resStaffId):
    cursor = conn.cursor()
    cursor.execute(
        'Update CUSTOMER Set FirstName = ?, LastName = ?, PhoneNumber = ?, Address = ?, Receivable = ?, ResponsibleStaffId = ? Where id = ?',
        (firstName, lastName, phone, address, receivable, resStaffId, id)
    )
    conn.commit()
    print("Updated")


def UpdateCompanyCustomer(conn, id, companyName, taxNumber, phone, address, receivable, resStaffId):
    cursor = conn.cursor()
    cursor.execute(
        'Update CUSTOMER Set CompanyName = ?, TaxNumber = ?, PhoneNumber = ?, Address = ?, Receivable = ?, ResponsibleStaffId = ? Where id = ?',
        (companyName, taxNumber, phone, address, receivable, resStaffId, id)
    )
    conn.commit()
    print("Updated")



def updatePurchaseReceiptProduct(conn, ReceiptId, ProductId, PurchaseUnitPrice, PurchaseAmount, TotalPrice):

    cursor = conn.cursor()
    cursor.execute(

        'Update PURCHASE_RECEIPT_PRODUCT Set PurchaseUnitPrice = ?, PurchaseAmount = ?, TotalPrice = ? where ReceiptId = ? and ProductId = ?', (
            PurchaseUnitPrice, PurchaseAmount, TotalPrice, ReceiptId, ProductId)

    )

    conn.commit()
    print("Updated")    

def updateSalesReceipt(conn, id, ReceiptNumber, CustomerId, Date):

    cursor = conn.cursor()
    cursor.execute(

        'Update SALES_RECEIPT Set ReceiptNumber = ?, CustomerId = ?, Date = ? where id = ? ', (
            ReceiptNumber, CustomerId, Date, id)

    )

    conn.commit()
    print("Updated")

def updateSalesReceiptProduct(conn, ReceiptId, ProductId, SaleUnitPrice, SaleAmount, TotalPrice):

    cursor = conn.cursor()
    cursor.execute(

        'Update SALES_RECEIPT_PRODUCT Set SaleUnitPrice = ?, SaleAmount = ?, TotalPrice = ? where ReceiptId = ? and ProductId = ?', (
            SaleUnitPrice, SaleAmount, TotalPrice, ReceiptId, ProductId)

    )

    conn.commit()
    print("Updated")    


def deleteStaff(conn, id):
    cursor = conn.cursor()
    cursor.execute(
        'Delete From STAFF Where id = ?', (id)
    )
    conn.commit()
    print("Deleted")


def deleteSupplier(conn, id):
    cursor = conn.cursor()
    cursor.execute(

        'exec dbo.deleteSupplier ?', (id)
    )
    conn.commit()
    print("Deleted")


def deleteCustomer(conn, id):
    cursor = conn.cursor()
    cursor.execute(

        'exec dbo.deleteCustomer ?', (id)
    )
    conn.commit()
    print("Deleted")

def deleteProduct(conn,id):
    cursor = conn.cursor()
    cursor.execute(

        'Delete From PRODUCT Where id = ? ', (id)
    )

    conn.commit()
    print("Deleted")

def deleteProductType(conn, id):
    cursor = conn.cursor()
    cursor.execute(

        'Delete From PRODUCT_TYPE where id = ? ', (id) 

    )
    conn.commit()
    print("Deleted")

def deletePurchaseReceipt(conn, id):
    cursor = conn.cursor()
    cursor.execute(
        'Delete From PURCHASE_RECEIPT where id = ? ', (id) 
)
    conn.commit()
    print("Deleted")

def deletePerson(conn, id):
    cursor = conn.cursor()
    cursor.execute(
        'Delete From CUSTOMER where id = ? ', (id) 
)
    conn.commit()
    print("Deleted")

def deleteCompany(conn, id):
    cursor = conn.cursor()
    cursor.execute(
        'Delete From CUSTOMER where id = ? ', (id) 
)
    conn.commit()
    print("Deleted")

def deletePurchaseReceiptProduct(conn,ReceiptId,ProductId):
    cursor = conn.cursor()
    cursor.execute(
        'Delete From PURCHASE_RECEIPT_PRODUCT where ReceiptId = ? and ProductId = ? ', (ReceiptId,ProductId) 
)
    conn.commit()
    print("Deleted")

def deleteSalesReceipt(conn, id):
    cursor = conn.cursor()
    cursor.execute(
        'Delete From SALES_RECEIPT where id = ? ', (id) 
)
    conn.commit()
    print("Deleted")

def deleteSalesReceiptProduct(conn,ReceiptId,ProductId):
    cursor = conn.cursor()
    cursor.execute(
        'Delete From SALES_RECEIPT_PRODUCT where ReceiptId = ? and ProductId = ? ', (ReceiptId,ProductId) 
)
    conn.commit()
    print("Deleted")