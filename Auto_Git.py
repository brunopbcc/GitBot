import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import requests


# Função para listar os repositórios do usuário
def load_repositories():
    global token, username
    token = entry_token.get()
    username = entry_username.get()

    if not token or not username:
        messagebox.showwarning("Informação inválida", "Por favor, insira um token e nome de usuário válidos.")
        return

    # Faz a requisição à API do GitHub
    headers = {'Authorization': f'token {token}'}
    response = requests.get(f'https://api.github.com/users/{username}/repos', headers=headers)

    if response.status_code == 200:
        repos_data = response.json()
        repo_names = [repo['name'] for repo in repos_data]
        repo_combo['values'] = repo_names  # Atualiza a combobox com os nomes dos repositórios
        messagebox.showinfo("Sucesso", "Repositórios carregados com sucesso.")
    else:
        messagebox.showerror("Erro",
                             "Não foi possível carregar os repositórios. Verifique o token e o nome de usuário.")


# Função para executar comandos do Git
def git_automation():
    project_directory = entry_directory.get()
    repo_name = repo_combo.get()
    commit_message = entry_commit_message.get()
    branch_name = entry_branch.get()

    if not project_directory or not repo_name or not commit_message or not username:
        messagebox.showwarning("Entrada inválida", "Por favor, preencha todos os campos obrigatórios.")
        return

    try:
        os.chdir(project_directory)
        run_command("git init")
        run_command("git add .")
        run_command(f'git commit -m "{commit_message}"')
        run_command("git remote remove origin")
        run_command(
            f"git remote add origin https://github.com/{username}/{repo_name}.git")  # Ajuste para usar o nome do usuário e do repo
        if branch_name:
            run_command(f"git checkout -b {branch_name}")
        run_command("git push -u origin " + (branch_name if branch_name else "master"))
        messagebox.showinfo("Sucesso", "Projeto enviado para o GitHub com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


# Função para executar comandos no terminal
def run_command(command):
    process = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.stdout.strip(), process.stderr.strip(), process.returncode


# Função para selecionar o diretório do projeto
def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory)


# Interface Gráfica
root = tk.Tk()
root.title("Automação de Git")

# Definir o layout
frame = tk.Frame(root, padx=20, pady=20, bg="#2e2e2e")
frame.pack(padx=10, pady=10)

# Campo para o nome de usuário do GitHub
label_username = tk.Label(frame, text="Nome de Usuário GitHub:", bg="#2e2e2e", fg="white")
label_username.grid(row=0, column=0, sticky="e")
entry_username = tk.Entry(frame, width=40)
entry_username.grid(row=0, column=1, padx=10, pady=5)

# Campo para o token do GitHub
label_token = tk.Label(frame, text="Token GitHub:", bg="#2e2e2e", fg="white")
label_token.grid(row=1, column=0, sticky="e")
entry_token = tk.Entry(frame, width=40, show="*")  # Oculta o token com '*'
entry_token.grid(row=1, column=1, padx=10, pady=5)
button_validate_token = tk.Button(frame, text="Carregar Repositórios", command=load_repositories, bg="#1e90ff",
                                  fg="white")
button_validate_token.grid(row=1, column=2, padx=(10, 0), pady=5)

# Campo para o caminho do diretório do projeto
label_directory = tk.Label(frame, text="Caminho do Projeto:", bg="#2e2e2e", fg="white")
label_directory.grid(row=2, column=0, sticky="e")
entry_directory = tk.Entry(frame, width=40)
entry_directory.grid(row=2, column=1, padx=10, pady=5)
button_browse = tk.Button(frame, text="Procurar", command=browse_directory, bg="#1e90ff", fg="white")
button_browse.grid(row=2, column=2, padx=(10, 0), pady=5)

# Campo para selecionar o repositório GitHub
label_repo = tk.Label(frame, text="Repositório GitHub:", bg="#2e2e2e", fg="white")
label_repo.grid(row=3, column=0, sticky="e")
repo_combo = ttk.Combobox(frame, width=37)
repo_combo.grid(row=3, column=1, padx=10, pady=5)

# Campo para a mensagem do commit
label_commit_message = tk.Label(frame, text="Mensagem do Commit:", bg="#2e2e2e", fg="white")
label_commit_message.grid(row=4, column=0, sticky="e")
entry_commit_message = tk.Entry(frame, width=40)
entry_commit_message.grid(row=4, column=1, padx=10, pady=5)

# Campo para a seleção da branch
label_branch = tk.Label(frame, text="Selecionar Branch:", bg="#2e2e2e", fg="white")
label_branch.grid(row=5, column=0, sticky="e")
entry_branch = tk.Entry(frame, width=40)
entry_branch.grid(row=5, column=1, padx=10, pady=5)

# Botão para iniciar a automação
button_start = tk.Button(frame, text="Enviar para GitHub", command=git_automation, bg="#1e90ff", fg="white")
button_start.grid(row=6, column=0, columnspan=3, pady=20)

# Iniciar a interface gráfica
root.mainloop()
