# from .connect_db import mydb, cursor
from .connect_db import connect
import datetime
import os

def get_usuario(usuario: str, clave: str):
	conn, cursor = connect()
	q1 = f'SELECT * FROM users WHERE username = "{usuario}"'
	cursor.execute(q1)
	usuario = cursor.fetchone()
	if (usuario is None):
		return 0

	if (usuario[1] != clave):
		return 0

	return(int(usuario[5]))


def letras_select_all():
	conn, cursor = connect()
	q1 = 'SELECT DISTINCT(SUBSTR(name, 1, 1)) FROM items' # ORDER BY DISTINCT(SUBSTR(name, 1, 1))'
	cursor.execute(q1)
	letras = cursor.fetchall()
	letras.sort()
	return(letras)

def items_select_all(letra: str):
	conn, cursor = connect()
	q1 = f'SELECT A.id, A.name, B.name, A.qty, A.price, A.price_venta, "foto" FROM items A INNER JOIN depositos B ON B.id = A.category WHERE SUBSTR(A.name, 1, 1) = "{letra}" ORDER BY A.name'
	cursor.execute(q1)
	items = cursor.fetchall()
	rit = []
	for it in items:
		file = '/imagenes/' + it[1] + '.jpg'
		if (not os.path.exists('assets' + file)):
			file = '/axm.jpg'
		rit.append([it[0], it[1], it[2], it[3], it[4], it[5], file])
	return(rit)

def item_select_by_id(id: int):
	conn, cursor = connect()
	q1 = f'SELECT name FROM items WHERE id = {id}'
	cursor.execute(q1)
	name = cursor.fetchone()
	return(name[0])

def items_select_by_text(text: str):
	conn, cursor = connect()
	q1 = f'SELECT A.id, A.name, B.name, A.qty, A.price, A.price_venta, "foto" FROM items A INNER JOIN depositos B ON B.id = A.category WHERE A.name like "%{text}%" ORDER BY A.name'
	cursor.execute(q1)
	items = cursor.fetchall()
	rit = []
	for it in items:
		file = '/imagenes/' + it[1] + '.jpg'
		if (not os.path.exists('assets' + file)):
			file = '/axm.jpg'
		rit.append([it[0], it[1], it[2], it[3], it[4], it[5], file])
	return(rit)


# def delete_stock_by_id(id: int):
# 	conn, cursor = connect()
# 	q1 = 'DELETE FROM items WHERE id = ' + str(id)
# 	cursor.execute(q1)
# 	conn.commit()
# 	return stocks_select_all(id_producto)

def item_ingegr(direccion: str, id: int, cantidad: int):
	conn, cursor = connect()
	if (direccion == 'in'):
		q1 = f'UPDATE items SET qty = qty + {cantidad} WHERE id = {id}'	
	else:
		q1 = f'UPDATE items SET qty = qty - {cantidad} WHERE id = {id}'	
	cursor.execute(q1)
	mydb.commit()
