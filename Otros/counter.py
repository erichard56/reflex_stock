# import reflex as rx

# class StateCounter(rx.State):
#     index: int = 0
#     def aumentar(self):
#         self.index += 1
#     def disminuir(self):
#         self.index -= 1
#     @rx.var
#     def getIndex(self) -> str:
#         return str(self.index)

# @rx.page(route='/counter', title='Contador')
# def counter() -> rx.Component:
#     return rx.fragment(
#         rx.center(
#             rx.vstack(
#                 rx.heading('Contador'),
#                 rx.text('Mi primer componente contador'),
#                 rx.hstack(
#                     rx.button('-', on_click=StateCounter.disminuir),
#                     rx.text(StateCounter.getIndex),
#                     rx.button('+', on_click=StateCounter.aumentar)
#                 )
#             )
#         )
#     )