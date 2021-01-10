import pyodbc

# LAPTOP-HCAE3FVL\MSSQLSERVER01;
# VG DESKTOP-CPMCPBA
# AFY DESKTOP-ISHU912
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=LAPTOP-HCAE3FVL\MSSQLSERVER01;"
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
        'insert into SALES_RECEIPT (ReceiptNumber,CustomerId,Date) values (?,?,?)',
        (receiptNumber, customerId, date)

    )
    conn.commit()
    print("Sale receipt created")



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
        'insert into SUPPLIER (SupplierName, PhoneNumber, Address, Debt) values (?,?,?,?)',
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



def insertPurchaseReceipt(conn, receiptNumber, supplierId, date):
    cursor = conn.cursor()
    cursor.execute(
        'insert into PURCHASE_RECEIPT (ReceiptNumber, SupplierId, Date) values(?,?,?)',
        (receiptNumber, supplierId, date)
    )
    conn.commit()
    print("Inserted")



def updateProductType(conn, id, type_name):
    cursor = conn.cursor()
    cursor.execute(
        'Update PRODUCT_TYPE set TypeName = ? Where id = ?', (type_name, id)
    )
    conn.commit()
    print('Updated')



def updateStaff(conn,id, tckn, fname, lname, phone,
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


def deleteStaff(conn, id):
    cursor = conn.cursor()
    cursor.execute(
        'Delete From STAFF Where id = ?', (id)
    )
    conn.commit()
    print("Deleted")