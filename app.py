import customtkinter as ctk
from tabs.tab_reemplazar import ReemplazarVariablesTab
from tabs.tab_unir import UnirDocumentosTab
from tabs.tab_excel_word import ExcelWordTab

ctk.set_appearance_mode("System")  # Light, Dark o System
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Herramientas de Documentos")
app.geometry("950x680")
app.minsize(800, 600)

tabview = ctk.CTkTabview(app)
tabview.pack(fill="both", expand=True, padx=10, pady=10)

ReemplazarVariablesTab(tabview.add("📝 Reemplazar Variables"))
UnirDocumentosTab(tabview.add("📄 Unir Documentos"))
ExcelWordTab(tabview.add("📊 Excel → Word"))

app.mainloop()
