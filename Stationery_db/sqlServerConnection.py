import pyodbc

conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=LAPTOP-HCAE3FVL\MSSQLSERVER01;"
    "Database=STATIONERY_BUSINESS;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()
cursor.execute('SELECT * FROM PRODUCT_TYPE')

for row in cursor:
    print(row)
    
"""read(conn)
create(conn)
update(conn)
delete(conn)
"""
conn.close()