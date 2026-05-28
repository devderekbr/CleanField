import tkinter as tk
import re
import pyperclip
import threading
import time

# =========================
# CONFIG
# =========================

monitorando = False

# =========================
# CORES
# =========================

BG = "#1e1e1e"
FRAME = "#2a2a2a"
INPUT = "#333333"
TEXT = "#ffffff"

BUTTON = "#3b82f6"
BUTTON_HOVER = "#2563eb"

SUCCESS = "#22c55e"
DANGER = "#ef4444"

# =========================
# FUNÇÕES
# =========================

def apenas_numeros(texto):
    return re.sub(r'\D', '', texto)


def formatar_documento(texto):
    numeros = apenas_numeros(texto)

    # CPF
    if len(numeros) == 11:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"

    # CNPJ
    elif len(numeros) == 14:
        return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:]}"

    return texto


def copiar_texto(campo, botao):
    texto = campo.get()

    root.clipboard_clear()
    root.clipboard_append(texto)

    texto_original = botao["text"]

    botao.config(
        text="COPIADO!",
        bg=SUCCESS
    )

    root.after(
        1000,
        lambda: botao.config(
            text=texto_original,
            bg=BUTTON
        )
    )


def atualizar_log(original, convertido):
    texto_log = f"{original} → {convertido}"

    label_log.config(text=texto_log)


# =========================
# 1 - LIMPEZA INSTANTÂNEA
# =========================

def limpeza_automatica(event=None):
    texto = campo_auto.get()

    texto_limpo = apenas_numeros(texto)

    if texto != texto_limpo:
        campo_auto.delete(0, tk.END)
        campo_auto.insert(0, texto_limpo)


# =========================
# 2 - LIMPEZA MANUAL
# =========================

def atualizar_limpeza_manual(event=None):
    texto = campo_manual_esquerda.get()

    resultado = apenas_numeros(texto)

    campo_manual_direita.config(state="normal")
    campo_manual_direita.delete(0, tk.END)
    campo_manual_direita.insert(0, resultado)
    campo_manual_direita.config(state="readonly")


# =========================
# 3 - FORMATAR
# =========================

def atualizar_formatacao(event=None):
    texto = campo_formatar_esquerda.get()

    resultado = formatar_documento(texto)

    campo_formatar_direita.config(state="normal")
    campo_formatar_direita.delete(0, tk.END)
    campo_formatar_direita.insert(0, resultado)
    campo_formatar_direita.config(state="readonly")


# =========================
# 4 - MONITOR CLIPBOARD
# =========================

def monitorar_clipboard():
    ultimo_processado = ""

    while monitorando:
        try:
            texto = pyperclip.paste()

            if texto != ultimo_processado:

                numeros = apenas_numeros(texto)

                # Apenas CPF/CNPJ
                if len(numeros) in [11, 14]:

                    # Só altera se realmente mudou
                    if texto != numeros:

                        pyperclip.copy(numeros)

                        atualizar_log(texto, numeros)

                        ultimo_processado = numeros

                    else:
                        ultimo_processado = texto

            time.sleep(0.5)

        except:
            pass


def alternar_monitoramento():
    global monitorando

    if not monitorando:
        monitorando = True

        botao_monitor.config(
            text="ATIVO",
            bg=SUCCESS
        )

        thread = threading.Thread(
            target=monitorar_clipboard,
            daemon=True
        )

        thread.start()

    else:
        monitorando = False

        botao_monitor.config(
            text="DESATIVADO",
            bg=DANGER
        )


# =========================
# JANELA
# =========================

root = tk.Tk()
root.title("CleanField")
root.geometry("520x450")
root.resizable(False, False)

root.configure(bg=BG)

# =========================
# TÍTULO
# =========================

titulo = tk.Label(
    root,
    text="CleanField",
    font=("Segoe UI", 18, "bold"),
    bg=BG,
    fg=TEXT
)

titulo.pack(pady=10)

# =========================
# 1 - LIMPEZA INSTANTÂNEA
# =========================

frame1 = tk.Frame(root)
frame1.configure(bg=FRAME)
frame1.pack(fill="x", padx=10, pady=5)

titulo1 = tk.Label(
    frame1,
    text="1 - Limpeza Instantânea",
    bg=FRAME,
    fg=TEXT,
    font=("Segoe UI", 10, "bold")
)

titulo1.pack(anchor="w", pady=(0, 5))

campo_auto = tk.Entry(
    frame1,
    font=("Segoe UI", 11),
    bg=INPUT,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    bd=10
)

campo_auto.pack(fill="x")

campo_auto.bind("<KeyRelease>", limpeza_automatica)

# =========================
# 2 - LIMPEZA MANUAL
# =========================

