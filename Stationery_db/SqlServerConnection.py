import pyodbc

# LAPTOP-HCAE3FVL\MSSQLSERVER01;
# VG DESKTOP-CPMCPBA
# AFY DESKTOP-ISHU912
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=DESKTOP-ISHU912;"
    "Database=STATIONERY_BUSINESS;"
    "Trusted_Connection=yes;"
)


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


