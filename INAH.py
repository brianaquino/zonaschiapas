import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font 
import mysql.connector
import csv
from tkinter import  filedialog

# Modos de color
modo_claro = {
    "fondo": "gray95",
    "texto": "black",
    "entrada": "white",
    "tree_bg": "#AAB7B8",
    "tree_fg": "black"
}

modo_oscuro = {
    "fondo": "#2C3E50",
    "texto": "white",
    "entrada": "#34495E",
    "tree_bg": "#34495E",
    "tree_fg": "white"
}

modo_actual = modo_claro  # Empieza en modo claro

def aplicar_modo():
    # Fondo de ventana y frames
    ventana.config(bg=modo_actual["fondo"])
    frame_principal.config(bg=modo_actual["fondo"])
    frame_resultados.config(bg=modo_actual["fondo"])
    frame_botones.config(bg=modo_actual["fondo"])
    etiqueta_contador.config(bg=modo_actual["fondo"], fg=modo_actual["texto"])
    labelimagen.config(background=modo_actual["fondo"])

    # Labels
    for widget in frame_principal.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=modo_actual["fondo"], fg=modo_actual["texto"])
    
    # Entradas
    for widget in frame_principal.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.config(bg=modo_actual["entrada"], fg=modo_actual["texto"], insertbackground=modo_actual["texto"])

    # Treeview
    style.configure("Treeview", background=modo_actual["tree_bg"], foreground=modo_actual["tree_fg"])
    style.configure("Treeview.Heading", background=modo_actual["tree_bg"], foreground="black")
    treeview.tag_configure('dark', background=modo_actual["tree_bg"], foreground=modo_actual["tree_fg"])

    boton_modo.config(bg=modo_actual["fondo"])



def alternar_modo_con_icono():
    global modo_actual, icono_modo
    if modo_actual == modo_claro:
        modo_actual = modo_oscuro
        boton_modo.config(image=icono_sol)
        icono_modo = icono_sol
    else:
        modo_actual = modo_claro
        boton_modo.config(image=icono_luna)
        icono_modo = icono_luna
    aplicar_modo()



def cargar_datos(event):
    global item_actual
    item_actual = treeview.focus()
    
    if item_actual:
        valores = treeview.item(item_actual,'values')

    entrada_municipio.delete(0, tk.END)
    entrada_municipio.insert(0,valores[0])
    entrada_clave.delete(0, tk.END)
    entrada_clave.insert(0,valores[1])
    entrada_fichacatalogo.delete(0, tk.END)
    entrada_fichacatalogo.insert(0,valores[2])
    entrada_seccion.delete(0, tk.END)
    entrada_seccion.insert(0,valores[3])
    entrada_manzana.delete(0, tk.END)
    entrada_manzana.insert(0,valores[4])
    entrada_numero.delete(0, tk.END)
    entrada_numero.insert(0,valores[5])
    entrada_nombreedificio.delete(0, tk.END)
    entrada_nombreedificio.insert(0,valores[6])
    entrada_localizacion.delete(0, tk.END)
    entrada_localizacion.insert(0,valores[7])
    entrada_barrio.delete(0, tk.END)
    entrada_barrio.insert(0,valores[8])
    entrada_siglo.delete(0,tk.END)
    entrada_siglo.insert(0,valores[9])
    entrada_catalogada.delete(0,tk.END)
    entrada_catalogada.insert(0,valores[10])
    entrada_decretada.delete(0,tk.END)
    entrada_decretada.insert(0,valores[11])
    entrada_uso.delete(0, tk.END)
    entrada_uso.insert(0,valores[12])
    entrada_niveles.delete(0,tk.END)
    entrada_niveles.insert(0,valores[13])
    entrada_material.delete(0,tk.END)
    entrada_material.insert(0,valores[14])
    entrada_cubierta.delete(0,tk.END)
    entrada_cubierta.insert(0,valores[15])
    entrada_conservacion.delete(0,tk.END)
    entrada_conservacion.insert(0,valores[16])

