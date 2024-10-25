import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog, Listbox, Scrollbar, Text, Checkbutton, IntVar, Toplevel, Label, Button


# Função para executar um comando no terminal
def run_command(command):
    process = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.stdout.strip(), process.stderr.strip(), process.returncode


# Função para listar arquivos modificados
def list_files():
    files_window = Toplevel(root)
    files_window.title("Selecione Arquivos para Commit")

    files, _, _ = run_command("git status -s")
    modified_files = files.splitlines()
    vars = []

    # Adicionar arquivos modificados com checkboxes
    for file in modified_files:
        var = IntVar()
        chk = Checkbutton(files_window, text=file, variable=var)
        chk.pack(anchor='w')
        vars.append((file, var))

    def select_files():
        selected_files = [file for file, var in vars if var.get() == 1]
        entry_selected_files.delete(0, tk.END)
        entry_selected_files.insert(0, " ".join(selected_files))
        files_window.destroy()

    button_select_files = Button(files_window, text="Selecionar Arquivos", command=select_files)
    button_select_files.pack(pady=10)


# Função para automatizar os passos do Git
def git_automation():
    project_directory = entry_directory.get()
    repo_url = entry_repo_url.get()
    commit_message = entry_commit_message.get()
    branch_name = entry_branch.get()
    selected_files = entry_selected_files.get()

    # Verificar se os campos estão preenchidos
    if not project_directory or not repo_url or not commit_message:
        messagebox.showwarning("Entrada inválida", "Por favor, preencha todos os campos obrigatórios.")
        return

    try:
        # Validar o diretório e a URL do repositório
        if not os.path.exists(project_directory):
            messagebox.showerror("Erro", "Diretório do projeto não encontrado.")
            return

        # Mudar para o diretório do projeto
        os.chdir(project_directory)
        log_output("Entrando no diretório do projeto: " + project_directory)

        # Inicializar o repositório Git
        run_command("git init")

        # Adicionar arquivos selecionados
        if selected_files:
            run_command(f"git add {selected_files}")
        else:
            run_command("git add .")

        # Fazer o commit com a mensagem fornecida
        run_command(f'git commit -m "{commit_message}"')

        # Remover e adicionar o repositório remoto
        run_command("git remote remove origin")
        run_command(f"git remote add origin {repo_url}")

        # Mudar para a branch especificada
        if branch_name:
            run_command(f"git checkout -b {branch_name}")

        # Enviar os arquivos para o GitHub
        stdout, stderr, returncode = run_command(f"git push -u origin {branch_name if branch_name else 'master'}")
        log_output("Push executado.")

        if returncode == 0:
            log_output(stdout)
            messagebox.showinfo("Sucesso", "Projeto enviado para o GitHub com sucesso!")
        else:
            log_output(stderr)
            messagebox.showerror("Erro", stderr)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


# Função para exibir logs
def log_output(message):
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)


# Função para selecionar o diretório do projeto
def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory)


# Função para listar branches disponíveis
def list_branches():
    project_directory = entry_directory.get()

    if not project_directory:
        messagebox.showwarning("Entrada inválida", "Por favor, preencha o caminho do projeto primeiro.")
        return

    os.chdir(project_directory)
    branches, _, _ = run_command("git branch")
    branch_list = branches.splitlines()

    # Atualizar a Listbox com as branches disponíveis
    listbox_branches.delete(0, tk.END)
    for branch in branch_list:
        listbox_branches.insert(tk.END, branch.strip())


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

# Campo para a mensagem do commit
label_commit_message = tk.Label(frame, text="Mensagem do Commit:")
label_commit_message.grid(row=2, column=0, sticky="e")
entry_commit_message = tk.Entry(frame, width=40)
entry_commit_message.grid(row=2, column=1, padx=10, pady=5)

# Campo para a seleção da branch
label_branch = tk.Label(frame, text="Selecionar Branch:")
label_branch.grid(row=3, column=0, sticky="e")
entry_branch = tk.Entry(frame, width=40)
entry_branch.grid(row=3, column=1, padx=10, pady=5)
button_list_branches = tk.Button(frame, text="Listar Branches", command=list_branches)
button_list_branches.grid(row=3, column=2)

# Listbox para exibir as branches
listbox_branches = Listbox(frame, height=5, width=40)
listbox_branches.grid(row=4, column=0, columnspan=3, pady=10)

# Campo para arquivos selecionados
label_selected_files = tk.Label(frame, text="Arquivos para Commit:")
label_selected_files.grid(row=5, column=0, sticky="e")
entry_selected_files = tk.Entry(frame, width=40)
entry_selected_files.grid(row=5, column=1, padx=10, pady=5)
button_select_files = tk.Button(frame, text="Selecionar Arquivos", command=list_files)
button_select_files.grid(row=5, column=2)

# Área de log
label_log = tk.Label(frame, text="Logs:")
label_log.grid(row=6, column=0, sticky="nw")
log_text = Text(frame, height=10, width=50, wrap="word")
log_text.grid(row=6, column=1, columnspan=2, pady=5)

# Botão para iniciar a automação
button_start = tk.Button(frame, text="Enviar para GitHub", command=git_automation, bg="green", fg="white")
button_start.grid(row=7, columnspan=3, pady=10)

# Iniciar a interface gráfica
root.mainloop()
