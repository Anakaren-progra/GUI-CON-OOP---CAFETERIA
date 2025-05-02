# main.py
import customtkinter as ctk
from tkinter import messagebox
from backend_oop import UsuarioManager, EmpleadoManager
from login_ui import LoginUI
from PIL import Image, ImageTk



# Configuración de apariencia
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# Instancias del backend
usuario_manager = UsuarioManager()
empleado_manager = EmpleadoManager()

# Ventana principal
ventana_inicio = ctk.CTk()
ventana_inicio.title("Sistema de Cafetería")
ventana_inicio.geometry("500x400")
ventana_inicio.iconbitmap("C:/Users/JK EVENTOS/OneDrive/Documentos/Python OOP/CAFE OOP/cafeteria_app/imagenes/taza.ico")

# Cargar la imagen de fondo
imagen_fondo = Image.open("C:/Users/JK EVENTOS/OneDrive/Documentos/Python OOP/CAFE OOP/cafeteria_app/imagenes/cafe_sinfondo.png")
imagen_fondo = imagen_fondo.resize((400, 350))  # Ajusta al tamaño de la ventana
fondo = ImageTk.PhotoImage(imagen_fondo)

# Crear un label que contenga la imagen
label_fondo = ctk.CTkLabel(ventana_inicio, image=fondo, text="")
label_fondo.place(x=0, y=50, relwidth=1, relheight=1)

# --------------------------
# Funciones para ventanas

def abrir_registro_cliente():
    ventana_inicio.withdraw()
    ventana = ctk.CTkToplevel()
    ventana.title("Registro de Cliente")
    ventana.geometry("400x500")
    
    

    def volver():
        ventana.destroy()
        ventana_inicio.deiconify()

    def registrar_usuario():
        nombre = entry_nombre.get()
        email = entry_email.get()
        contrasena = entry_contrasena.get()
        edad = entry_edad.get()

        if not nombre or not email or not contrasena or not edad:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            edad = int(edad)
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número válido")
            return

        usuario_manager.guardar_usuario(nombre, email, contrasena, edad)
        messagebox.showinfo("Éxito", "Cliente registrado correctamente")
        volver()

    ctk.CTkLabel(ventana, text="Registro de Cliente", font=("Arial", 20)).pack(pady=10)
    entry_nombre = ctk.CTkEntry(ventana, width=300, placeholder_text="Nombre")
    entry_email = ctk.CTkEntry(ventana, width=300, placeholder_text="Email")
    entry_contrasena = ctk.CTkEntry(ventana, width=300, show="*", placeholder_text="Contraseña")
    entry_edad = ctk.CTkEntry(ventana, width=300, placeholder_text="Edad")

    for widget in [entry_nombre, entry_email, entry_contrasena, entry_edad]:
        widget.pack(pady=5)

    ctk.CTkButton(ventana, text="Registrar", command=registrar_usuario).pack(pady=10)
    ctk.CTkButton(ventana, text="Volver", command=volver).pack(pady=5)


def abrir_registro_empleado():
    ventana_inicio.withdraw()
    ventana = ctk.CTkToplevel()
    ventana.title("Registro de Empleado")
    ventana.geometry("400x450")
    ventana.iconbitmap("C:/Users/JK EVENTOS/OneDrive/Documentos/Python OOP/CAFE OOP/cafeteria_app/imagenes/taza.ico")

    def volver():
        ventana.destroy()
        ventana_inicio.deiconify()

    def registrar_empleado():
        nombre = entry_nombre.get()
        email = entry_email.get()
        contrasena = entry_contrasena.get()
        rol = entry_rol.get()

        if not nombre or not email or not contrasena or not rol:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        empleado_manager.guardar_empleado(nombre, email, contrasena, rol)
        messagebox.showinfo("Éxito", "Empleado registrado correctamente")
        volver()

    ctk.CTkLabel(ventana, text="Registro de Empleado", font=("Arial", 20)).pack(pady=10)
    entry_nombre = ctk.CTkEntry(ventana, width=300, placeholder_text="Nombre")
    entry_email = ctk.CTkEntry(ventana, width=300, placeholder_text="Email")
    entry_contrasena = ctk.CTkEntry(ventana, width=300, show="*", placeholder_text="Contraseña")
    entry_rol = ctk.CTkEntry(ventana, width=300, placeholder_text="Rol (gerente, barista)")

    for widget in [entry_nombre, entry_email, entry_contrasena, entry_rol]:
        widget.pack(pady=5)

    ctk.CTkButton(ventana, text="Registrar", command=registrar_empleado).pack(pady=10)
    ctk.CTkButton(ventana, text="Volver", command=volver).pack(pady=5)


def abrir_login():
    ventana_inicio.withdraw()
    login = LoginUI(ventana_inicio)
    login.ventana_login.deiconify()
    
    


# --------------------------
# Interfaz de Inicio

#ctk.CTkLabel(ventana_inicio, text="Bienvenido a PANELA CANELA", font=("Arial", 20)).pack(pady=20)
ctk.CTkButton(ventana_inicio, text="Registrar Cliente", fg_color="#614f0c", command=abrir_registro_cliente).pack(pady=5)
ctk.CTkButton(ventana_inicio, text="Registrar Empleado", fg_color="#b49319", command=abrir_registro_empleado).pack(pady=5)
ctk.CTkButton(ventana_inicio, text="Iniciar Sesión", fg_color="#ff6b33",width=100,
    height=30,font=("Arial", 15), command=abrir_login).pack(pady=5)

ventana_inicio.mainloop()
