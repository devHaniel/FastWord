import pandas as pd
from wordOperaciones import reemplzar_variables
import os

def generar_documentos(path_excel, path_doc , dir_output):
    try:
        df = pd.read_excel(path_excel)
        diccionario = df.to_dict(orient='records')
        os.makedirs(dir_output, exist_ok=True)

        for i, row in enumerate(diccionario):
            output_path = f"{dir_output}/documento_{i+1}.docx"
            reemplzar_variables(path_doc, output_path, **row)
            print(f"Documento generado: {output_path}")

    except FileNotFoundError:
        print(f"El archivo Excel no se encontró en la ruta: {path_excel}")
        return

    except Exception as e:
        print(f"Ocurrió un error al leer el archivo Excel: {e}")
        return
    

if __name__ == "__main__":
    generar_documentos('/home/haniel/Documents/Python/tonteras/plantillas/reconocimientos.xlsx', '/home/haniel/Documents/Python/tonteras/plantillas/plantilla.docx', '/home/haniel/Documents/Python/tonteras/output')

