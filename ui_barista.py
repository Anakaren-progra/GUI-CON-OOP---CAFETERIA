# ui_barista.py
import customtkinter as ctk
from tkinter import messagebox
from backend_oop import BebidaManager, JSONStorage

class BaristaUI:
    def __init__(self,ventana_inicio, nombre):
        self.ventana_inicio = ventana_inicio
        self.nombre = nombre
        self.bebida_manager = BebidaManager()

        self.ventana = ctk.CTkToplevel()
        self.ventana.title("Entorno del Barista")
        self.ventana.geometry("600x500")

        self.crear_interfaz()

    def mostrar(self):
        self.ventana.deiconify()

    def crear_interfaz(self):
        ctk.CTkLabel(self.ventana, text=f"Bienvenido, {self.nombre}. Entorno del Barista", font=("Arial", 16)).pack(pady=10)

        self.tabs = ctk.CTkTabview(self.ventana)
        self.tabs.pack(pady=10, expand=True, fill="both")

        self.tab_registro = self.tabs.add("Registrar Producto")
        self.tab_productos = self.tabs.add("Productos Registrados")

        self.crear_tab_registro()
        self.crear_tab_productos()

        ctk.CTkButton(self.ventana, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=5)
    
    def cerrar_sesion(self):
        self.ventana.destroy()
        self.ventana_inicio.deiconify()


    # ------------------------------------
    def crear_tab_registro(self):
        self.entry_nombre = ctk.CTkEntry(self.tab_registro, width=400, placeholder_text="Nombre del producto")
        self.entry_ingredientes = ctk.CTkEntry(self.tab_registro, width=400, placeholder_text="Ingredientes (separados por coma)")
        self.entry_cantidades = ctk.CTkEntry(self.tab_registro, width=400, placeholder_text="Cantidades (ej. 50ml, 30gr)")
        self.combo_categoria = ctk.CTkOptionMenu(self.tab_registro, values=["Bebida fria", "Bebida caliente", "Postre"])
        self.combo_categoria.set("Bebida caliente")

        for widget in [self.entry_nombre, self.entry_ingredientes, self.entry_cantidades, self.combo_categoria]:
            widget.pack(pady=5)

        ctk.CTkButton(self.tab_registro, text="Registrar Producto", command=self.registrar_producto).pack(pady=10)

    def registrar_producto(self):
        nombre = self.entry_nombre.get().strip()
        ingredientes = [i.strip() for i in self.entry_ingredientes.get().split(",")]
        cantidades = [c.strip() for c in self.entry_cantidades.get().split(",")]
        categoria = self.combo_categoria.get()

        if not nombre or not ingredientes or not cantidades or not categoria:
            messagebox.showerror("Error", "Todos los campos deben estar llenos")
            return

        mensaje = self.bebida_manager.agregar_bebida(nombre, categoria, ingredientes, cantidades)
        messagebox.showinfo("Resultado", mensaje)
        self.actualizar_lista_productos()

    # ------------------------------------
    def crear_tab_productos(self):
        self.lista_bebidas = self.bebida_manager.cargar_bebidas()
        self.seleccion = ctk.StringVar()
        self.combo_bebidas = ctk.CTkOptionMenu(self.tab_productos, values=[b["nombre"] for b in self.lista_bebidas], variable=self.seleccion, command=lambda _: self.llenar_campos())
        self.combo_bebidas.pack(pady=10)

        self.entry_mod_nombre = ctk.CTkEntry(self.tab_productos, width=400, placeholder_text="Nombre")
        self.entry_mod_ingredientes = ctk.CTkEntry(self.tab_productos, width=400, placeholder_text="Ingredientes")
        self.entry_mod_cantidades = ctk.CTkEntry(self.tab_productos, width=400, placeholder_text="Cantidades")
        self.combo_mod_categoria = ctk.CTkOptionMenu(self.tab_productos, values=["Bebida fria", "Bebida caliente", "Postre"])
        self.combo_mod_categoria.set("Bebida caliente")

        for widget in [self.entry_mod_nombre, self.entry_mod_ingredientes, self.entry_mod_cantidades, self.combo_mod_categoria]:
            widget.pack(pady=5)

        ctk.CTkButton(self.tab_productos, text="Modificar Producto", command=self.modificar_producto).pack(pady=5)
        ctk.CTkButton(self.tab_productos, text="Eliminar Producto", command=self.eliminar_producto).pack(pady=5)
        ctk.CTkButton(self.tab_productos, text="Actualizar Lista", command=self.actualizar_lista_productos).pack(pady=5)

        if self.lista_bebidas:
            self.seleccion.set(self.lista_bebidas[0]["nombre"])
            self.llenar_campos()

    def llenar_campos(self):
        nombre = self.seleccion.get()
        for bebida in self.lista_bebidas:
            if bebida["nombre"] == nombre:
                self.entry_mod_nombre.delete(0, "end")
                self.entry_mod_ingredientes.delete(0, "end")
                self.entry_mod_cantidades.delete(0, "end")
                self.entry_mod_nombre.insert(0, bebida["nombre"])
                self.entry_mod_ingredientes.insert(0, ", ".join(bebida["ingredientes"]))
                self.entry_mod_cantidades.insert(0, ", ".join(bebida["cantidades"]))
                self.combo_mod_categoria.set(bebida["categoria"])
                break

    def modificar_producto(self):
        nombre_original = self.seleccion.get()
        nuevo_nombre = self.entry_mod_nombre.get()
        nuevos_ingredientes = [i.strip() for i in self.entry_mod_ingredientes.get().split(",")]
        nuevas_cantidades = [c.strip() for c in self.entry_mod_cantidades.get().split(",")]
        nueva_categoria = self.combo_mod_categoria.get()

        for bebida in self.lista_bebidas:
            if bebida["nombre"] == nombre_original:
                bebida["nombre"] = nuevo_nombre
                bebida["ingredientes"] = nuevos_ingredientes
                bebida["cantidades"] = nuevas_cantidades
                bebida["categoria"] = nueva_categoria
                JSONStorage.guardar("bebidas.json", self.lista_bebidas)
                messagebox.showinfo("Modificación", "Producto modificado con éxito")
                self.actualizar_lista_productos()
                return

    def eliminar_producto(self):
        nombre = self.seleccion.get()
        nuevas_bebidas = [b for b in self.lista_bebidas if b["nombre"] != nombre]

        if len(nuevas_bebidas) == len(self.lista_bebidas):
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        JSONStorage.guardar("bebidas.json", nuevas_bebidas)
        messagebox.showinfo("Eliminado", f"'{nombre}' eliminado con éxito")
        self.actualizar_lista_productos()

    def actualizar_lista_productos(self):
        self.lista_bebidas = self.bebida_manager.cargar_bebidas()
        nombres = [b["nombre"] for b in self.lista_bebidas]
        self.combo_bebidas.configure(values=nombres)

        if nombres:
            self.seleccion.set(nombres[0])
            self.llenar_campos()
        else:
            self.seleccion.set("")
            self.entry_mod_nombre.delete(0, "end")
            self.entry_mod_ingredientes.delete(0, "end")
            self.entry_mod_cantidades.delete(0, "end")
            self.combo_mod_categoria.set("Bebida caliente")
