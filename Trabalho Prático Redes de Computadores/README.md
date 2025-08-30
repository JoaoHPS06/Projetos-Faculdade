# MyFTP - Protocolo de Transferência de Arquivos sobre UDP

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Concluído-green?style=for-the-badge)

Um projeto acadêmico de Redes de Computadores que implementa um protocolo de transferência de arquivos (FTP) simplificado, construído do zero sobre o protocolo UDP, com uma interface gráfica para cliente e servidor.

### Demonstração Animada

![Demo do MyFTP](caminho/para/seu/gif_demo.gif)

## Visão Geral do Projeto

O MyFTP foi desenvolvido como trabalho prático para a disciplina de Redes de Computadores. O principal objetivo era construir um sistema cliente-servidor para transferência de arquivos que não utilizasse a confiabilidade do protocolo TCP. Em vez disso, o desafio central foi implementar uma camada de confiabilidade sobre o **UDP (User Datagram Protocol)**, que é inerentemente não confiável e não orientado à conexão.

O sistema consiste em duas aplicações com interface gráfica (GUI): um servidor capaz de lidar com múltiplos clientes simultaneamente e um cliente que permite ao usuário interagir com o sistema de arquivos remoto.

## Principais Funcionalidades

-   **Autenticação de Usuário:** Sistema de login com validação de credenciais no servidor.
-   **Navegação no Sistema de Arquivos Remoto:** Comandos `ls`, `cd`, `cd ..` e um botão para voltar à raiz.
-   **Manipulação de Diretórios:** Criação (`mkdir`) e remoção (`rmdir`) de pastas no servidor.
-   **Transferência de Arquivos Bidirecional:**
    -   **Upload (`put`):** Envio de arquivos do cliente para o servidor através de um botão de seleção ou da funcionalidade de arrastar e soltar (Drag and Drop).
    -   **Download (`get`):** Download de arquivos do servidor para o cliente.
-   **Interface Gráfica Intuitiva:** Tanto o cliente quanto o servidor possuem interfaces gráficas construídas com Tkinter, facilitando a interação e o monitoramento.
-   **Suporte Multiplataforma:** O sistema é compatível com Windows, macOS e Linux.

## Tecnologias Utilizadas

-   **Linguagem:** Python 3
-   **Rede:** Biblioteca `socket` para comunicação UDP.
-   **Interface Gráfica (GUI):** `Tkinter` (com `ttk` para um visual aprimorado) e `TkinterDnD2` para a funcionalidade de arrastar e soltar.
-   **Concorrência:** Biblioteca `threading`.

## Como Executar o Projeto

**Pré-requisitos:**
-   Python 3.8+
-   `tkinter` instalado no sistema (no Linux, pode ser necessário instalar com `sudo apt install python3-tk`).
-   `venv` para gerenciamento de ambiente virtual (no Linux, `sudo apt install python3-venv`).

**Passos para a Instalação:**

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/JoaoHPS06/Projetos-Faculdade/tree/main/Trabalho%20Pr%C3%A1tico%20Redes%20de%20Computadores] (https://github.com/JoaoHPS06/Projetos-Faculdade/tree/main/Trabalho%20Pr%C3%A1tico%20Redes%20de%20Computadores)
    cd Trabalho Prático Redes de Computadores
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Crie o ambiente
    python3 -m venv venv

    # Ative o ambiente
    # No Windows (Git Bash ou PowerShell):
    source venv/Scripts/activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o Servidor:**
    Em um terminal (com o venv ativado), inicie o servidor. Ele começará a ouvir na porta 12345.
    ```bash
    python3 server.py
    ```

5.  **Execute o Cliente:**
    Em **outro** terminal (também com o venv ativado), inicie o cliente.
    ```bash
    python3 client.py
    ```
    *Obs: Para conectar a um servidor em outra máquina na mesma rede, altere o IP "localhost" no arquivo `client.py` para o IP da máquina do servidor.*
