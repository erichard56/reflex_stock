from .connect_db import mydb, cursor
# from .connect_db import cursor
from datetime import date
import hashlib
import os

def chk_usuario(usuario: str, clave: str):
	# conn, cursor = connect()
	q1 = f'SELECT * FROM mstocks_users WHERE username = "{usuario}"'
	cursor.execute(q1)
	usuario = cursor.fetchone()
	res = hashlib.md5(clave.encode())
	clave2 = res.hexdigest()
	if (usuario is None):
		return (0, 0)

	if (usuario[2] != clave2):
		return (0, 0)

	return(int(usuario[0]), int(usuario[5]))


def get_usuarios():
	q1 = f'SELECT * FROM mstocks_users ORDER BY name'
	cursor.execute(q1)
	usuarios = cursor.fetchall()
	return(usuarios)

def get_usuario(id):
	q1 = f'SELECT * FROM mstocks_users WHERE id = {id}'
	cursor.execute(q1)
	usuario = cursor.fetchone()
	return(usuario)

def graba_clave(id, clave):
	res = hashlib.md5(clave.encode())
	clave2 = res.hexdigest()
	q1 = f'UPDATE mstocks_users SET password = "{clave2}" WHERE id = {id}'
	cursor.execute(q1)
	mydb.commit()


def items_select_all(letra: str):
	# conn, cursor = connect()
	q1 = f'SELECT A.id, CONCAT(A.name, "(", B.descrp, ")"), B.name, A.qty, A.price, A.price_venta, "foto" FROM mstocks_items A INNER JOIN depositos B ON B.id = A.category WHERE SUBSTR(A.name, 1, 1) = "{letra}" ORDER BY A.name'
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
	# conn, cursor = connect()
	q1 = f'SELECT CONCAT(name, " (", descrp, ")" FROM items WHERE id = {id}'
	cursor.execute(q1)
	name = cursor.fetchone()
	return(name[0])

def items_select_by_text(text: str):
	# conn, cursor = connect()
	q1 = f'SELECT A.id, CONCAT(A.name, " (", A.descrp, ")"), B.name, A.qty, A.price, A.price_venta, "foto" FROM mstocks_items A INNER JOIN mstocks_depositos B ON B.id = A.category WHERE A.name like "%{text}%" ORDER BY A.name'
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

def item_ingegr(direccion: str, id: int, cantidad: int, id_usuario: int):
	# conn, cursor = connect()
	q1 = f'SELECT qty from mstocks_items WHERE id = {id}'
	cursor.execute(q1)
	qty = int(cursor.fetchone()[0])
	if (direccion == 'in'):
		q1 = f'UPDATE mstocks_items SET qty = qty + {cantidad} WHERE id = {id}'	
		type = 1
		toqty = qty + cantidad
	else:
		q1 = f'UPDATE mstocks_items SET qty = qty - {cantidad} WHERE id = {id}'	
		type = 2
		toqty = qty + cantidad
	cursor.execute(q1)
	fecha = date.today()
	q1 = f'INSERT INTO mstocks_logs (id, type, item, fromqty, toqty, fromprice, toprice, date_added, user) VALUES (0, {type}, {id}, {qty}, {toqty}, 0.0, 0.0,  "{fecha}", {id_usuario})'
	cursor.execute(q1)
	# conn.commit()
	mydb.commit()


def get_logs(id: int):
	q1 = f'SELECT CONCAT(name, " (", descrp, ")") FROM mstocks_items WHERE id = {id}'
	cursor.execute(q1)
	name = cursor.fetchone()[0]

	q1 = f'SELECT type, item, fromqty, toqty, fromprice, toprice, date_added, user FROM mstocks_logs WHERE item = {id} ORDER BY date_added DESC, id DESC'
	cursor.execute(q1)
	logs = cursor.fetchall()
	res = []
	for log in logs:
		if (log[0] == 1):
			accion = 'Ingreso'
			desde = log[2]
			hasta = log[3]
		elif (log[0] == 2):
			accion = 'Egreso'
			desde = log[2]
			hasta = log[3]
		else:
			accion = 'Precio'
			desde = log[4]
			hasta = log[5]
		q1 = f'SELECT username FROM mstocks_users WHERE id = {log[7]}'
		cursor.execute(q1)
		usuario = cursor.fetchone()
		res.append([accion, desde, hasta, usuario, log[6]])
	return(name, res)

def get_item(id):
	q1 = f'SELECT * FROM mstocks_items WHERE id = {id}'
	cursor.execute(q1)
	item = cursor.fetchone()
	return(item)

def insmod_item(data, id_usuario):
	id = int(data['id'])
	q1 = f'SELECT price_venta from mstocks_items WHERE id = {id}'
	cursor.execute(q1)
	old_price_venta = float(cursor.fetchone()[0])

	name = data['name']
	descrp = data['descrp']
	price = float(data['price'])
	price_venta = float(data['price_venta'])
	if (id == 0):
		fecha = date.today()
		q1 = f'INSERT INTO mstocks_items (id, name, descrp, category, qty, price, price_venta, date_added) VALUES (0,"{name}", "{descrp}", 3, 0, {price}, {price_venta}, "{fecha}")'
	else:
		q1 = f'UPDATE mstocks_items SET name = "{name}", descrp = "{descrp}", price = {price}, price_venta = {price_venta} WHERE id = {id}'
	cursor.execute(q1)

	fecha = date.today()
	q1 = f'INSERT INTO mstocks_logs (id, type, item, fromqty, toqty, fromprice, toprice, date_added, user) VALUES (0, 3, {id}, 0, 0, {old_price_venta}, {price_venta}, "{fecha}", {id_usuario})'
	cursor.execute(q1)
	# conn.commit()
	mydb.commit()

def insmod_usuario(data):
	# id = int(data['id'])
	# name = data['name']
	# descrp = data['descrp']
	# price = float(data['price'])
	# price_venta = float(data['price_venta'])
	# if (id == 0):
	# 	fecha = date.today()
	# 	q1 = f'INSERT INTO mstocks_items (id, name, descrp, category, qty, price, price_venta, date_added) VALUES (0,"{name}", "{descrp}", 3, 0, {price}, {price_venta}, "{fecha}")'
	# else:
	# 	q1 = f'UPDATE mstocks_items SET name = "{name}", descrp = "{descrp}", price = {price}, price_venta = {price_venta} WHERE id = {id}'
	# cursor.execute(q1)
	# mydb.commit()
	a = 1
