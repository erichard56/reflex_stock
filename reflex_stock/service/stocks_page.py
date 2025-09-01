import reflex as rx
from .stocks_repository import item_ingegr
from .stocks_repository import items_select_by_text
from .stocks_repository import chk_usuario, get_logs, get_item, insmod_item, insmod_usuario
from .stocks_repository import get_usuarios, get_usuario, graba_clave, borrar_item, get_item_cant

from .logs import fnc_logs

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

class State(rx.State):
	role: int = 0
	username: str = ''
	id_usuario: int = 0
	opc: str = ''
	productos: list[list]
	producto: str = ''
	id_producto: int = 0
	cantidad: str = 1
	busq: str = ''
	error: str = ''
	logs: list[list]
	name: str
	descr: str
	precio: str
	precio_venta: str
	item: tuple
	usuarios: list[tuple]
	usuario: tuple
	clave: str
	verif: str
	email: str
	rol: str
	imagen: str
 

	@rx.event()
	async def handle_notify(self):
		async with self:
			await asyncio.sleep(2)
			self.error = ''

	@rx.event(background=True)
	async def evt_salir(self):
		async with self:
			self.role = 0
			self.opc = ''

	@rx.event(background=True)
	async def handle_ingresar(self, form_data: dict):
		async with self:
			self.id_usuario, self.role = chk_usuario(form_data['usuario'], form_data['clave'])
			if (self.role > 0):
				self.username = form_data['usuario']
			else:
				self.error = 'Usuario o Clave invalidos'
		if (self.error != ''):
			await self.handle_notify()

	@rx.event(background=True)
	async def handle_clave(self, form_data: dict):
		async with self:
			if (form_data['clave'] == form_data['verif']):
				graba_clave(form_data['id'], form_data['clave'])
				self.opc = ''
			else:
				self.error = 'La clave no coincide con la verificacion'
		if (self.error != ''):
			await self.handle_notify()

	@rx.event(background=True)
	async def handle_insmod_item(self, form_data: dict):
		async with self:
			insmod_item(form_data, self.id_usuario)
			self.productos = items_select_by_text(self.busq)
			self.opc = 'prods'

		if (self.error != ''):
			await self.handle_notify()

	@rx.event(background=True)
	async def evt_borrar_item(self, id_item):
		async with self:
			borrar_item(id_item)
			self.productos = items_select_by_text(self.busq)


	@rx.event(background=True)
	async def handle_insmod_user(self, form_data: dict):
		async with self:
			if (int(form_data['id']) == 0):
				if (form_data['clave'] == form_data['verif']):
					insmod_usuario(form_data)
					self.usuarios = get_usuarios()
					self.opc = 'users'
				else:
					self.error = 'La clave no coincide con la verificacion'
			else:
				insmod_usuario(form_data)
				self.usuarios = get_usuarios()
				self.opc = 'users'

		if (self.error != ''):
			await self.handle_notify()


	@rx.event(background=True)
	async def evt_usuarios(self):
		async with self:
			self.usuarios = get_usuarios()
			self.opc = 'users'


	@rx.event(background=True)
	async def evt_logs(self, id):
		async with self:
			self.producto, self.imagen, self.logs = get_logs(id)
			if (len(self.logs) > 0):
				fnc_logs(self.producto, self.imagen, self.logs)
			self.opc = 'logs'

	@rx.event(background=True)
	async def evt_precio(self, id):
		async with self:
			self.item = get_item(id)
			self.opc = 'prec'

	@rx.event(background=True)
	async def decrementar(self, id_item):
		async with self:
			qty = get_item_cant(id_item)
			if (qty > 0):
				item_ingegr('out', id_item, 1, self.id_usuario)
				self.productos = items_select_by_text(self.busq)
			else:
				self.error = 'Cantidad insuficiente'
		if (self.error != ''):
			await self.handle_notify()

	@rx.event(background=True)
	async def incrementar(self, id_item):
		async with self:
			item_ingegr('in', id_item, 1, self.id_usuario)
			self.productos = items_select_by_text(self.busq)

	@rx.event()
	def change_cantidad(self, value: str):
		self.cantidad = value

	@rx.event()
	def change_username(self, value: str):
		self.username = value

	@rx.event()
	def change_clave(self, value: str):
		self.clave = value

	@rx.event()
	def change_verif(self, value: str):
		self.verif = value

	@rx.event()
	def change_name(self, value: str):
		self.name = value

	@rx.event()
	def change_email(self, value: str):
		self.email = value

	@rx.event()
	def change_rol(self, value: str):
		self.rol = value

	@rx.event()
	def change_descr(self, value: str):
		self.descr = value

	@rx.event()
	def change_precio_venta(self, value: str):
		self.precio_venta = value

	@rx.event()
	def change_precio(self, value: str):
		self.precio = value

	@rx.event(background=True)
	async def agregar_stock(self, direccion, id_producto):
		async with self:
			cantidad = chkCantidad(self.cantidad)
			if (type(cantidad) == int):
				qty = get_item_cant(id_producto)
				if ((direccion == 'in') or (direccion == 'out' and qty >= cantidad)):
					item_ingegr(direccion, id_producto, cantidad, self.id_usuario)
					self.productos = items_select_by_text(self.busq)
					self.producto = self.productos[0][1]
					self.id_producto = self.productos[0][0]
				else:
					self.error = 'Cantidad insuficiente'
			else:
				self.error = cantidad

		if (self.error != ''):
			await self.handleNotify()

	def buscar_on_change(self, value: str):
		self.busq = value

	@rx.event(background=True)
	async def get_productos(self):
		async with self:
			self.error = ''
			if (self.busq != ''):
				self.productos = items_select_by_text(self.busq)
				if (len(self.productos) > 0):
					self.producto = self.productos[0][1]
					self.opc = 'prods'
					# self.letra = self.producto[0][0]
				else:
					self.error = 'No existen productos con esa busqueda'
			else:
				self.error = 'Debe ingresar un item en el campo Buscar'

		if (self.error != ''):
			await self.handleNotify()

	@rx.event(background=True)
	async def evt_nuevo_item(self):
		async with self:
			self.item = (0, '', '', 0, 0, 0.0, 0.0, '', '')
			self.opc='insmodproducto'

	@rx.event(background=True)
	async def evt_nuevo_usuario(self):
		async with self:
			self.usuario = (0, '', '', '', '', 0)
			self.opc='insmodusuario'

	@rx.event()
	async def handleNotify(self):
		async with self:
			await asyncio.sleep(2)
			self.error = ''

	@rx.event(background=True)
	async def evt_usuario(self, id):
		async with self:
			self.usuario = get_usuario(id)
			self.opc = 'insmodusuario'

	@rx.event(background=True)
	async def evt_clave(self, id):
		async with self:
			self.usuario = get_usuario(id)
			self.opc = 'clave'


