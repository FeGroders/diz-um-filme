import psycopg2
from os import environ

def connectDatabase():
    sql = 'CREATE TABLE IF NOT EXISTS ultimoIdLido (id text)'
    cursor.execute(sql)
    sql = 'INSERT INTO ultimoIdLido VALUES ("1415336022263611392")'
    cursor.execute(sql)
    conn.commit()
    cursor.execute('select * from ultimoIdLido')
    recset = cursor.fetchall()
    for rec in recset:
        print (rec)
    cursor.close()

def disconnectDatabase():
    conn.close()

def createDatabase():
    cursor.execute('SELECT count(*) FROM versao')
    records = cursor.fetchall()
    if records[0][0] < 1:
        cursor.execute('INSERT INTO versao VALUES (100)')
        cursor.execute('INSERT INTO ultimoIdLido VALUES ("1415336022263611392")')

def updateUltimoIdLido(id):
    cursor.execute('UPDATE ultimoIdLido SET id = "{}"'.format(id))
    conn.commit()

def getUltimoIdLido():
    cursor.execute('SELECT id FROM ultimoIdLido')
    records = cursor.fetchall()
    return records[0][0]

conn = psycopg2.connect(
        host=environ['HOST'],
        database=environ['DATABASE'],
        user=environ['USER'],
        password=environ['PASSWORD'])
cursor = conn.cursor()
connectDatabase()    
