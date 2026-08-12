import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from wordOperaciones import unir_documentos
import os
import threading


class UnirDocumentosTab(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.documentos = []

        self.pack(fill="both", expand=True)
        self._construir_ui()
        self._actualizar_botones()

    # ==========================
    # LÓGICA
    # ==========================

    def actualizar_lista(self):
        self.tabla.delete(*self.tabla.get_children())

        for i, path in enumerate(self.documentos, start=1):
            nombre = os.path.basename(path)

            self.tabla.insert(
                "",
                "end",
                values=(i, nombre, path)
            )

        self._actualizar_botones()

    def _actualizar_botones(self):
        estado_boton = "normal" if self.documentos else "disabled"
        self.btn_unir.configure(state=estado_boton)

    def agregar_documentos(self):
        archivos = filedialog.askopenfilenames(
            title="Seleccionar documentos Word",
            filetypes=[
                ("Documentos de Word", "*.docx"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not archivos:
            return

        for archivo in archivos:
            if archivo not in self.documentos:
                self.documentos.append(archivo)

        self.actualizar_lista()

        self.estado.configure(
            text=f"Estado: {len(self.documentos)} documento(s) agregado(s)."
        )

    def eliminar_documento(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Selecciona un documento para eliminar."
            )
            return

        indices = []

        for item in seleccion:
            valores = self.tabla.item(item, "values")
            indice = int(valores[0]) - 1
            indices.append(indice)

        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Deseas eliminar el documento seleccionado?"
        )

        if not respuesta:
            return

        for indice in sorted(indices, reverse=True):
            self.documentos.pop(indice)

        self.actualizar_lista()

        self.estado.configure(
            text=f"Estado: {len(self.documentos)} documento(s) en la lista."
        )

    def mover_arriba(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Selecciona un documento."
            )
            return

        item = seleccion[0]
        indice = int(self.tabla.item(item, "values")[0]) - 1

        if indice == 0:
            return

        self.documentos[indice], self.documentos[indice - 1] = (
            self.documentos[indice - 1],
            self.documentos[indice]
        )

        self.actualizar_lista()

        self._seleccionar_fila(indice - 1)

    def mover_abajo(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Selecciona un documento."
            )
            return

        item = seleccion[0]
        indice = int(self.tabla.item(item, "values")[0]) - 1

        if indice >= len(self.documentos) - 1:
            return

        self.documentos[indice], self.documentos[indice + 1] = (
            self.documentos[indice + 1],
            self.documentos[indice]
        )

        self.actualizar_lista()

        self._seleccionar_fila(indice + 1)

    def _seleccionar_fila(self, indice):
        items = self.tabla.get_children()

        if 0 <= indice < len(items):
            self.tabla.selection_set(items[indice])
            self.tabla.focus(items[indice])
            self.tabla.see(items[indice])

    def limpiar_lista(self):
        if not self.documentos:
            return

        respuesta = messagebox.askyesno(
            "Limpiar lista",
            "¿Deseas eliminar todos los documentos?"
        )

        if not respuesta:
            return

        self.documentos.clear()

        self.actualizar_lista()

        self.estado.configure(
            text="Estado: Lista vacía."
        )

    def unir_documentos(self):
        if not self.documentos:
            messagebox.showwarning(
                "Advertencia",
                "No hay documentos para unir."
            )
            return

        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar documento unido",
            defaultextension=".docx",
            filetypes=[("Documentos de Word", "*.docx")]
        )

        if not ruta_salida:
            return

        self.btn_unir.configure(state="disabled")

        ventana = ctk.CTkToplevel(self.winfo_toplevel())
        ventana.title("Uniendo documentos")
        ventana.geometry("320x120")
        ventana.resizable(False, False)
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="Uniendo documentos...",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(20, 10))

        barra = ctk.CTkProgressBar(ventana, mode="indeterminate")
        barra.pack(padx=20, pady=5, fill="x")
        barra.start()

        def ejecutar():
            try:
                result = unir_documentos(ruta_salida, *self.documentos)
                exito = True
            except Exception as e:
                result = str(e)
                exito = False

            self.after(0, finalizar, exito, result)

        def finalizar(exito, result):
            ventana.destroy()
            self._actualizar_botones()

            if exito:
                self.estado.configure(
                    text=f"Estado: Documentos unidos en {os.path.basename(ruta_salida)}."
                )
                messagebox.showinfo(
                    "Documentos",
                    result
                )
            else:
                messagebox.showerror(
                    "Error",
                    f"Ocurrió un error al unir los documentos:\n{result}"
                )

        threading.Thread(target=ejecutar, daemon=True).start()

    # ==========================
    # UI
    # ==========================

    def _construir_ui(self):
        frame_docs = ctk.CTkFrame(self)
        frame_docs.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(20, 10)
        )

        ctk.CTkLabel(
            frame_docs,
            text="📄 Documentos",
            font=("Segoe UI", 20, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        ctk.CTkLabel(
            frame_docs,
            text="Agrega los documentos Word en el orden en que deseas unirlos.",
            font=("Segoe UI", 13)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        frame_tabla = ctk.CTkFrame(
            frame_docs,
            fg_color="transparent"
        )
        frame_tabla.pack(
            fill="both",
            expand=True,
            padx=20
        )

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=("Orden", "Documento", "Ruta"),
            show="headings",
            selectmode="extended"
        )

        self.tabla.heading("Orden", text="#")
        self.tabla.heading("Documento", text="Documento")
        self.tabla.heading("Ruta", text="Ruta")

        self.tabla.column("Orden", width=50, anchor="center")
        self.tabla.column("Documento", width=250)
        self.tabla.column("Ruta", width=500)

        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        frame_botones = ctk.CTkFrame(
            frame_docs,
            fg_color="transparent"
        )
        frame_botones.pack(
            fill="x",
            padx=20,
            pady=15
        )

        ctk.CTkButton(
            frame_botones,
            text="＋ Agregar documentos",
            width=160,
            command=self.agregar_documentos
        ).pack(side="left")

        ctk.CTkButton(
            frame_botones,
            text="− Eliminar",
            width=120,
            fg_color="#D9534F",
            hover_color="#C9302C",
            command=self.eliminar_documento
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frame_botones,
            text="Limpiar",
            width=100,
            command=self.limpiar_lista
        ).pack(side="left")

        frame_orden = ctk.CTkFrame(self)
        frame_orden.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ctk.CTkLabel(
            frame_orden,
            text="Orden de unión:",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=15)

        ctk.CTkButton(
            frame_orden,
            text="↑ Subir",
            width=110,
            command=self.mover_arriba
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            frame_orden,
            text="↓ Bajar",
            width=110,
            command=self.mover_abajo
        ).pack(side="left", padx=5)

        self.btn_unir = ctk.CTkButton(
            frame_orden,
            text="Unir documentos",
            width=170,
            height=40,
            font=("Segoe UI", 15, "bold"),
            command=self.unir_documentos
        )
        self.btn_unir.pack(side="right", padx=15)

        self.estado = ctk.CTkLabel(
            self,
            text="Estado: Lista vacía.",
            anchor="w"
        )
        self.estado.pack(
            fill="x",
            padx=25,
            pady=(0, 15)
        )
