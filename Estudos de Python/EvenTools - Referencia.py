# Importa as bibliotecas que vamos usar no programa.
# datetime para pegar a data e hora atual, time para fazer o sleep, getpass para ocultar a senha, hashlib para não deixar a senha hardcoded, json para persistência e os para manipular os arquivos.
import json
import os
import time
from datetime import datetime
import getpass
import hashlib

# A lista principal que vai guardar todos os nossos eventos
eventos = []


# Funções Utilitárias <-

# Função simples pra limpar o terminal.
def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


# Salva a lista de 'eventos' no arquivo 'eventos.json'
def salvar_eventos():
    with open('eventos.json', 'w', encoding='utf-8') as f:
        json.dump(eventos, f, indent=4, ensure_ascii=False)

# Carrega os eventos do arquivo 'eventos.json'
def carregar_eventos():
    global eventos
    if os.path.exists('eventos.json'):
        try:
            with open('eventos.json', 'r', encoding='utf-8') as f:
                eventos = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            eventos = []

# Função que valida se as datas estão no formato certo.
def data_valida(prompt):
    while True:
        data_str = input(prompt)
        try:
            datetime.strptime(data_str, '%d/%m/%Y')
            return data_str
        except ValueError:
            print("\nErro: Formato de data inválido. Use DD/MM/AAAA.")
            time.sleep(2)


# Solicita a senha em opções onde só o cordenador deve ter acesso.
def autenticar_coordenador():

# hash da senha que escolhi, senha complexa: 123 :)
    senha_correta = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
    
    limpar_terminal()
    print("--- Acesso Restrito a Coordenadores ---")
    senha_digitada = getpass.getpass("Para continuar, digite a senha de coordenador: ")

# Senha_hash_digitada recebe o hash da senha que foi digitada pelo usuario.
# SHA-256 espera receber uma sequencia de bytes, o metodo .encode faz a conversão para bytes.
# Após o SHA-256 retornar o objeto hash, o .hexdigest pega o hash binário bruto que está dentro do objeto e converte em uma string hexadecimal
    senha_hash_digitada = hashlib.sha256(senha_digitada.encode()).hexdigest()

    if senha_hash_digitada == senha_correta:
        print("Acesso permitido!")
        time.sleep(1)
        return True
    else:
        print("\nSenha incorreta. Acesso negado.")
        time.sleep(2)
        return False


# Aqui começa as funções do menu principa <-

# Função para criar um novo evento.
def cadastrar_evento():

# Verifica se o usuário tem a senha de coordenador
    if not autenticar_coordenador():
        return

    limpar_terminal()
    print("--- Cadastro de Novo Evento ---")
    nome = input("Digite o nome do evento: ")
    if not nome:
        print("\nO nome do evento não pode ser vazio.")
        time.sleep(2)
        return

    data = data_valida("Data do evento (DD/MM/AAAA): ")
    descricao = input("Descrição do evento: ")

    try:
        max_p = int(input("Número máximo de participantes: "))
        novo_evento = {
            'nome': nome,
            'data': data,
            'descricao': descricao,
            'max_participantes': max_p,
            'participantes': []
        }
        eventos.append(novo_evento)
        print(f"\nEvento '{nome}' cadastrado com sucesso!")
    except ValueError:
        print("\nErro: O número de participantes deve ser um número inteiro.")
        time.sleep(2)
    
    input("\nPressione Enter para continuar...")


# Mostra todos os eventos que já foram cadastrados.
def visualizar_eventos():
    limpar_terminal()
    print("--- Eventos Disponíveis ---")
    if not eventos:
        print("\nNenhum evento cadastrado no momento.")
        return False
    for i, evento in enumerate(eventos):
        vagas_restantes = evento['max_participantes'] - len(evento['participantes'])
        print(f"\nID do evento: {i}")
        print(f"   Nome: {evento['nome']}")
        print(f"   Data: {evento['data']}")
        print(f"   Descrição: {evento['descricao']}")
        print(f"   Vagas restantes: {vagas_restantes}")
    print("\n--------------------------")
    return True


# Inscreve um aluno em um dos eventos.
def inscrever_aluno():
    if not visualizar_eventos():
        input("\nPressione Enter para continuar...")
        return
    try:
        id_ev = int(input("Digite o ID do evento para se inscrever: "))
        if not (0 <= id_ev < len(eventos)):
            print("\nErro: ID do evento inválido.")
            time.sleep(2)
            input("\nPressione Enter para continuar...")
            return
        nome_al = input("Digite seu nome completo: ")
        if not nome_al or any(char.isdigit() for char in nome_al):
            print("\nErro: Nome inválido. Não pode ser vazio ou conter números.")
            time.sleep(2)
            input("\nPressione Enter para continuar...")
            return
        evento = eventos[id_ev]
        if len(evento['participantes']) < evento['max_participantes']:
            evento['participantes'].append(nome_al)
            print(f"\nInscrição de {nome_al} no evento '{evento['nome']}' realizada com sucesso!")
        else:
            print(f"\nDesculpe, o evento '{evento['nome']}' está lotado.")
    except ValueError:
        print("\nErro: O ID do evento deve ser um número.")
        time.sleep(2)
    input("\nPressione Enter para continuar...")


