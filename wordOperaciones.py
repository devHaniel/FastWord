from docxcompose.composer import Composer
from docx import Document
from datetime import datetime
from docxtpl import DocxTemplate

def unir_documentos(output_path, *input_paths):

    base_doc = Document(input_paths[0])
    composer = Composer(base_doc)

    for file_path in input_paths[1:]:
        doc = Document(file_path)
        composer.append(doc)

    composer.save(output_path)
    return f"Documentos unidos! En: {output_path}"

def reemplzar_variables(path_doc, path_output = None, **kwargs):
    doc = DocxTemplate(path_doc)
    doc.render(kwargs)

    if path_output:
        doc.save(path_output)
    else:
        doc.save(path_doc)

    return f"Variables reemplazadas! En: {path_output if path_output else path_doc}"

if __name__ == "__main__":
    # Ejemplo de uso
    reemplzar_variables("/home/haniel/Downloads/Formato de Informe y Portada.docx", path_output="filled_template.docx", 
                        titulo="Juan", semana=3, sec=265, docente="Prof. Perez", fecha=datetime.now().strftime("%d/%m/%Y"))