import matplotlib.pyplot as plt
import matplotlib.collections as collections
import numpy as np
import pandas as pd

## importowanie danych z pliku csv
df = pd.read_csv("../../data/gettinglate.csv")

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


def plot_draw(points=False, lates=True, zeroes=True, sum_all=False):
    "Rysowanie wykresów, points - wykres punktowy ze spóźnieniami z poszczególnych dni, sum_all - wykres liniowy z sumowaniem poszczególnych dni"
    
    # zmienne do całki
    if sum_all == True:
        sum_p = []
        sum_k = []

    # inicjalizacja wykresu    
    fig, ax = plt.subplots()

    # inicjacja dla pętli
    if sum_all == True: # całka, pierwsza wartość
        sum_p.append(df.at[0, 'timep'])
        sum_k.append(df.at[0, 'timep'])

    if points == True:
        # punkty z czasem spóźnienia
        if df.at[0, 'timep'] > 0 and lates == True:
            ax.plot(0, df.at[0, 'timep'], 'r', label="Paweł")
        elif df.at[0, 'timep'] <= 0 and zeroes == True:
            ax.plot(0, -1, 'r*', label="Paweł")
        if df.at[0, 'timek'] > 0 and lates == True:
            ax.plot(0, df.at[0, 'timek'], 'b+', label="Kamil")
        elif df.at[0, 'timek'] <= 0 and zeroes == True:
            ax.plot(0, -2, 'b*', label="Kamil")

    # Pętla przypisująca punkty i licząca całkę    
    for i in range(1, df.shape[0]):
        # liczenie całki jeżeli podano parametr True
        if sum_all == True:
            # całka ze spóźnienia 1
            sum_p.append(sum_p[i - 1] + df.at[i, 'timep'])

            # całka ze spóźnienia 2
            sum_k.append(sum_k[i - 1] + df.at[i, 'timek'])

        # liczenie punktów jeżeli podano paramter True
        if points == True:
            # punkty z czasem spóźnienia
            if df.at[i, 'timep'] > 0 and lates == True:
                ax.plot(i, df.at[i, 'timep'], 'r.')
            elif df.at[i, 'timep'] <= 0 and zeroes == True:
                ax.plot(i, -1, 'r*')
                
            if df.at[i, 'timek'] > 0 and lates == True:
                ax.plot(i, df.at[i, 'timek'], 'b+')
            elif df.at[i, 'timek'] <= 0 and zeroes == True:
                ax.plot(i, -2, 'b*')

    if sum_all == True:
        ax.plot(sum_p, 'r', label="Suma Paweł")
        ax.plot(sum_k, 'b', label="Suma Kamil")
        ax.set(xlabel='Data', ylabel='Czas (minuty)',
                title='Liczba minut spóźnienia dla danej daty')

    if points == True:
        ax.set(xlabel='Data', ylabel='Czas (minuty)',
                title='Spóźnienie')

    # legenda
    legend = ax.legend(loc='upper left', shadow=True)
    legend.get_frame().set_facecolor('#d6e069')

    # zaznaczenie obszaru
    #collection = collections.BrokenBarHCollection.span_where(range(0, df.shape[0]), ymin=0, ymax=70, where=df['timek'] <= 0, facecolor='green', alpha=0.5)
    #ax.add_collection(collection)
    # rysowanie     
    ax.grid()
    plt.show()
    return

plot_draw(True, True, True, False)

## main
# wyznaczenie spóźnień
# late_p = np.array(calculate_late_time('minp', 'secp'))
# late_k = np.array(calculate_late_time('mink', 'seck'))
# wydruk pomocniczej tabeli
# print_table(late_p, late_k)

# setup wykresów
# plot_draw(True, True, True, False)

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