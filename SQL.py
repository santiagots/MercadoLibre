from typing import List
from Utility import getConfiguration, SetConfiguration
import datetime
import pyodbc 
from Class.Sale import Sale

def getProductSold(date) -> List[Sale]:
    server = getConfiguration("DataBase", "server")
    database = getConfiguration("DataBase", "database")

    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=Yes;')
    cursor = cnxn.cursor()
    
    sql = "SELECT p.Codigo, sum(I.Cantidad) Cantidad FROM NUEVA_VENTA_ITEMS I inner join PRODUCTOS P on I.CodigoProducto = P.Codigo WHERE I.FechaEdicion > '{date}'  group by p.Codigo".format(date = date)  
    cursor.execute(sql)
    row = cursor.fetchone()

    sales = []
    while row:
        sales.append(Sale(row[0],row[1]))
        print(row)
        row = cursor.fetchone()

    return sales

date = datetime.datetime(2020, 1, 1, 1, 1 , 1)
getProductSold(date)