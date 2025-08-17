from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import requests
import hashlib
import json
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconRightWidget
from kivymd.uix.dialog import MDDialog


# -------------------- CONFIG --------------------
Window.size = (400, 600)

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"


# -------------------- Screens --------------------
class LoginScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class MenuScreen(Screen):
    pass

class ChatScreen(Screen):
    pass

class DevicesScreen(Screen):
    pass

class HistoryScreen(Screen):
    pass

class ChatDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        self.detail_label = MDLabel(
            text='',
            halign='left',
            size_hint_y=None,
            markup=True
        )
        self.detail_label.bind(texture_size=self.detail_label.setter('size'))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.detail_label)

        action_buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)

        btn_block_media = MDFillRoundFlatButton(
            text='Bloquear Multimedia',
            size_hint_x=0.5
        )
        btn_block_media.bind(on_release=lambda x: MDApp.get_running_app().block_multimedia())
        
        btn_block_contact = MDFillRoundFlatButton(
            text='Bloquear Contacto',
            size_hint_x=0.5
        )
        btn_block_contact.bind(on_release=lambda x: MDApp.get_running_app().block_contact())

        action_buttons_layout.add_widget(btn_block_media)
        action_buttons_layout.add_widget(btn_block_contact)

        btn_back = MDFillRoundFlatButton(text='Volver al Historial', size_hint_y=None, height=40)
        btn_back.bind(on_release=self.go_back_to_history)

        layout.add_widget(MDLabel(text='Detalle del Chat', halign='center', font_style='H4'))
        layout.add_widget(scroll)
        layout.add_widget(action_buttons_layout)
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def go_back_to_history(self, instance):
        MDApp.get_running_app().sm.current = 'history'