@rx.page(route='/', title='Stocks')
@rx.page(route='/stocks', title='Stocks')
def stocks_page() -> rx.Component:
	return rx.box(
		rx.vstack(
			rx.card(
				rx.hstack(
					rx.vstack(
						rx.image(
							src = 'logo3x.jpeg', 
							width = '100%',
							height = 'auto',
							align = 'center'
						),
					),
					rx.box(
						rx.cond(
							State.role == 0,
							fnc_ingresar(),
							rx.vstack(
								rx.card(
									rx.hstack(
										rx.heading('Hola ', State.username),
										rx.match(
											State.role,
											(1, rx.heading('(Administrador)')),
											(2, rx.heading('(General Supervisor)')),
											(3, rx.heading('(Supervisor')),
											# (4, rx.heading('Empleado')),
										),
									)
								),
								rx.hstack(
									rx.card(
										rx.hstack(
											rx.input(placeholder = 'Producto??', on_change = State.buscar_on_change),
											rx.button('Buscar', on_click = State.get_productos),
											rx.cond (
												State.role == 1,
												rx.box(
													rx.button('Nuevo', on_click=State.evt_nuevo_item()),
												),
											),
										),
									),
									# rx.card(
										rx.hstack(
											rx.cond (
												State.role == 1,
												rx.card(
													rx.hstack(
														rx.button('Usuarios', on_click=State.evt_usuarios()),
														rx.button('Nuevo', on_click=State.evt_nuevo_usuario()),
													),
												),
											),
											rx.card(
												rx.button('Salir', on_click=State.evt_salir()),
											),
										)
									# )
								),
							),
						),
						margin_x='20px',
					),
				),
				width='100%',
			),
			rx.box(
				rx.cond(
					State.role > 0,
					rx.box(
						rx.match(
							State.opc,
							('prods', table_producto(State.busq)),
							('logs', fnc_logs(State.producto, State.imagen, State.logs)),
							('prec', fnc_insmod_item(State.item)),
							('insmodproducto', fnc_insmod_item(State.item)),
							('users', fnc_usuarios(State.usuarios)),
							('clave', fnc_clave(State.usuario)),
							('insmodusuario', fnc_insmod_usuario(State.usuario)),
						),
					),
				),
			),
		),
		rx.cond(
			State.error != '',
			notify_component(
					State.error,
					'shield_alert',
					'yellow'
				),
		),
		direction = 'column',
		style = { 'width':'80%', 'margin':'auto' },
		spacing ='2'
	)
	
