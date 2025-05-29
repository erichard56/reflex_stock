from ..model.stocks_model import Producto, Stock #, Clases, SubClases
from .connect_db import connect
import datetime

def letras_select_all():
	conn, cursor = connect()
	q1 = 'SELECT DISTINCT(SUBSTR(producto, 1, 1)) FROM productos ORDER BY producto'
	cursor.execute(q1)
	letras = cursor.fetchall()
	return(letras)

def productos_select_all(letra: str):
	conn, cursor = connect()
	q1 = 'SELECT * FROM productos WHERE SUBSTR(producto, 1, 1) = "' + str(letra) + '" ORDER BY producto'
	cursor.execute(q1)
	productos = cursor.fetchall()
	return(productos)

def producto_select_by_id(id: int):
	conn, cursor = connect()
	q1 = 'SELECT producto FROM productos WHERE id = ' + str(id)
	cursor.execute(q1)
	producto = cursor.fetchone()
	return(producto[0])

def productos_select(text: str):
	conn, cursor = connect()
	q1 = 'SELECT * FROM productos WHERE producto like "%' + text + '%" ORDER BY producto'
	cursor.execute(q1)
	productos = cursor.fetchall()
	return(productos)

def stocks_select_all(id_producto: int):
	lapso = datetime.datetime.now().year * 12 + datetime.datetime.now().month
	conn, cursor = connect()
	q1 = 'SELECT id, cantidad, id_producto, ' + \
			' concat(mes, "-", anio), anio * 12 + mes - ' + str(lapso)  + ' AS falta, ' + \
			' CASE ' + \
				' WHEN anio * 12 + mes - 24305 <= 0 THEN "red" ' + \
				' WHEN anio * 12 + mes - 24305 <= 2 THEN "orange" ' + \
				' ELSE "green" ' + \
				' END AS color ' + \
			' FROM stocks WHERE id_producto = ' + str(id_producto) + ' ORDER BY falta'
	cursor.execute(q1) 
	stocks = cursor.fetchall()
	return(stocks)

def delete_stock(id: int, id_producto: int):
	conn, cursor = connect()
	q1 = 'DELETE FROM stocks WHERE id = ' + str(id)
	cursor.execute(q1)
	conn.commit()
	return stocks_select_all(id_producto)

def decrementar_stock(id: int, id_producto: int):
	conn, cursor = connect()
	q1 = 'UPDATE STOCKS set cantidad = cantidad - 1 where id = ' + str(id)
	cursor.execute(q1)
	conn.commit()
	return stocks_select_all(id_producto)

def incrementar_stock(id: int, id_producto: int):
	conn, cursor = connect()
	q1 = 'UPDATE STOCKS set cantidad = cantidad + 1 where id = ' + str(id)
	cursor.execute(q1)
	conn.commit()
	return stocks_select_all(id_producto)

def agregar_stock(id_producto: int, cantidad: int, mes: int, anio: int):
	conn, cursor = connect()
	q1 = 'INSERT INTO stocks VALUES(NULL, ' + str(cantidad) + ', ' + str(id_producto) + \
		', ' + str(mes) + ', ' + str(anio) + ')'
	cursor.execute(q1)
	conn.commit()
	return stocks_select_all(id_producto)
