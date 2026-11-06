import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = "data"


def load(name):
    return pd.read_csv(f"{DATA_DIR}/{name}.csv", sep=",", quotechar='"', low_memory=False)


def main():
    print("=" * 70)
    print("YIELD - Segmento: apartamento de 1 quarto no Centro (Itapema)")
    print("=" * 70)

    vivareal = load("VivaReal_Itapema")
    details = load("Details_Itapema")
    mesh = load("Mesh_Ids_Data_Itapema")
    price_av = load("Price_AV_Itapema")

    # --- Lado VivaReal: preco mediano de venda ---
    v = vivareal.copy()
    v["area"] = pd.to_numeric(v["usable_area"], errors="coerce")
    v["beds"] = pd.to_numeric(v["bedrooms"], errors="coerce")
    v["price"] = pd.to_numeric(v["sale_price"], errors="coerce")

    v_filtro = v[
        (v["listing_type"] == "apartamento")
        & (v["business_types"].isin(["Venda", "Ambos"]))  # ambos sao "para venda"
        & (v["area"] >= 20)
        & (v["area"] <= 500)
        & (v["suburb"] == "Centro")
        & (v["beds"] == 1)
        & v["price"].notna()
    ]
    mediana_venda = v_filtro["price"].median()
    print(f"\n[VivaReal] anúncios apto 1q Centro (area 20-500m2): {len(v_filtro):,}")
    print(f"  MEDIANA preço de venda: R$ {mediana_venda:,.2f}")

    # --- Lado Airbnb: diaria mediana ---
    m = mesh.drop_duplicates(subset="airbnb_listing_id", keep="first")[
        ["airbnb_listing_id", "suburb"]
    ]
    d = details.merge(m, on="airbnb_listing_id", how="left")
    d["beds"] = pd.to_numeric(d["number_of_bedrooms"], errors="coerce")

    d_filtro = d[
        (d["listing_type"] == "apartamento")
        & (d["suburb"] == "Centro")
        & (d["beds"] == 1)
    ]
    ids_segmento = set(d_filtro["airbnb_listing_id"])

    p = price_av[price_av["airbnb_listing_id"].isin(ids_segmento)].copy()
    p["price"] = pd.to_numeric(p["price"], errors="coerce")
    p = p[p["price"].notna()]
    mediana_diaria = p["price"].median()

    print(f"\n[Airbnb] listings 1q Centro (suburb real via Mesh_Ids): {len(d_filtro):,}")
    print(f"  diárias válidas no segmento (Price_AV): {len(p):,}")
    print(f"  MEDIANA diária: R$ {mediana_diaria:,.2f}")

    # --- Premissas e Yield ---
    ocupacao_dias = 120
    receita_anual = mediana_diaria * ocupacao_dias
    yield_pct = (receita_anual / mediana_venda) * 100

    print("\n" + "-" * 70)
    print("PREMISSAS")
    print(f"  1. preço de compra = mediana VivaReal = R$ {mediana_venda:,.2f}")
    print(f"  2. diária Airbnb   = mediana Price_AV = R$ {mediana_diaria:,.2f}")
    print(f"  3. ocupação anual  = {ocupacao_dias} dias")
    print(f"  4. receita anual   = diária x 120     = R$ {receita_anual:,.2f}")
    print("  5. rentabilidade (Yield) = (receita / preço) x 100")
    print("-" * 70)
    print(f"  >>> YIELD BRUTO ANUAL do perfil Centro + 1 quarto: {yield_pct:.2f}%")
    print("=" * 70)


if __name__ == "__main__":
    main()
