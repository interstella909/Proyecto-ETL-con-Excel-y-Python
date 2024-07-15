import pandas as pd
import numpy as np

# Leer el archivo de Excel
df = pd.read_excel('DATA.xlsx', sheet_name='Base dsp-analytics-daily')

# Eliminar filas vacías y duplicadas
df.dropna(how='all', inplace=True)
df.drop_duplicates(inplace=True)

# Imprimir estadísticas descriptivas y el dataframe
print(df.describe())
print(df)

# Manejo de valores nulos
missing_values = df.isnull().sum()
print(missing_values)

# Tipos de datos por columna
data_types = df.dtypes
print(data_types)

# Convertir columnas a tipo float
df['Unique Visitors'] = pd.to_numeric(df['Unique Visitors'], errors='coerce')
df['Frequency'] = pd.to_numeric(df['Frequency'], errors='coerce')

# Rellenar valores nulos con la media
df['Unique Visitors'].fillna(df['Unique Visitors'].mean(), inplace=True)
df['Frequency'].fillna(df['Frequency'].mean(), inplace=True)

# Convertir Unique Visitors a int
df['Unique Visitors'] = df['Unique Visitors'].astype(int)

# Confirmar cambios
missing_values = df.isnull().sum()
print(missing_values)
data_types = df.dtypes
print(data_types)

# Transformar categorías redundantes
category_replacements = {
    'Cremas': 'Crema',
    'Quesos': 'Queso',
    'AlimLiq': 'AlimentoLiquido',
    'AlimentoLIquido': 'AlimentoLiquido',
    'Aliquido': 'AlimentoLiquido',
    'Yogurth': 'Yogurt',
    'Yoghurt': 'Yogurt',
    'Leches': 'Leche',
    'Form': 'Fórmulas',
    'Formulas': 'Fórmulas'
}
df['CATEGORIA'] = df['CATEGORIA'].replace(category_replacements)

# Crear columnas adicionales
df['Day'] = df['Date'].dt.day
df['Month'] = df['Date'].dt.month
df['Impressions by thousands'] = df['Impressions'] / 1000
df['Cost by unit'] = df['Spend'] / df['Units']

# Crear columna 'Best Practice'
df['Best Practice'] = np.where(df['ROAS'] > 20, 'BP', 'No BP')

# Imprimir el dataframe final
print(df)

# Crear tabla organizada por ventas de mayor a menor por categoría
tabla_organizada = df.groupby('CATEGORIA')['Sales'].sum().sort_values(ascending=False)
df_tabla_organizada = pd.DataFrame({'Categoría': tabla_organizada.index, 'Ventas': tabla_organizada.values})
print("\nTabla de datos organizando por ventas de mayor a menor")
print(df_tabla_organizada.to_string(index=False))

# Crear tabla con el porcentaje del gasto total por categoría
gasto_por_categoria = df.groupby('CATEGORIA')['Spend'].sum()
gasto_total = gasto_por_categoria.sum()
porcentaje_gasto = (gasto_por_categoria / gasto_total) * 100
df_porcentaje_gasto = pd.DataFrame({'Categoría': porcentaje_gasto.index, 'Porcentaje Gasto': porcentaje_gasto.values})
df_porcentaje_gasto_ordenado = df_porcentaje_gasto.sort_values(by='Porcentaje Gasto', ascending=False)
print("\nTabla con porcentaje del gasto total que se invirtió para cada categoría")
print(df_porcentaje_gasto_ordenado.to_string(index=False))

# Guardar la base de datos transformada
with pd.ExcelWriter('base_datos_transformada.xlsx') as writer:
    df.to_excel(writer, sheet_name='Base transformada', index=False)
    df_tabla_organizada.to_excel(writer, sheet_name='Categorías por ventas', index=False)
    df_porcentaje_gasto_ordenado.to_excel(writer, sheet_name='Porcentaje gasto por categoría', index=False)
