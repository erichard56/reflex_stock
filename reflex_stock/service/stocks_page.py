import reflex as rx
from ..model.stocks_model import Producto, Stock, StockLapso
from .stocks_service import letras_select_all_service, productos_select_all_service, stocks_select_all_service, \
			producto_select_by_id_service, productos_select_service, \
			delete_stock_service, decrementar_stock_service, incrementar_stock_service, agregar_stock_service
from .notify import notify_component
import asyncio
import datetime

def chkCantidad(cantidad):
	try:
		n = int(cantidad)
		if (n > 0):
			return(n)
		else:
			return('Cantidad debe ser mayor que 0')
	except:
		return('Cantidad debe ser numerico')

def chkVencimiento(vencimiento):
	vencimiento = vencimiento.replace('/', '-')
	if (vencimiento.find('-') > 0):
		m, a = vencimiento.split('-')
		try:
			mes = int(m)
			if (1 <= mes <= 12):
				try:
					anio = int(a)
					if (anio < 100):
						anio += 2000
						vencimiento = '-'.join([str(mes), str(anio)]) 
						return(mes, anio)
				except:
					return('Año fuera de rango', '')	# anio esta fuera de rango
			else:
				return('Mes debe estar entre 1 y 12', '')	# mes esta fuera de rango
		except:
			return('El mes debe ser numérico', '')	# mes no es numerico
	else:
		return('Debe ser algo de la forma mm/aaaa', '')	# falta el separador


class StockState(rx.State):
	letras: list[tuple]
	letra: str
	productos: list[tuple[Producto]]
	stocks: list[tuple[StockLapso]]
	producto: str = ''
	id_producto: int = 0
	cantidad: str = 0
	vencimiento: str = ''
	producto_buscar: str
	error: str = ''

	@rx.event(background=True)
	async def get_all_letras(self):
		async with self:
			self.letras = letras_select_all_service()
			self.letra = self.letras[0][0]
			self.productos = productos_select_all_service(self.letra)
			self.id_producto = self.productos[0][0]
			self.producto = producto_select_by_id_service(self.id_producto)
			self.stocks = stocks_select_all_service(self.id_producto)

	@rx.event(background=True)
	async def get_letra(self, letra):
		async with self:
			self.productos = productos_select_all_service(letra)
			self.id_producto = self.productos[0][0]
			self.producto = producto_select_by_id_service(self.id_producto)
			self.stocks = stocks_select_all_service(self.id_producto)

	@rx.event(background=True)
	async def get_stock(self, id_producto):
		async with self:
			self.id_producto = id_producto
			self.producto = producto_select_by_id_service(self.id_producto)
			self.stocks = stocks_select_all_service(self.id_producto)

	@rx.event(background=True)
	async def delete_stock_by_id(self, id_stock, id_producto):
		async with self:
			self.stocks = delete_stock_service(id_stock, id_producto)

	@rx.event(background=True)
	async def decrementar(self, id_stock, id_producto):
		async with self:
			self.stocks = decrementar_stock_service(id_stock, id_producto)

	@rx.event(background=True)
	async def incrementar(self, id_stock, id_producto):
		async with self:
			self.stocks = incrementar_stock_service(id_stock, id_producto)

	@rx.event()
	def change_cantidad(self, value: str):
		self.cantidad = value

	@rx.event()
	def change_vencimiento(self, value: str):
		self.vencimiento = value

	@rx.event(background=True)
	async def agregar_stock(self, id_producto):
		async with self:
			cantidad = chkCantidad(self.cantidad)
			if (type(cantidad) == int):
				mes, anio = chkVencimiento(self.vencimiento)
				if (type(mes) == int):
					agregar_stock_service(id_producto, cantidad, mes, anio)
					self.stocks = stocks_select_all_service(id_producto)
					self.cantidad = ''
					self.vencimiento = ''
				else:
					self.error = mes
			else:
				self.error = cantidad

		if (self.error != ''):
			await self.handleNotify()

	def buscar_on_change(self, value: str):
		self.producto_buscar = value

	@rx.event(background=True)
	async def get_productos(self):
		async with self:
			self.error = ''
			self.productos = productos_select_service(self.producto_buscar)
			if (len(self.productos) == 0):
				self.error = 'No existen productos con esa busqueda'
				self.productos = productos_select_all_service(self.letra)
				self.producto = self.productos[0][1]
			self.id_producto = self.productos[0][0]
			self.stocks = stocks_select_all_service(self.id_producto)

		if (self.error != ''):
			await self.handleNotify()

	@rx.event()
	async def handleNotify(self):
		async with self:
			await asyncio.sleep(2)
			self.error = ''

