import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from excelOperaciones import generar_documentos
import os
import threading


class ExcelWordTab(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.path_excel = ""
        self.path_plantilla = ""
        self.dir_output = ""

        self.pack(fill="both", expand=True)
        self._construir_ui()
        self._actualizar_botones()

    # ==========================
    # LÓGICA
    # ==========================

    def _actualizar_botones(self):
        estado = "normal" if (
            self.path_excel and self.path_plantilla and self.dir_output
        ) else "disabled"
        self.btn_generar.configure(state=estado)

    def examinar_excel(self):
        self.path_excel = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[
                ("Archivos de Excel", "*.xlsx *.xls"),
                ("Todos los archivos", "*.*")
            ]
        )
        self.entradaExcel.delete(0, ctk.END)
        self.entradaExcel.insert(0, self.path_excel)
        self._actualizar_botones()

    def examinar_plantilla(self):
        self.path_plantilla = filedialog.askopenfilename(
            title="Seleccionar plantilla Word",
            filetypes=[("Documentos de Word", "*.docx")]
        )
        self.entradaPlantilla.delete(0, ctk.END)
        self.entradaPlantilla.insert(0, self.path_plantilla)
        self._actualizar_botones()

    def examinar_salida(self):
        self.dir_output = filedialog.askdirectory(
            title="Seleccionar carpeta de salida"
        )
        self.entradaSalida.delete(0, ctk.END)
        self.entradaSalida.insert(0, self.dir_output)
        self._actualizar_botones()

    def generar_documentos(self):
        if not self.path_excel:
            messagebox.showwarning(
                "Advertencia",
                "Debes seleccionar un archivo Excel."
            )
            return

        if not self.path_plantilla:
            messagebox.showwarning(
                "Advertencia",
                "Debes seleccionar una plantilla Word."
            )
            return

        if not self.dir_output:
            messagebox.showwarning(
                "Advertencia",
                "Debes seleccionar una carpeta de salida."
            )
            return

        self.btn_generar.configure(state="disabled")

        ventana = ctk.CTkToplevel(self.winfo_toplevel())
        ventana.title("Generando documentos")
        ventana.geometry("340x120")
        ventana.resizable(False, False)
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text="Generando documentos...",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(20, 10))

        barra = ctk.CTkProgressBar(ventana, mode="indeterminate")
        barra.pack(padx=20, pady=5, fill="x")
        barra.start()

        def ejecutar():
            try:
                generar_documentos(
                    self.path_excel,
                    self.path_plantilla,
                    self.dir_output
                )
                exito = True
                result = "Documentos generados correctamente."
            except Exception as e:
                result = str(e)
                exito = False

            self.after(0, finalizar, exito, result)

        def finalizar(exito, result):
            ventana.destroy()
            self._actualizar_botones()

            if exito:
                self.estado.configure(
                    text=f"Estado: Documentos generados en {os.path.basename(self.dir_output)}."
                )
                messagebox.showinfo(
                    "Información",
                    result
                )
            else:
                self.estado.configure(
                    text="Estado: Ocurrió un error al generar."
                )
                messagebox.showerror(
                    "Error",
                    f"Ocurrió un error al generar los documentos:\n{result}"
                )

        threading.Thread(target=ejecutar, daemon=True).start()

    # ==========================
    # UI
    # ==========================

    def _construir_ui(self):
        frame_docs = ctk.CTkFrame(self)
        frame_docs.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            frame_docs,
            text="📊 Archivos",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))

        frame1 = ctk.CTkFrame(frame_docs, fg_color="transparent")
        frame1.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(frame1, text="Excel:", width=90).pack(side="left")

        self.entradaExcel = ctk.CTkEntry(frame1)
        self.entradaExcel.pack(side="left", fill="x", expand=True, padx=10)

        ctk.CTkButton(
            frame1,
            text="Examinar",
            width=120,
            command=self.examinar_excel
        ).pack(side="left")

        frame2 = ctk.CTkFrame(frame_docs, fg_color="transparent")
        frame2.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(frame2, text="Plantilla:", width=90).pack(side="left")

        self.entradaPlantilla = ctk.CTkEntry(frame2)
        self.entradaPlantilla.pack(side="left", fill="x", expand=True, padx=10)

        ctk.CTkButton(
            frame2,
            text="Examinar",
            width=120,
            command=self.examinar_plantilla
        ).pack(side="left")

        frame3 = ctk.CTkFrame(frame_docs, fg_color="transparent")
        frame3.pack(fill="x", padx=20, pady=(5, 15))

        ctk.CTkLabel(frame3, text="Salida:", width=90).pack(side="left")

        self.entradaSalida = ctk.CTkEntry(frame3)
        self.entradaSalida.pack(side="left", fill="x", expand=True, padx=10)

        ctk.CTkButton(
            frame3,
            text="Examinar",
            width=120,
            command=self.examinar_salida
        ).pack(side="left")

        ctk.CTkLabel(
            frame_docs,
            text=(
                "Cada fila del Excel se usará como datos para generar un "
                "documento Word a partir de la plantilla."
            ),
            font=("Segoe UI", 13),
            anchor="w"
        ).pack(anchor="w", padx=20, pady=(0, 15))

        frameAccion = ctk.CTkFrame(self, fg_color="transparent")
        frameAccion.pack(fill="x", padx=20, pady=10)

        self.btn_generar = ctk.CTkButton(
            frameAccion,
            text="Generar Documentos",
            width=200,
            height=40,
            font=("Segoe UI", 15, "bold"),
            command=self.generar_documentos
        )
        self.btn_generar.pack(side="right", padx=10)

        self.estado = ctk.CTkLabel(
            self,
            text="Estado: Listo.",
            anchor="w"
        )
        self.estado.pack(fill="x", padx=25, pady=(0, 15))
