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
    creditos.config(bg=modo_actual["fondo"])
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
        valores = treeview.item(item_actual, 'values')
        entrada_identificador.delete(0, tk.END)
        entrada_identificador.insert(0, valores[0])
        entrada_clave.delete(0, tk.END)
        entrada_clave.insert(0, valores[1])
        entrada_folio.delete(0, tk.END)
        entrada_folio.insert(0, valores[2])
        entrada_nombre.delete(0, tk.END)
        entrada_nombre.insert(0, valores[3])
        entrada_municipio.delete(0, tk.END)
        entrada_municipio.insert(0, valores[4])
        entrada_estructuras.delete(0, tk.END)
        entrada_estructuras.insert(0, valores[5])
        entrada_concentracion.delete(0, tk.END)
        entrada_concentracion.insert(0, valores[6])
        entrada_concheros.delete(0, tk.END)
        entrada_concheros.insert(0, valores[7])
        entrada_manifestaciones.delete(0, tk.END)
        entrada_manifestaciones.insert(0, valores[8])
        entrada_paleontologico.delete(0, tk.END)
        entrada_paleontologico.insert(0, valores[9])
        entrada_yacimiento.delete(0, tk.END)
        entrada_yacimiento.insert(0, valores[10])
        entrada_utmestenad.delete(0, tk.END)
        entrada_utmestenad.insert(0, valores[11])
        entrada_utmnortenad.delete(0, tk.END)
        entrada_utmnortenad.insert(0, valores[12])
        entrada_utmestewgs.delete(0, tk.END)
        entrada_utmestewgs.insert(0, valores[13])
        entrada_utmnortewgs.delete(0, tk.END)
        entrada_utmnortewgs.insert(0, valores[14])
        

def actualizar_datos():
    item_actual = treeview.focus()  # aquí obtienes el id_monumento porque es el iid
    if item_actual:
        # No uses valores[0] para WHERE, usa item_actual
        valores = treeview.item(item_actual, 'values')
        nuevoidentificador = entrada_identificador.get()
        nuevoclave = entrada_clave.get()
        nuevofolio = entrada_folio.get()
        nuevonombre = entrada_nombre.get()
        nuevomunicipio = entrada_municipio.get()
        nuevoestructuras = entrada_estructuras.get()
        nuevoconcentracion = entrada_concentracion.get()
        nuevoconcheros = entrada_concheros.get()
        nuevomanifestaciones = entrada_manifestaciones.get()
        nuevopaleontologico = entrada_paleontologico.get()
        nuevoyacimiento = entrada_yacimiento.get()
        nuevoutmestenad = entrada_utmestenad.get()
        nuevoutmnortenad = entrada_utmnortenad.get()
        nuevoutmestewgs = entrada_utmestewgs.get()
        nuevoutmnortewgs = entrada_utmnortewgs.get()
        
        conexion = mysql.connector.connect(
            host="localhost", user="root", password="root", database="zonas_01"
        )

        try:
            cursor1 = conexion.cursor()
            cursor1.execute("""
                UPDATE zonas SET 
                    identificador = %s, clave = %s, folio_real = %s, nombre = %s, municipio = %s, 
                    estructura = %s, concentracion = %s, concheros = %s, manifestaciones = %s, 
                    paleontologico = %s, yacimiento = %s, UTM_ESTE_NAD27 = %s,  UTM_NORTE_NAD27 = %s, 
                    UTM_ESTE_WGS84 = %s, UTM_NORTE_WGS84 = %s
                WHERE identificador = %s
            """, (
                nuevoidentificador, nuevoclave, nuevofolio, nuevonombre, nuevomunicipio,
                nuevoestructuras, nuevoconcentracion, nuevoconcheros, nuevomanifestaciones, nuevopaleontologico,
                nuevoyacimiento, nuevoutmestenad, nuevoutmnortenad, nuevoutmestewgs, nuevoutmnortewgs, item_actual
            ))
            conexion.commit()
            cursor1.close()

            # Obtener fecha_actu con el id
            cursor2 = conexion.cursor(buffered=True)
            cursor2.execute("SELECT fecha_actu FROM monumentos WHERE id_identificador = %s", (item_actual,))
            resultado = cursor2.fetchone()
            cursor2.close()

            fecha_actu = resultado[0] if resultado else "Desconocida"

            # Actualizar visualmente el Treeview
            treeview.item(item_actual, values=(
                nuevoidentificador, nuevoclave, nuevofolio, nuevonombre, nuevomunicipio,
                nuevoestructuras, nuevoconcentracion, nuevoconcheros, nuevomanifestaciones, nuevopaleontologico,
                nuevoyacimiento, nuevoutmestenad, nuevoutmnortenad, nuevoutmestewgs, nuevoutmnortewgs, str(fecha_actu)
            ))

            datos = f"""Identificador: {nuevoidentificador}
Clave del Sitio: {nuevoclave}
Folio Real: {nuevofolio}
Nombre: {nuevonombre}
Municipio: {nuevomunicipio}
Estructuras: {nuevoestructuras}
Concentración de Materiales: {nuevoconcentracion}
Concheros: {nuevoconcheros}
Manifestaciones Gráfico-Rupestres: {nuevomanifestaciones}
Paleontológico: {nuevopaleontologico}
Yacimiento de Materias Primas: {nuevoyacimiento}
UTM ESTE NAD 27: {nuevoutmestenad}
UTM NORTE NAD 27: {nuevoutmnortenad}
UTM ESTE WGS 84: {nuevoutmestewgs}
UTM NORTE WGS 84: {nuevoutmnortewgs}
Última actualización: {fecha_actu}
"""
            messagebox.showinfo("Información", "¡Datos actualizados con éxito!\n\n" + datos)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        finally:
            conexion.close()

        

