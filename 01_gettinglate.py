import matplotlib.pyplot as plt
import matplotlib.collections as collections
import numpy as np
import pandas as pd
import seaborn as sns

## importowanie danych z pliku csv
df = pd.read_csv("../../data/gettinglate.csv")
colorTheme = '#ffddc4'
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

# usunięcie pierwszej kolumny, przemianowanie i zapisanie tabeli
df = df.drop('Lp', axis=1)
df.columns = ['weekday', 'day', 'month', 'onhour', 'timep', 'presp', 'timek', 'presk']
df.to_csv("gettinglate_new.csv")

# lista różnych ważnych statystyk
stats = {'Spawacz' : pd.Series([df['timep'].sum(), df['timep'].mean(), 0., df['timep'].median(), df['timep'].std()], index=['Suma', 'Średnia', 'Procent', 'Mediana', 'Standard']),
    'Bandzior' : pd.Series([df['timek'].sum(), df['timek'].mean(), 0., df['timek'].median(), df['timek'].std()], index=['Suma', 'Średnia', 'Procent', 'Mediana', 'Standard'])}
dfstats = pd.DataFrame(stats)

def plot_points():  
    "Rysowanie wykresu z punktami, które oznaczają czas spóźnenia w minutach"
    fig, ax = plt.subplots()
    # pierwszy punkt i label
    ax.plot(0, df.at[0, 'timek'], color=colorKamil, marker='P', markersize=12, label="Bandzior")
    ax.plot(0, df.at[0, 'timep'], color=colorPawel, marker='.', markersize=14, label="Spawacz")

    # punkty z czasem spóźnienia
    for i in range(1, df.shape[0]):
        ax.plot(i, df.at[i, 'timek'], color=colorKamil, marker='P', markersize=12)
        ax.plot(i, df.at[i, 'timep'], color=colorPawel, marker='.', markersize=14) 

    # Oznaczenie osi
    ax.set(xlabel='Data', ylabel='Czas', title='Spóźnienia')

    # Linie średniej
    ax.hlines(13.16, 0, df.shape[0] - 1, color=colorPawel)
    ax.hlines( 7.18, 0, df.shape[0] - 1, color=colorKamil)

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
    # Oznaczenia przedziałów na osi x
    plt.xticks(np.arange(0, 61), df.day.astype(str), fontsize="8")
    collection1 = collections.BrokenBarHCollection.span_where(range(0, df.shape[0]), ymin=0, ymax=70, where=df['month'] == 4, facecolor='grey', alpha=0.3)
    collection2 = collections.BrokenBarHCollection.span_where(range(0, df.shape[0]), ymin=0, ymax=70, where=df['month'] == 6, facecolor='grey', alpha=0.3)
    ax.add_collection(collection1)
    ax.add_collection(collection2)
    # Linie pomocnicze, rysowanie
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=1)

    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    plt.show()
    return

def plot_sum():
    "Rysowanie wykresu z całką spóźnienia"
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
    ax.plot(sum_p, color=colorPawel, label="Suma Spawacz")
    ax.plot(sum_k, color=colorKamil, label="Suma Bandzior")
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
    # Oznaczenia przedziałów na osi x
    plt.xticks(np.arange(0, 61), df.day.astype(str), fontsize="8")
    collection1 = collections.BrokenBarHCollection.span_where(range(0, df.shape[0]), ymin=0, ymax=700, where=df['month'] == 4, facecolor='grey', alpha=0.3)
    collection2 = collections.BrokenBarHCollection.span_where(range(0, df.shape[0]), ymin=0, ymax=700, where=df['month'] == 6, facecolor='grey', alpha=0.3)
    ax.add_collection(collection1)
    ax.add_collection(collection2)
    # Linie pomocnicze, rysowanie
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=1)

    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    plt.show()
    return

def plot_present():
    "Rysowanie wykresu słupkowego z procentem spóźnień"
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
    # procent spóźniania
    statsMeans = (temp1[0] / (60 - p) * 100, temp2[0] / (60 - k) * 100)
    # dorównanie do 100%
    statsTotal = (100 - statsMeans[0], 100 - statsMeans[1])
    ind = np.arange(2)    # lokacje na osi x
    width = 0.2       # grubość paska
    # statystyki
    dfstats.at["Procent", "Spawacz"] = temp1[0]
    dfstats.at["Procent", "Bandzior"] = temp2[0]

    # rysowanie słupków
    p1 = plt.bar(ind, statsMeans, width, color=[colorPawel, colorKamil])
    p2 = plt.bar(ind, statsTotal, width, bottom=statsMeans, color=colorSecondary)

    # tekst na słupkach
    for rect in p1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height) + '%', ha='center', va='bottom')

    # podpis osi
    plt.xticks(ind, ('Spawacz', 'Bandzior'))
    plt.yticks(np.arange(0, 101, 10))
    
    # legenda
    legend = plt.legend((p1[0], p1[1], p2[0]), ('[%] spóźnienie Spawacz', '[%] spóźnienie Bandzior', 'Całkowity czas'))
    legend.get_frame().set_facecolor(colorTheme)

    plt.show()
    return
    
def plot_corr(df, dropDuplicates = True):
    "Rysowanie wykresu korelacji zmiennych"
    df1 = df.copy()
    df1 = df1.drop('presp', axis=1)
    df1 = df1.drop('presk', axis=1)
    df1 = df1.drop('day', axis=1)
    df1.columns = ['Dzień tygodnia','Miesiąc', 'Godzina rozpoczęcia', 'Spóźnienie Spawacz', 'Spóźnienie Bandzior']
    df1 = df1.corr()
    print(df1)

    # Stworzenie macierzy trójkątnej z symetrycznej
    if dropDuplicates:    
        mask = np.zeros_like(df1, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True

    # kolor tła
    sns.set_style(style = 'white')

    # Set up  matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 11))

    # Add diverging colormap from red to blue
    cmap = sns.diverging_palette(250, 10, as_cmap=True)

    # Draw correlation plot with or without duplicates
    if dropDuplicates:
        sns.heatmap(df1, mask=mask, cmap=cmap, 
                square=True,
                linewidth=.5, annot=True, annot_kws={"size":10})
    else:
        sns.heatmap(df1, cmap=cmap, 
                square=True,
                linewidth=.5, annot=True, annot_kws={"size":10})
    plt.savefig('Figure_4.png', bbox_inches='tight')
    plt.show()
    return
 
plot_points()
plot_sum()
plot_present()
plot_corr(df, dropDuplicates=False)
print(dfstats)