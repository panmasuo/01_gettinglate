import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## importowanie danych z pliku csv
df = pd.read_csv("../../data/gettinglate.csv")

def calculate_late_time(minutes, seconds):
    "Zwraca listę spóźnień w kolejnych dniach. Obliczenie czasu spóźninia na podstawie minut i sekund dla danego użytkownika"
    time = []
    for i in range(0, (df['Lp'].size)):
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

    return

def plot_draw(points=False, sum_all=False):
    "Rysowanie wykresów, points - wykres punktowy ze spóźnieniami z poszczególnych dni, sum_all - wykres liniowy z sumowaniem poszczególnych dni"
    
    # zmienne do całki
    if sum_all == True:
        sum_p = []
        sum_k = []

    # inicjalizacja wykresu    
    fig, ax = plt.subplots()

    # 
    for i in range(len(late_p)):
        # liczenie całki jeżeli podano parametr True
        if sum_all == True:
            # całka ze spóźnienia 1
            if i == 0:
                sum_p.append(late_p[i])
            else:
                sum_p.append(sum_p[i - 1] + late_p[i])

            # całka ze spóźnienia 2
            if i == 0:
                sum_k.append(late_k[i])
            else:
                sum_k.append(sum_k[i - 1] + late_k[i])

        # liczenie punktów jeżeli podano paramter True
        if points == True:
            # punkty z czasem spóźnienia
            if late_p[i] > 0:
                ax.plot(i, late_p[i], 'r.')
            else:
                ax.plot(i, 0, 'y*')
            if late_k[i] > 0:
                ax.plot(i, late_k[i], 'b+')
            else:
                ax.plot(i, 0, 'g*')

    if sum_all == True:
        ax.plot(sum_p, 'r')
        ax.plot(sum_k, 'b')
        ax.set(xlabel='Data', ylabel='Czas (minuty)',
                title='Liczba minut spóźnienia dla danej daty')

    if points == True:
        ax.set(xlabel='Data', ylabel='Czas (minuty)',
                title='Liczba minut spóźnienia dla danej daty')

    # rysowanie
    ax.grid()
    plt.show()
    return

## main
# wyznaczenie spóźnień
late_p = calculate_late_time('minp', 'secp')
late_k = calculate_late_time('mink', 'seck')
# wydruk pomocniczej tabeli
print_table(late_p, late_k)
plot_draw(True, False)
