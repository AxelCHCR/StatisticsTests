import math as m
import scipy.stats

alfa = 0.05

def pruebasRandom(nameFile):
    archivo = open(nameFile)
    randoms = archivo.readlines()
    archivo.close()
    for i in range(0,len(randoms)):
        randoms[i] = float(randoms[i])
    return randoms

def coef_bin(n, k):
    r = 1
    for i in range(1, min(k, n - k) + 1):
        r *= (n - i + 1)
        r //= i
    return r

def calcularMedia(nombreArchivo):
    archivo = open(nombreArchivo, "r")
    lineas = archivo.readlines()
    archivo.close()
    cantidadNumeros = len(lineas)
    suma = 0
    for linea in lineas:
        suma += eval(linea)
    return suma/cantidadNumeros

############################## PROMEDIO ##############################
def promedio(nameFile):
    u = 1 / 2
    randoms = pruebasRandom(nameFile)
    n = len(randoms)
    x = sum(randoms) / n
    z0 = (x - u) / (m.sqrt(1/12) / m.sqrt(n))
    return z0 > -1.96 and z0 < 1.96

############################## VARIANZA ##############################
def largoValores(nombreArchivo):
    with open(nombreArchivo, "r") as archivo:
        return len(archivo.readlines())
    
def calcularJi2(cantidadValores, s2, varianza):
    return (((cantidadValores-1)*s2)/varianza)

def validacionJiCuadradoVar(gl, j2):
    global tablaJiCuadradoIzq, alfa
    val1 = scipy.stats.chi2.ppf (alfa/2, gl)
    val2 = scipy.stats.chi2.ppf (1- alfa/2, gl)
    print(gl)
    print(j2)
    print(val1)
    print(val2)
    return val1 <= j2 and j2 <= val2

def calcularS2(nombreArchivo, media):
    archivo = open(nombreArchivo, "r")
    numeros = archivo.readlines()
    cantidadNumeros = len(numeros)
    resultado = 0
    for numero in numeros:
        resultado += pow((eval(numero)-media), 2)
    return resultado/(cantidadNumeros-1)

def pruebaDeVarianza(nombreArchivo):
    media = calcularMedia(nombreArchivo)
    s2 = calcularS2(nombreArchivo, media)
    total = largoValores(nombreArchivo)
    ji2 = calcularJi2(total, s2, 1/12)
    return validacionJiCuadradoVar(total - 1, ji2)

############################## CORRIDAS ##############################
def pruebaDeCorridas(nombreArchivo):
    archivo = open(nombreArchivo, "r")
    lineas = archivo.readlines()
    archivo.close()
    anterior = ""
    siguiente = " "
    h = 0
    largo = len(lineas)
    for linea in range(0,largo-1):
        if float(lineas[linea]) <= float(lineas[linea+1]):
            siguiente = "+"
        else:
            siguiente = "-"
        if anterior != siguiente:
            h+=1
        anterior = siguiente
    esperanza = ((2 * largo) - 1) / 3
    varianza = m.sqrt(((16 * largo)- (largo - 1)) / 90)
    z0 = (h-esperanza)/varianza
    print(z0)
    return z0 > -1.96 and z0 < 1.96

############################## HUECOS DE DIGITOS ##############################
feMinimaHD = 5

def pruebaHuecosDigitos(nombreArchivo):
    global feMinimaHD
    archivo = open(nombreArchivo, "r")
    lineas = archivo.readlines()
    archivo.close()
    secuencia = ""
    for linea in lineas:
        secuencia += ('{:.4f}'.format(float(linea)))[2:]
    secuencia = secuencia.replace("\n", "")
    frecObtenida = []
    tamHueco = [-1] * 10
    for i in range(0,len(secuencia)):
        digito = int(secuencia[i])
        for j in range(0, len(tamHueco)):
            if (j != digito and tamHueco[j] != -1) or (j == digito and tamHueco[j] == -1):
                tamHueco[j] += 1
            elif j == digito:
                frecObtenida += [0] * (tamHueco[j] - len(frecObtenida) + 1)
                frecObtenida[tamHueco[j]] += 1
                tamHueco[j] = 0
    tablaProbabilidades = [0.1 * ((0.9) ** x) for x in range(0,len(frecObtenida))]
    pos = -1
    total = sum(frecObtenida)
    frecEsperada = []
    for i in range(0,len(tablaProbabilidades)):
        if pos == -1 and tablaProbabilidades[i] * total < feMinimaHD:
            pos = i
        frecEsperada += [tablaProbabilidades[i] * total]
    return jiCuadrado(frecObtenida[:pos], frecEsperada[:pos], pos - 1)

############################## HUECOS DE NUMEROS ##############################
inf = 0.2
sup = 0.8
feMinimaHN = 5

