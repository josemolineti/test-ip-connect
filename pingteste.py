import subprocess
import threading
from tkinter import *
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
            aux = '192.168.' + str(i) + '.200'
            aux1 = str(i) + '.200.'
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
        msg = simpledialog.askstring(title="Inserir novo IP", prompt="Digite o Final do IP que deseja inserir\n\nEx: 1.200")
        if msg == '':
            messagebox.showerror("Erro", "Digite um IP")
            inserir()
        elif msg == None:
            messagebox.showwarning("Atenção", "Nenhum IP foi inserido.\n\nOperação cancelada.")
        else:
            data = sqlite3.connect('data_ip.db')
            cursor = data.cursor()

            cursor.execute("SELECT id FROM ips")
            aux = cursor.fetchall()
            id = msg + '.'
            ip = '192.168.' + msg


            j = 0
            while j < len(aux):


                if id == aux[j][0]:
                    messagebox.showerror("Erro", "O IP " + ip + " já exite na lista ou não é um IP válido.")
                    inserir()
                    return False




                j = j + 1

            if True:
                if len(msg) == 5:
                    ident = msg[0]
                    cursor.execute(f"INSERT INTO ips (ident, id, ip) VALUES (?, ?, ?)", [int(ident), id, ip])
                    data.commit()
                    cursor.close()
                    messagebox.showinfo("Sucesso", "IP " + ip + " inserido com sucesso!")
                    reset()

                elif len(msg) == 6:
                    auxiliar = slice(0, 2)
                    ident = msg[auxiliar]
                    cursor.execute(f"INSERT INTO ips (ident, id, ip) VALUES (?, ?, ?)", [int(ident), id, ip])
                    data.commit()
                    cursor.close()
                    messagebox.showinfo("Sucesso", "IP " + ip + " inserido com sucesso!")
                    reset()

                elif len(msg) == 7:
                    auxiliar = slice(0, 3)
                    ident = msg[auxiliar]

                    if int(msg[auxiliar]) < 100 or int(msg[auxiliar]) > 255:
                        messagebox.showerror("Erro", "Digite um IP válido.")
                        inserir()
                    else:
                        cursor.execute(f"INSERT INTO ips (ident, id, ip) VALUES (?, ?, ?)", [int(ident), id, ip])
                        data.commit()
                        cursor.close()
                        messagebox.showinfo("Sucesso", "IP " + ip + " inserido com sucesso!")
                        reset()
                else:
                    messagebox.showerror("Erro", "Digite um IP válido.")
                    inserir()
    def remover():
        msg = simpledialog.askstring(title="Remover IP", prompt="Digite o Final do IP que deseja remover\n\nEx: 1.200")
        if msg == '':
            messagebox.showerror("Erro", "Digite um IP")
            remover()
        elif msg == None:
            messagebox.showwarning("Atenção", "Nenhum IP foi removido.\n\nOperação cancelada.")

        else:
            data = sqlite3.connect('data_ip.db')
            cursor = data.cursor()

            cursor.execute("SELECT id FROM ips")
            aux = cursor.fetchall()
            id = msg + '.'
            ip = '192.168.' + msg

            j=0
            while j < len(aux):
                if id == aux[j][0]:
                    cursor.execute("DELETE FROM ips WHERE id = ?", [id])
                    data.commit()
                    cursor.close()
                    messagebox.showinfo("Sucesso!", "O IP "+ ip +" foi removido com sucesso!")
                    reset()
                    return False


                j = j + 1

            if True:
                messagebox.showerror("Erro", "O IP " + ip + " não existe na lista.")
                remover()


    def sair():
        msg = messagebox.askyesno("Sair", "Tem certeza que deseja sair?")

        if msg == 'Yes':
            print("OI")
        else:
            print("Não")


    tela =Tk()

    ######ARRUMAR AQUI
    barraMenu=Menu(tela)
    btnOpc=Menu(barraMenu, tearoff=0)

    btnOpc.add_command(label="Inserir", command=inserir)
    btnOpc.add_command(label="Remover", command=remover)
    btnOpc.add_separator()
    btnOpc.add_command(label="Sair", command=sair)
    barraMenu.add_cascade(label="Menu", menu=barraMenu)

    tela.config(menu=barraMenu)

    data = sqlite3.connect('data_ip.db')
    cursor = data.cursor()

    cursor.execute("SELECT x FROM coord")
    x = cursor.fetchall()
    cursor.execute("SELECT y FROM coord")
    y = cursor.fetchall()

    coord = (str(x[0][0]) + "x" + str(y[0][0]))
    print(coord)

    tela.title("Ip - Verificar")
    tela.geometry(coord)

    labels = []
    for ip in ip_list:
        label =Label(tela, text=ip)
        label.pack()
        labels.append(label)

    button =Button(tela, text='Atualizar', command=botao_atualizar)
    button.pack(padx=10, pady=10)

    #buttonA = tk.Button(tela, text='Inserir', command=inserir)
    #buttonA.pack()
#
    #botao2 = tk.Button(tela, text='Remover', command=remover)
    #botao2.pack()


    atualizar_label = threading.Thread(target=atualizar)
    atualizar_label.start()


    tela.mainloop()



data = datetime.now()



main()