def actualizar_datos():
    item_actual = treeview.focus()
    if item_actual:
        valores = treeview.item(item_actual, 'values')
        nuevomunicipio = entrada_municipio.get()
        nuevoclave = entrada_clave.get()
        nuevofichacatalogo = entrada_fichacatalogo.get()
        nuevoseccion = entrada_seccion.get()
        nuevomanzana = entrada_manzana.get()
        nuevonumero = entrada_numero.get()
        nuevonombreedificio = entrada_nombreedificio.get()
        nuevolocalizacion = entrada_localizacion.get()
        nuevobarrio = entrada_barrio.get()
        nuevosiglo = entrada_siglo.get()
        nuevocatalogada = entrada_catalogada.get()
        nuevodecretada = entrada_decretada.get()
        nuevouso = entrada_uso.get()
        nuevoniveles = entrada_niveles.get()
        nuevomaterial = entrada_material.get()
        nuevocubierta = entrada_cubierta.get()
        nuevoconservacion = entrada_conservacion.get()   

        conexion = mysql.connector.connect(host="localhost", user="root", password="root", database="Monumentos_01")
        cursor = conexion.cursor()
        cursor.execute("UPDATE monumentos SET municipio = %s, clave = %s, ficha_catalogo = %s, seccion = %s, manzana = %s, numero = %s, nombre_edificio = %s, localizacion = %s, barrio = %s, siglo_contruccion = %s, catalogada = %s, decretada = %s, uso_actual = %s, niveles = %s, material_construccion = %s, tipo_cubierta = %s, cons_carac_org = %s WHERE municipio = %s",
               (nuevomunicipio, nuevoclave, nuevofichacatalogo, nuevoseccion, nuevomanzana, nuevonumero, nuevonombreedificio, nuevolocalizacion, nuevobarrio, nuevosiglo, nuevocatalogada, nuevodecretada, nuevouso, nuevoniveles, nuevomaterial, nuevocubierta, nuevoconservacion, valores[0]))
        conexion.commit()
        cursor.close()
        conexion.close()

        treeview.item(item_actual, values=(nuevomunicipio, nuevoclave, nuevofichacatalogo, nuevoseccion, nuevomanzana, nuevonumero, nuevonombreedificio, nuevolocalizacion, nuevobarrio, nuevosiglo, nuevocatalogada, nuevodecretada, nuevouso, nuevoniveles, nuevomaterial, nuevocubierta, nuevoconservacion))
        datos = "Municipio: "+ nuevomunicipio +"\n"+"Clave: " + nuevoclave +"\n"+"Ficha de Catálogo: " + nuevofichacatalogo +"\n"+"Sección: " + nuevoseccion +"\n"+"Manzana: " + nuevomanzana + "\n"+"Número: " + nuevonumero +"\n"+"Nombre del edificio: " + nuevonombreedificio+"\n"+"Localización: " + nuevolocalizacion +"\n"+"Barrio: " + nuevobarrio +"\n" +"Siglo: " + nuevosiglo +"\n" +"Catalogada: " + nuevocatalogada +"\n"+"Decretada: " + nuevodecretada +"\n" + "Uso: " + nuevouso +"\n" +"Niveles: " + nuevoniveles +"\n" +"Material: " + nuevomaterial +"\n" +"Cubierta: " + nuevocubierta +"\n" +"Conservación: " + nuevoconservacion +"\n"
        messagebox.showinfo("Información", "¡Datos actualizados con éxito!" + "\n\n" + datos)
    
        