def borrarRegistro(treeview):
    if not treeview.selection():
        messagebox.showwarning("Selecciona un registro", "Primero selecciona un registro en la tabla.")
        return

    respuesta = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que quieres eliminar este monumento?")
    if not respuesta:
        return
    
    conexion = mysql.connector.connect(host="localhost", user="root", password="root", database="zonas_01")
    cursor = conexion.cursor()
    
    try:
        for item in treeview.selection():
            # item es el iid, que es el id_monumento oculto
            cursor.execute("DELETE FROM monumentos WHERE identificador = %s", (item,))
            treeview.delete(item)
        conexion.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al eliminar: {e}")
    finally:
        cursor.close()
        conexion.close()

    

def insertarRegistro(identificador,clave,folio,nombre,municipio,estructuras,concentracion,concheros,manifestaciones,paleontologico,yacimiento, utmestenad, utmnortenad, utmestewgs, utmnortewgs):
    try: 
        conexion = mysql.connector.connect(
            host = "localhost",
            user = "root",
            port = "3306",
            password = "root",
            database = "zonas_01"
            )

        cursor = conexion.cursor()
    #crear el query
        query  = "INSERT INTO zonas (identificador, clave, folio_real, nombre, municipio, estructura, concentracion, concheros, manifestaciones, paleontologico, yacimiento, UTM_ESTE_NAD27,  UTM_NORTE_NAD27, UTM_ESTE_WGS84, UTM_NORTE_WGS84)" + "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s)"
        valores = (identificador,clave,folio,nombre,municipio,estructuras,concentracion,concheros,manifestaciones,paleontologico,yacimiento, utmestenad, utmnortenad, utmestewgs, utmnortewgs)
    #ejecucion del query
        cursor.execute(query, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        messagebox.showinfo("Información", "Datos guardados en la base de datos")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar los datos: {err}")

def guardar_valores():
    # 1. Obtener todo como texto
    identificador = entrada_identificador.get().strip()
    clave = entrada_clave.get().strip()
    folio = entrada_folio.get().strip()
    nombre = entrada_nombre.get().strip()
    municipio = entrada_municipio.get().strip()
    estructuras = entrada_estructuras.get().strip()
    concentracion = entrada_concentracion.get().strip()
    concheros = entrada_concheros.get().strip()
    manifestaciones = entrada_manifestaciones.get().strip()
    paleontologico = entrada_paleontologico.get().strip()
    yacimiento = entrada_yacimiento.get().strip()
    utmestenad = entrada_utmestenad.get().strip()
    utmnortenad = entrada_utmnortenad.get().strip()
    utmestewgs = entrada_utmestewgs.get().strip()
    utmnortewgs = entrada_utmnortewgs.get().strip()

    # Validaciones
    if not municipio or not clave or not nombre:
        messagebox.showwarning("Campos obligatorios", "Por favor llena Municipio, Clave y Nombre.")
        return False

    if len(municipio) > 100 or not all(c.isalpha() or c.isspace() or c in "-_" for c in municipio):
        messagebox.showerror("Dato inválido", "El campo 'Municipio' debe tener solo letras y hasta 100 caracteres.")
        return False

    if not clave.isdigit():
        messagebox.showerror("Dato inválido", "El campo 'Clave' debe ser un número.")
        return False

    # Convertir valores numéricos necesarios
    try:
        clave = int(clave)
        identificador = int(identificador) if identificador else None
    except ValueError:
        messagebox.showerror("Dato inválido", "Los campos numéricos deben contener números válidos.")
        return False

    # 4. Insertar
    insertarRegistro(
        identificador, clave, folio, nombre, municipio,
        estructuras, concentracion, concheros, manifestaciones,
        paleontologico, yacimiento, utmestenad, utmnortenad,
        utmestewgs, utmnortewgs
    )

    datos = f"""Clave del Sitio: {clave}
Folio Real: {folio}
Nombre: {nombre}
Municipio: {municipio}
Estructuras: {estructuras}
Concentración de Materiales: {concentracion}
Concheros: {concheros}
Manifestaciones Gráfico-Rupestres: {manifestaciones}
Paleontológico: {paleontologico}
Yacimiento de Materias Primas: {yacimiento}
UTM ESTE NAD 27: {utmestenad}
UTM NORTE NAD 27: {utmnortenad}
UTM ESTE WGS 84: {utmestewgs}
UTM NORTE WGS 84: {utmnortewgs}"""

    messagebox.showinfo("Información", "Datos guardados con éxito:\n\n" + datos)
    limpiar_campos()
    buscar()



def limpiar_campos():
    entrada_identificador.delete(0, tk.END)
    entrada_clave.delete(0, tk.END)
    entrada_folio.delete(0, tk.END)
    entrada_nombre.delete(0, tk.END)
    entrada_municipio.delete(0, tk.END)
    entrada_estructuras.delete(0, tk.END)
    entrada_concentracion.delete(0, tk.END)
    entrada_concheros.delete(0, tk.END)
    entrada_manifestaciones.delete(0, tk.END)
    entrada_paleontologico.delete(0,tk.END)
    entrada_yacimiento.delete(0,tk.END)
    entrada_utmestenad.delete(0,tk.END)
    entrada_utmnortenad.delete(0, tk.END)
    entrada_utmestewgs.delete(0,tk.END)
    entrada_utmnortewgs.delete(0,tk.END)

def borrar():
    limpiar_campos()

def buscar():
    campos = {
        "z.identificador": entrada_identificador.get(),
        "z.clave": entrada_clave.get(),
        "z.folio_real": entrada_folio.get(),
        "z.nombre": entrada_nombre.get(),
        "z.municipio": entrada_municipio.get(),
        "z.estructura": entrada_estructuras.get(),
        "z.concentracion": entrada_concentracion.get(),
        "z.concheros": entrada_concheros.get(),
        "z.manifestaciones": entrada_manifestaciones.get(),
        "z.paleontologico": entrada_paleontologico.get(),
        "z.yacimiento": entrada_yacimiento.get(),
        "z.UTM_ESTE_NAD27": entrada_utmestenad.get(),
        "z.UTM_NORTE_NAD27": entrada_utmnortenad.get(),
        "z.UTM_ESTE_WGS84": entrada_utmestewgs.get(),
        "z.UTM_NORTE_WGS84": entrada_utmnortewgs.get()
    }

    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="zonas_01"
        )
        cursor = conexion.cursor()

        consulta = """
        SELECT z.identificador, z.clave, z.folio_real, z.nombre, z.municipio, z.estructura, 
               z.concentracion, z.concheros, z.manifestaciones, z.paleontologico, z.yacimiento, 
               z.UTM_ESTE_NAD27, z.UTM_NORTE_NAD27, z.UTM_ESTE_WGS84, z.UTM_NORTE_WGS84, z.fecha_actu
        FROM zonas z
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
            id_mon = fila[0]
            valores_mostrar = fila[0:]  # todo menos id_monumento
            treeview.insert("", "end", iid=str(id_mon), values=valores_mostrar)

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

    messagebox.showinfo("Detalles de la zona", detalles)


def exportar_resultados():
    seleccionados = treeview.selection()
    exportar_todo = not seleccionados  # Si no hay selección, exportamos todo

    filas = treeview.get_children()
    if not filas:
        messagebox.showwarning("Sin resultados", "No hay datos en la tabla para exportar.")
        return

    archivo = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Archivo CSV", "*.csv")],
        title="Guardar como"
    )
    if not archivo:
        return  # Cancelado

    try:
        with open(archivo, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)

            # Encabezados
            columnas = [treeview.heading(col)["text"] for col in treeview["columns"]]
            escritor.writerow(columnas)

            # Filas seleccionadas o todas
            filas_a_exportar = seleccionados if not exportar_todo else filas

            for fila in filas_a_exportar:
                datos = treeview.item(fila)["values"]
                escritor.writerow(datos)

        if not exportar_todo:
            messagebox.showinfo("Exportación exitosa", f"{len(seleccionados)} filas exportadas a:\n{archivo}")
        else:
            messagebox.showinfo("Exportación exitosa", f"Todos los datos fueron exportados a:\n{archivo}")

    except Exception as e:
        messagebox.showerror("Error al exportar", f"Ocurrió un error:\n{e}")



# INTERFAZ

ventana = tk.Tk()
ventana.title("Búsqueda de Zonas Arqueológicas")
ventana.config(bg= "gray95")
ventana.state('zoomed') 
ventana.iconbitmap('inah_icon.ico')
  # Arriba a la derecha


fuente_lbprincipal = font.Font(family ="Helvetica", size = 14, weight="bold")

tk.Label(ventana, text=" ZONAS ARQUEOLÓGICAS DE CHIAPAS", background="#2C3E50", foreground="#ffffff", font= fuente_lbprincipal).pack()

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
tk.Label(frame_principal, text="Identificador:", font=fuente_label, foreground="gray30").grid(row=0, column=0, sticky="e", padx=5, pady=2)
entrada_identificador = tk.Entry(frame_principal)
entrada_identificador.grid(row=0, column=1, padx=5, pady=2)


tk.Label(frame_principal, text="Clave del Sitio:", font=fuente_label, foreground="gray30").grid(row=1, column=0, sticky="e", padx=5, pady=2)
entrada_clave = tk.Entry(frame_principal)
entrada_clave.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frame_principal, text="Folio Real:", font=fuente_label, foreground="gray30").grid(row=2, column=0, sticky="e", padx=5, pady=2)
entrada_folio = tk.Entry(frame_principal)
entrada_folio.grid(row=2, column=1, padx=5, pady=2)

tk.Label(frame_principal, text="Nombre:", font= fuente_label, foreground="gray30").grid(row=3, column=0, sticky="e", padx=5, pady=2)
entrada_nombre = tk.Entry(frame_principal)
entrada_nombre.grid(row=3, column=1, padx=5, pady=2)

tk.Label(frame_principal, text="Municipio:", font= fuente_label, foreground="gray30").grid(row=4, column=0, sticky="e", padx=5, pady=2)
entrada_municipio = tk.Entry(frame_principal)
entrada_municipio.grid(row=4, column=1, padx=5, pady=2)

tk.Label(frame_principal, text="Estructuras:", font= fuente_label, foreground="gray30").grid(row=5, column=0, sticky="e", padx=5, pady=2)
entrada_estructuras = tk.Entry(frame_principal)
entrada_estructuras.grid(row=5, column=1, padx=5, pady=2)

tk.Label(frame_principal, text="Concentración de Materiales:", font= fuente_label, foreground="gray30").grid(row=6, column=0, sticky="e", padx=5, pady=2)
entrada_concentracion = tk.Entry(frame_principal)
entrada_concentracion.grid(row=6, column=1, padx=5, pady=2)

# Segunda columna (2)
tk.Label(frame_principal, text="Concheros:", font= fuente_label, foreground="gray30").grid(row=0, column=2, sticky="e", padx=5, pady=2)
entrada_concheros = tk.Entry(frame_principal)
entrada_concheros.grid(row=0, column=3, padx=5, pady=2)

tk.Label(frame_principal, text="Manifestaciones Gráfico-Rupestres:", font=fuente_label, foreground="gray30").grid(row=1, column=2, sticky="e", padx=5, pady=2)
entrada_manifestaciones = tk.Entry(frame_principal)
entrada_manifestaciones.grid(row=1, column=3, padx=5, pady=2)

tk.Label(frame_principal, text="Paleontológico:", font=fuente_label, foreground="gray30").grid(row=2, column=2, sticky="e", padx=5, pady=2)
entrada_paleontologico = tk.Entry(frame_principal)
entrada_paleontologico.grid(row=2, column=3, padx=5, pady=2)

tk.Label(frame_principal, text="Yacimiento de Materias Primas:", font=fuente_label, foreground="gray30").grid(row=3, column=2, sticky="e", padx=5, pady=2)
entrada_yacimiento = tk.Entry(frame_principal)
entrada_yacimiento.grid(row=3, column=3, padx=5, pady=2)

tk.Label(frame_principal, text="UTM ESTE NAD 27:", font=fuente_label, foreground="gray30").grid(row=4, column=2, sticky="e", padx=5, pady=2)
entrada_utmestenad = tk.Entry(frame_principal)
entrada_utmestenad.grid(row=4, column=3, padx=5, pady=2)

tk.Label(frame_principal, text="UTM NORTE NAD 27:", font=fuente_label, foreground="gray30").grid(row=5, column=2, sticky="e", padx=5, pady=2)
entrada_utmnortenad = tk.Entry(frame_principal)
entrada_utmnortenad.grid(row=5, column=3, padx=5, pady=2)

tk.Label(frame_principal, text="UTM ESTE WGS 84:", font=fuente_label, foreground="gray30").grid(row=6, column=2, sticky="e", padx=5, pady=2)
entrada_utmestewgs = tk.Entry(frame_principal)
entrada_utmestewgs.grid(row=6, column=3, padx=5, pady=2)

# Tercera columna (4)
tk.Label(frame_principal, text="UTM NORTE WGS 84:", font=fuente_label, foreground="gray30").grid(row=0, column=4, sticky="e", padx=5, pady=2)
entrada_utmnortewgs = tk.Entry(frame_principal)
entrada_utmnortewgs.grid(row=0, column=5, padx=5, pady=2)


creditos = tk.Label(ventana, text="© Brian Aquino - 2025", font=("Arial", 8), fg="gray")
creditos.pack(side="bottom", anchor="e", padx=5, pady=5)


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
columnas = ("Identificador", "Clave del Sitio", "Folio Real", "Nombre del Sitio", "Municipio", "Estructuras", "Concentracion de Materiales",
            "Concheros", "Manifestaciones Gráfico-Rupestres", "Paleontológico", "Yacimiento de Materias Primas", "UTM ESTE NAD 27",
            "UTM NORTE NAD 27", "UTM ESTE WGS 84", "UTM NORTE WGS 84", "Ultima actualización")

treeview = ttk.Treeview(frame_resultados, columns=columnas, show="headings", yscrollcommand=scroll.set, xscrollcommand= h_scrollbar.set, selectmode="extended")
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