import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect('indicateurs.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE historique (
    date TEXT,
    indicateur TEXT,
    valeur REAL
)''')

dates = pd.date_range('2023-01-01', periods=12, freq='M')
indicateurs = [
    "Taux d'exécution physique",
    "Taux d'exécution financière",
    "Taux de consommation des délais",
    "Taux d'électrification",
    "Nombre d'emplois créés",
    "Puissance installée (MWc)"
]

for date in dates:
    for indicateur in indicateurs:
        valeur = np.random.randint(30, 100)
        cursor.execute('INSERT INTO historique (date, indicateur, valeur) VALUES (?, ?, ?)',
                       (date.strftime('%Y-%m-%d'), indicateur, valeur))

conn.commit()
conn.close()
print('Base de données recréée avec succès.')