def borrarRegistro(treeview):
    if not treeview.selection():
        messagebox.showwarning("Selecciona un registro", "Primero selecciona un registro en la tabla.")
        return

    respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que quieres eliminar este monumento?")
    if not respuesta:
        return
    
    selected_item = treeview.selection()[0]
    uid = treeview.item(selected_item)['values'][0]
    conexion = mysql.connector.connect(host="localhost", user="root", password="root", database="Monumentos_01")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM monumentos WHERE municipio = %s", (uid,))
    conexion.commit()
    treeview.delete(selected_item)
    cursor.close()
    conexion.close()
    

def insertarRegistro(municipio,clave,fichacatalogo,seccion,manzana,numero,nombreedificio,localizacion,barrio,siglo,catalogada, decretada, uso, niveles, material, cubierta, conservacion):
    try: 
        conexion = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            database = "Monumentos_01"
            )

        cursor = conexion.cursor()
    #crear el query
        query  = "INSERT INTO monumentos (municipio, clave, ficha_catalogo, seccion, manzana, numero, nombre_edificio, localizacion, barrio, siglo_contruccion, catalogada, decretada, uso_actual, niveles, material_construccion, tipo_cubierta, cons_carac_org)" + "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s)"
        valores = (municipio, clave, fichacatalogo, seccion, manzana, numero, nombreedificio, localizacion, barrio, siglo, catalogada, decretada, uso, niveles, material, cubierta, conservacion)
    #ejecucion del query
        cursor.execute(query, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        messagebox.showinfo("Información", "Datos guardados en la base de datos")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar los datos: {err}")

def guardar_valores():
    municipio = entrada_municipio.get().strip()
    clave = entrada_clave.get().strip()
    fichacatalogo = entrada_fichacatalogo.get().strip()
    seccion = entrada_seccion.get().strip()
    manzana = entrada_manzana.get().strip()
    numero = entrada_numero.get().strip()
    nombreedificio = entrada_nombreedificio.get().strip()
    localizacion = entrada_localizacion.get().strip()
    barrio = entrada_barrio.get().strip()
    siglo = entrada_siglo.get().strip()
    catalogada = entrada_catalogada.get().strip()
    decretada = entrada_decretada.get().strip()
    uso = entrada_uso.get().strip()
    niveles = entrada_niveles.get().strip()
    material = entrada_material.get().strip()
    cubierta = entrada_cubierta.get().strip()
    conservacion = entrada_conservacion.get().strip()

    # Validaciones
    if not municipio or not clave or not nombreedificio:
        messagebox.showwarning("Campos obligatorios", "Por favor llena al menos Municipio, Clave y Nombre del Edificio.")
        return

    if seccion and not seccion.isdigit():
        messagebox.showerror("Dato inválido", "El campo 'Sección' debe ser un número.")
        return

    if niveles and not niveles.isdigit():
        messagebox.showerror("Dato inválido", "El campo 'Niveles' debe ser un número.")
        return

    insertarRegistro(municipio,clave,fichacatalogo,seccion,manzana,numero,nombreedificio,localizacion,barrio,siglo,catalogada, decretada, uso, niveles, material, cubierta, conservacion)

    datos = f"""Municipio: {municipio}
                Clave: {clave}
                Ficha de Catálogo: {fichacatalogo}
                Sección: {seccion}
                Manzana: {manzana}
                Número: {numero}
                Nombre del edificio: {nombreedificio}
                Localización: {localizacion}
                Barrio: {barrio}
                Siglo: {siglo}
                Catalogada: {catalogada}
                Decretada: {decretada}
                Uso: {uso}
                Niveles: {niveles}
                Material: {material}
                Cubierta: {cubierta}
                Conservación: {conservacion}"""

    messagebox.showinfo("Información", "Datos guardados con éxito:\n\n" + datos)
    limpiar_campos()
    buscar()

def limpiar_campos():
    entrada_municipio.delete(0, tk.END)
    entrada_clave.delete(0, tk.END)
    entrada_fichacatalogo.delete(0, tk.END)
    entrada_seccion.delete(0, tk.END)
    entrada_manzana.delete(0, tk.END)
    entrada_numero.delete(0, tk.END)
    entrada_nombreedificio.delete(0, tk.END)
    entrada_localizacion.delete(0, tk.END)
    entrada_barrio.delete(0, tk.END)
    entrada_siglo.delete(0,tk.END)
    entrada_catalogada.delete(0,tk.END)
    entrada_decretada.delete(0,tk.END)
    entrada_uso.delete(0, tk.END)
    entrada_niveles.delete(0,tk.END)
    entrada_material.delete(0,tk.END)
    entrada_cubierta.delete(0,tk.END)
    entrada_conservacion.delete(0,tk.END)

def borrar():
    limpiar_campos()

def buscar():
    campos={
    "m.municipio" : entrada_municipio.get(),
    "m.clave" : entrada_clave.get(),
    "m.ficha_catalogo" : entrada_fichacatalogo.get(),
    "m.seccion" : entrada_seccion.get(),
    "m.manzana" : entrada_manzana.get(),
    "m.numero" : entrada_numero.get(),
    "m.nombre_edificio" : entrada_nombreedificio.get(),
    "m.localizacion" : entrada_localizacion.get(),
    "m.barrio" : entrada_barrio.get(),
    "m.siglo_contruccion" : entrada_siglo.get(),
    "m.catalogada" : entrada_catalogada.get(),
    "m.decretada" : entrada_decretada.get(),
    "m.uso_actual" : entrada_uso.get(),
    "m.niveles" : entrada_niveles.get(),
    "m.material_construccion" : entrada_material.get(),
    "m.tipo_cubierta" : entrada_cubierta.get(),
    "m.cons_carac_org" : entrada_conservacion.get()
    }

    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Monumentos_01"
        )
        cursor = conexion.cursor()

        consulta = """
        SELECT m.municipio, m.clave, m.ficha_catalogo, m.seccion, m.manzana, m.numero, m.nombre_edificio, m.localizacion, m.barrio, m.siglo_contruccion, m.catalogada, m.decretada, m.uso_actual, m.niveles, m.material_construccion, m.tipo_cubierta, m.cons_carac_org
        FROM monumentos m 
        """
    
        condiciones = []
        valores = []

        for campo_sql, valor in campos.items():
            if valor.strip() != "":
                condiciones.append(f"{campo_sql}=%s")
        
                valores.append(valor.strip())
        if condiciones:
            consulta += " WHERE " + " AND ".join(condiciones)
            
        cursor.execute(consulta, valores)
        resultados_obtenidos = cursor.fetchall()    

        treeview.delete(*treeview.get_children())

        for fila in resultados_obtenidos:
            treeview.insert("", "end", values=fila)

        conexion.close()
        etiqueta_contador.config(text=f"Resultados encontrados: {len(resultados_obtenidos)}")


    except Exception as e:
        print("Error al conectar o ejecutar consulta:", e)
        etiqueta_contador.config(text="Resultados encontrados: 0")

