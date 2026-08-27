import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = "data"
OCUPACAO_DIAS = 120
MIN_AMOSTRA = 10

def load(name):
    return pd.read_csv(f"{DATA_DIR}/{name}.csv", sep=",", quotechar='"', low_memory=False)

def main():
    print("=" * 78)
    print("RANKING DE YIELD BRUTO ANUAL - todos os bairros x nº de quartos (Itapema)")
    print(f"filtros: apto p/ venda | area util 20-500m2 | ocupacao {OCUPACAO_DIAS} dias")
    print(f"exigência: >= {MIN_AMOSTRA} imóveis na amostra VivaReal E >= {MIN_AMOSTRA} no Airbnb")
    print("=" * 78)

    vivareal = load("VivaReal_Itapema")
    details = load("Details_Itapema")
    mesh = load("Mesh_Ids_Data_Itapema")
    price_av = load("Price_AV_Itapema")

    # ---- lado VIVA REAL: mediana de venda por (bairro, quartos) ----
    v = vivareal.copy()
    v["area"] = pd.to_numeric(v["usable_area"], errors="coerce")
    v["beds"] = pd.to_numeric(v["bedrooms"], errors="coerce")
    v["price"] = pd.to_numeric(v["sale_price"], errors="coerce")

    v_filtro = v[
        (v["listing_type"] == "apartamento")
        & (v["business_types"].isin(["Venda", "Ambos"]))
        & (v["area"] >= 20)
        & (v["area"] <= 500)
        & (v["beds"] >= 1)
        & v["price"].notna()
        & v["suburb"].notna()
    ]

    v_agg = (
        v_filtro.groupby(["suburb", "beds"])
        .agg(n_viva=("price", "size"), mediana_venda=("price", "median"))
        .reset_index()
    )

    # ---- lado AIRBNB: mediana da diaria por (bairro, quartos) ----
    m = mesh.drop_duplicates(subset="airbnb_listing_id", keep="first")[
        ["airbnb_listing_id", "suburb"]
    ]

    d = details.merge(m, on="airbnb_listing_id", how="inner")
    d["beds"] = pd.to_numeric(d["number_of_bedrooms"], errors="coerce")
    d_filtro = d[(d["listing_type"] == "apartamento") & (d["beds"] >= 1) & d["suburb"].notna()]

    p = price_av.drop_duplicates(subset=["airbnb_listing_id", "date"])
    p["price"] = pd.to_numeric(p["price"], errors="coerce")
    p = p[p["price"].notna()]
    dp = d_filtro.merge(p, on="airbnb_listing_id", how="inner")

    dp_agg = (
        dp.groupby(["suburb", "beds"])
        .agg(
            n_airbnb=("airbnb_listing_id", "nunique"),
            mediana_diaria=("price", "median"),
        )
        .reset_index()
    )

    # ---- combina e aplica condicao de amostra minima ----
    merged = v_agg.merge(dp_agg, on=["suburb", "beds"], how="inner")
    merged = merged[(merged["n_viva"] >= MIN_AMOSTRA) & (merged["n_airbnb"] >= MIN_AMOSTRA)]

    merged["receita_anual"] = merged["mediana_diaria"] * OCUPACAO_DIAS
    merged["yield_pct"] = (merged["receita_anual"] / merged["mediana_venda"]) * 100

    merged["perfil"] = merged["suburb"] + " - " + merged["beds"].astype(int).astype(str) + " quarto(s)"

    merged = merged.sort_values("yield_pct", ascending=False).reset_index(drop=True)

    print(f"\nperfis que atendem >= {MIN_AMOSTRA} imóveis nas duas amostras: {len(merged)}")
    print("\n--- TODOS OS PERFIS QUALIFICADOS (ordenados por yield) ---")
    cols = ["perfil", "n_viva", "mediana_venda", "n_airbnb", "mediana_diaria", "receita_anual", "yield_pct"]
    with pd.option_context("display.max_rows", None, "display.width", 120):
        print(merged[cols].to_string(index=False, formatters={
            "mediana_venda": lambda x: f"R$ {x:,.2f}",
            "mediana_diaria": lambda x: f"R$ {x:,.2f}",
            "receita_anual": lambda x: f"R$ {x:,.2f}",
            "yield_pct": lambda x: f"{x:.2f}%",
        }))

    print("\n--- TOP 5 PERFIS MAIS RENTÁVEIS ---")
    top5 = merged.head(5).reset_index(drop=True)
    for i, r in top5.iterrows():
        print(
            f"{i+1}. {r['perfil']}: yield {r['yield_pct']:.2f}% | \n"
            f"venda mediana R$ {r['mediana_venda']:,.2f} (n={r['n_viva']}) | \n"
            f"diária mediana R$ {r['mediana_diaria']:,.2f} (n={r['n_airbnb']}) | \n"
            f"receita anual R$ {r['receita_anual']:,.2f}"
        )
    print("=" * 78)

if __name__ == "__main__":
    main()