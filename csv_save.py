from dataclasses import dataclass

@dataclass
class Item:
    id: str
    name: str
   
def export_csv(data, filename):
    with open(f'csv/{filename}', "w", encoding="utf-8") as file:
        file.write("id,name\n")
        for item in data:
            file.write(f"{item.id},{item.name}\n")
