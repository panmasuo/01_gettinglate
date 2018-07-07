import matplotlib.pyplot as plt
import matplotlib.collections as collections
import numpy as np
import pandas as pd

## importowanie danych z pliku csv
df = pd.read_csv("../../data/gettinglate.csv")
colorTheme = '#bbff47'
colorSecondary = '#fff4a8'
colorPawel = '#a81212'
colorKamil = '#084c7a'

## zmiana tabeli
#  dodanie sekund do minut
df.loc[df['mink'] != -1, 'mink'] = abs(df['mink']) + abs(df['seck'])/60
df.loc[df['mink'] == -1, 'mink'] = 0
df.loc[df['minp'] != -1, 'minp'] = abs(df['minp']) + abs(df['secp'])/60
df.loc[df['minp'] == -1, 'minp'] = 0

# zamiana przyjścia na nową kolumne zamiast sekund False - nieprzyjście True - przyjście
df.loc[df['secp'] >= 0, 'secp']  = True
df.loc[df['secp'] != True, 'secp'] = False
df.loc[df['seck'] >= 0, 'seck']  = True
df.loc[df['seck'] != True, 'seck'] = False

# usunięcie pierwszej kolumny i przemianowanie
df = df.drop('Lp', axis=1)
df.columns = ['weekday', 'day', 'month', 'onhour', 'timep', 'presp', 'timek', 'presk']
df.to_csv("../../data/gettinglate_new.csv")

def plot_points():
    fig, ax = plt.subplots()
    # pierwszy punkt i label
    ax.plot(0, df.at[0, 'timep'], color=colorPawel, marker='.', label="Paweł")
    ax.plot(0, df.at[0, 'timek'], color=colorKamil, marker='+', label="Kamil")

    for i in range(1, df.shape[0]):
        # punkty z czasem spóźnienia
        ax.plot(i, df.at[i, 'timep'], color=colorPawel, marker='.') 
        ax.plot(i, df.at[i, 'timek'], color=colorKamil, marker='+')

    # Oznaczenie osi
    ax.set(xlabel='Data', ylabel='Czas', title='Spóźnienia')

    # Legenda
    legend = ax.legend(loc='upper left', shadow=True)
    legend.get_frame().set_facecolor(colorTheme)

    # Linie pomocnicze, organizacja
    major_ticksX = np.arange(0, 61, 5)
    major_ticksY = np.arange(0, 71, 5)
    minor_ticksX = np.arange(0, 61, 1)
    minor_ticksY = np.arange(0, 71, 1)

    # Linie pomocnicze, wyznaczanie
    ax.set_xticks(major_ticksX)
    ax.set_xticks(minor_ticksX, minor=True)
    ax.set_yticks(major_ticksY)
    ax.set_yticks(minor_ticksY, minor=True)

    # Linie pomocnicze, rysowanie
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=1)

    plt.show()
    return

def plot_sum():
    fig, ax = plt.subplots()
    # zmienne do całki
    sum_p = []
    sum_k = []

    # inicjacja dla pętli
    sum_p.append(df.at[0, 'timep'])
    sum_k.append(df.at[0, 'timep'])

    # Pętla przypisująca punkty i licząca całkę    
    for i in range(1, df.shape[0]):
        # całka ze spóźnienia 1
        sum_p.append(sum_p[i - 1] + df.at[i, 'timep'])
        # całka ze spóźnienia 2
        sum_k.append(sum_k[i - 1] + df.at[i, 'timek'])

    # oznaczenie osi
    ax.plot(sum_p, color=colorPawel, label="Suma Paweł")
    ax.plot(sum_k, color=colorKamil, label="Suma Kamil")
    ax.set(xlabel='Data', ylabel='Czas', title='Suma czasu spóźnienia')

    # legenda
    legend = ax.legend(loc='upper left', shadow=True)
    legend.get_frame().set_facecolor(colorTheme)
    # Linie pomocnicze, organizacja
    major_ticksX = np.arange(0, 61, 5)
    major_ticksY = np.arange(0, 701, 50)
    minor_ticksX = np.arange(0, 61, 1)
    minor_ticksY = np.arange(0, 701, 10)
    # Linie pomocnicze, wpisywanie
    ax.set_xticks(major_ticksX)
    ax.set_xticks(minor_ticksX, minor=True)
    ax.set_yticks(major_ticksY)
    ax.set_yticks(minor_ticksY, minor=True)
    
    # Linie pomocnicze, rysowanie
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=1)

    plt.show()
    return

