import subprocess
import threading
import tkinter as tk

ip_list = [
    '192.168.1.200',
    '192.168.2.200',
    '192.168.3.200',
    '192.168.4.200',
    '192.168.5.200',
    '192.168.6.200',
    '192.168.7.200',
    '192.168.8.200',
    '192.168.9.200',
    '192.168.10.200',
    '192.168.11.200',
    '192.168.12.200',
    '192.168.13.200',
    '192.168.14.200',
    '192.168.15.200',
    '192.168.16.200',
    '192.168.17.200',
    '192.168.18.200',
    '192.168.19.200',
    '192.168.20.200',
    '192.168.21.200',
    '192.168.22.200',
    '192.168.23.200',
    '192.168.24.200',
    '192.168.25.200',
    '192.168.26.200',
    '192.168.27.200',
    '192.168.28.200',
    '192.168.29.200',
    '192.168.30.200',
    '192.168.31.200',
    '192.168.32.200',
    '192.168.33.200',
    '192.168.34.200'
]

def ping(ip):
    try:
        result = subprocess.check_output(['ping', '-n', '1', '-w', '100', ip])
        return True
    except subprocess.CalledProcessError:
        return False

def atualizar():
    for i, ip in enumerate(ip_list):
        result = ping(ip)
        cor = 'green' if result else 'red'
        labels[i].config(bg=cor, foreground="white")
    tela.after(300000, atualizar)

def botao_atualizar():
    atualizar()


tela = tk.Tk()
tela.title("Ip - Verificar")
tela.geometry("200x750")
labels = []
for ip in ip_list:
    label = tk.Label(tela, text=ip)
    label.pack()
    labels.append(label)

button = tk.Button(tela, text='Atualizar', command=botao_atualizar)
button.pack()

atualizar_label = threading.Thread(target=atualizar)
atualizar_label.start()

tela.mainloop()
