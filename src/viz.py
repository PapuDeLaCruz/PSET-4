import seaborn as sns
import matplotlib.pyplot as plt

def plot_cohort_heatmap(cohort_df, title="Cohort Retention Heatmap"):
    plt.figure(figsize=(14, 6))
    sns.heatmap(cohort_df, annot=True, fmt=".1f", linewidth=1, linecolor='gray')
    plt.title(title)
    plt.ylabel("Primera visita")
    plt.xlabel("Edad (meses)")
    plt.tight_layout()
    plt.show()

def plot_kpi(kpi_series, title="Evolución del KPI", ylabel="Valor", xlabel="Fecha"):
    plt.figure(figsize=(10, 4))
    kpi_series.plot(marker='o')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#para el ROMI
for i in (1,2,3,4,5,9,10):
    a = vis_ord[vis_ord['source_id'] == i].groupby('compra_mes')['revenue'].sum()
    b = costos[costos['source_id'] == i].groupby('dt_mes')['costs'].sum()
    romi = ((a - b) / b) * 100

    plt.figure(figsize=(10, 4))
    romi.plot(marker='o')
    plt.title(f"ROMI mensual - Fuente {i}")
    plt.ylabel("ROMI (%)")
    plt.xlabel("Mes")
    plt.grid(True)
    plt.tight_layout()
    plt.show()