def plot_present():

    fig, ax = plt.subplots()
    # ilość nie przyjść bez spóźnienia (żeby odjąć od całkowitej puli)    
    p = 0
    k = 0
    for i in range(df.shape[0]):
        if (df.at[i, 'timep'] == 0) and (df.at[i, 'presp'] == False):
            p += 1

        if (df.at[i, 'timek'] == 0) and (df.at[i, 'presk'] == False):
            k += 1

    # zmienić to
    temp1 = df[df.timep > 0].count()
    temp2 = df[df.timek > 0].count()
    statsMeans = (temp1[0] / (60 - p) * 100, temp2[0] / (60 - k) * 100)
    statsTotal = (100 - statsMeans[0], 100 - statsMeans[1])
    ind = np.arange(2)    # the x locations for the groups
    width = 0.2       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, statsMeans, width, color=[colorPawel, colorKamil])
    p2 = plt.bar(ind, statsTotal, width, bottom=statsMeans, color=colorSecondary)

    plt.xticks(ind, ('Paweł', 'Kamil'))
    plt.yticks(np.arange(0, 101, 10))
    
    #legend = plt.legend((p1[0], p2[0]), ('Spóźnienie', 'Całkowity czas'))
    #legend.get_frame().set_facecolor(colorTheme)
    plt.show()
    return
 
#plot_points()
plot_sum()
#plot_present()


# zaznaczenie obszaru
#collection = collections.BrokenBarHCollection.span_where(range(0, df.shape[0]), ymin=0, ymax=70, where=df['timek'] <= 0, facecolor='green', alpha=0.5)
#ax.add_collection(collection)


## main
# wyznaczenie spóźnień
# late_p = np.array(calculate_late_time('minp', 'secp'))
# late_k = np.array(calculate_late_time('mink', 'seck'))
# wydruk pomocniczej tabeli
# print_table(late_p, late_k)

# np_df = np.array(df)
# print(np.corrcoef(np_df[:,7], np_df[:,0]))

# def print_table(late_table1, late_table2):
#     "Drukowanie tablicy z ogólnymi danymi"
#     sum = 0
#     iter = 0
#     for i in range(0, len(late_table1)):
#         if late_table1[i] > 0:
#             sum += late_table1[i]
#             iter += 1

#     values_1 = {'Suma(min)': sum, '(h)': sum/60, 'Ilość': iter, 'Procent': iter/len(late_table1)*100,
#             'Średnio': sum/iter}

#     sum = 0
#     iter = 0
#     for i in range(0, len(late_table2)):
#         if late_table2[i] > 0:
#             sum += late_table2[i]
#             iter += 1
#     values_2 = {'Suma(min)': sum, '(h)': sum/60, 'Ilość': iter, 'Procent': iter/len(late_table2)*100,
#             'Średnio': sum/iter}
            
#     print('Imię\tMinuty\tGodziny\tIlość\tProcent\tŚrednio')
#     print('Paweł\t{0[Suma(min)]:0.0f}min\t{0[(h)]:0.1f}h\t{0[Ilość]:d}\t{0[Procent]:0.1f}%\t{0[Średnio]:0.1f}min '.format(values_1))
#     print('Kamil\t{0[Suma(min)]:0.0f}min\t{0[(h)]:0.1f}h\t{0[Ilość]:d}\t{0[Procent]:0.1f}%\t{0[Średnio]:0.1f}min '.format(values_2))

#     return


# def calculate_late_time(minutes, seconds):
#     "Zwraca listę spóźnień w kolejnych dniach. Obliczenie czasu spóźninia na podstawie minut i sekund dla danego użytkownika"
#     time = []
#     for i in range(0, (df['Lp'].size)):
#         if df[minutes][i] == -1:     # -1 oznacza nie przyjście na pierwsze zajęcia, następne bez spóźnienia
#             time.append(-1)
#         elif df[minutes][i] >= 0:    # normalny pomiar spóźnienia                     
#             value = df[minutes][i] + (df[seconds][i] / 60)
#             time.append(value)
#         else:                       # spóźnienie na następne zajęcia
#             value = (df[minutes][i] + (df[seconds][i] / 60)) * -1
#             time.append(value)
#     return time