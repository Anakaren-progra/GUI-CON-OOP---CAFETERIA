# login_ui.py
import customtkinter as ctk
from tkinter import messagebox
from backend_oop import AuthManager
from ui_gerente import GerenteUI
from ui_barista import BaristaUI
from ui_cliente import ClienteUI
from PIL import ImageTk, Image




class LoginUI:
    def __init__(self, ventana_inicio):
        self.ventana_inicio = ventana_inicio
        self.ventana_login = ctk.CTkToplevel(ventana_inicio)
        self.ventana_login.title("Login")
        

        self.ventana_login.geometry("400x300")
        self.ventana_login.withdraw()
        

        self.auth = AuthManager()
        self.crear_interfaz()

    def crear_interfaz(self):
        ctk.CTkLabel(self.ventana_login, text="Iniciar Sesión", font=("Arial", 20)).pack(pady=10)

        self.entry_email = ctk.CTkEntry(self.ventana_login, width=300, placeholder_text="Email")
        self.entry_contrasena = ctk.CTkEntry(self.ventana_login, width=300, show="*", placeholder_text="Contraseña")
        self.entry_email.pack(pady=5)
        self.entry_contrasena.pack(pady=5)

        ctk.CTkButton(self.ventana_login, text="Ingresar", command=self.iniciar_sesion).pack(pady=10)
        ctk.CTkButton(self.ventana_login, text="Volver", command=self.volver_a_inicio).pack(pady=5)

    def volver_a_inicio(self):
        self.ventana_login.destroy()  # Cerramos solo la ventana de login
        self.ventana_inicio.deiconify()  # Volvemos a mostrar la ventana principal

    def iniciar_sesion(self):
        email = self.entry_email.get()
        contrasena = self.entry_contrasena.get()

        tipo_usuario, nombre = self.auth.validar_login(email, contrasena)
        if tipo_usuario:
            messagebox.showinfo("Éxito", f"Bienvenido, {nombre}")
            self.ventana_login.withdraw()

            if tipo_usuario == "gerente":
                GerenteUI(self.ventana_login,nombre).mostrar()
            elif tipo_usuario == "barista":
                BaristaUI(self.ventana_login,nombre).mostrar()
            else:
                ClienteUI(self.ventana_login, nombre, email).mostrar()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    
