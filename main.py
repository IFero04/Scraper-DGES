from console import clear_console, add_dot_every_second
from api import get_ensino, get_escolas, get_cursos, get_alunos
from csv_save import export_csv, Item
from alive_progress import alive_bar

def main():
    ensinos = get_ensino('col1listas.asp')
    print('\tENSINOS ENCONTRADOS')
    for ensino in ensinos:
        print(f'{ensino["id"]}. {ensino["nome"]}')
    print('0. Get All')
    escolha = int(input('\nEscolha o ensino que deseja ver as escolas: '))
    clear_console()

    if escolha == 0:
        for ensino in ensinos:
            print(f"\tENSINO [{ensino['nome']}]\n")
            escolas, CodR = get_escolas(ensino["link"])
            with alive_bar(len(escolas), bar='bubbles', spinner='crab') as main_bar:
                for escola in escolas:
                    cursos = get_cursos('col1listaredir.asp', {'CodEstab': escola['id'], 'CodR': CodR})
                    print(f'COLETAR ALUNOS DA ESCOLA {escola["nome"]}')
                    itens_alunos = []
                    for curso in cursos:
                        alunos = get_alunos('col1listacol.asp', {'CodEstab': escola['id'], 'CodR': CodR, 'CodCurso': curso['id']})
                        for aluno in alunos:
                            item_aluno = Item(id=aluno['id'], nome=aluno['nome'], cod_curso=curso['id'], curso=curso['nome'])
                            itens_alunos.append(item_aluno)

                    print(f'A ESCREVER DADOS PARA CSV [alunos_{escola["id"]}.csv]')
                    export_csv(itens_alunos, f'alunos_{escola["id"]}.csv')
                    print('DADOS EXPORTADOS COM SUCESSO!')
                    print()
                    main_bar()
                
    else:
        if escolha < 1 or escolha > len(ensinos):
            print('Escolha inválida')
            return
        
        escolas, CodR = get_escolas(ensinos[escolha-1]["link"])
        add_dot_every_second(f'A Procurar Escolas de {ensinos[escolha-1]["nome"]} ')

        clear_console()
        print('\tESCOLAS ENCONTRADAS')
        for escola in escolas:
            print(f'{escola["id"]}. {escola["nome"]}')

        escolha = input('\nEscolha a escola que deseja verificar: ')
        ids_escolas = [escola["id"] for escola in escolas]
        if escolha not in ids_escolas:
            print('Escolha inválida')
            return
        
        clear_console()
        cursos = get_cursos('col1listaredir.asp', {'CodEstab': escolha, 'CodR': CodR})
        print('\tCURSOS ENCONTRADOS')
        for curso in cursos:
            print(f'{curso["id"]}. {curso["nome"]}')

        print('\nA COLETAR DADOS DOS ALUNOS ')
        itens_alunos = []
        with alive_bar(len(cursos), bar='bubbles',spinner='crab') as bar:
            for curso in cursos:
                alunos = get_alunos('col1listacol.asp', {'CodEstab': escolha, 'CodR': CodR, 'CodCurso': curso['id']})
                for aluno in alunos:
                    item_aluno = Item(id=aluno['id'], nome=aluno['nome'], cod_curso=curso['id'], curso=curso['nome'])
                    itens_alunos.append(item_aluno)
                bar()
            
        print(f'A ESCREVER DADOS PARA CSV [alunos_{escolha}.csv]')
        export_csv(itens_alunos, f'alunos_{escolha}.csv')
        print('DADOS EXPORTADOS COM SUCESSO!')
        
if __name__ == '__main__':
    main()
