import sys
import json
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

v = pd.read_csv(r"data/VivaReal_Itapema.csv", sep=",", quotechar='"', low_memory=False)

v["area"] = pd.to_numeric(v["usable_area"], errors="coerce")
v["beds"] = pd.to_numeric(v["bedrooms"], errors="coerce")
v["price"] = pd.to_numeric(v["sale_price"], errors="coerce")

def parse_amenities(raw):
    if pd.isna(raw):
        return []
    try:
        return json.loads(str(raw).replace('""', '"'))
    except Exception:
        return []

v["amenity_list"] = v["amenities"].apply(parse_amenities)

f = v[
    (v["listing_type"] == "apartamento")
    & (v["business_types"].isin(["Venda", "Ambos"]))
    & (v["suburb"] == "Morretes")
    & (v["beds"] == 3)
    & (v["price"] < 600000)
    & (v["area"] >= 60)
    & (v["area"] <= 150)
    & v["price"].notna()
].copy()

core = {"POOL", "BARBECUE_GRILL"}
f["has_pool"] = f["amenity_list"].apply(lambda lst: "POOL" in lst)
f["has_churrasqueira"] = f["amenity_list"].apply(lambda lst: "BARBECUE_GRILL" in lst)
f["n_amen"] = f["amenity_list"].apply(len)
f["preco_m2"] = (f["price"] / f["area"]).round(0)

f = f[(f["has_pool"] | f["has_churrasqueira"])]
f = f.sort_values("price", ascending=True).reset_index(drop=True)

top3 = f.head(3)
print("TOP 3 - apto 3q Morretes < R$ 600k (area 60-150 m2) com boas amenidades:")
print("-" * 100)
for i, r in top3.iterrows():
    print(f"listing_id: {r['listing_id']}")
    print(f"Preço : R$ {r['price']:,.0f}")
    print(f"Área util: {r['area']:.0f} m2")
    print(f"R$/m2 : R$ {r['preco_m2']:,.0f}")
    print(f"Amenidades: {', '.join(r['amenity_list'])}")
    print(f"n° total: {r['n_amen']} amenidades | Pool: {r['has_pool']} | Churrasqueira: {r['has_churrasqueira']}")
    print("-" * 100)