def mostrar_detalle(event):
    item = treeview.focus()
    if not item:
        return

    valores = treeview.item(item, "values")
    columnas = treeview["columns"]

    detalles = ""
    for i in range(len(columnas)):
        detalles += f"{columnas[i]}: {valores[i]}\n"

    messagebox.showinfo("Detalles del Monumento", detalles)


def exportar_resultados():
    filas = treeview.get_children()
    if not filas:
        messagebox.showwarning("Sin resultados", "No hay datos en la tabla para exportar.")
        return

    archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivo CSV", "*.csv")])
    if not archivo:
        return  # Cancelado

    try:
        with open(archivo, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            # Encabezados
            columnas = [treeview.heading(col)["text"] for col in treeview["columns"]]
            escritor.writerow(columnas)
            # Filas
            for fila in filas:
                datos = treeview.item(fila)["values"]
                escritor.writerow(datos)

        messagebox.showinfo("Exportación exitosa", f"Datos exportados correctamente a:\n{archivo}")

    except Exception as e:
        messagebox.showerror("Error al exportar", f"Ocurrió un error:\n{e}")


# INTERFAZ

ventana = tk.Tk()
ventana.title("Búsqueda de monumentos")

width= ventana.winfo_screenwidth()               
height= ventana.winfo_screenheight()               
ventana.geometry("%dx%d" % (width, height))
ventana.config(bg= "gray95")

  # Arriba a la derecha


fuente_lbprincipal = font.Font(family ="Helvetica", size = 14, weight="bold")

tk.Label(ventana, text="MONUMENTOS DEL ESTADO DE CHIAPAS", background="#2C3E50", foreground="#ffffff", font= fuente_lbprincipal).pack()

#imagen - logo INAH
image = tk.PhotoImage(file= "R.png")
image = image.subsample(10,10)
labelimagen = ttk.Label(ventana,image=image, background="gray95")
labelimagen.place(x=10, y=10)
icono_sol = tk.PhotoImage(file="sol.png")
icono_luna = tk.PhotoImage(file="luna.png")
icono_modo = icono_luna  # Comienza en modo claro
boton_modo = tk.Button(ventana, image=icono_modo, bg="white", bd=0, command=lambda: alternar_modo_con_icono())
boton_modo.place(relx=0.97, rely=0.01, anchor="ne")


# Entradas
# Crear un frame principal para organizar mejor los elementos
frame_principal = tk.Frame(ventana)
frame_principal.pack(padx=10, pady=10)
frame_principal.config(bg="white", bd=5, relief="ridge")

fuente_label = font.Font(family="Segoe UI", size= 10, underline=0)
# Primera columna (0)
tk.Label(frame_principal, text="Municipio:", font=fuente_label, foreground="gray30").grid(row=0, column=0, sticky="e", padx=5, pady=2)
entrada_municipio = tk.Entry(frame_principal)
entrada_municipio.grid(row=0, column=1, padx=5, pady=2)


tk.Label(frame_principal, text="Clave:", font=fuente_label, foreground="gray30").grid(row=1, column=0, sticky="e", padx=5, pady=2)
entrada_clave = tk.Entry(frame_principal)
entrada_clave.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frame_principal, text="Ficha Catálogo:", font=fuente_label, foreground="gray30").grid(row=2, column=0, sticky="e", padx=5, pady=2)
entrada_fichacatalogo = tk.Entry(frame_principal)
entrada_fichacatalogo.grid(row=2, column=1, padx=5, pady=2)

