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

def validar_nota(nota):
    return 0 <= nota <= 100

def adicionar_aluno():
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
        aluno = Aluno(nome=nome, nota1=nota1, nota2=nota2, nota3=nota3, nota4=nota4, media=media)
        session.add(aluno)
        session.commit()
        messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
        atualizar_lista()
    except ValueError:
        messagebox.showerror("Erro", "Insira notas válidas!")

def atualizar_lista():
    lista.delete(0, tk.END)
    alunos = session.query(Aluno).all()
    for aluno in alunos:
        lista.insert(tk.END, f"{aluno.nome} - Média: {aluno.media:.2f}")

def excluir_aluno():
    selecionado = lista.curselection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um aluno para excluir!")
        return
    aluno_nome = lista.get(selecionado).split(" - ")[0]
    aluno = session.query(Aluno).filter_by(nome=aluno_nome).first()
    if aluno:
        session.delete(aluno)
        session.commit()
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Aluno excluído!")

def atualizar_aluno():
    selecionado = lista.curselection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um aluno para atualizar!")
        return
    aluno_nome = lista.get(selecionado).split(" - ")[0]
    aluno = session.query(Aluno).filter_by(nome=aluno_nome).first()
    if aluno:
        try:
            aluno.nome = entry_nome.get()
            aluno.nota1 = float(entry_nota1.get())
            aluno.nota2 = float(entry_nota2.get())
            aluno.nota3 = float(entry_nota3.get())
            aluno.nota4 = float(entry_nota4.get())

            if not all(map(validar_nota, [aluno.nota1, aluno.nota2, aluno.nota3, aluno.nota4])):
                messagebox.showerror("Erro", "As notas devem estar entre 0 e 100!")
                return
            
            aluno.media = (aluno.nota1 + aluno.nota2 + aluno.nota3 + aluno.nota4) / 4
            session.commit()
            atualizar_lista()
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
        except ValueError:
            messagebox.showerror("Erro", "Insira notas válidas!")

root = tk.Tk()
root.title("Sistema de Média de Alunos")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Nome:").grid(row=0, column=0)
entry_nome = tk.Entry(frame)
entry_nome.grid(row=0, column=1)

tk.Label(frame, text="Nota 1:").grid(row=1, column=0)
entry_nota1 = tk.Entry(frame)
entry_nota1.grid(row=1, column=1)

tk.Label(frame, text="Nota 2:").grid(row=2, column=0)
entry_nota2 = tk.Entry(frame)
entry_nota2.grid(row=2, column=1)

tk.Label(frame, text="Nota 3:").grid(row=3, column=0)
entry_nota3 = tk.Entry(frame)
entry_nota3.grid(row=3, column=1)

tk.Label(frame, text="Nota 4:").grid(row=4, column=0)
entry_nota4 = tk.Entry(frame)
entry_nota4.grid(row=4, column=1)

tk.Button(root, text="Adicionar Aluno", command=adicionar_aluno).pack()

tk.Label(root, text="Lista de Alunos:").pack()
lista = tk.Listbox(root, width=40, height=10)
lista.pack()

tk.Button(root, text="Excluir Aluno", command=excluir_aluno).pack()

tk.Button(root, text="Atualizar Aluno", command=atualizar_aluno).pack()

atualizar_lista()
root.mainloop()