frame2 = tk.Frame(root)
frame2.configure(bg=FRAME)
frame2.pack(fill="x", padx=10, pady=5)

titulo2 = tk.Label(
    frame2,
    text="2 - Limpeza Manual",
    bg=FRAME,
    fg=TEXT,
    font=("Segoe UI", 10, "bold")
)

titulo2.pack(anchor="w", pady=(0, 5))

container2 = tk.Frame(frame2)
container2.configure(bg=FRAME)
container2.pack(fill="x")

campo_manual_esquerda = tk.Entry(
    container2,
    font=("Segoe UI", 11),
    bg=INPUT,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    bd=10
)

campo_manual_esquerda.pack(
    side="left",
    expand=True,
    fill="x",
    padx=5
)

campo_manual_esquerda.bind(
    "<KeyRelease>",
    atualizar_limpeza_manual
)

botao_limpar = tk.Button(
    container2,
    text="COPIAR",
    command=lambda: copiar_texto(
        campo_manual_direita,
        botao_limpar
    ),
    bg=BUTTON,
    fg="white",
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    font=("Segoe UI", 9, "bold")
)

botao_limpar.pack(side="left", padx=5)

campo_manual_direita = tk.Entry(
    container2,
    font=("Segoe UI", 11),
    bg=INPUT,
    fg=TEXT,
    insertbackground=TEXT,
    readonlybackground=INPUT,
    relief="flat",
    bd=10,
    state="readonly"
)

campo_manual_direita.pack(
    side="left",
    expand=True,
    fill="x",
    padx=5
)

# =========================
# 3 - FORMATAR
# =========================

frame3 = tk.Frame(root)
frame3.configure(bg=FRAME)
frame3.pack(fill="x", padx=10, pady=5)

titulo3 = tk.Label(
    frame3,
    text="3 - Formatar CPF/CNPJ",
    bg=FRAME,
    fg=TEXT,
    font=("Segoe UI", 10, "bold")
)

titulo3.pack(anchor="w", pady=(0, 5))

container3 = tk.Frame(frame3)
container3.configure(bg=FRAME)
container3.pack(fill="x")

campo_formatar_esquerda = tk.Entry(
    container3,
    font=("Segoe UI", 11),
    bg=INPUT,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    bd=10
)

campo_formatar_esquerda.pack(
    side="left",
    expand=True,
    fill="x",
    padx=5
)

campo_formatar_esquerda.bind(
    "<KeyRelease>",
    atualizar_formatacao
)

botao_formatar = tk.Button(
    container3,
    text="COPIAR",
    command=lambda: copiar_texto(
        campo_formatar_direita,
        botao_formatar
    ),
    bg=BUTTON,
    fg="white",
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2",
    font=("Segoe UI", 9, "bold")
)

botao_formatar.pack(side="left", padx=5)

campo_formatar_direita = tk.Entry(
    container3,
    font=("Segoe UI", 11),
    bg=INPUT,
    fg=TEXT,
    insertbackground=TEXT,
    readonlybackground=INPUT,
    relief="flat",
    bd=10,
    state="readonly"
)

campo_formatar_direita.pack(
    side="left",
    expand=True,
    fill="x",
    padx=5
)

# =========================
# 4 - CLIPBOARD AUTOMÁTICO
# =========================

frame4 = tk.Frame(root)
frame4.configure(bg=FRAME)
frame4.pack(fill="x", padx=10, pady=5)

titulo4 = tk.Label(
    frame4,
    text="4 - Clipboard Automático",
    bg=FRAME,
    fg=TEXT,
    font=("Segoe UI", 10, "bold")
)

titulo4.pack(anchor="w", pady=(0, 5))

botao_monitor = tk.Button(
    frame4,
    text="DESATIVADO",
    font=("Segoe UI", 10, "bold"),
    width=20,
    command=alternar_monitoramento,
    bg=DANGER,
    fg="white",
    activebackground=DANGER,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2"
)

botao_monitor.pack(pady=5)

# =========================
# LOG
# =========================

frame_log = tk.Frame(root)
frame_log.configure(bg=FRAME)
frame_log.pack(fill="x", padx=10, pady=5)

titulo_log = tk.Label(
    frame_log,
    text="Última Conversão",
    bg=FRAME,
    fg=TEXT,
    font=("Segoe UI", 10, "bold")
)

titulo_log.pack(anchor="w", pady=(0, 5))

label_log = tk.Label(
    frame_log,
    text="Nenhuma conversão ainda.",
    anchor="w",
    justify="left",
    bg=FRAME,
    fg=TEXT,
    font=("Segoe UI", 9)
)

label_log.pack(fill="x")

# =========================
# START
# =========================

root.mainloop()