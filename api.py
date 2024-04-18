import requests
from bs4 import BeautifulSoup
from util import extract_escolas, extract_cursos

URL = "https://dges.gov.pt/coloc/2023/"


def get_ensino(page):
    url = str(URL + page)
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
    url = str(URL + page)
    CodR = ""
    escolas = []
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        CodR = soup.find("input", {"name": "CodR"})

        select = soup.find("select", {"name": "CodEstab"})
        if select:
            options = select.find_all("option")
            values_texts = [(option['value'], option.get_text(strip=True)) for option in options]

            for value, text in values_texts:
                text = extract_escolas(text)
                escolas.append({
                    "id": value,
                    "nome": text
                })
    else:
        print("Failed to retrieve data from the website.")

    return escolas, CodR["value"]

def get_cursos(page, options):
    url = str(URL + page)
    cursos = []
    payload = {
        'CodEstab': options['CodEstab'],
        'CodR': options['CodR'],
        'listagem': "Lista de Colocados"
    }
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        select = soup.find("select", {"name": "CodCurso"})
        if select:
            options = select.find_all("option")
            values_texts = [(option['value'], option.get_text(strip=True)) for option in options]

            for value, text in values_texts:
                text = extract_cursos(text)
                cursos.append({
                    "id": value,
                    "nome": text.split("-")[1].strip()
                })

    else:
        print("Failed to retrieve data from the website.")
    
    return cursos

def get_alunos(page, options):
    url = str(URL + page)
    alunos = []
    payload = {
        'CodEstab': options['CodEstab'],
        'CodR': options['CodR'],
        "CodCurso": options['CodCurso'],
        "search": "Continuar"
    }
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table')

        for row in table.find_all("tr"):
                columns = row.find_all('td')
                if len(columns) == 2: 
                    aluno_id = columns[0].get_text(strip=True)
                    aluno_nome = columns[1].get_text(strip=True)
                    alunos.append({'id': aluno_id, 'nome': aluno_nome})
                    
        alunos = alunos[1:]

    else:
        print("Failed to retrieve data from the website.")
     
    return alunos