@rx.page(route='/stocks', title='Stocs Vero', on_load=StockState.get_all_letras)
def stocks_page() -> rx.Component:
	return rx.flex(
		rx.hstack(
			rx.heading(
				'Stocks Vero', 
				align = 'center',
				style = { 'padding':'10px' }
			),
			justify='center',
		),
		rx.hstack(
			rx.foreach(StockState.letras, row_letras),
			justify = 'center',
			style = { 'margin_top':'5px' }
		),
		rx.hstack(
			rx.input(
				placeholder = 'Producto??', 
				on_change = StockState.buscar_on_change
			),
			rx.button(
				'Buscar', 
				on_click = StockState.get_productos
			),
			justify = 'end',
		),
		rx.flex(
			table_producto(),
			table_stock(),
		),
		rx.cond(
			StockState.error != '',
			notify_component(
					StockState.error,
					'shield_alert',
					'yellow'
				),
		),
		direction = 'column',
		style = { 'width':'72vw', 'margin':'auto' },
		spacing ='2'
	)

def row_letras(letra: tuple) -> rx.Component:
	return rx.button(
			letra[0], 
			on_click = StockState.get_letra(letra[0])
		)

def table_producto() -> rx.Component:
	return rx.table.root(
		rx.table.header( 
			rx.table.row(
				rx.table.column_header_cell(
					rx.heading('Productos'),
					justify = 'center',
					min_width = '33vw'
				),
			),			
		),
		rx.table.body(
			rx.foreach(StockState.productos, row_productos)
		),
		style= { 'border':'thick double' },
	)

def row_productos(producto: Producto) -> rx.Component:
	return rx.table.row(
		rx.table.cell(
			rx.button(
				producto[1], 
				variant = 'ghost',
				size = '3',
				on_click = StockState.get_stock(producto[0])
			),
			align = 'right',
		)
	)

def table_stock() -> rx.Component:
	return rx.table.root(
		rx.table.header( 
			rx.table.row(
				rx.table.column_header_cell(
					rx.heading(
						StockState.producto.replace('"', ''), 
						color_scheme = 'orange',
					),
					min_width = '33vw',
					justify = 'center', 
					col_span = 4,
				),
			),
			rx.table.row(
				rx.table.column_header_cell('Cantidad', justify = 'center'),
				rx.table.column_header_cell('Vencimiento', justify = 'center'),
				rx.table.column_header_cell('Meses', justify = 'center'),
				rx.table.column_header_cell('Acciones', justify = 'center'),
			),			
		),
		rx.table.body(
			rx.foreach(StockState.stocks, row_stocks),
			rx.table.row(
				rx.table.cell(
					rx.input(
						placeholder = 'Cant', 
						type = 'number', 
						style = { 'text_align': 'center' },
						value = StockState.cantidad, on_change=StockState.change_cantidad()
					)
				),
				rx.table.cell(
					rx.input(
						placeholder = 'mm/aaaa', 
						type = 'text', 
						style = { 'text_align': 'center' },
						value = StockState.vencimiento, on_change=StockState.change_vencimiento()
					)
				),
				rx.table.cell(
					rx.button(
						'Agregar', 
						size = '2',
						on_click = StockState.agregar_stock(StockState.id_producto)
					),
					col_span=3
				),
			)
		),
		style= { 'border':'thick double' },
	)

def row_stocks(stock: StockLapso) -> rx.Component:
	return rx.table.row(
		rx.table.cell(stock[1], justify = 'center', style={ 'color':stock[5], 'font_size':'16px' }),
		rx.table.cell(stock[3], justify = 'center', style={ 'color':stock[5], 'font_size':'16px' }),
		rx.table.cell(stock[4], justify = 'center', style={ 'color':stock[5], 'font_size':'16px' }),
		rx.table.cell(
			rx.hstack(
				rx.button(
					rx.icon("minus", on_click = StockState.decrementar(stock[0], stock[2])),
				),
				rx.button(
					rx.icon('trash-2', on_click = StockState.delete_stock_by_id(stock[0], stock[2])),
				),
				rx.button(
        			rx.icon("plus", on_click = StockState.incrementar(stock[0], stock[2])),
				),
			)
		),
	)

app = rx.App()
app.add_page(stocks_page)