def frecObservadas(randoms):
    global inf, sup
    fo = []
    tamHueco = -1
    for i in range(0,len(randoms)):
        if (randoms[i] >= inf and randoms[i] <= sup and tamHueco != -1):
            fo[tamHueco] += 1
            tamHueco = 0
        else:
            tamHueco += 1
            if (tamHueco == len(fo)):
                fo += [0]
    return fo

def huecosNumeros(nameFile):
    global inf, sup, feMinimaHN
    randoms = pruebasRandom(nameFile)
    pos = -1
    t = sup - inf
    fo = frecObservadas(randoms)
    total = sum(fo)
    p = [t * ((1 - t) ** x) for x in range(0,len(fo))]
    fe = []
    for i in range(0,len(p)):
        if pos == -1 and p[i] * total < feMinimaHN:
            pos = i
        fe += [p[i] * total]
    return jiCuadrado(fo[:pos], fe[:pos], pos - 1)

############################## POKER ##############################
def Casos(randoms):
    casos = [0] * 7
    
    for i in randoms:
        numStr = str(i)[2:7]
        while len(numStr) != 5:
            numStr += "0"
        rep = [numStr.count(i) for i in numStr]
        
        if rep[0] == 5:
            casos[6] += 1
            continue
        
        if rep[0] == 4 or rep[1] == 4:
            casos[5] += 1
            continue

        if rep[0] == 3 or rep[1] == 3 or rep[2] == 3:
            if rep[0] == 2 or rep[1] == 2 or rep[2] == 2 or rep[3] == 2:
                casos[4] += 1
            else:
                casos[3] += 1
            continue

        if rep[0] == 2 or rep[1] == 2 or rep[2] == 2 or rep[3] == 2:
            pos = -1
            par2 = False
            for i in range(0,4):
                if rep[i] == 2:
                    pos = i
                    break
            for i in range(0,4):
                if numStr[i] != numStr[pos]:
                    if rep[i] == 2:
                        casos[2] += 1
                        par2 = True
                        break
            if not par2:
                casos[1] += 1
            continue

        casos[0] += 1
        
    return casos

##def probabilidades():
##    p = [0] * 7
##    p[0] = (10 * 9 * 8 * 7 * 6) / (10 ** 5)
##    p[1] = ((10 * 9 * 8 * 7) / (10 ** 5)) * coef_bin(5,2)
##    p[2] = (1 / 2) * ((10 * 9 * 8) / (10 ** 5)) * coef_bin(5,2) * coef_bin(3,2)
##    p[3] = ((10 * 9 * 8) / (10 ** 5)) * coef_bin(5,3)
##    p[4] = ((10 * 9) / (10 ** 5)) * coef_bin(5,3)
##    p[5] = ((10 * 9) / (10 ** 5)) * coef_bin(5,4)
##    p[6] = 10 / (10 ** 5)
##    return p

def poker(nameFile):
    randoms = pruebasRandom(nameFile)
    total = len(randoms)
    fo = Casos(randoms)
    p = [0.3024, 0.5040, 0.1080, 0.0720, 0.0090, 0.0045, 0.0001]
    fe = [i * total for i in p]
    return jiCuadrado(fo, fe, len(fo) - 1)

############################## SERIES ##############################
c = 4

def series(nameFile):
    global c
    randoms = pruebasRandom(nameFile)
    total = len(randoms)
    fo = [0] * (c ** 2)
    for i in range(0,total - 1):
        posX = -1
        posY = -1
        for j in range(0, c):
            if posX == -1 and randoms[i] <= (j + 1) / c:
                posX = j
            if posY == -1 and randoms[i + 1] <= (j + 1) / c:
                posY = (c - (j + 1)) * c
        fo[posY + posX] += 1

    fe = [(total - 1) / (c ** 2)] * (c ** 2)
    return jiCuadrado(fo, fe, len(fo) - 1)
            

############################## JI CUADRADO ##############################
def jiCuadrado(fo, fe, gl):
    gl = len(fo) - 1
    result = 0
    for i in range(0,len(fo)):
        result += ((fo[i] - fe[i]) ** 2) / fe[i]
    return validacionJiCuadrado(gl, result)

def validacionJiCuadrado(gl, j2):
    global tablaJiCuadradoIzq, alfa
    val = scipy.stats.chi2.ppf (1 - alfa, gl)
    print(gl)
    print(j2)
    print(val)
    return j2 <= val

