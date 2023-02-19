import os
from joblib import Parallel, delayed
import pandas as pd
import numpy
import openpyxl


with open("iplist.txt") as file:
    temp = file.read()
    temp = temp.splitlines()
    print(temp)



    for ip in temp:
        resultado = os.popen(f"ping {ip}").read()
        if(("unreachable") or ("Request time out") or ("inacessível") or ("A vida útil (TTL) expirou em trânsito.")) in resultado:
            print(resultado)
            arq = open("output.txt", "a")
            arq.write(str(ip) + ' - não conectado'+"\n")
            arq.close()
        else:
            print(resultado)
            arq = open("output.txt", "a")
            arq.write(str(ip) + ' - Conectado!' + "\n")
            arq.close()

#resultado = Parallel