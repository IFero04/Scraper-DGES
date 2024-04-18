from dataclasses import dataclass

@dataclass
class Item:
    id: str
    nome: str
    cod_curso: str
    curso: str
   
def export_csv(data, filename):
    with open(f'csv/{filename}', "w", encoding="utf-8") as file:
        file.write("Código Curso;Curso;Nº Identificação(parcial);Nome\n")
        for item in data:
            file.write(f"{item.cod_curso};{item.curso};{item.id};{item.nome}\n")

