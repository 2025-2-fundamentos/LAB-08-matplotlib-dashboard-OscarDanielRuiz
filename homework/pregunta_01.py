# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""


def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """

    import pandas as pd
    import matplotlib
    import matplotlib.pyplot as plt
    import os

    def load_data():
        return pd.read_csv("files/input/shipping-data.csv")

    def save_plot(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path)
        plt.close()

    def Warehouse_block(df):
        df = df.copy()
        plt.figure()
        counts = df.Warehouse_block.value_counts()
        counts.plot.bar(
            title="Shipping per Warehouse",
            xlabel="Warehouse Block",
            ylabel="Record count",
            color="tab:blue",
            fontsize=8,
        )
        ax = plt.gca()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        save_plot("docs/shipping_per_warehouse.png")

    def mode_of_shipment(df):
        df = df.copy()
        plt.figure()
        counts = df.Mode_of_Shipment.value_counts()
        counts.plot.pie(
            title="Mode of Shipment",
            wedgeprops={"width": 0.35},
            ylabel="",
            colors=["tab:blue", "tab:orange", "tab:green"],
        )
        save_plot("docs/mode_of_shipment.png")

    def average_customer_rating(df):
        df = df.copy()
        plt.figure()
        resumen = (
            df[["Mode_of_Shipment", "Customer_rating"]]
            .groupby("Mode_of_Shipment")
            .describe()
        )
        resumen.columns = resumen.columns.droplevel()
        resumen = resumen[["mean", "min", "max"]]
        plt.barh(
            y=resumen.index.values,
            width=resumen["max"].values - 1,
            left=resumen["min"].values,
            height=0.9,
            color="lightgray",
            alpha=0.8,
        )
        colores = ["tab:green" if v >= 3.0 else "tab:orange" for v in resumen["mean"].values]
        plt.barh(
            y=resumen.index.values,
            width=resumen["mean"].values - 1,
            left=resumen["min"].values,
            height=0.5,
            alpha=1.0,
            color=colores,
        )
        plt.title("Average Customer Rating")
        ax = plt.gca()
        ax.spines["left"].set_color("gray")
        ax.spines["bottom"].set_color("gray")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        save_plot("docs/average_customer_rating.png")

    def weight_in_gms(df):
        df = df.copy()
        plt.figure()
        df.Weight_in_gms.plot.hist(
            title="Shipped Weight Distribution",
            color="tab:orange",
            edgecolor="white",
        )
        ax = plt.gca()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        save_plot("docs/weight_distribution.png")

    def create_html_dashboard():
        html_code = """<!DOCTYPE html>
    <html>
        <body>
            <h1>Shipping Dashboard Example</h1>
            <div style="width:45%;float:left">
                <img src="shipping_per_warehouse.png" alt="Fig 1">
                <img src="mode_of_shipment.png" alt="Fig 2">
            </div>

            <div style="width:45%;float:left">
                <img src="average_customer_rating.png" alt="Fig 3">
                <img src="weight_distribution.png" alt="Fig 4">
            </div>
        </body>
    </html>
    """
        os.makedirs("docs", exist_ok=True)
        with open("docs/index.html", "w", encoding="utf-8") as f:
            f.write(html_code)

    df = load_data()
    Warehouse_block(df)
    mode_of_shipment(df)
    average_customer_rating(df)
    weight_in_gms(df)
    create_html_dashboard()