tk.Label(frame_principal, text="Sección:", font= fuente_label, foreground="gray30").grid(row=3, column=0, sticky="e", padx=5, pady=2)
entrada_seccion = tk.Entry(frame_principal)
entrada_seccion.grid(row=3, column=1, padx=5, pady=2)

tk.Label(frame_principal, text="Manzana:", font= fuente_label, foreground="gray30").grid(row=4, column=0, sticky="e", padx=5, pady=2)
entrada_manzana = tk.Entry(frame_principal)
entrada_manzana.grid(row=4, column=1, padx=5, pady=2)

tk.Label(frame_principal, text="Número:", font= fuente_label, foreground="gray30").grid(row=5, column=0, sticky="e", padx=5, pady=2)
entrada_numero = tk.Entry(frame_principal)
entrada_numero.grid(row=5, column=1, padx=5, pady=2)

tk.Label(frame_principal, text="Nombre del Edificio:", font= fuente_label, foreground="gray30").grid(row=6, column=0, sticky="e", padx=5, pady=2)
entrada_nombreedificio = tk.Entry(frame_principal)
entrada_nombreedificio.grid(row=6, column=1, padx=5, pady=2)

# Segunda columna (2)
tk.Label(frame_principal, text="Localización:", font= fuente_label, foreground="gray30").grid(row=0, column=2, sticky="e", padx=5, pady=2)
entrada_localizacion = tk.Entry(frame_principal)
entrada_localizacion.grid(row=0, column=3, padx=5, pady=2)

