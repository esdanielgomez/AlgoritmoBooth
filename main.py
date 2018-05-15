from PyQt5.uic.properties import QtWidgets

listaResultados = []

def getString(array):
    return str(array).replace("[", "").replace("'", "").replace(",", "").replace("]", "").replace(" ", "")


def getBinario(numero, numeroBitsNecesarios):
    bn = list(bin(numero))
    binario=""
    for i in range (2,len(bin(numero))):
        binario+=bn[i]
    binario = binario.replace("b","")
    #Se ajusta la cifra a 8, 16 o 32 bits
    if (len(binario) < numeroBitsNecesarios):
        if (numero < 0):
            binario = rellenarBitsIzquierda(binario, numeroBitsNecesarios, "1"); # bit de signo negativo

        else:
            binario = rellenarBitsIzquierda(binario, numeroBitsNecesarios, "0");
    elif (len(binario) > numeroBitsNecesarios):
        binario = quitarBitsIzquierda(binario, numeroBitsNecesarios);

    return binario;


def binarioToDecimal(binario):
    mult = 1;

    #Si el numero es negativo * /
    subStr = ""
    for i in range(0,1): subStr+=list(binario)[i] #binario.substring(0, 1)
    if (subStr == "1"):
        mult = -1
        binario = getComplemento2(binario);

    array = list(binario);

    numero = 0;
    exp = 0
    for i in range(len(array)-1, -1, -1):
        numero += (int(array[i]) * (2**exp));
        exp+=1

    return numero * mult;

def rellenarBitsIzquierda(binario, numeroBitsNecesarios, bitRelleno):
    while(len(binario) < numeroBitsNecesarios):
        binario = bitRelleno + binario
    return binario

def quitarBitsIzquierda(numBinario, numeroBitsNecesarios):
    numBinario = ""
    for i in range(0,len(numBinario) - numeroBitsNecesarios): numBinario+=list(numBinario)[i]
    return numBinario;


def igualarTamaniosArrayBits(arrayBinario1, arrayBinario2):
#/ * Retorna una array de tamanio 2: array[0] es el binario1, array[1] es el binario2 ambos con el mismo tamaño(el del mas grande) * /
    array = []
    binario1 = getString(arrayBinario1)
    binario2 = getString(arrayBinario2);

    if (len(arrayBinario1) > len(arrayBinario2)):
        binario2 = rellenarBitsIzquierda(binario2, len(arrayBinario1), arrayBinario2[0]);
    # arrayBinario2[0] representa el signo
    elif (len(arrayBinario2) > len(arrayBinario1)):
        rellenarBitsIzquierda(binario1, len(arrayBinario2), arrayBinario1[0]);
    # arrayBinario1[0] representa el signo

    array.append(binario1)
    array.append(binario2)

    return array;

def sumarBinario(arrayBinario1, arrayBinario2):

    #Igualamos los tamanios de los arrays * /
    a = igualarTamaniosArrayBits(arrayBinario1, arrayBinario2);


    arrayBinario1 = list(a[0]);
    arrayBinario2 = list(a[1]);

    respuesta = "";
    llevo = "0";

    r = ""
    d1 = ""
    d2 = ""
    max = len(arrayBinario1) - 1
    for v in range(max, -1, -1):
        d1 = arrayBinario1[v];
        d2 = arrayBinario2[v];

        if (d1 == "0" and d2 == "0"):
            r = "0";
            if (llevo == "1"):
                r = "1"
            llevo = "0"
        elif (d1 == "0" and d2 == "1"):
            r = "1";
            if (llevo == "1"):
                r = "0";
                llevo = "1";
            else:
                llevo = "0";
        elif (d1 == "1" and d2 == "0"):
            r = "1";
            if (llevo == "1"):
                r = "0";
                llevo = "1";
            else:
                llevo = "0";
        elif (d1 == "1" and d2 == "1"):
            r = "0";
            if (llevo == "1"):
                r = "1";
            llevo = "1";

        respuesta = r + respuesta;

    #En caso de que al final se haya llevado algun valor
    if (llevo == "1"):
        respuesta = llevo + respuesta;

    return list(respuesta);

def getComplemento1(binario):
    array = list(binario)
    for i in range(0, len(array)) :
        if (array[i] == "0"):
            array[i] = "1"
        elif (array[i] == "1"):
            array[i] = "0"
    return getString(array)

def getComplemento2(binario):
    complemento1 = list(getComplemento1(binario))
    return getString(sumarBinario(complemento1, list("01")))

def desplazarDerecha(arrayBinario):
        for i in range(len(arrayBinario) - 2, -1, -1):
            arrayBinario[i+1] = arrayBinario[i]

        # Se mantiene el ultimo digito
        arrayBinario[0] = arrayBinario[1]
        return arrayBinario

def almacenarResultado(binario, idFila, info, iteracion, overflow):
    registro = []
    for i in range(5): registro.append(0)
    registro[0] = iteracion

    if (overflow):
        registro[1] = "1";
    else:
        registro[1] = "";

    # Separamos la fila en tres grupos

    registro2 = ""
    for i in range(0, int((len(binario)-1)/2)): registro2+=binario[i]
    registro2+="    "
    for i in range(int((len(binario)-1)/2), len(binario)- 1): registro2 += binario[i]
    registro2 += "    "
    for i in range(len(binario)- 1, len(binario)): registro2 += binario[i]

    registro[2] = registro2
    registro[3] = idFila;
    registro[4] = info;

    listaResultados.append(registro);

