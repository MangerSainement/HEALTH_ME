import pandas as pd
import numpy as np

# lire le donnees de csv
df = pd.read_csv('Nutritions_US_new(Donnees orginales).csv', encoding='utf-8', delimiter=';')
df = df.drop(df.columns[0], axis=1)

df.fillna(value=0, inplace=True)

# Supprimer la ligne contenant la valeur d'exception spécifiée
df = df.drop(df[df['Water_(g)'] == '5.411.221.754.465.820'].index)

df = df.drop(df[df['Ash_(g)'] == '17.834.683.992.911.900'].index)

df = df.drop(df[df['Fiber_TD_(g)'] == '21.874.450.951.683.600'].index)

df = df.drop(df[df['Sugar_Tot_(g)'] == '8.543.065.536.073.600'].index)

df = df.drop(df[df['Calcium_(mg)'] == '7.673.821.369.343.750'].index)

df = df.drop(df[df['Iron_(mg)'] == '26.996.738.376.127.700'].index)

df = df.drop(df[df['Magnesium_(mg)'] == '35.295.988.076.015.400'].index)

df = df.drop(df[df['Phosphorus_(mg)'] == '1.651.421.264.157.830'].index)

df = df.drop(df[df['Potassium_(mg)'] == '2.794.727.403.156.380'].index)

df = df.drop(df[df['Sodium_(mg)'] == '312.495.922.820.719'].index)

df = df.drop(df[df['Zinc_(mg)'] == '2.117.438.149.430.970'].index)

df = df.drop(df[df['Copper_(mg)'] == '0.19598407009159685'].index)

df = df.drop(df[df['Selenium_(mg)'] == '15.591.015.514.809.500'].index)

df = df.drop(df[df['Vit_C_(mg)'] == '9.231.133.968.891.090'].index)

df = df.drop(df[df['Folic_Acid_(mg)'] == '23.169.011.998.222.400'].index)

df = df.drop(df[df['Vit_B12_(mg)'] == '13.924.720.284.322.700'].index)

df = df.drop(df[df['Manganese_(mg)'] == 0.6581556561085978].index)

# Garger les colonnes qu'on a besoin
cols_besoin = ['NDB_No', 'Shrt_Desc', 'Water_(g)', 'Energ_Kcal', 'Protein_(g)', 'Lipid_Tot_(g)', 'Ash_(g)',
               'Carbohydrt_(g)', 'Fiber_TD_(g)', 'Sugar_Tot_(g)', 'Calcium_(mg)', 'Iron_(mg)', 'Magnesium_(mg)',
               'Phosphorus_(mg)', 'Potassium_(mg)', 'Sodium_(mg)', 'Zinc_(mg)', 'Copper_(mg)', 'Manganese_(mg)',
               'Selenium_(mg)', 'Vit_C_(mg)', 'Thiamin_(mg)', 'Riboflavin_(mg)', 'Niacin_(mg)', 'Vit_B6_(mg)',
               'Folic_Acid_(mg)', 'Vit_B12_(mg)']

df = df[cols_besoin]

# Supprimer "W/"
Value_recherche = "W/"
df['Shrt_Desc'] = df['Shrt_Desc'].str.replace(Value_recherche, '')

# pd.set_option('display.max_columns', None)

print(df[:500])

# df.to_csv('./Données_propres.csv', index=False)
