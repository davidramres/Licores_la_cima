from tkinter import messagebox, ttk
from tkinter import *
import pandas as pd
import sqlite3
import controladores2 as controladores
import modelos
from PIL import Image, ImageTk


# Crear conexión a la base de datos
conexion = sqlite3.connect("La_cima.db")
cursor = conexion.cursor()
class Menu_principal():    
    def __init__(self):
        # creando ventana principal con titulo, tamaño y colorz
        self.ventana = Tk()
        self.ventana.title("Licores La cima")
        self.ventana.geometry("1000x600")
        self.ventana.config(bg="black")
       # Cargar la imagen de fondo
        imagen = Image.open("cima.png")
        self.imagen_fondo = ImageTk.PhotoImage(imagen)
        self.ventana.iconbitmap("icono.ico")
        # Crear un widget de etiqueta para la imagen de fond        
        self.ventana.withdraw()  
        self.clase_producto = modelos.Producto(0, "", 0, 0, "") 
        self.controlador = controladores.Controlador()
        self.total_producto = 0
        self.clase_venta = modelos.Venta("", 0, 0, 0)
        self.clase_Detalle = modelos.DetalleVenta(0, 0, 0, 0, 0.0, 0.0)
        self.clase_cliente = modelos.Cliente(0, "", "", "")
        self.clase_empleado = modelos.Empleado(0, "", "", "")
        self.imagen_fondo = self.imagen_fondo         
        # Crear la ventana de inicio de sesión 
        ventana_inicio = Toplevel() 
        ventana_inicio.title("Inicio de Sesión") 
        fondo = Label(ventana_inicio, image=self.imagen_fondo)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)
        ventana_inicio.geometry("300x200")
        ventana_inicio.iconbitmap("icono.ico")
        # Crear los widgets de la ventana de inicio de sesión
        label_usuario = Label(ventana_inicio, text="Usuario:") 
        label_usuario.pack(pady=5) 
        entrada_usuario = Entry(ventana_inicio) 
        entrada_usuario.pack(pady=5) 
        label_contraseña = Label(ventana_inicio, text="Contraseña:") 
        label_contraseña.pack(pady=5) 
        entrada_contraseña = Entry(ventana_inicio, show="*") 
        entrada_contraseña.pack(pady=5)
        boton_inicio = Button(ventana_inicio, text="Iniciar Sesión", command=lambda: self.controlador.verificar_usuario(self.ventana, ventana_inicio, entrada_usuario.get(), entrada_contraseña.get())) 
        boton_inicio.pack(pady=20)        
        #creando barra de menu
        menu_bar = Menu(self.ventana)
        # Agregar el menu a la ventana
        self.ventana.config(menu=menu_bar)
        # Crear el menu General para la barra de menu
        menu_general = Menu(self.ventana, tearoff=0)
        # agregando opciones a la barra de menu
        menu_general.add_command(label="Inventario Bajo", command=self.menu_inventario_bajo)
        menu_general.add_command(label="Empleados", command=self.menu_empleados)
        menu_general.add_command(label="Clientes",command=self.menu_clientes)       
        menu_general.add_command(label="Salir", command=self.ventana.quit)
        # Agregar el menu general a la barra de menu
        menu_bar.add_cascade(label="General", menu=menu_general)        
        # Creando el marco izquierdo con borde solido y fuente de letra, va ubicado dentro de la ventana
        self.marco_izq = LabelFrame(self.ventana, text="Menu Principal", font=('Helvetica', 14, 'bold'), bd=2, relief="solid")
        fondo = Label(self.marco_izq, image=self.imagen_fondo)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)
        #ubicando el marco izquierdo en la cuadricula de la ventana con grid
        self.marco_izq.grid(row=0, column=0, sticky=N+S+E+W, padx=10, pady=10)
        
        #creamos una lista con las opciones que luego iran en combobox reportes
        opciones_combo=["Reporte de ventas totales","Reporte de ventas por fecha","Reporte de ventas por empleado","Reporte de ventas por cliente","Productos más vendidos","Productos menos vendidos"]
        # Agregando botones al marco izquierdo la funcion sticky es para que el boton se expanda cardinalmente
        Button(self.marco_izq, text="Productos", font=('Helvetica', 12, 'bold'), command=self.boton_productos).grid(row=0, column=0, sticky=N+S+E+W, padx=10, pady=15)
        Button(self.marco_izq, text="Ventas", command=self.boton_ventas, font=('Helvetica', 12, 'bold')).grid(row=1, column=0, sticky=N+S+E+W, padx=10, pady=15)
        Label(self.marco_izq, text="Reportes y Graficos").grid(row=2, column=0, sticky=N+S+E+W, padx=10, pady=10)
        combo_reportes=  ttk.Combobox(self.marco_izq, values=opciones_combo, state='readonly',width=30)
        combo_reportes.bind("<<ComboboxSelected>>",lambda event: self.manejar_reporte(combo_reportes.get()))
        combo_reportes.grid(row=3, column=0, sticky=N+S+E+W, padx=10, pady=1)

        # Creando el marco derecho con borde
        self.marco_der = LabelFrame(self.ventana, text="Area de gestión", font=('Helvetica', 14, 'bold'), bd=2, relief="solid")
        fondo = Label(self.marco_der, image=self.imagen_fondo)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)
        self.marco_der.grid(row=0, column=1, sticky=N+S+E+W, padx=10, pady=10)

        # Configurar la cuadrícula de la ventana principal para que el marco izquierdo ocupe la 1a columna y el marco derecho ocupe la  2a columna
        self.ventana.grid_rowconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(0, weight=1)
        self.ventana.grid_columnconfigure(1, weight=2)

        # Agregando un Treeview debajo de los marcos
        self.tabla_frame = Frame(self.ventana, bg="lightblue")
        self.tabla_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=N+S+E+W)
        self.tabla = ttk.Treeview(self.tabla_frame, columns=("nombre", "precio", "cantidad", "tipo"), show="headings")
        self.tabla.heading("nombre", text="Producto")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.heading("tipo", text="Tipo")        
        self.tabla.pack(fill=BOTH, expand=True)
        self.prod_seleccionado= self.tabla.item(self.tabla.selection())['text']#nos da solo la propiedad text del objeto Tree (tabla)
        self.ventana.grid_rowconfigure(1, weight=1)
        #llamamos al metodo mostrar productos para llenar la tabla al iniciar la aplicacion
        self.controlador.llenar_tabla(self.tabla, self.clase_producto)
        
        #creamos una ventana para mostrar el inventario bajo
        self.ventana_InventarioBajo = Toplevel(self.ventana)
        self.ventana_InventarioBajo.iconbitmap("icono.ico")
        self.ventana_InventarioBajo.withdraw()
        #hacemos la consulta a una de las vistas de la base de datos 
        cursor.execute('SELECT * FROM InventarioBajo')
        resultados = cursor.fetchall()
        #si hay productos en el inventario bajo
        if resultados:
            #mostramos un mensaje de confirmacion y lueho creamos la ventana
            messagebox.showinfo("Base de datos", "Hay productos en el inventario bajo")
            self.ventana_InventarioBajo.title("Inventario bajo")            
            self.ventana_InventarioBajo.geometry("400x200")            
            fondo = Label(self.ventana_InventarioBajo, image=self.imagen_fondo)
            fondo.place(x=0, y=0, relwidth=1, relheight=1)
            #creamos la lista con los productos que estan en el inventario bajo
            lista_inventario_bajo = Listbox(self.ventana_InventarioBajo, width=50, height=10)
            #recorremos la lista de productos para mostrarlos con su cantidad
            for producto in resultados:
                lista_inventario_bajo.insert(END, f"{producto[0]}  =  {producto[1]}")
            #mostramos la lista
            lista_inventario_bajo.pack()
            #mostramos la ventana
            self.ventana_InventarioBajo.deiconify()

    #funcion para mostrar productos en un TreeView
    def llenar_tabla_con_productos(self):
    # Limpia las columnas existentes
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text="")  # Elimina los encabezados
            self.tabla["columns"] = ("nombre", "precio", "cantidad", "tipo")

    # Configura los encabezados correctos para productos
            self.tabla.heading("nombre", text="Producto")
            self.tabla.heading("precio", text="Precio")
            self.tabla.heading("cantidad", text="Cantidad")
            self.tabla.heading("tipo", text="Tipo")
        self.clase_producto.mostrar_productos(self.tabla)
    #funcion para agregar productos
    def boton_productos(self):
        self.controlador.limpiar_marco(self.marco_der)  # Limpia el marco derecho para insertar los campos adecuados
    # Configurar los campos de entrada
        Label(self.marco_der, text="Producto:").grid(row=0, column=1, sticky=W+E, padx=10, pady=5)
        self.nombre_producto = Entry(self.marco_der, width=85)
        self.nombre_producto.grid(row=0, column=2, sticky=W+E, padx=10, pady=5)
        # Configurar los campos de entrada
        Label(self.marco_der, text="Precio:").grid(row=1, column=1, sticky=W+E, padx=10, pady=5)
        self.precio_producto = Entry(self.marco_der, width=85)
        self.precio_producto.grid(row=1, column=2, sticky=W+E, padx=10, pady=5)
        # Configurar los campos de entrada
        Label(self.marco_der, text="Cantidad:").grid(row=2, column=1, sticky=W+E, padx=10, pady=5)
        self.cantidad_producto = Entry(self.marco_der, width=85)
        self.cantidad_producto.grid(row=2, column=2, sticky=W+E, padx=10, pady=5)
        # Configurar los campos de entrada
        Label(self.marco_der, text="Tipo:").grid(row=3, column=1, sticky=W+E, padx=10, pady=5)
        self.tipo_producto = Entry(self.marco_der, width=85)
        self.tipo_producto.grid(row=3, column=2, sticky=W+E, padx=10, pady=5)
        # Configurar los botones
        Button(self.marco_der, text="Guardar", command=self.boton_guardar_producto).grid(row=4, column=2, sticky=W+E, padx=10, pady=5)
        Button(self.marco_der, text="Actualizar", command=self.boton_actualizar_producto).grid(row=5, column=2, sticky=W+E, padx=10, pady=5)
        Button(self.marco_der, text="Eliminar", command=self.boton_eliminar_producto).grid(row=6, column=2, sticky=W+E, padx=10, pady=5)
        
        # Eliminar el Treeview existente antes de crear uno nuevo
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()

        # Crear un nuevo Treeview con los encabezados para productos
        self.tabla = ttk.Treeview(self.tabla_frame, columns=("nombre", "precio", "cantidad", "tipo"), show="headings")
        self.tabla.heading("nombre", text="Producto")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.pack(fill=BOTH, expand=True)

        # Llenar la tabla con datos
        self.controlador.llenar_tabla(self.tabla, self.clase_producto)
        
    #metodo del boton guardar producto
    def boton_guardar_producto(self):
        #si los campos no estan vacios, osea si la validacion es verdadera llamamos al metodo agregar producto de la clase Producto del modulo licores que ya hemos instanciado
        if self.validacion():
            #llamamos al metodo y le pasamos los datos de los campos de texto de la interfaz grafica
            self.clase_producto.agregar_producto(self.nombre_producto.get(), self.precio_producto.get(), self.cantidad_producto.get(), self.tipo_producto.get())
            self.controlador.llenar_tabla(self.tabla, self.clase_producto)
        else:
            messagebox.showwarning("Advertencia", "Los campos no pueden estar vacios")
            
    #metodo para eliminar un producto         
    def boton_eliminar_producto(self): 
        #obtenemos el  producto seleccionado de la tabla
        prod_seleccionado = self.tabla.selection() 
        #si hay un producto seleccionado 
        if prod_seleccionado: 
            #obtenemos el nombre del producto desde el item seleccionado en la tabla y lo guardamos
            nombre = self.tabla.item(prod_seleccionado)['values'][0] 
            #llamamos al metodo eliminar producto de la clase Producto le pasamos el nombre del producto
            self.clase_producto.eliminar_producto(nombre) 
            #actualizamos la tabla para que muestre los cambios
            self.controlador.llenar_tabla(self.tabla, self.clase_producto) 
        else: 
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto")  
             
        #metodo para actualizar un producto    
    def boton_actualizar_producto(self):
        prod_seleccionado= self.tabla.selection()
        if prod_seleccionado:
            nombre_actual=self.tabla.item(prod_seleccionado)['values'][0]
            precio_actual= self.tabla.item(prod_seleccionado)['values'][1]
            cantidad_actual= self.tabla.item(prod_seleccionado)['values'][2]
            tipo_actual= self.tabla.item(prod_seleccionado)['values'][3] 
            #creamos la ventana
            self.ventana_edicion=Toplevel()
            self.ventana_edicion.title("Editar producto")
            self.ventana_edicion.iconbitmap("icono.ico")
            Label(self.ventana_edicion,text="Nombre actual:").grid(row=0, column= 1)
            self.nombre_actual= Entry(self.ventana_edicion, textvariable=StringVar(self.ventana_edicion,value=nombre_actual),state='readonly')
            self.nombre_actual.grid(row=0,column=2)
            Label(self.ventana_edicion,text="Nuevo nombre:").grid(row=1, column= 1)
            self.nuevo_nombre= Entry(self.ventana_edicion)
            self.nuevo_nombre.grid(row=1,column=2)
            Label(self.ventana_edicion,text="Precio actual:").grid(row=2, column= 1)
            self.precio_actual= Entry(self.ventana_edicion, textvariable=StringVar(self.ventana_edicion,value=precio_actual),state='readonly')
            self.precio_actual.grid(row=2,column=2)
            Label(self.ventana_edicion,text="Nuevo precio:").grid(row=3, column= 1)
            self.nuevo_precio= Entry(self.ventana_edicion)
            self.nuevo_precio.grid(row=3,column=2)
            Label(self.ventana_edicion,text="Cantidad actual:").grid(row=4, column= 1)
            self.cantidad_actual= Entry(self.ventana_edicion, textvariable=StringVar(self.ventana_edicion,value=cantidad_actual),state='readonly')
            self.cantidad_actual.grid(row=4,column=2)
            Label(self.ventana_edicion,text="Nuevo cantidad:").grid(row=5, column= 1)
            self.nueva_cantidad= Entry(self.ventana_edicion)
            self.nueva_cantidad.grid(row=5,column=2)
            Label(self.ventana_edicion,text="Tipo actual:").grid(row=6, column= 1)
            self.tipo_actual= Entry(self.ventana_edicion, textvariable=StringVar(self.ventana_edicion,value=tipo_actual),state='readonly')
            self.tipo_actual.grid(row=6,column=2)
            Label(self.ventana_edicion,text="Nuevo tipo:").grid(row=7, column= 1)
            self.nuevo_tipo= Entry(self.ventana_edicion)
            self.nuevo_tipo.grid(row=7,column=2)
            #boton para guardar los cambios
            self.controlador.llenar_tabla(self.tabla, self.clase_producto)            
            def guardar_cambios():
                # Llamamos al método de la clase Producto para actualizar los datos
                self.clase_producto.actualizar_producto(
                    nombre_actual,        
                    precio_actual,
                    cantidad_actual,
                    tipo_actual,
                    self.nuevo_nombre.get(),
                    self.nuevo_precio.get(),
                    self.nueva_cantidad.get(),
                    self.nuevo_tipo.get()
                )                
                # Cerramos la ventana a traves del metodo destroy
                self.ventana_edicion.destroy()
                self.controlador.llenar_tabla(self.tabla, self.clase_producto)
            Button(self.ventana_edicion, text="Guardar cambios", command=guardar_cambios).grid(row=8, column=2, sticky=W+E, padx=10, pady=5)
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto")
            
    # Boton de ventas
    def boton_ventas(self):
        self.controlador.limpiar_marco(self.marco_der)
        # Limpia las columnas existentes
        self.tabla["columns"] = ("fechaVenta", "totalVenta", "nombreCliente", "nombreEmpleado")
        # Configura los encabezados correctos para ventas
        self.tabla.heading("fechaVenta", text="Fecha", anchor=CENTER)
        self.tabla.heading("totalVenta", text="Total", anchor=CENTER)
        self.tabla.heading("nombreCliente", text="Cliente", anchor=CENTER)
        self.tabla.heading("nombreEmpleado", text="Empleado", anchor=CENTER)
        self.controlador.llenar_tabla_ventas(self.tabla, self.clase_venta)                    
        # Combobox de productos
        opciones_combo_productos = self.controlador.datos_comboclase("Producto")
        Label(self.marco_der, text="Producto:").grid(row=0, column=1, sticky=W+E, padx=10, pady=5)
        self.combo_productos = ttk.Combobox(self.marco_der, values=opciones_combo_productos, state='readonly')
        self.combo_productos.grid(row=0, column=2, sticky=W+E, padx=10, pady=5)
        self.combo_productos.bind("<<ComboboxSelected>>", self.actualizar_campos_producto)

        # Entradas para precio, cantidad y tipo
        Label(self.marco_der, text="Precio:").grid(row=1, column=1, sticky=W+E, padx=10, pady=5)
        self.precio_producto = Entry(self.marco_der, state='readonly')
        self.precio_producto.grid(row=1, column=2, sticky=W+E, padx=10, pady=5)
        # Entrada para la cantidad
        Label(self.marco_der, text="Cantidad:").grid(row=2, column=1, sticky=W+E, padx=10, pady=5)
        self.cantidad_producto = Entry(self.marco_der)
        self.cantidad_producto.grid(row=2, column=2, sticky=W+E, padx=10, pady=5)
        # Entrada para el tipo
        Label(self.marco_der, text="Tipo:").grid(row=3, column=1, sticky=W+E, padx=10, pady=5)
        self.tipo_producto = Entry(self.marco_der, state='readonly')
        self.tipo_producto.grid(row=3, column=2, sticky=W+E, padx=10, pady=5)

        # Combobox para clientes
        opciones_combo_clientes = self.controlador.datos_comboclase("Cliente")
        Label(self.marco_der, text="Cliente:").grid(row=4, column=1, sticky=W+E, padx=10, pady=5)
        self.combo_clientes = ttk.Combobox(self.marco_der, values=opciones_combo_clientes, state='readonly')
        self.combo_clientes.grid(row=4, column=2, sticky=W+E, padx=10, pady=5)

        # Combobox para empleados
        opciones_combo_empleados = self.controlador.datos_comboclase("Empleado")
        Label(self.marco_der, text="Empleado:").grid(row=5, column=1, sticky=W+E, padx=10, pady=5)
        self.combo_empleados = ttk.Combobox(self.marco_der, values=opciones_combo_empleados, state='readonly')
        self.combo_empleados.grid(row=5, column=2, sticky=W+E, padx=10, pady=5)

        # Botones de acción
        Button(self.marco_der, text="Agregar a Venta", command=self.agregar_a_venta).grid(row=6, column=2, sticky=W+E, padx=10, pady=5)
        Button(self.marco_der, text="Cancelar Venta", command=self.cancelar_venta).grid(row=7, column=2, sticky=W+E, padx=10, pady=5)
        Button(self.marco_der, text="Liquidar Venta", command=self.liquidar_venta).grid(row=8, column=2, sticky=W+E, padx=10, pady=5)

        # Tabla para detalles de venta
        self.tabla_venta = ttk.Treeview(self.marco_der, columns=("producto", "precio", "cantidad", "subtotal"), show="headings")
        self.tabla_venta.heading("producto", text="Producto")
        self.tabla_venta.heading("precio", text="Precio")
        self.tabla_venta.heading("cantidad", text="Cantidad")
        self.tabla_venta.heading("subtotal", text="Subtotal")
        self.tabla_venta.grid(row=9, column=1, columnspan=2, padx=10, pady=10)

    # Etiqueta para el total
        self.total_venta = 0
        self.etiqueta_total = Label(self.marco_der, text=f"Total: {self.total_venta}", font=("Arial", 12))
        self.etiqueta_total.grid(row=6, column=1, padx=10, pady=5)
    # Funciones para actualizar los campos
    def actualizar_campos_producto(self, event):
        producto_seleccionado = self.combo_productos.get()
        detalles_producto = self.controlador.obtener_detalles_producto(producto_seleccionado)
        if detalles_producto:
            self.precio_producto.config(state='normal')
            self.tipo_producto.config(state='normal')
            self.cantidad_producto.config(state='normal')
            self.cantidad_producto.delete(0, END)
            self.precio_producto.delete(0, END)
            self.tipo_producto.delete(0, END)
            self.cantidad_producto.insert(0, detalles_producto['cantidad'])
            self.precio_producto.insert(0, detalles_producto['precio'])
            self.tipo_producto.insert(0, detalles_producto['tipo'])
            self.precio_producto.config(state='readonly')
            self.tipo_producto.config(state='readonly')
            self.cantidad_producto.config(state='normal')
    # Función para agregar un producto a la venta
    def agregar_a_venta(self):
        producto = self.combo_productos.get()
        precio = float(self.precio_producto.get())
        cantidad = int(self.cantidad_producto.get())
        subtotal = precio * cantidad
        self.total_venta += subtotal
        self.etiqueta_total.config(text=f"Total: {self.total_venta} $")
        self.tabla_venta.insert("", "end", values=(producto, precio, cantidad, subtotal))
 
    def cancelar_venta(self):
        self.total_venta = 0
        self.etiqueta_total.config(text=f"Total: {self.total_venta} $")
        self.tabla_venta.delete(*self.tabla_venta.get_children())
        
    # Función para liquidar la venta
    def liquidar_venta(self):
        # Obtener datos del cliente y empleado
        cliente = self.combo_clientes.get()
        empleado = self.combo_empleados.get()
        # Validar que se haya seleccionado un cliente y un empleado
        if not cliente or not empleado:
            messagebox.showwarning("Error", "Debe seleccionar un cliente y un empleado")
            return
        codigo_cliente = self.controlador.obtener_codigo_cliente(cliente)
        codigo_empleado = self.controlador.obtener_codigo_empleado(empleado)
        fecha_actual = self.controlador.obtener_fecha()
        
        # Crear registro de venta
        nueva_venta = modelos.Venta(fecha_actual, self.total_venta, codigo_cliente, codigo_empleado)
        codigo_venta = nueva_venta.agregar_venta()  # Obtener el código de la nueva venta

        if codigo_venta is None:
            messagebox.showerror("Base de datos", "No se pudo obtener el código de la nueva venta.")
            return

        # Guardar detalles de venta y actualizar la cantidad de productos vendidos
        detalles_venta = self.tabla_venta.get_children()
        for item in detalles_venta:
            nombre_producto = self.tabla_venta.item(item)["values"][0]
            codigo_producto = self.controlador.obtener_codigo_producto(nombre_producto)
            cantidad = int(self.tabla_venta.item(item)["values"][2])
            precio = float(self.tabla_venta.item(item)["values"][1])
            subtotal = precio * cantidad
            self.clase_Detalle.agregar_detalle_venta(codigo_venta, codigo_producto, cantidad, precio, subtotal)

        # Actualizar la cantidad de productos vendidos en la base de datos
        for item in detalles_venta:
            nombre_producto = self.tabla_venta.item(item)["values"][0]
            codigo_producto= self.controlador.obtener_codigo_producto(nombre_producto)
            cantidad = int(self.tabla_venta.item(item)["values"][2])
            self.clase_producto.actualizar_cantidad(codigo_producto, cantidad)

        # Limpiar la tabla de ventas
        self.tabla_venta.delete(*self.tabla_venta.get_children())
        self.total_venta = 0
        self.etiqueta_total.config(text=f"Total: {self.total_venta}")


        self.tabla["columns"] = ("fechaVenta", "totalVenta", "nombreCliente", "nombreEmpleado")
        self.tabla.heading("fechaVenta", text="Fecha", anchor=CENTER)
        self.tabla.heading("totalVenta", text="Total", anchor=CENTER)
        self.tabla.heading("nombreCliente", text="Cliente", anchor=CENTER)
        self.tabla.heading("nombreEmpleado", text="Empleado", anchor=CENTER)
        self.tabla.grid(row=10, column=1, columnspan=2, padx=10, pady=10)

        self.tabla_venta["columns"] = ("producto", "precio", "cantidad", "subtotal")
        self.tabla_venta.heading("producto", text="Producto", anchor=CENTER)
        self.tabla_venta.heading("precio", text="Precio", anchor=CENTER)
        self.tabla_venta.heading("cantidad", text="Cantidad", anchor=CENTER)
        self.tabla_venta.heading("subtotal", text="Subtotal", anchor=CENTER)
        self.tabla_venta.grid(row=10, column=1, columnspan=2, padx=10, pady=10)

        self.controlador.llenar_tabla_ventas(self.tabla, self.clase_venta)      
        
    #metodo del menu reportes
    def manejar_reporte(self, seleccion):
        def configurar_ventana_reporte(titulo):
            ventana_reporte = Toplevel()
            ventana_reporte.title(titulo)
            ventana_reporte.geometry("640x480")
            ventana_reporte.iconbitmap("icono.ico")
            fondo = ttk.Label(ventana_reporte, image=self.imagen_fondo)
            fondo.place(x=0, y=0, relwidth=1, relheight=1)
            return ventana_reporte

        if seleccion == "Productos más vendidos":
            controladores.Controlador.generar_reporte_mas_vendidos()
        elif seleccion == "Productos menos vendidos":
            controladores.Controlador.generar_reporte_menos_vendidos()
        elif seleccion == "Reporte de ventas totales":
            ventana_reporte = configurar_ventana_reporte("Reporte de Ventas Totales")
            controladores.Controlador.generar_reporte_ventas_totales(ventana_reporte, self.imagen_fondo)
        elif seleccion == "Reporte de ventas por fecha":
            ventana_reporte = configurar_ventana_reporte("Reporte de Ventas por Fecha")
            eti_fecha = Label(ventana_reporte, text="Ingrese la fecha:")
            eti_fecha.pack()
            fecha = Entry(ventana_reporte)
            fecha.pack()
            boton_generar = Button(ventana_reporte, text="Generar Reporte", command=lambda: controladores.Controlador.generar_reporte_ventas_fecha(fecha.get(), ventana_reporte, self.imagen_fondo))
            boton_generar.pack()
        elif seleccion == "Reporte de ventas por empleado":
            ventana_reporte = configurar_ventana_reporte("Reporte de Ventas por Empleado")
            eti_empleado = Label(ventana_reporte, text="Ingrese el nombre del empleado:")
            eti_empleado.pack()
            empleado = Entry(ventana_reporte)
            empleado.pack()
            boton_generar = Button(ventana_reporte, text="Generar Reporte", command=lambda: controladores.Controlador.generar_reporte_ventas_por_empleado(empleado.get(), ventana_reporte, self.imagen_fondo))
            boton_generar.pack()
        elif seleccion == "Reporte de ventas por cliente":
            ventana_reporte = configurar_ventana_reporte("Reporte de Compras por Cliente")
            eti_cliente = Label(ventana_reporte, text="Ingrese el nombre del cliente:")
            eti_cliente.pack()
            cliente = Entry(ventana_reporte)
            cliente.pack()
            boton_generar = Button(ventana_reporte, text="Generar Reporte", command=lambda: controladores.Controlador.generar_reporte_ventas_por_cliente(cliente.get(), ventana_reporte, self.imagen_fondo))
            boton_generar.pack()
        else:
            messagebox.showinfo("Reporte", "Seleccione un reporte válido.")


    def menu_inventario_bajo(self):
        ventana_inventario_bajo = Toplevel()
        ventana_inventario_bajo.title("Inventario Bajo")
        ventana_inventario_bajo.geometry("480x360")
        ventana_inventario_bajo.iconbitmap("icono.ico")
        fondo = Label(ventana_inventario_bajo, image=self.imagen_fondo)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)

        etiqueta = Label(ventana_inventario_bajo, text="Productos con Inventario Bajo", font=("Arial", 16))
        etiqueta.pack()

        tree = ttk.Treeview(ventana_inventario_bajo)
        tree["columns"] = ( "nombre", "precio", "cantidad", "tipo")
        tree.column("#0", width=0, stretch=NO)
        tree.column("nombre", width=150, anchor=CENTER)
        tree.column("precio", width=100, anchor=CENTER)
        tree.column("cantidad", width=100, anchor=CENTER)
        tree.column("tipo", width=100, anchor=CENTER)
        tree.heading("nombre", text="Nombre")
        tree.heading("precio", text="Precio")
        tree.heading("cantidad", text="Cantidad")
        tree.heading("tipo", text="Tipo")
        tree.pack(fill=BOTH, expand=True)

    # Obtener productos con inventario bajo y mostrarlos en el Treeview
        conexion = sqlite3.connect("La_cima.db") 
        cursor = conexion.cursor() 
        cursor.execute("SELECT nombre, precio, cantidad, tipo FROM Producto WHERE cantidad < 25")
        productos_bajo_inventario = cursor.fetchall() 
        for row in productos_bajo_inventario:
            tree.insert("", "end", values=row) 
            conexion.close() 
        def exportar_csv(): 
            nombre_archivo = "inventario_bajo.csv" 
            df = pd.DataFrame(productos_bajo_inventario, columns=["Nombre", "Precio", "Cantidad", "Tipo"]) 
            df.to_csv(nombre_archivo, index=False) 
            messagebox.showinfo("Exportar CSV", f"Inventario bajo exportado como {nombre_archivo}") 
            
        boton_exportar = Button(ventana_inventario_bajo, text="Exportar a CSV", command=exportar_csv) 
        boton_exportar.pack() 
        Button(ventana_inventario_bajo, text="Salir", command=ventana_inventario_bajo.destroy).pack()

                       
    #metodo del menu clientes
    def menu_clientes(self):
    # Limpia las columnas existentes
        self.tabla["columns"] = ("nombre", "direccion", "telefono")
    # Configura los encabezados correctos para clientes
        self.tabla.heading("nombre", text="Cliente")
        self.tabla.heading("direccion", text="Dirección")
        self.tabla.heading("telefono", text="Teléfono")
    # Llama al método para llenar la tabla
        self.controlador.llenar_tabla_clientes(self.tabla, self.clase_cliente)
        self.controlador.limpiar_marco(self.marco_der)       
        # Añadir etiquetas y entrys en el marco izquierdo usando grid para ubicarlos 
        Label(self.marco_der, text="Nombre:").grid(row=0, column=1, sticky=W+E, padx=10, pady=5)
        #guardamos la informacion de los cuadros de txto en variables
        self.nombre_cliente = Entry(self.marco_der,width=85)
        self.nombre_cliente.grid(row=0, column=2, sticky=W+E, padx=10, pady=5)
        Label(self.marco_der, text="Direccion:").grid(row=1, column=1, sticky=W+E, padx=10, pady=5)
        self.direccion_cliente = Entry(self.marco_der,width=85)
        self.direccion_cliente.grid(row=1, column=2, sticky=W+E, padx=10, pady=5)
        Label(self.marco_der, text="Telefono:").grid(row=2, column=1, sticky=W+E, padx=10, pady=5)
        self.telefono_cliente = Entry(self.marco_der,width=85)
        self.telefono_cliente.grid(row=2, column=2, sticky=W+E, padx=10, pady=5)
        Button(self.marco_der, text="Guardar", command=self.boton_guardar_cliente).grid(row=4, column=2, sticky=W+E, padx=10, pady=5)
        Button(self.marco_der, text="Actualizar", command=self.boton_actualizar_cliente).grid(row=5, column=2, sticky=W+E, padx=10, pady=5)#
        Button(self.marco_der, text="Eliminar", command=self.boton_eliminar_cliente).grid(row=6, column=2, sticky=W+E, padx=10, pady=5)
        # Agregar el marco izquierdo al marco principal
        self.tabla_frame = Frame(self.ventana, bg="lightblue")
        self.tabla_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=N+S+E+W)
        # Crear la tabla
        self.tabla = ttk.Treeview(self.tabla_frame, columns=("nombre", "direccion", "telefono"), show="headings")
        self.tabla.heading("nombre", text="Cliente")
        self.tabla.heading("direccion", text="Direccion")
        self.tabla.heading("telefono", text="Telefono")      
        self.tabla.pack(fill=BOTH, expand=True)
        self.cli_seleccionado= self.tabla.item(self.tabla.selection())['text']#nos da solo la propiedad text del objeto Tree (tabla)
        self.ventana.grid_rowconfigure(1, weight=1)
        #llamamos al metodo mostrar productos para llenar la tabla al iniciar la aplicacion
        self.controlador.llenar_tabla_clientes(self.tabla, self.clase_cliente)
    
    #metodo para guardar clientes
    def boton_guardar_cliente(self):
        if len(self.nombre_cliente.get()) != 0 and len(self.direccion_cliente.get()) !=0 and len(self.telefono_cliente.get() ) !=0 :
            self.clase_cliente.agregar_cliente(self.nombre_cliente.get(), self.direccion_cliente.get(), self.telefono_cliente.get())
            self.controlador.llenar_tabla_clientes(self.tabla, self.clase_cliente)
        else:
            messagebox.showinfo("Error", "Por favor, complete todos los campos.")  
    #metodo para actualizar clientes
    def boton_actualizar_cliente(self):
        cli_seleccionado= self.tabla.selection()
        if cli_seleccionado:
            nombre_actual=self.tabla.item(cli_seleccionado)['values'][0]
            direccion_actual= self.tabla.item(cli_seleccionado)['values'][1]
            telefono_actual= self.tabla.item(cli_seleccionado)['values'][2]
            #creamos la ventana
            self.ventana_edicion=Toplevel()
            self.ventana_edicion.title("Editar cliente")
            self.ventana_edicion.iconbitmap("icono.ico")
            fondo = Label(self.ventana_edicion, image=self.imagen_fondo)
            fondo.place(x=0, y=0, relwidth=1, relheight=1)
            Label(self.ventana_edicion,text="Nombre actual:").grid(row=0, column= 1)
            self.nombre_actual= Entry(self.ventana_edicion, textvariable=StringVar(self.ventana_edicion,value=nombre_actual),state='readonly')
            self.nombre_actual.grid(row=0,column=2)
            Label(self.ventana_edicion,text="Nuevo nombre:").grid(row=1, column= 1)
            self.nuevo_nombre= Entry(self.ventana_edicion)
            self.nuevo_nombre.grid(row=1,column=2)
            Label(self.ventana_edicion,text="Direccion actual:").grid(row=2, column= 1)
            self.direccion_actual= Entry(self.ventana_edicion, textvariable=StringVar(self.ventana_edicion,value=direccion_actual),state='readonly')
            self.direccion_actual.grid(row=2,column=2)
            Label(self.ventana_edicion,text="Nueva direccion:").grid(row=3, column= 1)
            self.nueva_direccion= Entry(self.ventana_edicion)
            self.nueva_direccion.grid(row=3,column=2)
            Label(self.ventana_edicion,text="Telefono actual:").grid(row=4, column= 1)
            self.telefono_actual= Entry(self.ventana_edicion, textvariable=StringVar(self.ventana_edicion,value=telefono_actual),state='readonly')
            self.telefono_actual.grid(row=4,column=2)
            Label(self.ventana_edicion,text="Nuevo telefono:").grid(row=5, column= 1)
            self.nuevo_telefono= Entry(self.ventana_edicion)
            self.nuevo_telefono.grid(row=5,column=2)
            #creamos el boton
            def guardar_cambios():
                # Llamamos al método de la clase Producto para actualizar los datos
                self.clase_cliente.editar_cliente(nombre_actual,direccion_actual,telefono_actual,self.nuevo_nombre.get(),self.nueva_direccion.get(),self.nuevo_telefono.get())                
                # Cerramos la ventana a traves del metodo destroy
                self.controlador.llenar_tabla_clientes(self.tabla, self.clase_cliente)
                self.ventana_edicion.destroy()                
            Button(self.ventana_edicion, text="Guardar cambios", command=guardar_cambios).grid(row=8, column=2, sticky=W+E, padx=10, pady=5)
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente")
    #metodo para eliminar clientes
    def boton_eliminar_cliente(self): 
        #obtenemos el  cliente seleccionado de la tabla
        cli_seleccionado = self.tabla.selection() 
        #si hay un producto seleccionado 
        if cli_seleccionado: 
            #obtenemos el nombre del cliente desde el item seleccionado en la tabla y lo guardamos
            nombre = self.tabla.item(cli_seleccionado)['values'][0] 
            #llamamos al metodo eliminar producto de la clase Producto le pasamos el nombre del producto
            self.clase_cliente.eliminar_cliente(nombre) 
            #actualizamos la tabla para que muestre los cambios
            self.controlador.llenar_tabla_clientes(self.tabla, self.clase_cliente) 
        else: 
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente") 
        self.controlador.llenar_tabla_clientes(self.tabla, self.clase_cliente)   
    # metodo para menu de empleados
    def menu_empleados(self):
    # Limpia las columnas existentes
        self.tabla["columns"] = ("nombre", "direccion", "telefono")
    # Configura los encabezados correctos para clientes
        self.tabla.heading("nombre", text="Empleado")
        self.tabla.heading("direccion", text="Dirección")
        self.tabla.heading("telefono", text="Teléfono")
    # Llama al método para llenar la tabla
        self.controlador.llenar_tabla_empleados(self.tabla, self.clase_empleado)
        self.controlador.limpiar_marco(self.marco_der)       
        # Añadir etiquetas y entrys en el marco izquierdo usando grid para ubicarlos 
        Label(self.marco_der, text="Nombre:").grid(row=0, column=1, sticky=W+E, padx=10, pady=5)
        #guardamos la informacion de los cuadros de txto en variables
        self.nombre_empleado = Entry(self.marco_der,width=85)
        self.nombre_empleado.grid(row=0, column=2, sticky=W+E, padx=10, pady=5)
        Label(self.marco_der, text="Direccion:").grid(row=1, column=1, sticky=W+E, padx=10, pady=5)
        self.direccion_empleado = Entry(self.marco_der,width=85)
        self.direccion_empleado.grid(row=1, column=2, sticky=W+E, padx=10, pady=5)
        Label(self.marco_der, text="Telefono:").grid(row=2, column=1, sticky=W+E, padx=10, pady=5)
        self.telefono_empleado = Entry(self.marco_der,width=85)
        self.telefono_empleado.grid(row=2, column=2, sticky=W+E, padx=10, pady=5)
        Button(self.marco_der, text="Guardar", command=self.boton_guardar_empleado).grid(row=4, column=2, sticky=W+E, padx=10, pady=5)
        Button(self.marco_der, text="Actualizar", command=self.boton_actualizar_empleado).grid(row=5, column=2, sticky=W+E, padx=10, pady=5)#
        Button(self.marco_der, text="Eliminar", command=self.boton_eliminar_empleado).grid(row=6, column=2, sticky=W+E, padx=10, pady=5)
        # Agregar el marco izquierdo al marco principal
        self.tabla_frame = Frame(self.ventana, bg="lightblue")
        self.tabla_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=N+S+E+W)
        # Crear la tabla
        self.tabla = ttk.Treeview(self.tabla_frame, columns=("nombre", "direccion", "telefono"), show="headings")
        self.tabla.heading("nombre", text="Empleado")
        self.tabla.heading("direccion", text="Direccion")
        self.tabla.heading("telefono", text="Telefono")      
        self.tabla.pack(fill=BOTH, expand=True)
        self.emp_seleccionado= self.tabla.item(self.tabla.selection())['text']#nos da solo la propiedad text del objeto Tree (tabla)
        self.ventana.grid_rowconfigure(1, weight=1)
        #llamamos al metodo mostrar productos para llenar la tabla al iniciar la aplicacion
        self.controlador.llenar_tabla_empleados(self.tabla, self.clase_empleado)
    
    #metodo para guardar empleado
    def boton_guardar_empleado(self):
        if len(self.nombre_empleado.get()) != 0 and len(self.direccion_empleado.get()) !=0 and len(self.telefono_empleado.get() ) !=0 :
            self.clase_empleado.agregar_empleado(self.nombre_empleado.get(), self.direccion_empleado.get(), self.telefono_empleado.get())
            self.controlador.llenar_tabla_empleados(self.tabla, self.clase_empleado)
        else:
            messagebox.showinfo("Error", "Por favor, complete todos los campos.")  
    #metodo para actualizar empleado
    def boton_actualizar_empleado(self):
        emp_seleccionado= self.tabla.selection()
        if emp_seleccionado:
            nombre_actual=self.tabla.item(emp_seleccionado)['values'][0]
            direccion_actual= self.tabla.item(emp_seleccionado)['values'][1]
            telefono_actual= self.tabla.item(emp_seleccionado)['values'][2]
            #creamos la ventana
            self.ventana_edicion=Toplevel()
            self.ventana_edicion.title("Editar empleado")
            self.ventana_edicion.iconbitmap("icono.ico")
            fondo = Label(self.ventana_edicion, image=self.imagen_fondo)
            fondo.place(x=0, y=0, relwidth=1, relheight=1)
            Label(self.ventana_edicion,text="Nombre actual:").grid(row=0, column= 1)
            self.nombre_actual= Entry(self.ventana_edicion, textvariable=StringVar(self.ventana_edicion,value=nombre_actual),state='readonly')
            self.nombre_actual.grid(row=0,column=2)
            Label(self.ventana_edicion,text="Nuevo nombre:").grid(row=1, column= 1)
            self.nuevo_nombre= Entry(self.ventana_edicion)
            self.nuevo_nombre.grid(row=1,column=2)
            Label(self.ventana_edicion,text="Direccion actual:").grid(row=2, column= 1)
            self.direccion_actual= Entry(self.ventana_edicion, textvariable=StringVar(self.ventana_edicion,value=direccion_actual),state='readonly')
            self.direccion_actual.grid(row=2,column=2)
            Label(self.ventana_edicion,text="Nueva direccion:").grid(row=3, column= 1)
            self.nueva_direccion= Entry(self.ventana_edicion)
            self.nueva_direccion.grid(row=3,column=2)
            Label(self.ventana_edicion,text="Telefono actual:").grid(row=4, column= 1)
            self.telefono_actual= Entry(self.ventana_edicion, textvariable=StringVar(self.ventana_edicion,value=telefono_actual),state='readonly')
            self.telefono_actual.grid(row=4,column=2)
            Label(self.ventana_edicion,text="Nuevo telefono:").grid(row=5, column= 1)
            self.nuevo_telefono= Entry(self.ventana_edicion)
            self.nuevo_telefono.grid(row=5,column=2)
            #creamos el boton
            def guardar_cambios():
                # Llamamos al método de la clase Producto para actualizar los datos
                self.clase_empleado.editar_empleado(nombre_actual,direccion_actual,telefono_actual,self.nuevo_nombre.get(),self.nueva_direccion.get(),self.nuevo_telefono.get())                
                # Cerramos la ventana a traves del metodo destroy
                self.controlador.llenar_tabla_empleados(self.tabla, self.clase_empleado)
                self.ventana_edicion.destroy()                
            Button(self.ventana_edicion, text="Guardar cambios", command=guardar_cambios).grid(row=8, column=2, sticky=W+E, padx=10, pady=5)
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un empleado")
    #metodo para eliminar empleado
    def boton_eliminar_empleado(self): 
        #obtenemos el  cliente seleccionado de la tabla
        emp_seleccionado = self.tabla.selection() 
        #si hay un producto seleccionado 
        if emp_seleccionado: 
            #obtenemos el nombre del empleado desde el item seleccionado en la tabla y lo guardamos
            nombre = self.tabla.item(emp_seleccionado)['values'][0] 
            #llamamos al metodo eliminar producto de la clase Producto le pasamos el nombre del producto
            self.clase_empleado.eliminar_empleado(nombre) 
            #actualizamos la tabla para que muestre los cambios
            self.controlador.llenar_tabla_empleados(self.tabla, self.clase_empleado) 
        else: 
            messagebox.showwarning("Advertencia", "Debe seleccionar un empleado") 
        self.controlador.llenar_tabla_empleados(self.tabla, self.clase_empleado)  
      #metodo para validar que los campos no esten vacios
    def validacion(self):
        # validacion de que los campos no esten vacios por medio de la cantidad de elementos que hay en cada variable
        return len(self.nombre_producto.get()) != 0 and len(self.precio_producto.get()) !=0 and len(self.cantidad_producto.get()) !=0 and len(self.tipo_producto.get()) !=0  
     

#intanciamos la clase para que se ejecute
menu= Menu_principal()
#metodo para que la ventana se muestre en pantalla y se mantenga abierta
menu.ventana.mainloop()