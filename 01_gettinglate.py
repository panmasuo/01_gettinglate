import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## importowanie danych z pliku csv
df = pd.read_csv("../data/gettinglate.csv")

def calculate_late_time(minutes, seconds):
    "Obliczenie czasu spóźninia na podstawie minut i sekund dla danego użytkownika"
    time = []
    for i in range(0, df['Lp'].size):
        if df[minutes][i] == -1:     # -1 oznacza nie przyjście na pierwsze zajęcia, następne bez spóźnienia
            time.append(-1)
        elif df[minutes][i] >= 0:    # normalny pomiar spóźnienia                     
            value = df[minutes][i] + (df[seconds][i] / 60)
            time.append(value)
        else:                       # spóźnienie na następne zajęcia
            value = (df[minutes][i] + (df[seconds][i] / 60)) * -1
            time.append(value)
    return time

def print_table(late_table1, late_table2):
    "Drukowanie tablicy z ogólnymi danymi"
    sum = 0
    iter = 0
    for i in range(0, len(late_table1)):
        if late_table1[i] > 0:
            sum += late_table1[i]
            iter += 1

    values_1 = {'Suma(min)': sum, '(h)': sum/60, 'Ilość': iter, 'Procent': iter/len(late_table1)*100,
            'Średnio': sum/iter}

    sum = 0
    iter = 0
    for i in range(0, len(late_table2)):
        if late_table2[i] > 0:
            sum += late_table2[i]
            iter += 1
    values_2 = {'Suma(min)': sum, '(h)': sum/60, 'Ilość': iter, 'Procent': iter/len(late_table2)*100,
            'Średnio': sum/iter}
            


    print('Imię\tMinuty\tGodziny\tIlość\tProcent\tŚrednio')
    print('Paweł\t{0[Suma(min)]:0.0f}min\t{0[(h)]:0.1f}h\t{0[Ilość]:d}\t{0[Procent]:0.1f}%\t{0[Średnio]:0.1f}min '.format(values_1))
    print('Kamil\t{0[Suma(min)]:0.0f}min\t{0[(h)]:0.1f}h\t{0[Ilość]:d}\t{0[Procent]:0.1f}%\t{0[Średnio]:0.1f}min '.format(values_2))

    return 0

late_p = calculate_late_time('minp', 'secp')
late_k = calculate_late_time('mink', 'seck')

print_table(late_p, late_k)