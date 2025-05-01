import pandas as pd

costos = pd.read_csv('../../data/processed/costos_processed.csv')
ordenes = pd.read_csv('../../data/processed/ordenes_processed.csv')
visitas = pd.read_csv('../../data/processed/visitas_processed.csv')
vis_ord = pd.read_csv('../../data/processed/visitas_y_ordenes_processed.csv')
vis_ord_no_dup = pd.read_csv('../../data/processed/visitas_y_ordenes_sin_duplicados.csv')

#KPI
print(vis_ord_no_dup.iloc[:,-1].mean())

#Cohortes LTV

cohortes_ltv = vis_ord.pivot_table(
    index='primera_visita_mes',
    columns = 'edad_meses',
    values = 'revenue',
    aggfunc='mean'
)

print(cohortes_ltv)