def fnc_ingresar() -> rx.Component:
	return rx.form(
		rx.card(
			rx.hstack(
				rx.input(placeholder='Usuario', type='text', name='usuario'),
				rx.input(placeholder='Clave', type='password', name='clave'),
				rx.button(rx.icon('smile'), 'Ingresar', type='submit'),
			),
		),
		on_submit=State.handle_ingresar,
		reset_on_submit=True,
	)

def fnc_menu() -> rx.Component:
	return rx.box(
		table_producto(State.busq),
		rx.cond(
			State.error != '',
			notify_component(State.error, 'shield_alert', 'yellow'),
		),
		width='100%',
	)

def table_producto(busq) -> rx.Component:
	return rx.card(
		rx.table.root(
			rx.table.header( 
				rx.table.row(
					rx.table.column_header_cell('Producto', width='40%'),
					# rx.table.column_header_cell('Deposito', width='20%'),
					rx.table.column_header_cell('Stock', width='10%'),
					rx.table.column_header_cell('Precio', width='10%'),
					rx.table.column_header_cell('Precio de Venta', width='10%'),
					rx.table.column_header_cell('Imagen', width='10%'),
					rx.table.column_header_cell('Acciones', width='10%')
				),			
			),
			rx.cond(
				busq != '',
				rx.table.body(
					rx.foreach(State.productos, row_productos)
				),
			),
		),
		width='100%',
	)

def row_productos(producto) -> rx.Component:
	return rx.table.row(
		rx.table.cell(rx.text(producto[1])),
		# rx.table.cell(rx.text(producto[2])),
		rx.table.cell(rx.text(producto[3])),
		rx.table.cell(rx.text(producto[4])),
		rx.table.cell(rx.text(producto[5])),
		rx.cond(
			producto[6] == 'axm',
			rx.image(src='/axm.jpg', width='50%'),
            rx.image(src=producto[6], width="50px", height="50px"),
		),
		rx.table.cell(
			rx.hstack(
				rx.button(rx.icon("plus", on_click = State.incrementar(producto[0]))),
				rx.button(rx.icon("minus", on_click = State.decrementar(producto[0]))),
				fnc_ingegr('in', producto[0]),
				fnc_ingegr('out', producto[0]),
				rx.button(rx.icon('pencil'), on_click=State.evt_precio(producto[0])),
				fnc_borrar_item(producto[0]),
				# rx.button(rx.icon('eraser'), on_click=State.evt_borrar_item(producto[0])),
				rx.button('Logs', on_click=State.evt_logs(producto[0])),
			)
		),
	)


def fnc_ingegr(direccion, id) -> rx.Component:
	return rx.box(
		rx.dialog.root(
			rx.cond(
				direccion == 'in', 
				rx.dialog.trigger(rx.button("Ing")),
				rx.dialog.trigger(rx.button("Egr")),
			),
			rx.dialog.content(
				rx.hstack(
					rx.cond(
						direccion == 'in', 
						rx.dialog.title(rx.button("Ingreso")),
						rx.dialog.title(rx.button("Egreso")),
					),
					rx.text("Cantidad: ", margin_bottom="4px", weight="bold"),
					rx.input(default_value="1", placeholder="1", on_change=State.change_cantidad()),
					rx.dialog.close(rx.button("Cancel", color_scheme="gray", variant="soft")),
					rx.dialog.close(rx.button("Save"), on_click=State.agregar_stock(direccion, id)),
				),
				spacing="3",
			),
		)
	)


def fnc_borrar_item(id) -> rx.Component:
	return rx.box(
		rx.dialog.root(
			rx.dialog.trigger(rx.button(rx.icon('eraser'))),
			rx.dialog.content(
				rx.hstack(
					rx.dialog.title(rx.text("Borrado de un Item")),
					rx.dialog.close(rx.button("Cancel", color_scheme="gray", variant="soft")),
					rx.dialog.close(rx.button("Confirmar"), on_click=State.evt_borrar_item(id)),
				),
				spacing="3",
			),
		)
	),


def fnc_insmod_item(item: list = None) -> rx.Component:
	return rx.card(
		rx.form(
			rx.vstack(
				rx.cond(
					item[0] == 0,
					rx.heading("Nuevo Producto"),
					rx.heading("Modificacion"),
				),
				rx.input(default_value=item[0], name='id', style={'width':'0px', 'height':'0px'}),
				rx.hstack(
					rx.text("Nombre: ", margin_bottom="4px", weight="bold"),
					rx.input(default_value=item[1], placeholder=item[1], name='name', on_change=State.change_name()),
				),
				rx.hstack(
					rx.text("Descripcion: ", margin_bottom="4px", weight="bold"),
					rx.input(default_value=item[2], placeholder=item[2], name='descrp', on_change=State.change_descr()),
				),
				rx.hstack(
					rx.text("Precio: ", margin_bottom="4px", weight="bold"),
					rx.input(default_value=item[5], placeholder=item[5], step="0.1", name='price', on_change=State.change_precio()),
				),
				rx.hstack(
					rx.text("Precio de Venta: ", margin_bottom="4px", weight="bold"),
					rx.input(default_value=item[6], placeholder=item[6], step="0.1", name='price_venta', on_change=State.change_precio_venta()),
				),
				rx.hstack(
					rx.text('Imagen', margin_bottom="4px", weight="bold"),
					rx.cond(
						item[8] == 'axm',
						rx.image(src='/axm.jpg', width='50%'),
						rx.image(item[8], width='20%'),
					),
					rx.hstack(
						rx.input(name='imagen', type='file', accept='image/*'),
					),
				),
				rx.hstack(
					rx.button("Cancel", color_scheme="gray", variant="soft"),
					rx.button("Grabar", type='submit'),
				),
			),
			on_submit=State.handle_insmod_item,
			reset_on_submit=True,
		),
	)