# Mostra a lista de todo mundo que se inscreveu em um evento específico.
def visualizar_inscritos():
    if not visualizar_eventos():
        input("\nPressione Enter para continuar...")
        return
    try:
        id_ev = int(input("Digite o ID do evento para ver os inscritos: "))
        if not (0 <= id_ev < len(eventos)):
            print("\nErro: ID do evento inválido.")
            time.sleep(2)
            input("\nPressione Enter para continuar...")
            return
        limpar_terminal()
        evento = eventos[id_ev]
        print(f"--- Lista de Inscritos: {evento['nome']} ---")
        if not evento['participantes']:
            print("\nNenhum aluno inscrito neste evento.")
        else:
            for participante in evento['participantes']:
                print(f"- {participante}")
        print("\n--------------------------------------")
    except ValueError:
        print("\nErro: O ID do evento deve ser um número.")
        time.sleep(2)
    input("\nPressione Enter para continuar...")


# Permite editar os dados de um evento que já existe.
def atualizar_evento():
    if not autenticar_coordenador():
        return
        
    if not visualizar_eventos():
        input("\nPressione Enter para continuar...")
        return
    try:
        id_ev = int(input("Digite o ID do evento a atualizar: "))
        if not (0 <= id_ev < len(eventos)):
            print("\nErro: ID do evento inválido.")
            time.sleep(2)
            input("\nPressione Enter para continuar...")
            return
        
        limpar_terminal()
        print(f"--- Atualizando Evento: {eventos[id_ev]['nome']} ---")
        novo_nome = input("Digite o novo nome do evento: ")
        nova_data = data_valida("Digite a nova data (DD/MM/AAAA): ")
        nova_descricao = input("Nova descrição do evento: ")
        novo_max_p = int(input("Novo máximo de participantes: "))
        
        eventos[id_ev]["nome"] = novo_nome
        eventos[id_ev]["data"] = nova_data
        eventos[id_ev]["descricao"] = nova_descricao
        eventos[id_ev]["max_participantes"] = novo_max_p
        
        print(f"\nEvento '{novo_nome}' atualizado com sucesso!")
    except ValueError:
        print("\nErro: ID e Vagas devem ser números inteiros.")
        time.sleep(2)
    input("\nPressione Enter para continuar...")


# Apaga um evento da lista.
def excluir_evento():
    if not autenticar_coordenador():
        return
        
    if not visualizar_eventos():
        input("\nPressione Enter para continuar...")
        return
    try:
        id_ev = int(input("Digite o ID do evento a excluir: "))
        if not (0 <= id_ev < len(eventos)):
            print("\nErro: ID do evento inválido.")
            time.sleep(2)
            input("\nPressione Enter para continuar...")
            return
        evento_nome = eventos[id_ev]['nome']
        resposta = input(f"Tem certeza que deseja excluir o evento '{evento_nome}'? (S/N): ").strip().lower()

        if resposta == 's':
            evento_removido = eventos.pop(id_ev)
            print(f"\nEvento '{evento_removido['nome']}' removido com sucesso!")
        elif resposta == 'n':
            print("\nOperação cancelada.")
        else:
            print("\nResposta inválida. Operação cancelada.")
    except ValueError:
        print("\nErro: O ID do evento deve ser um número.")
        time.sleep(2)
    input("\nPressione Enter para continuar...")

# --- ☕︎ Função Principal que Roda Tudo ☕︎ ---
def main():
    carregar_eventos()
    while True:
        limpar_terminal()
        print("============== EvenTools ===============")
        print("1. Cadastrar Novo Evento (Coordenador)")
        print("2. Visualizar Eventos Disponíveis")
        print("3. Inscrever Aluno em um Evento")
        print("4. Visualizar Inscritos de um Evento")
        print("5. Atualizar um Evento (Coordenador)")
        print("6. Excluir um Evento (Coordenador)")
        print("0. Sair do Sistema")
        print("========================================")
        
        opcao = input("Digite a opção desejada: ")
        if opcao == '1':
            cadastrar_evento()
        elif opcao == "2":
            visualizar_eventos()
            input("\nPressione Enter para continuar...")
        elif opcao == "3":
            inscrever_aluno()
        elif opcao == "4":
            visualizar_inscritos()
        elif opcao == "5":
            atualizar_evento()
        elif opcao == "6":
            excluir_evento()
        elif opcao == '0':
            salvar_eventos()
            print("\nSalvando dados... UniFECAF agradece, até logo!")
            time.sleep(2)
            limpar_terminal()
            break
        else:
            print("\nErro: Opção inválida. Tente novamente.")
            time.sleep(2)

# Essa linha é o que começa o programa. chama a função main() que executa tudo.
main()