import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///alunos.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    nota1 = Column(Float, nullable=False)
    nota2 = Column(Float, nullable=False)
    nota3 = Column(Float, nullable=False)
    nota4 = Column(Float, nullable=False)
    media = Column(Float, nullable=False)

Base.metadata.create_all(engine)

aluno_selecionado_id = None

def validar_nota(nota):
    return 0 <= nota <= 100

def adicionar_aluno():
    global aluno_selecionado_id
    nome = entry_nome.get()
    try:
        nota1 = float(entry_nota1.get())
        nota2 = float(entry_nota2.get())
        nota3 = float(entry_nota3.get())
        nota4 = float(entry_nota4.get())

        if not all(map(validar_nota, [nota1, nota2, nota3, nota4])):
            messagebox.showerror("Erro", "As notas devem estar entre 0 e 100!")
            return

        media = (nota1 + nota2 + nota3 + nota4) / 4

        if aluno_selecionado_id is None:
            aluno = Aluno(nome=nome, nota1=nota1, nota2=nota2, nota3=nota3, nota4=nota4, media=media)
            session.add(aluno)
            messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
        else:
            aluno = session.get(Aluno, aluno_selecionado_id)
            if aluno:
                aluno.nome = nome
                aluno.nota1 = nota1
                aluno.nota2 = nota2
                aluno.nota3 = nota3
                aluno.nota4 = nota4
                aluno.media = media
                messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
            aluno_selecionado_id = None

        session.commit()
        atualizar_lista()
        limpar_campos()
    except ValueError:
        messagebox.showerror("Erro", "Insira notas válidas!")

def atualizar_lista():
    lista.delete(0, tk.END)
    alunos = session.query(Aluno).all()
    for aluno in alunos:
        lista.insert(tk.END, f"{aluno.id} - {aluno.nome} - Média: {aluno.media:.2f}")

def excluir_aluno():
    global aluno_selecionado_id
    selecionado = lista.curselection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um aluno para excluir!")
        return
    aluno_id = int(lista.get(selecionado).split(" - ")[0])
    aluno = session.get(Aluno, aluno_id)
    if aluno:
        session.delete(aluno)
        session.commit()
        atualizar_lista()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Aluno excluído!")
        aluno_selecionado_id = None

def carregar_aluno():
    global aluno_selecionado_id
    selecionado = lista.curselection()
    if not selecionado:
        return
    aluno_id = int(lista.get(selecionado).split(" - ")[0])
    aluno = session.get(Aluno, aluno_id)
    if aluno:
        aluno_selecionado_id = aluno.id
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, aluno.nome)
        entry_nota1.delete(0, tk.END)
        entry_nota1.insert(0, aluno.nota1)
        entry_nota2.delete(0, tk.END)
        entry_nota2.insert(0, aluno.nota2)
        entry_nota3.delete(0, tk.END)
        entry_nota3.insert(0, aluno.nota3)
        entry_nota4.delete(0, tk.END)
        entry_nota4.insert(0, aluno.nota4)

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_nota1.delete(0, tk.END)
    entry_nota2.delete(0, tk.END)
    entry_nota3.delete(0, tk.END)
    entry_nota4.delete(0, tk.END)

root = tk.Tk()
root.title("🎓 Sistema de Média de Alunos")
root.configure(bg="#F8F4FF")

fonte_titulo = ("Comic Sans MS", 20, "bold")
fonte_normal = ("Comic Sans MS", 12)
cor_botao = "#8e44ad"
cor_botao_hover = "#9b59b6"
cor_fundo = "#F8F4FF"
cor_entrada = "#ffffff"
cor_texto = "#2c3e50"

frame = tk.Frame(root, bg=cor_fundo)
frame.pack(pady=10)

def criar_label(texto, linha):
    label = tk.Label(frame, text=texto, bg=cor_fundo, fg=cor_texto, font=fonte_normal)
    label.grid(row=linha, column=0, sticky="e", pady=3)
    return label

def criar_entry(linha):
    entry = tk.Entry(frame, font=fonte_normal, bg=cor_entrada, fg=cor_texto, bd=2, relief="groove")
    entry.grid(row=linha, column=1, pady=3, padx=5)
    return entry

criar_label("Nome:", 0)
entry_nome = criar_entry(0)

criar_label("Nota 1:", 1)
entry_nota1 = criar_entry(1)

criar_label("Nota 2:", 2)
entry_nota2 = criar_entry(2)

criar_label("Nota 3:", 3)
entry_nota3 = criar_entry(3)

criar_label("Nota 4:", 4)
entry_nota4 = criar_entry(4)

def criar_botao(texto, comando):
    botao = tk.Button(root, text=texto, command=comando, bg=cor_botao, fg="white",
                      font=fonte_normal, relief="flat", padx=10, pady=5)
    botao.pack(pady=5)
    botao.bind("<Enter>", lambda e: botao.config(bg=cor_botao_hover))
    botao.bind("<Leave>", lambda e: botao.config(bg=cor_botao))
    return botao

criar_botao("Salvar Aluno (Adicionar/Atualizar)", adicionar_aluno)

tk.Label(root, text="Lista de Alunos:", bg=cor_fundo, font=fonte_titulo, fg=cor_texto).pack(pady=5)
lista = tk.Listbox(root, width=50, height=10, font=("Courier New", 11), bg="white", fg=cor_texto, bd=2, relief="groove")
lista.pack()
lista.bind("<<ListboxSelect>>", lambda event: carregar_aluno())

criar_botao("Excluir Aluno", excluir_aluno)

atualizar_lista()
root.mainloop()
