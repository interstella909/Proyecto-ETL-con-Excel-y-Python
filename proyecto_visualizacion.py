import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
#pio.renderers.default = "vscode"
pio.renderers

# Crea un dataframe (df) con los datos de la hoja que necesitamos
df = pd.read_excel('base_datos_transformada.xlsx', sheet_name='Base transformada')

# Agrupamos las ventas por Retail
sales_by_retail = df.groupby('RETAIL')['Sales'].sum()

# Plotting gráfico de pay
sales_by_retail.plot.pie(autopct='%1.1f%%', startangle=90, cmap='viridis')
plt.title('Sales Distribution by Retail')
plt.ylabel('')
plt.show()

# Añadir la columna 'Month-Year' para análisis de tendencias
df['Month-Year'] = df['Date'].dt.to_period('M').astype(str)
# Agregar ventas por mes
monthly_sales = df.groupby('Month-Year')['Sales'].sum().reset_index()
# Calcular cambio porcentual mes a mes
monthly_sales['Pct Change'] = monthly_sales['Sales'].pct_change()
# Verificar el DataFrame agregado
print(monthly_sales)

# Graficar la tendencia de ventas por mes
fig = px.line(monthly_sales, x='Month-Year', y='Sales', title='Sales Trend by Month')
fig.show()

# Graficar el cambio porcentual mes a mes
fig2 = px.bar(monthly_sales, x='Month-Year', y='Pct Change', title='Monthly Sales Percentage Change')
fig2.show()

# Calcular el ROAS promedio por Retail y Categoría
roas_by_category_retail = df.groupby(['RETAIL', 'CATEGORIA'])['ROAS'].mean().reset_index()
# Encontrar la categoría con el mejor ROAS para cada Retail
best_roas_by_retail = roas_by_category_retail.loc[roas_by_category_retail.groupby('RETAIL')['ROAS'].idxmax()].reset_index(drop=True)
# Verificar el DataFrame
print(best_roas_by_retail)

# Graficar el mejor ROAS por categoría en cada Retail
fig3 = px.bar(best_roas_by_retail, x='RETAIL', y='ROAS', color='CATEGORIA', title='Best ROAS by Category in Each Retail')
fig3.show()
