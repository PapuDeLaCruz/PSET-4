import pandas as pd

#lectura inicial
visits = pd.read_csv('../data/raw/visits_log_us.csv')
orders = pd.read_csv('../data/raw/orders_log_us.csv')
costs = pd.read_csv('../data/raw/costs_us.csv')

#cambiando el nombre de las columnas y pasando a datetime (se que da igual pq les mandamos a csv y toca hacer a la lectura pero bueno)
visits['End Ts'] = pd.to_datetime(visits['End Ts'])
visits['Start Ts'] = pd.to_datetime(visits['Start Ts'])

visits.columns = [column.lower().replace(' ','_') for column in visits.columns]

costs['dt']=pd.to_datetime(costs['dt'])
orders['Buy Ts']=pd.to_datetime(orders['Buy Ts'])
orders.columns = [column.lower().replace(' ','_') for column in orders.columns]

#guardando el interim
visits.to_csv('../../data/interim/visits.csv')
costs.to_csv('../../data/interim/costs.csv')
orders.to_csv('../../data/interim/orders.csv')

#cargando del interim
visitas = pd.read_csv('../../data/interim/visits.csv')
ordenes = pd.read_csv('../../data/interim/orders.csv')
costos = pd.read_csv('../../data/interim/costs.csv')

#agregando columnas utiles con el tipo correcto para el analisis
visitas['end_ts'] = pd.to_datetime(visitas['end_ts'])
visitas['start_ts'] = pd.to_datetime(visitas['start_ts'])
costos['dt']=pd.to_datetime(costos['dt'])
ordenes['buy_ts']=pd.to_datetime(ordenes['buy_ts'])

visitas['sesion_mes'] = pd.to_datetime(visitas['start_ts'].dt.strftime('%Y-%m-01'))
visitas['sesion_semana'] = visitas['start_ts'].dt.isocalendar().week
visitas['sesion_fecha'] = visitas['start_ts'].dt.date

visitas['duracion_visita'] = visitas['end_ts']-visitas['start_ts']

visitas = visitas.sort_values(by=['uid', 'start_ts'])
visitas['tiempo_entre_visitas'] = visitas.groupby('uid')['start_ts'].diff()

visitas = visitas.sort_values(by=['uid', 'start_ts'],ascending=True)
visitas['primera_visita'] = visitas.groupby('uid')['start_ts'].transform('first')

visitas.sort_values('uid').head(10)
ordenes = orders.sort_values(by=['uid', 'buy_ts'],ascending=True)
ordenes['primera_compra'] = ordenes.groupby('uid')['buy_ts'].transform('first')

vis_ord_prev = ordenes.merge(visitas,on='uid',how='inner')
#creando una unioni entre visitas y ordenes, esto nos da todas las compras varias veces
vis_ord = vis_ord_prev[(vis_ord_prev['buy_ts'] >= vis_ord_prev['start_ts']) & (vis_ord_prev['buy_ts'] <= vis_ord_prev['end_ts'])]
#no todas las sesiones resultan en una compra

vis_ord = vis_ord.sort_values(by=['uid', 'start_ts'])

vis_ord_no_dup = vis_ord.drop_duplicates(subset='uid', keep='first').copy()

#agregando  columnas utiles para el analisis
vis_ord_no_dup['tiempo_registro_compra'] = vis_ord_no_dup['primera_compra']-vis_ord_no_dup['primera_visita']

vis_ord_no_dup = vis_ord_no_dup.sort_values(by='tiempo_registro_compra')

vis_ord_no_dup['conversion_dia'] = vis_ord_no_dup['tiempo_registro_compra'].dt.days
vis_ord_no_dup['conversion_mes'] = (vis_ord_no_dup['tiempo_registro_compra'].dt.days)//31


ordenes['compra_cohorte_dia'] = ordenes['buy_ts'].dt.date
ordenes['compra_cohorte_mes'] = ordenes['buy_ts'].dt.to_period('M')
ordenes['compra_cohorte_year'] = ordenes['buy_ts'].dt.year

ordenes['cohorte_hora_del_dia'] = ordenes['buy_ts'].dt.hour

ordenes['compra_cohorte_hora_mes'] = ordenes['buy_ts'].dt.strftime('%m %H:00')

ordenes['compra_cohorte_hora_mes_dia'] = ordenes['buy_ts'].dt.strftime('%m-%d %H:00')

ordenes['compra_cohorte_hora_year_mes_dia'] = ordenes['buy_ts'].dt.to_period('h')

vis_ord['primera_visita_dia'] = pd.to_datetime(vis_ord['primera_visita'].dt.date)
vis_ord['primera_visita_mes'] = pd.to_datetime(vis_ord['primera_visita'].dt.strftime('%Y-%m-01'))

import numpy as np

vis_ord.sort_values('uid')

vis_ord['edad_meses']=((vis_ord['sesion_mes']-vis_ord['primera_visita_mes'])/(30*np.timedelta64(1,'D'))).round().astype('int')

vis_ord.sort_values('uid').head(10)

costos['dt_dia'] = pd.to_datetime(costos['dt'].dt.date)
costos['dt_mes'] = pd.to_datetime(costos['dt'].dt.strftime('%Y-%m-01'))

visitas['primera_visita_dia'] = pd.to_datetime(visitas['primera_visita'].dt.date)
visitas['primera_visita_mes'] = pd.to_datetime(visitas['primera_visita'].dt.strftime('%Y-%m-01'))

vis_ord['compra_mes'] = pd.to_datetime(vis_ord['buy_ts'].dt.strftime('%Y-%m-01'))
vis_ord['compra_semana'] = vis_ord['buy_ts'].dt.isocalendar().week
vis_ord['compra_fecha'] = vis_ord['buy_ts'].dt.date

ordenes['compra_mes'] = pd.to_datetime(ordenes['buy_ts'].dt.strftime('%Y-%m-01'))
ordenes['compra_semana'] = ordenes['buy_ts'].dt.isocalendar().week
ordenes['compra_fecha'] = ordenes['buy_ts'].dt.date

#eliminando columnas innecesarias
vis_ord_no_dup.drop('Unnamed: 0',axis=1,inplace=True)
costos.drop('Unnamed: 0',axis=1,inplace=True)
visitas.drop('Unnamed: 0',axis=1,inplace=True)
vis_ord.drop('Unnamed: 0',axis=1,inplace=True)

#enviando a processed
costos.to_csv('../../data/processed/costos_processed.csv')
ordenes.to_csv('../../data/processed/ordenes_processed.csv')
visitas.to_csv('../../data/processed/visitas_processed.csv')
vis_ord.to_csv('../../data/processed/visitas_y_ordenes_processed.csv')
vis_ord_no_dup.to_csv('../../data/processed/visitas_y_ordenes_sin_duplicados.csv')
