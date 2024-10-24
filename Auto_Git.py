import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

# Função para executar um comando no terminal
def run_command(command):
    process = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode == 0:
        print(f"Comando '{command}' executado com sucesso.")
    else:
        print(f"Erro ao executar o comando '{command}': {process.stderr}")

# Função para automatizar os passos do Git
def git_automation():
    project_directory = entry_directory.get()
    repo_url = entry_repo_url.get()

    # Verificar se os campos estão preenchidos
    if not project_directory or not repo_url:
        messagebox.showwarning("Entrada inválida", "Por favor, preencha todos os campos.")
        return

    try:
        # Mudar para o diretório do projeto
        os.chdir(project_directory)
        print(f"Entrando no diretório do projeto: {project_directory}")

        # Inicializar o repositório Git
        run_command("git init")

        # Adicionar todos os arquivos
        run_command("git add .")

        # Fazer o primeiro commit
        commit_message = "Primeiro commit automático"
        run_command(f'git commit -m "{commit_message}"')

        # Adicionar o repositório remoto
        run_command(f"git remote add origin {repo_url}")

        # Enviar os arquivos para o GitHub
        run_command("git push -u origin master")

        # Mostrar mensagem de sucesso
        messagebox.showinfo("Sucesso", "Projeto enviado para o GitHub com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

# Função para selecionar o diretório do projeto
def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory)

# Criar a janela principal
root = tk.Tk()
root.title("Automação de Git")

# Definir o layout
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

# Campo para o caminho do diretório do projeto
label_directory = tk.Label(frame, text="Caminho do Projeto:")
label_directory.grid(row=0, column=0, sticky="e")
entry_directory = tk.Entry(frame, width=40)
entry_directory.grid(row=0, column=1, padx=10, pady=5)
button_browse = tk.Button(frame, text="Procurar", command=browse_directory)
button_browse.grid(row=0, column=2)

# Campo para a URL do repositório no GitHub
label_repo_url = tk.Label(frame, text="URL do Repositório GitHub:")
label_repo_url.grid(row=1, column=0, sticky="e")
entry_repo_url = tk.Entry(frame, width=40)
entry_repo_url.grid(row=1, column=1, padx=10, pady=5)

# Botão para iniciar a automação
button_start = tk.Button(frame, text="Enviar para GitHub", command=git_automation, bg="green", fg="white")
button_start.grid(row=2, columnspan=3, pady=10)

# Iniciar a interface gráfica
root.mainloop()
