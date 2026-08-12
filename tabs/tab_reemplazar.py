import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from wordOperaciones import reemplzar_variables


class ReemplazarVariablesTab(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.path_doc = ""
        self.path_output = ""
        self.variables_dict = {}

        self.pack(fill="both", expand=True)
        self._construir_ui()

    # ==========================
    # LÓGICA
    # ==========================

    def generar_documento(self):
        if not self.path_doc:
            messagebox.showwarning(
                "Advertencia",
                "Debes seleccionar una plantilla."
            )
            return

        if not self.variables_dict:
            messagebox.showwarning(
                "Advertencia",
                "Debes ingresar al menos una variable."
            )
            return

        try:
            result = reemplzar_variables(
                self.path_doc,
                self.path_output if self.path_output else None,
                **self.variables_dict
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Ocurrió un error al generar el documento:\n{e}"
            )
            return

        messagebox.showinfo(
            "Información",
            result
        )

    def examinar_plantilla(self):
        self.path_doc = filedialog.askopenfilename(
            title="Seleccionar Plantilla",
            filetypes=[("Documentos de Word", "*.docx")]
        )
        self.entradaPlantilla.delete(0, ctk.END)
        self.entradaPlantilla.insert(0, self.path_doc)

    def examinar_salida(self):
        self.path_output = filedialog.asksaveasfilename(
            title="Seleccionar Ubicación de Salida",
            filetypes=[("Documentos de Word", "*.docx")]
        )
        self.entradaSalida.delete(0, ctk.END)
        self.entradaSalida.insert(0, self.path_output)

    def agregar_variable(self):
        ventana = ctk.CTkToplevel(self.winfo_toplevel())
        ventana.title("Agregar Variable")
        ventana.geometry("400x250")
        ventana.resizable(False, False)

        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="Nueva Variable",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(20, 15))

        ctk.CTkLabel(
            ventana,
            text="Nombre de la variable:"
        ).pack(anchor="w", padx=30)

        entrada_variable = ctk.CTkEntry(ventana)
        entrada_variable.pack(fill="x", padx=30, pady=(5, 10))

        ctk.CTkLabel(
            ventana,
            text="Valor:"
        ).pack(anchor="w", padx=30)

        entrada_valor = ctk.CTkEntry(ventana)
        entrada_valor.pack(fill="x", padx=30, pady=(5, 15))

        def guardar():
            variable = entrada_variable.get().strip()
            valor = entrada_valor.get()

            if not variable:
                return

            self.variables_dict[variable] = valor
            self.tabla.insert(
                "",
                "end",
                values=(variable, valor)
            )

            ventana.destroy()

        ctk.CTkButton(
            ventana,
            text="Agregar",
            command=guardar
        ).pack(pady=10)

    def eliminar_variable(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            self.estado.configure(
                text="Estado: Selecciona una variable para eliminar."
            )
            return

        for item in seleccion:
            variable = self.tabla.item(item, "values")[0]
            del self.variables_dict[variable]
            self.tabla.delete(item)

        self.estado.configure(text="Estado: Variable eliminada.")

    # ==========================
    # UI
    # ==========================

    def _construir_ui(self):
        frame_docs = ctk.CTkFrame(self)
        frame_docs.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            frame_docs,
            text="📄 Documentos",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))

        frame1 = ctk.CTkFrame(frame_docs, fg_color="transparent")
        frame1.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(frame1, text="Plantilla:", width=90).pack(side="left")

        self.entradaPlantilla = ctk.CTkEntry(frame1)
        self.entradaPlantilla.pack(side="left", fill="x", expand=True, padx=10)

        ctk.CTkButton(
            frame1,
            text="Examinar",
            width=120,
            command=self.examinar_plantilla
        ).pack(side="left")

        frame2 = ctk.CTkFrame(frame_docs, fg_color="transparent")
        frame2.pack(fill="x", padx=20, pady=(5, 15))

        ctk.CTkLabel(frame2, text="Guardar:", width=90).pack(side="left")

        self.entradaSalida = ctk.CTkEntry(frame2)
        self.entradaSalida.pack(side="left", fill="x", expand=True, padx=10)

        ctk.CTkButton(
            frame2,
            text="Examinar",
            width=120,
            command=self.examinar_salida
        ).pack(side="left")

        frameVariables = ctk.CTkFrame(self)
        frameVariables.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(
            frameVariables,
            text="📝 Variables",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))

        self.tabla = ttk.Treeview(
            frameVariables,
            columns=("Variable", "Valor"),
            show="headings",
            height=12
        )

        self.tabla.heading("Variable", text="Variable")
        self.tabla.heading("Valor", text="Valor")

        self.tabla.column("Variable", width=220)
        self.tabla.column("Valor", width=500)

        self.tabla.pack(fill="both", expand=True, padx=20)

        frameBotones = ctk.CTkFrame(frameVariables, fg_color="transparent")
        frameBotones.pack(fill="x", padx=20, pady=15)

        ctk.CTkButton(
            frameBotones,
            text="+ Agregar",
            width=120,
            command=self.agregar_variable
        ).pack(side="left")

        ctk.CTkButton(
            frameBotones,
            text="- Eliminar",
            width=120,
            fg_color="#D9534F",
            hover_color="#C9302C",
            command=self.eliminar_variable
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frameBotones,
            text="Generar Documento",
            width=180,
            height=40,
            font=("Segoe UI", 15, "bold"),
            command=self.generar_documento
        ).pack(side="right")

        self.estado = ctk.CTkLabel(
            self,
            text="Estado: Listo.",
            anchor="w"
        )
        self.estado.pack(fill="x", padx=25, pady=(0, 15))
