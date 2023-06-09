import ssl
import sqlite3
import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, LeaveOneOut


class Wine:
    def __init__(self, listOfOtherAttributes, decisiveAttribute, ):
        self.attribute = decisiveAttribute
        self.listOfAttributes = listOfOtherAttributes

    def __repr__(self):
        return f"Wine(listOfOtherAttributes = {self.listOfAttributes},decisiveAttribute={self.attribute},)"

    def getAttribute(self):
        return self.attribute


ssl._create_default_https_context = ssl._create_unverified_context

# Wczytaj dane z adresu podanego w pliku tekstowym: pliktextowy.txt
# do ramki danych.
# Użyj reszty wierszy jako nagłówków ramki danych.
# Uwaga! Zobacz która zmienna jest zmienną objaśnianą, będzie to potrzebne do dalszych zadań.

url = ""
headers = []

file1 = open('pliktextowy.txt', 'r')
lines = file1.readlines()
counter = 0
for line in lines:
    if counter == 0:
        url = line.rstrip()
    else:
        headers.append(line.rstrip())
    counter += 1

df = pd.read_csv(url, names=headers)  # tutaj podmień df. Ma zawierać wczytane dane.
# Zadanie1 przypisz nazwy kolumn z df w jednej linii:   (2pkt)

wynik1 = df.columns.values.tolist()
print(wynik1)

# Zadanie 2: Wypisz liczbę wierszy oraz kolumn ramki danych w jednej linii.  (2pkt)
wynik2 = df.shape
print(wynik2)

# Zadanie Utwórz klasę Wine na podstawie wczytanego zbioru:
# wszystkie zmienne objaśniające powinny być w liscie.
# Zmienna objaśniana jako odrębne pole.
# metoda __init__ powinna posiadać 2 parametry:
# listę (zmienne objaśniające) oraz liczbę(zmienna objaśniana).
# nazwy mogą być dowolne.

# Klasa powinna umożliwiać stworzenie nowego obiektu na podstawie
# już istniejącego obiektu jak w pdf z lekcji lab6.
# podpowiedź: metoda magiczna __repr__
# Nie pisz metody __str__.

# Zadanie 3 Utwórz przykładowy obiekt:   (3pkt)
wynik3 = Wine([1213, 121323, 112434, 12321324], 1)  # do podmiany. Pamiętaj - ilość elementów, jak w zbiorze danych.
# Uwaga! Pamiętaj, która zmienna jest zmienną objaśnianą
print(wynik3)

# Zadanie 4.                             (3pkt)
# Zapisz wszystkie dane z ramki danych do listy obiektów typu Wine.
# Nie podmieniaj listy, dodawaj elementy.
# Uwaga! zobacz w jakiej kolejności podawane są zmienne objaśniane i objąśniająca.
# Podpowiedź zobacz w pliktextowy.txt
wineList = []
for i in range(0, df.shape[0]):
    attributeList = []

    for j in range(1, df.shape[1]):
        attributeList.append(float(df.iloc[i, j]))

    wineList.append(Wine(attributeList, float(df.iloc[i, 0])))
wynik4 = len(wineList)
print(wynik4)

# Zadanie5 - Weź ostatni element z listy i na podstawie         (3pkt)
# wyniku funkcji repr utwórz nowy obiekt - eval(repr(obiekt))
# do wyniku przypisz zmienną objaśnianą z tego obiektu:
wynik5 = eval(repr(wineList[len(wineList) - 1])).attribute
print(wynik5)

# Zadanie 6:                                                          (3pkt)
# Zapisz ramkę danych  do bazy SQLite nazwa bazy(dopisz swoje imię i nazwisko):
# wines_imie_nazwisko, nazwa tabeli: wines.
# Następnie wczytaj dane z tabeli wybierając z bazy danych tylko wiersze z typem wina nr 3
# i zapisz je do nowego data frame:
conn = sqlite3.connect('wines_dominik_nykiel')
c = conn.cursor()

c.execute(
    'CREATE TABLE IF NOT EXISTS wines (TypeOf number ,Alcohol number, Malic_acid number, Ash number, Alcalinity_of_ash number,Magnesium number,Total_phenols number,Flavanoids number,Nonflavanoid_phenols number,Proanthocyanins number,Color_intensity number,Hue number,OD280_OD315_of_diluted_wines number, Proline number)')
conn.commit()
df.to_sql('wines', conn, if_exists='replace', index=False)

c.execute('SELECT * FROM wines WHERE TypeOf = 3')

wynik6 = "W następnej linijce podmień na nowy  data frame z winami tylko klasy trzeciej:"
wynik6 = pd.DataFrame(c.fetchall(), columns=['TypeOf', 'Alcohol', 'Malic_acid', 'Ash', 'Alcalinity_of_ash', 'Magnesium',
                                             'Total_phenols', 'Flavanoids', 'Nonflavanoid_phenols', 'Proanthocyanins',
                                             'Color_intensity', 'Hue', 'OD280_OD315_of_diluted_wines', 'Proline'])

print(wynik6.shape)

# Zadanie 7                                                          (1pkt)
# Utwórz model regresji Logistycznej z domyślnymi ustawieniami:

model = LogisticRegression()

wynik7 = model.__class__.__name__
print(wynik7)

# Zadanie 8:                                                        (3pkt)
# Dokonaj podziału ramki danych na dane objaśniające i  do klasyfikacji.
# Znormalizuj dane objaśniające za pomocą:
# preprocessing.normalize(X)
# Wytenuj model na wszystkich danych bez podziału na zbiór treningowy i testowy.
# Wykonaj sprawdzian krzyżowy, używając LeaveOneOut() zamiast KFold (Parametr cv)
#  Podaj średnią dokładność (accuracy)

X = df.iloc[:, 1:].values
y = df.iloc[:, 0].values
X = preprocessing.normalize(X)
model.fit(X, y)

scores = cross_val_score(model, X, y, cv=LeaveOneOut(), scoring="accuracy")
wynik8 = scores.mean()
print(wynik8)
