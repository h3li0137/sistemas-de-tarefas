import argparse
import logging
import gui

def initialize():
    # Configurações iniciais, como carregar preferências do usuário
    print("Inicializando o ambiente...")

def main():
    # Configuração do logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("Iniciando o Gerenciador de Tarefas")

    # Argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Gerenciador de Tarefas")
    parser.add_argument("--debug", action="store_true", help="Executar em modo de depuração")
    args = parser.parse_args()

    if args.debug:
        logging.info("Modo de depuração ativado")

    # Inicialização do ambiente
    initialize()

    # Iniciar a GUI
    try:
        gui.root.mainloop()
    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