# -------------------- App --------------------
class MainApp(MDApp):
    url = "https://ancla-49cb4-default-rtdb.firebaseio.com/"
    key = "jtDbJ2cyGCyNHPtiuoqIYzm1K6qjVDu3ngTfEHgB"
    dialog = None 

    def build(self):
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.theme_style = "Dark"

        self.sm = ScreenManager()
        self.history = []

        self.build_login()
        self.build_register()
        self.build_menu()
        self.build_chat()
        self.build_devices()
        self.build_history()
        
        self.chat_detail_screen = ChatDetailScreen(name='chat_detail')
        self.sm.add_widget(self.chat_detail_screen)

        return self.sm

    # -------------------- Login --------------------
    def build_login(self):
        login_layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
        self.user = MDTextField(hint_text='Usuario')
        self.password = MDTextField(hint_text='Contraseña', password=True)
        self.signal = MDLabel(text='', halign='center', theme_text_color='Custom', text_color=(1,0.35,0.12,1))

        btn_login = MDFillRoundFlatButton(text='Ingresar', pos_hint={'center_x':0.5})
        btn_login.bind(on_release=self.login)

        btn_register = MDFillRoundFlatButton(text='Registrarse', pos_hint={'center_x':0.5})
        btn_register.bind(on_release=lambda x: setattr(self.sm, 'current', 'register'))

        login_layout.add_widget(MDLabel(text='Login', halign='center', font_style='H4'))
        login_layout.add_widget(self.user)
        login_layout.add_widget(self.password)
        login_layout.add_widget(self.signal)
        login_layout.add_widget(btn_login)
        login_layout.add_widget(btn_register)

        login_screen = Screen(name='login')
        login_screen.add_widget(login_layout)
        self.sm.add_widget(login_screen)

    # -------------------- Register --------------------
    def build_register(self):
        register_layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
        self.new_user = MDTextField(hint_text='Nuevo usuario')
        self.new_password = MDTextField(hint_text='Contraseña', password=True)
        self.new_password_two = MDTextField(hint_text='Confirmar contraseña', password=True)
        self.signal_register = MDLabel(text='', halign='center', theme_text_color='Custom', text_color=(1,0.35,0.12,1))

        btn_register_user = MDFillRoundFlatButton(text='Registrarse', pos_hint={'center_x':0.5})
        btn_register_user.bind(on_release=self.register)

        btn_back = MDFillRoundFlatButton(text='Volver', pos_hint={'center_x':0.5})
        btn_back.bind(on_release=lambda x: setattr(self.sm, 'current', 'login'))

        register_layout.add_widget(MDLabel(text='Registro', halign='center', font_style='H4'))
        register_layout.add_widget(self.new_user)
        register_layout.add_widget(self.new_password)
        register_layout.add_widget(self.new_password_two)
        register_layout.add_widget(self.signal_register)
        register_layout.add_widget(btn_register_user)
        register_layout.add_widget(btn_back)

        register_screen = Screen(name='register')
        register_screen.add_widget(register_layout)
        self.sm.add_widget(register_screen)

    # -------------------- Menu --------------------
    def build_menu(self):
        layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
        btn_chat = MDFillRoundFlatButton(text='Asistente virtual')
        btn_chat.bind(on_release=lambda x: setattr(self.sm, 'current', 'chat'))

        btn_devices = MDFillRoundFlatButton(text='Dispositivos')
        btn_devices.bind(on_release=lambda x: setattr(self.sm, 'current', 'devices'))

        btn_history = MDFillRoundFlatButton(text='Historial')
        btn_history.bind(on_release=lambda x: setattr(self.sm, 'current', 'history'))

        layout.add_widget(MDLabel(text='Menú', halign='center', font_style='H4'))
        layout.add_widget(btn_chat)
        layout.add_widget(btn_devices)
        layout.add_widget(btn_history)

        menu_screen = Screen(name='menu')
        menu_screen.add_widget(layout)
        self.sm.add_widget(menu_screen)

    # -------------------- Chat --------------------
    def build_chat(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.chat_log = MDLabel(text='', halign='left', size_hint_y=None, markup=True)
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))

        self.scroll = ScrollView(size_hint=(1, 1))
        self.scroll.add_widget(self.chat_log)

        self.chat_input = MDTextField(hint_text='Escribe un mensaje...')
        btn_send = MDFillRoundFlatButton(text='Enviar', size_hint_y=None, height=40)
        btn_send.bind(on_release=self.send_message)

        btn_back = MDFillRoundFlatButton(text='Volver', size_hint_y=None, height=40)
        btn_back.bind(on_release=lambda x: setattr(self.sm, 'current', 'menu'))

        layout.add_widget(self.scroll)
        layout.add_widget(self.chat_input)
        layout.add_widget(btn_send)
        layout.add_widget(btn_back)

        chat_screen = Screen(name='chat')
        chat_screen.add_widget(layout)
        self.sm.add_widget(chat_screen)

    # -------------------- Devices --------------------
    def build_devices(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.device_input = MDTextField(hint_text='Nombre del dispositivo')
        self.device_number = MDTextField(hint_text='Número de celular')
        # La variable self.device_code se mantiene para que la función add_device no falle,
        # pero el campo de texto ya no se muestra al usuario.
        self.device_code = MDTextField(hint_text='Introducir código (método directo)')

        self.devices_list = MDLabel(text='', halign='left', size_hint_y=None)
        
        devices_scroll_view = ScrollView(size_hint=(1, 1))
        self.devices_list_widget = MDList()
        devices_scroll_view.add_widget(self.devices_list_widget)

        # Se ha eliminado el layout horizontal y el botón "Agregar Directo".
        # Ahora solo hay un botón para el flujo de verificación.
        btn_add_with_verification = MDFillRoundFlatButton(text='Agregar y Verificar Dispositivo')
        btn_add_with_verification.bind(on_release=self.prompt_for_verification_code)
        
        btn_back = MDFillRoundFlatButton(text='Volver')
        btn_back.bind(on_release=lambda x: setattr(self.sm, 'current', 'menu'))

        layout.add_widget(MDLabel(text='Dispositivos', halign='center', font_style='H4'))
        layout.add_widget(self.device_input)
        layout.add_widget(self.device_number)
        
        # El campo de texto para el código directo ya no se añade al layout.
        # layout.add_widget(self.device_code) 
        
        # Se añade directamente el único botón de agregar.
        layout.add_widget(btn_add_with_verification)
        
        layout.add_widget(devices_scroll_view)
        layout.add_widget(btn_back)

        devices_screen = Screen(name='devices')
        devices_screen.add_widget(layout)
        self.sm.add_widget(devices_screen)

    # -------------------- History --------------------
    def build_history(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        self.scroll_history = ScrollView(size_hint=(1,1))
        self.history_list = MDList()
        self.scroll_history.add_widget(self.history_list)

        btn_back = MDFillRoundFlatButton(text='Volver')
        btn_back.bind(on_release=lambda x: setattr(self.sm, 'current', 'menu'))

        layout.add_widget(MDLabel(text='Historial', halign='center', font_style='H4'))
        layout.add_widget(self.scroll_history)
        layout.add_widget(btn_back)

        history_screen = Screen(name='history')
        history_screen.add_widget(layout)
        self.sm.add_widget(history_screen)

        predef_chats = [
            {"title":"Conversación cotidiana", "preview":"Usuario1: ¡Hola! ...", "alert":False, "full_content": "Usuario1: ¡Hola! ¿Cómo estás?\nUsuario2: ¡Hola! Muy bien, ¿y tú?\nUsuario1: Genial, aquí viendo una peli."},
            {"title":"Mensaje sospechoso", "preview":"Adulto desconocido: Hey ...", "alert":True, "full_content": "Adulto desconocido: Hey, vi tu perfil y me pareces muy interesante. ¿No eres muy joven para estar aquí?\nUsuario: Tengo 14.\nAdulto desconocido: Genial, a mí me gustan jóvenes. No le digas a nadie que hablamos."},
            {"title":"Intento manipulación", "preview":"Adulto desconocido: Todos ...", "alert":True, "full_content": "Adulto desconocido: Todos tus amigos te van a dejar de lado si no haces lo que te digo. Solo yo soy tu amigo de verdad.\nUsuario: No lo sé...\nAdulto desconocido: Confía en mí."},
            {"title":"Bullying", "preview":"Usuario1: Vi tus fotos ...", "alert":True, "full_content": "Usuario1: Vi tus fotos y das pena ajena.\nUsuario2: ¿Por qué dices eso?\nUsuario1: Porque es la verdad, todos en la escuela se ríen de ti."},
            {"title":"Amigos normales", "preview":"Usuario1: ¿Quieres jugar ...", "alert":False, "full_content": "Usuario1: ¿Quieres jugar videojuegos más tarde?\nUsuario2: ¡Claro! ¿A las 5?\nUsuario1: Perfecto, nos vemos."}
        ]
        self.history = predef_chats
        self.update_history_list()

    def update_history_list(self):
        self.history_list.clear_widgets()
        for chat in self.history:
            alert_symbol = "⚠️ " if chat.get("alert") else ""
            item_text = f"{alert_symbol}{chat.get('title')}: {chat.get('preview')}"
            
            chat_content = chat.get("full_content", "No hay contenido detallado.")
            
            list_item_props = {
                'text': item_text,
                'on_release': lambda x, content=chat_content: self.show_chat_detail(content)
            }
            
            if chat.get("alert"):
                list_item_props['theme_text_color'] = 'Custom'
                list_item_props['text_color'] = (1, 0.3, 0.3, 1)

            list_item = OneLineAvatarIconListItem(**list_item_props)
            self.history_list.add_widget(list_item)
            
    def show_chat_detail(self, content):
        self.chat_detail_screen.detail_label.text = content
        self.sm.current = 'chat_detail'

    # -------------------- Funciones --------------------
    def login(self, instance):
        userx = self.user.text.strip()
        passwordx = self.password.text.strip()
        state = False

        try:
            data = requests.get(self.url + ".json?auth=" + self.key).json() or {}
            for _, value in data.items():
                if isinstance(value, dict) and userx == value.get('User'):
                    hashed_input = hashlib.sha256(passwordx.encode()).hexdigest()
                    if hashed_input == value.get('Password'):
                        state = True
                        self.signal.text = '¡Login exitoso!'
                        break
                    else:
                        self.signal.text = 'Contraseña incorrecta'
                        break
            if not state and self.signal.text not in ['Contraseña incorrecta']:
                self.signal.text = 'Usuario incorrecto'
        except Exception as e:
            self.signal.text = 'Error al conectarse'
            print(e)

        self.password.text = ''

        if state:
            self.sm.current = 'menu'

    def register(self, instance):
        userx = self.new_user.text.strip()
        pass1 = self.new_password.text.strip()
        pass2 = self.new_password_two.text.strip()
        state = ''

        if pass1 != pass2:
            state = 'Las contraseñas no coinciden'
        elif len(userx) < 4:
            state = 'El usuario debe tener al menos 4 caracteres'
        elif len(pass1) < 4:
            state = 'La contraseña debe tener al menos 4 caracteres'
        else:
            try:
                data = requests.get(self.url + ".json?auth=" + self.key).json() or {}
                if any(isinstance(v, dict) and v.get('User') == userx for v in data.values()):
                    state = 'El usuario ya existe'
                else:
                    hashed_password = hashlib.sha256(pass1.encode()).hexdigest()
                    requests.patch(
                        self.url + ".json?auth=" + self.key,
                        json={userx: {"User": userx, "Password": hashed_password}}
                    )
                    state = 'Registrado correctamente'
            except Exception as e:
                state = 'Error al conectarse'
                print(e)

        self.signal_register.text = state
        self.new_user.text = ''
        self.new_password.text = ''
        self.new_password_two.text = ''

    def send_message(self, instance):
        user_msg = self.chat_input.text.strip()
        if not user_msg:
            return

        full_chat_so_far = self.chat_log.text
        full_chat_so_far += f"[b]Tú:[/b] {user_msg}\n"
        self.chat_log.text = full_chat_so_far

        headers = {"Content-Type": "application/json"}
        payload = json.dumps({"contents": [{"parts": [{"text": user_msg}]}]})

        try:
            resp = requests.post(GEMINI_URL, headers=headers, data=payload)
            resp.raise_for_status()
            resp_json = resp.json()

            if "candidates" in resp_json:
                gemini_reply = resp_json["candidates"][0]["content"]["parts"][0]["text"]
                self.chat_log.text += f"[b]Asistente:[/b] {gemini_reply}\n"
                full_chat_so_far += f"[b]Asistente:[/b] {gemini_reply}\n"
            else:
                error_message = resp_json.get("error", {}).get("message", "Respuesta inválida.")
                self.chat_log.text += f"[b]Error:[/b] {error_message}\n"
        except Exception as e:
            self.chat_log.text += f"[b]Error de Conexión:[/b] {e}\n"

        self.history.insert(0, {
            "title":"Chat reciente",
            "preview": user_msg[:30] + "...",
            "alert":False,
            "full_content": full_chat_so_far.replace('[b]', '').replace('[/b]', '')
        })
        self.update_history_list()

        self.chat_input.text = ''
        self.scroll.y = 0

    def add_device(self, instance):
        name = self.device_input.text.strip()
        number = self.device_number.text.strip()
        code = self.device_code.text.strip()
        
        if name and number and code:
            device_text = f"{name} ({number}) - Código: {code}"
            list_item = OneLineAvatarIconListItem(text=device_text)
            delete_icon = IconRightWidget(icon="trash-can-outline")
            delete_icon.bind(on_release=lambda x, item=list_item: self.delete_device(item))
            list_item.add_widget(delete_icon)
            self.devices_list_widget.add_widget(list_item)
            self.device_input.text = ''
            self.device_number.text = ''
            self.device_code.text = ''
        else:
            self.show_alert_dialog("Atención", "Para el método directo, todos los campos son obligatorios.")

    # *** AÑADIDO: Nueva función para iniciar el flujo del diálogo de verificación ***
    def prompt_for_verification_code(self, instance):
        name = self.device_input.text.strip()
        number = self.device_number.text.strip()

        if not name or not number:
            self.show_alert_dialog("Atención", "Para agregar con verificación, el nombre y el número son obligatorios.")
            return

        # Crear el contenido del diálogo
        content_layout = BoxLayout(orientation="vertical", spacing="10dp", size_hint_y=None)
        content_layout.add_widget(MDLabel(text="Esperando código..."))
        self.code_input_field = MDTextField(
            hint_text="Código de 4 dígitos",
            max_text_length=4,
            input_filter="int"
        )
        content_layout.add_widget(self.code_input_field)

        # Crear y mostrar el diálogo
        if self.dialog and hasattr(self.dialog, 'is_open') and self.dialog.is_open: self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Verificar Dispositivo",
            type="custom",
            content_cls=content_layout,
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(
                    text="ACEPTAR", 
                    on_release=lambda x: self.finalize_device_addition(name, number)
                ),
            ],
        )
        self.dialog.open()

    # *** AÑADIDO: Nueva función que se ejecuta al presionar ACEPTAR en el diálogo ***
    def finalize_device_addition(self, name, number):
        code = self.code_input_field.text.strip()
        
        if len(code) != 4:
            self.show_alert_dialog("Error de Código", "El código debe tener exactamente 4 dígitos.")
            return
        
        self.dialog.dismiss()
        
        device_text = f"{name} ({number}) - Verificado con: {code}"
        list_item = OneLineAvatarIconListItem(text=device_text)
        delete_icon = IconRightWidget(icon="trash-can-outline")
        delete_icon.bind(on_release=lambda x, item=list_item: self.delete_device(item))
        list_item.add_widget(delete_icon)
        self.devices_list_widget.add_widget(list_item)
        
        self.device_input.text = ""
        self.device_number.text = ""
        self.device_code.text = ""
        self.show_alert_dialog("Éxito", f"Dispositivo '{name}' verificado y agregado.")

    def delete_device(self, device_item):
        self.devices_list_widget.remove_widget(device_item)

    def block_multimedia(self):
        self.show_alert_dialog("Confirmación", "El contenido multimedia de este chat ha sido bloqueado.")

    def block_contact(self):
        self.show_alert_dialog("Confirmación", "El contacto ha sido bloqueado y no podrá enviarte más mensajes.")

    def show_alert_dialog(self, title, text):
        # *** AÑADIDO: Pequeña mejora para cerrar diálogos existentes antes de abrir uno nuevo ***
        if self.dialog and hasattr(self.dialog, 'is_open') and self.dialog.is_open:
            self.dialog.dismiss()
            
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="CERRAR",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ],
        )
        self.dialog.open()

# -------------------- Run App --------------------
if __name__ == '__main__':
    MainApp().run()