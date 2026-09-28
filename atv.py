import tkinter as tk
from tkinter import ttk, messagebox

# Janela Principal
janela = tk.Tk()
janela.title("TaskManager")
janela.geometry("900x600")
janela.configure(bg="#fdf8f5")

# Dados em memória
lista_tarefas = []
lista_agendamentos = []

# -------------------- PALETA DE CORES --------------------
COR_MENU = "#006b9c"        # Marrom Chocolate
COR_HOVER = "#40A7C7"       # Marrom Claro
COR_ROSA = "#59b6c2"        # Rosa Destaque
COR_FUNDO = "#fdf8f5"       # Nude Claro
COR_TEXTO = "#00256b"       # Marrom Escuro

# -------------------- MENU LATERAL --------------------
lateral = tk.Frame(janela, bg=COR_MENU, width=160)
lateral.pack(side="left", fill="y")
lateral.pack_propagate(False)

area_principal = tk.Frame(janela, bg=COR_FUNDO, padx=20, pady=20)
area_principal.pack(side="left", fill="both", expand=True)

def limpar_area():
    for widget in area_principal.winfo_children():
        widget.destroy()

# Efeito Hover simples no menu
def ao_entrar(e): e.widget.config(bg=COR_HOVER)
def ao_sair(e): e.widget.config(bg=COR_MENU)

def criar_botao_menu(texto, comando):
    btn = tk.Button(
        lateral, text=texto, command=comando,
        bg=COR_MENU, fg="white", font=("Arial", 10, "bold"),
        bd=0, activebackground=COR_ROSA, activeforeground="white",
        anchor="w", padx=15, pady=10, cursor="hand2"
    )
    btn.bind("<Enter>", ao_entrar)
    btn.bind("<Leave>", ao_sair)
    btn.pack(fill="x", pady=2)
    return btn