def algoritmoDeBooth(binario1, binario2):

    multiplicando = list(binario1);
    ca2Multiplicando = list(getComplemento2(binario1));
    multiplicador = list(binario2);

    x = len(multiplicando)
    y = len(multiplicador)

    # ARRAY P String[x + y + 1];
    P = []
    for i in range(x+y+1):
        P.append(0)

    for i in range(0, x+y+1):
        if (i < len(multiplicando)):
            P[i] = multiplicando[i];
        else:
            P[i] = "0";

    # ARRAY S [x+y+1]
    S = [];
    for i in range(x+y+1):
        S.append(0)

    for i in range(0,x+y+1):
        if (i < len(ca2Multiplicando)):
            S[i] = ca2Multiplicando[i];
        else:
            S[i] = "0";

    # ARRAY T
    T = []
    for i in range(x+y+1):
        T.append(0)

    T[x+y] = "0";

    j = len(multiplicador) - 1
    for i in range(x+y-1, -1, -1):
        if (j >= 0):
            T[i] = multiplicador[j];
        else:
            T[i] = "0";

        j=j-1

    almacenarResultado(getString(P), "P", "", "", False);
    almacenarResultado(getString(S), "S", "", "", False);
    almacenarResultado(getString(T), "T", "", "", False);

    filVacia = ["","","","",""]
    listaResultados.append(filVacia)

    #ITERACIONES DEL ALGORITMO

    b1 = ""
    b2 = "";
    aux = []
    overflow = False;

    for i in range(1,x+1):
        b1 = T[len(T)-2];
        b2 = T[len(T)-1];



        if (b1 == "0" and b2 == "1"):
            aux = sumarBinario(T, P);

            if (len(aux) > len(P)):
                overflow = True;
                subStr = ""

                for k in range(1,len(aux)): subStr+=aux[k] #getString(aux).substring(1, aux.length)
                T = list(subStr);
            else:
                T = aux;

            almacenarResultado(getString(T), "", "T+P", "", overflow);
        elif (b1 == "1" and b2 == "0"): # T = T + S
            aux = sumarBinario(T, S)
            if (len(aux) > len(P)):
                overflow = True
                subStr = ""
                for k in range(1, len(aux)): subStr += aux[k]  # getString(aux).substring(1, aux.length)
                T = list(subStr)
            else:
                T = aux;

            almacenarResultado(getString(T), "", "T+S", " ", overflow);

        overflow = False;
        T = desplazarDerecha(T);
        almacenarResultado(getString(T), "T", "Desplazamiento", str(i) + "", overflow);
        filVacia = ["", "", "", "", ""]
        listaResultados.append(filVacia)

    # desplazamiento final
    T = desplazarDerecha(T);
    almacenarResultado(getString(T), "", "Desplazamiento Final", "", overflow);

    return getString(T)

#------------------------------------------------------------------
#Ejemplo en consola:

#binario1 = "1010"; binario2 = "101"
#resultadoBinario = algoritmoDeBooth(binario1,binario2)
#print(binarioToDecimal(resultadoBinario))



#------------------------------------------------------------------
# APLICACION EN QT

import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi


class DemoImpl(QDialog):
    def __init__(self, *args):
        super(DemoImpl, self).__init__(*args)
        loadUi('GUI.ui', self)

        self.btnCalcular.clicked.connect(self.btnCalcularAccion)


    def btnCalcularAccion(self):

        #Obtener los numeros ingresados:
        try:
            numero1 = int(self.numero1.text())
            numero2 = int(self.numero2.text())

            # Numero de bits necesarios

            if (self.opt8.isChecked()):
                numeroBits = 8
            elif (self.opt16.isChecked()):
                numeroBits = 16
            else:
                numeroBits = 32

            # Se muestran los numeros binarios
            binario1 = getBinario(numero1, numeroBits)
            binario2 = getBinario(numero2, numeroBits)

            self.binario1.setText(binario1)
            self.binario2.setText(binario2)

            # El complemento a 2
            complemento2 = getComplemento2(binario1)

            self.complemento.setText(complemento2)

            # Los resultados
            listaResultados.clear()
            resultadoB = algoritmoDeBooth(binario1, binario2)
            resultadoD = binarioToDecimal(resultadoB)

            self.resultadoBinario.setText(resultadoB)
            self.resultadoDecimal.setText(str(resultadoD))

            table = QTableWidget(self)
            table.setRowCount(len(listaResultados))
            table.setColumnCount(5)

            # Set the table headers
            table.setHorizontalHeaderLabels(["Iteración","Overflow", "Número binario", "Id", "Paso"])

            for i in range(0,len(listaResultados)):
                for j in range(0,5):
                    table.setItem(i, j, QTableWidgetItem(str(listaResultados[i][j])))
                    print(listaResultados)


            table.resizeColumnToContents(0)
            table.resizeColumnToContents(2)
            table.resizeColumnToContents(3)
            table.resizeColumnToContents(4)

            self.grid.addWidget(table,0,0)

        except ValueError:
            print("Numero incorrecto!")




app = QApplication(sys.argv)
widget = DemoImpl()
widget.show()
app.exec_()