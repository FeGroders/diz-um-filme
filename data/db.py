import sqlite3

banco = sqlite3.connect('./data/dizumfilme.db')
cursor = banco.cursor()

def createDatabase():
    cursor.execute('SELECT count(*) FROM versao')
    records = cursor.fetchall()
    if records[0][0] < 1:
        cursor.execute('INSERT INTO versao VALUES (100)')
        cursor.execute('INSERT INTO ultimoIdLido VALUES ("1415336022263611392")')

def updateUltimoIdLido(id):
    cursor.execute('UPDATE ultimoIdLido SET id = "{}"'.format(id))
    banco.commit()

def getUltimoIdLido():
    cursor.execute('SELECT id FROM ultimoIdLido')
    records = cursor.fetchall()
    return records[0][0]

cursor.execute('CREATE TABLE IF NOT EXISTS versao (versao id)')
cursor.execute('CREATE TABLE IF NOT EXISTS ultimoIdLido (id text)')
createDatabase()    
banco.commit()