# -------------------- 1. INÍCIO / DASHBOARD --------------------
def carregar_inicio():
    limpar_area()

    tk.Label(area_principal, text="DASHBOARD", font=("Arial", 16, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(anchor="w", pady=(0, 15))

    total = len(lista_tarefas)
    pendentes = sum(1 for t in lista_tarefas if t["status"] == "Pendente")
    concluidas = sum(1 for t in lista_tarefas if t["status"] == "Concluída")

    # Cartões Informativos
    frame_cards = tk.Frame(area_principal, bg=COR_FUNDO)
    frame_cards.pack(anchor="w", pady=(0, 20))

    def criar_card(parent, titulo, valor):
        card = tk.LabelFrame(parent, text=f" {titulo} ", bg="white", fg=COR_TEXTO, font=("Arial", 9, "bold"), padx=15, pady=10)
        card.pack(side="left", padx=(0, 10))
        tk.Label(card, text=str(valor), font=("Arial", 18, "bold"), bg="white", fg=COR_ROSA).pack()

    criar_card(frame_cards, "Total de Tarefas", total)
    criar_card(frame_cards, "Pendentes", pendentes)
    criar_card(frame_cards, "Concluídas", concluidas)

    # Resumo
    tk.Label(area_principal, text="Próximas Tarefas:", font=("Arial", 11, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(anchor="w", pady=(10, 5))
    for t in lista_tarefas[:5]:
        txt = f"- {t['titulo']} | Prioridade: {t['prioridade']} | Status: {t['status']}"
        tk.Label(area_principal, text=txt, bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 10)).pack(anchor="w", pady=2)

# -------------------- 2. TAREFAS --------------------
def carregar_tarefas():
    limpar_area()

    tk.Label(area_principal, text="GERENCIADOR DE TAREFAS", font=("Arial", 14, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(anchor="w", pady=(0, 10))

    # Formulário simplificado na mesma tela
    frame_form = tk.LabelFrame(area_principal, text=" Nova Tarefa ", bg=COR_FUNDO, fg=COR_TEXTO, padx=10, pady=10)
    frame_form.pack(fill="x", pady=(0, 15))

    tk.Label(frame_form, text="Título:", bg=COR_FUNDO).grid(row=0, column=0, sticky="w")
    ent_titulo = tk.Entry(frame_form, width=20)
    ent_titulo.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(frame_form, text="Responsável:", bg=COR_FUNDO).grid(row=0, column=2, sticky="w")
    ent_resp = tk.Entry(frame_form, width=15)
    ent_resp.grid(row=0, column=3, padx=5, pady=2)

    tk.Label(frame_form, text="Prioridade:", bg=COR_FUNDO).grid(row=1, column=0, sticky="w")
    combo_prio = ttk.Combobox(frame_form, values=["Alta", "Média", "Baixa"], state="readonly", width=17)
    combo_prio.set("Alta")
    combo_prio.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(frame_form, text="Data/Hora:", bg=COR_FUNDO).grid(row=1, column=2, sticky="w")
    ent_data = tk.Entry(frame_form, width=15)
    ent_data.insert(0, "28/09/2026")
    ent_data.grid(row=1, column=3, padx=5, pady=2)

    def salvar_tarefa():
        # Validação simples
        if not ent_titulo.get().strip():
            messagebox.showwarning("Atenção", "Informe o título da tarefa.")
            return

        lista_tarefas.append({
            "titulo": ent_titulo.get().strip(),
            "responsavel": ent_resp.get().strip(),
            "prioridade": combo_prio.get(),
            "data": ent_data.get().strip(),
            "status": "Pendente"
        })
        carregar_tarefas()

    tk.Button(frame_form, text="Salvar Tarefa", command=salvar_tarefa, bg=COR_ROSA, fg="white", bd=0, padx=10, pady=3).grid(row=1, column=4, padx=10)

    # Tabela (Treeview)
    colunas = ("id", "titulo", "responsavel", "prioridade", "data", "status")
    tree = ttk.Treeview(area_principal, columns=colunas, show="headings", height=7)

    tree.heading("id", text="ID")
    tree.heading("titulo", text="Tarefa")
    tree.heading("responsavel", text="Responsável")
    tree.heading("prioridade", text="Prioridade")
    tree.heading("data", text="Data")
    tree.heading("status", text="Status")

    tree.column("id", width=30)
    tree.column("titulo", width=150)
    tree.column("responsavel", width=100)
    tree.column("prioridade", width=80)
    tree.column("data", width=80)
    tree.column("status", width=90)

    for idx, t in enumerate(lista_tarefas, start=1):
        tree.insert("", "end", values=(idx, t["titulo"], t["responsavel"], t["prioridade"], t["data"], t["status"]))

    tree.pack(fill="x", pady=(0, 10))

    # Botões de Ação na Tabela
    frame_botoes = tk.Frame(area_principal, bg=COR_FUNDO)
    frame_botoes.pack(anchor="w")

    def concluir():
        sel = tree.selection()
        if sel:
            idx = int(tree.item(sel[0])["values"][0]) - 1
            lista_tarefas[idx]["status"] = "Concluída"
            carregar_tarefas()

    def excluir():
        sel = tree.selection()
        if sel:
            idx = int(tree.item(sel[0])["values"][0]) - 1
            del lista_tarefas[idx]
            carregar_tarefas()

    tk.Button(frame_botoes, text="Concluir Tarefa", command=concluir, bg="#5c3a21", fg="white", bd=0, padx=10, pady=4).pack(side="left", padx=(0, 5))
    tk.Button(frame_botoes, text="Excluir Tarefa", command=excluir, bg="#a94442", fg="white", bd=0, padx=10, pady=4).pack(side="left")

# -------------------- 3. AGENDA --------------------
def carregar_agenda():
    limpar_area()

    tk.Label(area_principal, text="AGENDA DE COMPROMISSOS", font=("Arial", 14, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(anchor="w", pady=(0, 10))

    frame_form = tk.LabelFrame(area_principal, text=" Novo Agendamento ", bg=COR_FUNDO, fg=COR_TEXTO, padx=10, pady=10)
    frame_form.pack(fill="x", pady=(0, 15))

    tk.Label(frame_form, text="Compromisso:", bg=COR_FUNDO).grid(row=0, column=0, sticky="w")
    ent_comp = tk.Entry(frame_form, width=20)
    ent_comp.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(frame_form, text="Data/Hora:", bg=COR_FUNDO).grid(row=0, column=2, sticky="w")
    ent_data_ag = tk.Entry(frame_form, width=15)
    ent_data_ag.insert(0, "30/09/2026 10:00")
    ent_data_ag.grid(row=0, column=3, padx=5, pady=2)

    def agendar():
        if not ent_comp.get().strip():
            messagebox.showwarning("Atenção", "Preencha o compromisso.")
            return
        lista_agendamentos.append({"titulo": ent_comp.get().strip(), "data": ent_data_ag.get().strip()})
        carregar_agenda()

    tk.Button(frame_form, text="Agendar", command=agendar, bg=COR_ROSA, fg="white", bd=0, padx=10, pady=3).grid(row=0, column=4, padx=10)

    tk.Label(area_principal, text="Próximos Agendamentos:", font=("Arial", 11, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(anchor="w", pady=(5, 5))
    for item in lista_agendamentos:
        txt = f"- {item['data']} : {item['titulo']}"
        tk.Label(area_principal, text=txt, bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 10)).pack(anchor="w", pady=2)

# -------------------- 4. CONFIGURAÇÕES --------------------
def carregar_configuracoes():
    limpar_area()

    tk.Label(area_principal, text="CONFIGURAÇÕES", font=("Arial", 14, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(anchor="w", pady=(0, 10))

    def limpar_tudo():
        lista_tarefas.clear()
        lista_agendamentos.clear()
        messagebox.showinfo("Sucesso", "Todos os dados foram apagados.")

    tk.Label(area_principal, text="Apagar todos os dados do sistema:", bg=COR_FUNDO, fg=COR_TEXTO).pack(anchor="w", pady=(0, 5))
    tk.Button(area_principal, text="Limpar Dados", command=limpar_tudo, bg="#a94442", fg="white", bd=0, padx=10, pady=5).pack(anchor="w")

# Botões do Menu Lateral
criar_botao_menu("Início", carregar_inicio)
criar_botao_menu("Tarefas", carregar_tarefas)
criar_botao_menu("Agenda", carregar_agenda)
criar_botao_menu("Configurações", carregar_configuracoes)

# Carrega a tela inicial por padrão
carregar_inicio()

janela.mainloop()