tk.Label(frame_principal, text="Barrio:", font=fuente_label, foreground="gray30").grid(row=1, column=2, sticky="e", padx=5, pady=2)
entrada_barrio = tk.Entry(frame_principal)
entrada_barrio.grid(row=1, column=3, padx=5, pady=2)

tk.Label(frame_principal, text="Siglo de Construcción:", font=fuente_label, foreground="gray30").grid(row=2, column=2, sticky="e", padx=5, pady=2)
entrada_siglo = tk.Entry(frame_principal)
entrada_siglo.grid(row=2, column=3, padx=5, pady=2)

tk.Label(frame_principal, text="Catalogada:", font=fuente_label, foreground="gray30").grid(row=3, column=2, sticky="e", padx=5, pady=2)
entrada_catalogada = tk.Entry(frame_principal)
entrada_catalogada.grid(row=3, column=3, padx=5, pady=2)

tk.Label(frame_principal, text="Decretada:", font=fuente_label, foreground="gray30").grid(row=4, column=2, sticky="e", padx=5, pady=2)
entrada_decretada = tk.Entry(frame_principal)
entrada_decretada.grid(row=4, column=3, padx=5, pady=2)

tk.Label(frame_principal, text="Uso Actual:", font=fuente_label, foreground="gray30").grid(row=5, column=2, sticky="e", padx=5, pady=2)
entrada_uso = tk.Entry(frame_principal)
entrada_uso.grid(row=5, column=3, padx=5, pady=2)

tk.Label(frame_principal, text="Niveles:", font=fuente_label, foreground="gray30").grid(row=6, column=2, sticky="e", padx=5, pady=2)
entrada_niveles = tk.Entry(frame_principal)
entrada_niveles.grid(row=6, column=3, padx=5, pady=2)

# Tercera columna (4)
tk.Label(frame_principal, text="Material de Construcción:", font=fuente_label, foreground="gray30").grid(row=0, column=4, sticky="e", padx=5, pady=2)
entrada_material = tk.Entry(frame_principal)
entrada_material.grid(row=0, column=5, padx=5, pady=2)

tk.Label(frame_principal, text="Tipo de Cubierta:", font=fuente_label, foreground="gray30").grid(row=1, column=4, sticky="e", padx=5, pady=2)
entrada_cubierta = tk.Entry(frame_principal)
entrada_cubierta.grid(row=1, column=5, padx=5, pady=2)

tk.Label(frame_principal, text="Conservación:", font=fuente_label, foreground="gray30").grid(row=2, column=4, sticky="e", padx=5, pady=2)
entrada_conservacion = tk.Entry(frame_principal)
entrada_conservacion.grid(row=2, column=5, padx=5, pady=2)

# Frame para botones
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)
frame_botones.config(bg="white", bd=5, relief="ridge")

icon_buscar = tk.PhotoImage(file="buscar.png")
icon_limpiar = tk.PhotoImage(file="limpiar.png")
icon_guardar = tk.PhotoImage(file="guardar.png")
icon_borrar = tk.PhotoImage(file="borrar.png")
icon_actualizar = tk.PhotoImage(file="actualizar.png")
icon_exportar = tk.PhotoImage(file="exportar.png")

fuente_botones = font.Font(family ="Arial", size = 10, weight="bold")

boton_buscar = tk.Button(frame_botones, text="Buscar", image=icon_buscar, compound="left", bg= "#F39C12", fg="white", command=buscar)
boton_buscar.grid(row=0, column=0, padx=10)
boton_buscar.bind('<Enter>', lambda e: e.widget.config(bg="#D35400"))
boton_buscar.bind('<Leave>', lambda e: e.widget.config(bg="#F39C12"))


