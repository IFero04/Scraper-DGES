import requests
from bs4 import BeautifulSoup
from console import clear_console, add_dot_every_second
from csv_save import export_csv, Item

URL = "https://dges.gov.pt/coloc/2023/"

def extract_substring(text):
    have_text = False
    result = ''
    for char in text:
        if char.isdigit() and have_text:
            break
        if char.isalpha():
            have_text = True
        result += char
    return result.strip()

def get_ensino(page):
    url = f'https://dges.gov.pt/coloc/2023/{page}'
    ensinos = []
    id_count = 1
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table")

        for row in table.find_all("tr")[1:]:
            columns = row.find_all("td")
            if columns: 
                data_list = [column.get_text(strip=True) for column in columns]
                hrefs = [column.find("a")['href'] if column.find("a") else '' for column in columns]
                
                for i in range(len(data_list)):
                    word_list = data_list[i].split()
                    if word_list and word_list[0] == "Ensino":
                        ensinos.append({
                            "id": id_count,
                            "nome": data_list[i],
                            "link": hrefs[i]
                        })
                        id_count += 1
    else:
        print("Failed to retrieve data from the website.")
    
    return ensinos

def get_escolas(page):
    url = f'https://dges.gov.pt/coloc/2023/{page}'
    escolas = []
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        select = soup.find("select", {"name": "CodEstab"})
        if select:
            options = select.find_all("option")
            values_texts = [(option['value'], option.get_text(strip=True)) for option in options]

            for value, text in values_texts:
                text = extract_substring(text)
                escolas.append({
                    "id": value,
                    "nome": text
                })
    else:
        print("Failed to retrieve data from the website.")

    return escolas
    
def get_colocados(page, selected_option):
    url = f'https://dges.gov.pt/coloc/2023/{page}'
    payload = {
        'CodEstab': selected_option,
        'listagem': 'Lista de Colocados'
    }
    response = requests.post(url, data=payload)
    print(response.status_code)
    print(response.content)


def main1():
    get_colocados('ccol1listaredir.asp', '0140')

def main():
    ensinos = get_ensino('col1listas.asp')
    print('\tENSIONOS ENCONTRADOS')
    for ensino in ensinos:
        print(f'{ensino["id"]}. {ensino["nome"]}')
    escolha = int(input('\nEscolha o ensino que deseja ver as escolas: '))
    if escolha < 1 or escolha > len(ensinos):
        print('Escolha inválida')
        return

    clear_console()
    escolas = get_escolas(ensinos[escolha-1]["link"])
    export_csv([Item(escola["id"], escola["nome"]) for escola in escolas], 'escolas.csv')
    add_dot_every_second(f'A Procurar Escolas de {ensinos[escolha-1]["nome"]} ')

    clear_console()
    print('\tESCOLAS ENCONTRADAS')
    for escola in escolas:
        print(f'{escola["id"]}. {escola["nome"]}')
    
         
        

if __name__ == '__main__':
    main()