def fnc_usuarios(usuarios) -> rx.Component:
	return rx.box(
		rx.flex(
			rx.card(
				rx.heading('Usuarios'),
			),
			rx.card(
				rx.table.root(
					rx.table.header( 
						rx.table.row(
							rx.table.column_header_cell('Nombre'),
							rx.table.column_header_cell('Usuario'),
							rx.table.column_header_cell('Email'),
							rx.table.column_header_cell('Rol'),
							rx.table.column_header_cell('Registrado'),
							rx.table.column_header_cell('Acciones'),
						),			
					),
					rx.table.body(
						rx.foreach(usuarios, fnc_usuarios_one)
					),
				),
			),
		),
		width='100%',
	)

def fnc_usuarios_one(usuario):
	return rx.table.row(
		rx.table.cell(rx.text(usuario[3])),
		rx.table.cell(rx.text(usuario[1])),
		rx.table.cell(rx.text(usuario[4])),
		rx.table.cell(rx.text(usuario[5])),
		rx.table.cell(rx.text(usuario[6])),
		rx.table.cell(
			rx.button(rx.icon('pencil'), on_click=State.evt_usuario(usuario[0])),
			rx.button(rx.icon('lock-keyhole'), on_click=State.evt_clave(usuario[0])),
		),
	)

def fnc_clave(usuario) -> rx.Component:
	return rx.form (
		rx.hstack(
			rx.card(
				rx.heading(usuario[1]),
			),
			rx.card(
				rx.hstack(
					rx.input(default_value=usuario[0], name='id', style={'width':'0px', 'height':'0px'}),
					rx.input(placeholder='Nueva Clave', type='password', name='clave'),
					rx.input(placeholder='Verificacion', type='password', name='verif'),
					rx.button('Grabar', type='submit'),
				),
			),
		),
		on_submit=State.handle_clave,
		reset_on_submit=True,
	)


def fnc_insmod_usuario(usuario: list = None) -> rx.Component:
	return rx.card(
		rx.form(
			rx.vstack(
				rx.cond(
					usuario[0] == 0,
					rx.heading("Nuevo Usuario"),
					rx.heading("Modificacion"),
				),
				rx.input(default_value=usuario[0], name='id', style={'width':'0px', 'height':'0px'}),
				rx.hstack(
					rx.text("Usuario: ", margin_bottom="4px", weight="bold"),
					rx.input(default_value=usuario[1], placeholder=usuario[1], name='username', on_change=State.change_name()),
				),
				rx.cond(
					usuario[0] == 0,
					rx.box(
						rx.hstack(
							rx.text("Clave: ", margin_bottom="4px", weight="bold"),
							rx.input(name='clave', type='password', on_change=State.change_clave()),
						),
						rx.hstack(
							rx.text("Verificacion: ", margin_bottom="4px", weight="bold"),
							rx.input(name='verif', type='password', on_change=State.change_verif()),
						),
					),
				),
				rx.hstack(
					rx.text("Nombre: ", margin_bottom="4px", weight="bold"),
					rx.input(default_value=usuario[3], placeholder=usuario[3], name='name', on_change=State.change_name()),
				),
				rx.hstack(
					rx.text("Email: ", margin_bottom="4px", weight="bold"),
					rx.input(default_value=usuario[4], placeholder=usuario[4], name='email', type='email', on_change=State.change_email()),
				),
				rx.hstack(
					rx.text("Rol: ", margin_bottom="4px", weight="bold"),
					rx.input(default_value=usuario[5], placeholder=usuario[5], name='rol', type='number', on_change=State.change_rol()),
				),
				rx.hstack(
					rx.button("Cancel", color_scheme="gray", variant="soft"),
					rx.button("Grabar", type='submit'),
				),
			),
			on_submit=State.handle_insmod_user,
			reset_on_submit=True,
		),
	)



app = rx.App()
app.add_page(stocks_page)

