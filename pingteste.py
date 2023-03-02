import subprocess
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
from datetime import *


def main():
    data = sqlite3.connect('data_ip.db')
    cursor = data.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS ips (ident integer, id string, ip string)")
    cursor.execute("CREATE TABLE IF NOT EXISTS coord (x integer, y integer)")
    data.commit()
    data.close()

    def inserir_inicial():
        data = sqlite3.connect('data_ip.db')
        cursor = data.cursor()
        i = 1
        while i < 35:
            print(i)
            aux = '192.168.' + str(i) + '.200'
            aux1 = str(i) + '.200.'
            print(aux)
            print(aux1)
            cursor.execute(f"INSERT INTO ips (ident, id, ip) VALUES(?, ?, ?)", [i, aux1, aux])
            i = i + 1

        data.commit()
        data.close()

    ip_list = []

    def reset():
        tela.destroy()
        main()

    def select():
        try:
            data = sqlite3.connect('data_ip.db')
            cursor = data.cursor()
            cursor.execute(f"SELECT ip FROM ips")
            temp = cursor.fetchall()
            i = 0
            while i < len(temp):
                ip_list.append(temp[i][0])
                i = i + 1

            print(ip_list)

            cursor.close()

        except sqlite3.Error as error:
            messagebox.showerror("Erro", error)

    select()

    def ping(ip):
        try:
            result = subprocess.check_output(['ping', '-n', '1', '-w', '100', ip])
            return True
        except subprocess.CalledProcessError:
            return False

    def atualizar():
        horario = datetime.now()
        horarioFinal = tk.StringVar()
        horarioFinal.set("Atualizado - " + str(horario.hour) + ":" + str(horario.minute))
        a = tk.Label(tela, textvariable=horarioFinal)
        a.pack(side=tk.RIGHT)
        #MUDAR O PLACE PARA PACK

        try:
            for i, ip in enumerate(ip_list):
                result = ping(ip)
                cor = 'green' if result else 'red'
                labels[i].config(bg=cor, foreground="white")
            tela.after(180000, atualizar)
        except Exception as erro:
            if str(erro) == "list index out of range":
                messagebox.showerror("Erro", "Erro de indice, aperte em OK para reiniciar.")
                reset()




    def botao_atualizar():
        atualizar()

    def inserir():
        msg = simpledialog.askstring(title="Insira o IP", prompt="Insira o Final do IP - Ex: 1.200")
        print(msg)
        if msg == '':
            messagebox.showerror("Erro", "Insira um IP")
            inserir()
        elif msg == None:
            messagebox.showwarning("Atenção", "Nenhum IP foi inserido.")
        else:
            data = sqlite3.connect('data_ip.db')
            cursor = data.cursor()

            cursor.execute("SELECT id FROM ips")
            aux = cursor.fetchall()
            ident = len(aux) + 1
            id = msg + '.'
            ip = '192.168.' + msg

            j = 0
            while j < len(aux):
                if id == aux[j][0]:
                    messagebox.showerror("Erro", "O IP já exite na lista.")
                    return False

                j = j + 1
                print(j)

            if True:
                cursor.execute(f"INSERT INTO ips (ident, id, ip) VALUES (?, ?, ?)", [ident, id, ip])
                data.commit()

                cursor.close()

                print(ip_list)
                messagebox.showinfo("Sucesso", "IP " + ip + " inserido com sucesso!")
                reset()


            cursor.close()


    tela = tk.Tk()
    tela.title("Ip - Verificar")
    tela.geometry("300x850")

    labels = []
    for ip in ip_list:
        label = tk.Label(tela, text=ip)
        label.pack()
        labels.append(label)


    button = tk.Button(tela, text='Atualizar', command=botao_atualizar)
    button.pack(padx=10, pady=10)

    buttonA = tk.Button(tela, text='Inserir', command=inserir)
    buttonA.pack()


    atualizar_label = threading.Thread(target=atualizar)
    atualizar_label.start()

    tela.mainloop()



data = datetime.now()



main()