##tablaJiCuadradoDer = [[ 0.99,   0.975,    0.95,    0.90,    0.80  ],\
##                      [0.0002,  0.0010,  0.0039,  0.0158,  0.0642 ],\
##                      [0.0201,  0.0506,  0.1026,  0.2107,  0.4463 ],\
##                      [0.1148,  0.2158,  0.3518,  0.5844,  1.0052 ],\
##                      [0.2971,  0.4844,  0.7107,  1.0636,  1.6488 ],\
##                      [0.5543,  0.8312,  1.1455,  1.6103,  2.3425 ],\
##                      [0.8721,  1.2373,  1.6354,  2.2041,  3.0701 ],\
##                      [1.2390,  1.6899,  2.1673,  2.8331,  3.8223 ],\
##                      [1.6465,  2.1797,  2.7326,  3.4895,  4.5936 ],\
##                      [2.0879,  2.7004,  3.3251,  4.1682,  5.3801 ],\
##                      [2.5582,  3.2470,  3.9403,  4.8652,  6.1791 ],\
##                      [3.0535,  3.8157,  4.5748,  5.5778,  6.9887 ],\
##                      [3.5706,  4.4038,  5.2260,  6.3038,  7.8073 ],\
##                      [4.1069,  5.0087,  5.8919,  7.0415,  8.6339 ],\
##                      [4.6604,  5.6287,  6.5706,  7.7895,  9.4673 ],\
##                      [5.2294,  6.2621,  7.2609,  8.5468,  10.3070],\
##                      [5.8122,  6.9077,  7.9616,  9.3122,  11.1521],\
##                      [6.4077,  7.5642,  8.6718,  10.0852, 12.0023],\
##                      [7.0149,  8.2307,  9.3904,  10.8649, 12.8570],\
##                      [7.6327,  8.9065,  10.1170, 11.6509, 13.7158],\
##                      [8.2604,  9.5908,  10.8508, 12.4426, 14.5784],\
##                      [8.8972,  10.2829, 11.5913, 13.2396, 15.4446],\
##                      [9.5425,  10.9823, 12.3380, 14.0415, 16.3140],\
##                      [10.1957, 11.6885, 13.0905, 14.8480, 17.1865],\
##                      [10.8563, 12.4011, 13.8484, 15.6587, 18.0618],\
##                      [11.5240, 13.1197, 14.6114, 16.4734, 18.9397],\
##                      [12.1982, 13.8439, 15.3792, 17.2919, 19.8202],\
##                      [12.8785, 14.5734, 16.1514, 18.1139, 20.7030],\
##                      [13.5647, 15.3079, 16.9279, 18.9392, 21.5880],\
##                      [14.2564, 16.0471, 17.7084, 19.7677, 22.4751],\
##                      [14.9535, 16.7908, 18.4927, 20.5992, 23.364 ]]

##tablaJiCuadradoIzq = [[ 0.2,     0.1,     0.05,   0.025,    0.01  ],\
##                      [1.6424,  2.7055,  3.8415,  5.0239,  6.6349 ],\
##                      [3.2189,  4.6052,  5.9915,  7.3778,  9.2104 ],\
##                      [4.6416,  6.2514,  7.8147,  9.3484,  11.3449],\
##                      [5.9886,  7.7794,  9.4877,  11.1433, 13.2767],\
##                      [7.2893,  9.2363,  11.0705, 12.8325, 15.0863],\
##                      [8.5581,  10.6446, 12.5916, 14.4494, 16.8119],\
##                      [9.8032,  12.0170, 14.0671, 16.0128, 18.4753],\
##                      [11.0301, 13.3616, 15.5073, 17.5345, 20.0902],\
##                      [12.2421, 14.6837, 16.9190, 19.0228, 21.6660],\
##                      [13.4420, 15.9872, 18.3070, 20.4832, 23.2093],\
##                      [14.6314, 17.2750, 19.6752, 21.9200, 24.7250],\
##                      [15.8120, 18.5493, 21.0261, 23.3367, 26.2170],\
##                      [16.9848, 19.8119, 22.3620, 24.7356, 27.6882],\
##                      [18.1508, 21.0641, 23.6848, 26.1189, 29.1412],\
##                      [19.3107, 22.3071, 24.9958, 27.4884, 30.5780],\
##                      [20.4651, 23.5418, 26.2962, 28.8453, 31.9999],\
##                      [21.6146, 24.7690, 27.5871, 30.1910, 33.4087],\
##                      [22.7595, 25.9894, 28.8693, 31.5264, 34.8052],\
##                      [23.9004, 27.2036, 30.1435, 32.8523, 36.1908],\
##                      [25.0375, 28.4120, 31.4104, 34.1696, 37.5663],\
##                      [26.1711, 29.6151, 32.6706, 35.4789, 38.9322],\
##                      [27.3015, 30.8133, 33.9245, 36.7807, 40.2894],\
##                      [28.4288, 32.0069, 35.1725, 38.0756, 41.6383],\
##                      [29.5533, 33.1962, 36.4150, 39.3641, 42.9798],\
##                      [30.6752, 34.3816, 37.6525, 40.6465, 44.3140],\
##                      [31.7946, 35.5632, 38.8851, 41.9231, 45.6416],\
##                      [32.9117, 36.7412, 40.1133, 43.1945, 46.9629],\
##                      [34.0266, 37.9159, 41.3372, 44.4608, 48.2783],\
##                      [35.1394, 39.0875, 42.5569, 45.7223, 49.5878],\
##                      [36.2502, 40.2560, 43.7730, 46.9792, 50.8923]]