boton_borrar = tk.Button(frame_botones, text="Limpiar Datos", image=icon_limpiar, compound="left", bg="gray70", fg="white", command=borrar)
boton_borrar.grid(row=0, column=4, padx=10)
boton_borrar.bind('<Enter>', lambda e: e.widget.config(bg="gray60"))
boton_borrar.bind('<Leave>', lambda e: e.widget.config(bg="gray70"))


boton_guardar = tk.Button(frame_botones, text="Guardar Datos", image=icon_guardar, compound="left", bg="#27AE60", fg="white", command= guardar_valores)
boton_guardar.grid(row=0, column=1, padx=10)
boton_guardar.bind('<Enter>', lambda e: e.widget.config(bg="#219653"))
boton_guardar.bind('<Leave>', lambda e: e.widget.config(bg="#27AE60"))

boton_eliminarmonumento = tk.Button(frame_botones, text ="Borrar Monumento", image=icon_borrar, compound="left", bg="#E74C3C", fg="white", command=lambda: borrarRegistro(treeview))
boton_eliminarmonumento.grid(row=0, column=2, padx=10)
boton_eliminarmonumento.bind('<Enter>', lambda e: e.widget.config(bg="#C0392B"))
boton_eliminarmonumento.bind('<Leave>', lambda e: e.widget.config(bg="#E74C3C"))

boton_actualizardatos = tk.Button(frame_botones, text = "Actualizar Datos", image=icon_actualizar, compound="left", bg="#2980B9", fg="white", command= actualizar_datos)
boton_actualizardatos.grid(row=0, column=3, padx=10)
boton_actualizardatos.bind('<Enter>', lambda e: e.widget.config(bg="#1A5276"))
boton_actualizardatos.bind('<Leave>', lambda e: e.widget.config(bg="#2980B9"))

boton_exportar = tk.Button(frame_botones, text="Exportar a Excel", image=icon_exportar, compound="left", bg="#8E44AD", fg="white", command=exportar_resultados)
boton_exportar.grid(row=0, column=5, padx=10)
boton_exportar.bind('<Enter>', lambda e: e.widget.config(bg="#6C3483"))
boton_exportar.bind('<Leave>', lambda e: e.widget.config(bg="#8E44AD"))


# Frame para resultados (abajo)
frame_resultados = tk.Frame(ventana)
frame_resultados.pack(fill="both", expand=True, padx=10, pady=10)
frame_resultados.config(bg="white", bd=5, relief="ridge")
etiqueta_contador = tk.Label(ventana, text="Resultados encontrados: 0", bg="gray95", fg="black", font=("Segoe UI", 10, "bold"))
etiqueta_contador.pack()


# Scroll
scroll = tk.Scrollbar(frame_resultados)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

h_scrollbar = tk.Scrollbar(frame_resultados, orient=tk.HORIZONTAL)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)



item_actual = None

# TreeView
columnas = ("Municipio", "Clave", "Ficha Catalogo", "Sección", "Manzana", "Número", "Nombre del Edificio",
            "Localización", "Barrio", "Siglo Construcción", "Catalogada", "Decretada",
            "Uso Actual", "Niveles", "Material Construcción", "Tipo de cubierta", "Conservación")

treeview = ttk.Treeview(frame_resultados, columns=columnas, show="headings", yscrollcommand=scroll.set, xscrollcommand= h_scrollbar.set)
for col in columnas:
    treeview.heading(col, text=col)
    treeview.column(col, anchor="center", width=80)


treeview.bind("<<TreeviewSelect>>", cargar_datos)
treeview.bind("<Double-1>", mostrar_detalle)

treeview.pack(fill="both", expand=True, padx=10, pady=10)
scroll.config(command=treeview.yview)
h_scrollbar.config(command=treeview.xview)

#dar estilo al treeview
style= ttk.Style()
style.theme_use("clam")
style.map("Treeview", background=[('selected', 'darkblue')])
style.map("Treeview.Heading", background=[('active', "#3E637C")])

aplicar_modo()

ventana.mainloop()