import sqlite3

banco = sqlite3.connect('./db/dizumfilme.db')

cursor = banco.cursor()

cursor.execute('CREATE TABLE ultimoIdLido (id text)')
cursor.execute('INSERT INTO ultimoIdLido(id) VALUES ("0")')
banco.commit

def updateUltimoIdLido(id):
    cursor.execute('UPDATE ultimoIdLido SET id = "'+id+'"')
    banco.commit

def getUltimoIdLido():
    cursor.execute('SELECT id FROM ultimoIdLido')
    records = cursor.fetchall()
    for id in records:
        idFinal = id[0]
    return idFinal