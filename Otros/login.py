# import reflex as rx
# import requests as rq
# import re

# class loginState(rx.State):
# 	loader: bool = False
# 	username: str = "example@mail.com"
# 	password: str
# 	error = False
# 	response: dict = {}

# 	@rx.event(background=True)
# 	async def loginService(self, data: dict):
# 		async with self:
# 			self.loader = True
# 			self.error = False
# 			response = rq.post('http://localhost:8080/auth/login', json=data, headers={'Content-type':'application/json'})
# 			if(response.stauts.code == 200):
# 				self.response = response.json()
# 				self.loader = False
# 				return rx.redirect('/')
# 			else:
# 				self.loader = False
# 				self.error = True

# 	@rx.var
# 	def user_invalid(self) -> bool:
# 		return not(re.match(r"[^@]+@[^@]+.[^@]+", self.username) and "example@mail.com")
	
# 	@rx.var
# 	def user_empty(self) -> bool:
# 		return not self.username.strip()
	
# 	@rx.var
# 	def password_empty(self) -> bool:
# 		return not(self.password.strip())
	
# 	@rx.var
# 	def validate_fields(self) -> bool:
# 		return(
# 			self.user_empty
# 			or self.user_invalid
# 			or self.password_empty
# 		)


# @rx.page(route='/login', title='login')
# def login() -> rx.Component:
# 	return rx.section(
# 		rx.flex(
# 			rx.image(src='/ellos aprenden lo que ven.jpg', width="300px", border_radius="15px 50px"),
# 			rx.heading('Inicio de Sesion'),
# 			rx.form.root(
# 				rx.flex(
# 					field_form_component_general('Usuario', 'Ingrese su correo', 'Ingrese un correo valido',
# 								  'username', loginState.set_username, loginState.user_invalid),

# 					field_form_component('Contraseña', 'Ingrese su contraseña', 'password',
# 						  loginState.set_password, 'password'),

# 					rx.form.submit(
# 						rx.cond(
# 							loginState.loader,
# 							rx.spinner(color='red', size='1'),
# 							rx.button(
# 								'Iniciar sesion',
# 								disabled = loginState.validate_fields,
# 								width="30vw",
# 							),
# 						),
# 						as_child = True,
# 					),
# 					direction = 'column',
# 					justify = 'center',
# 					align = 'center',
# 					spacing = '2',
# 				),
# 				rx.cond(
# 					loginState.error,
# 					rx.callout(
# 						'Credenciales incorrectas',
# 						icon = 'alert_triangle',
# 						# color_scheme= = 'red',
# 						role = 'alert',
# 						stype = {'margin_top':'10px'}
# 					)
# 				),
# 				on_submit = loginState.loginService,
# 				reset_on_submit = True,
# 				width = '80%',
# 			),
# 			width = '100%',
# 			direction = 'column',
# 			align = 'center',
# 			justify = 'center',
# 		),
# 		style = style_section,
# 		justify = 'center',
# 		width = '30%',
# 	)

# def field_form_component(label: str, placeholder: str, name_var: str, 
# 						 on_change_function, type_field: str) -> rx.Component:
# 	return rx.form.field(
# 		rx.flex(
# 			rx.form.label(label),
# 			rx.form.control(
# 				rx.input(
# 					placeholder = placeholder,
# 					on_change = on_change_function, 
# 					name = name_var,
# 					type = type_field,
# 					required= True,
# 				),
# 				as_child = True,
# 			),
# 			rx.form.message(
# 					'El campo no puede ser nulo',
# 					match = 'valueMissing',
# 					color = 'red',
# 			),
# 			direction = 'column',
# 			spacing = '2',
# 			align = 'stretch',
# 		),
# 		name = name_var,
# 		width = "30vw"
# 	)

# def field_form_component_general(label: str, placeholder: str, message_validate: str, name: str, 
# 						 on_change_function, show) -> rx.Component:
# 	return rx.form.field(
# 		rx.flex(
# 			rx.form.label(label),
# 			rx.form.control(
# 				rx.input(
# 					placeholder = placeholder,
# 					on_change = on_change_function, 
# 					name = name,
# 					required= True,
# 				),
# 				as_child = True
# 			),
# 			rx.form.message(
# 				message_validate,
# 				name = name,
# 				match = 'valueMissing',
# 				force_match = show,
# 				color = 'red',
# 			),
# 			direction = 'column',
# 			spacing = '2',
# 			align = 'stretch',
# 		),
# 		name = name,
# 		width = "30vw"
# 	)

# style_section = {
# 	'height': '90vw',
# 	'width': '80%',
# 	'margin': 'auto',
# }