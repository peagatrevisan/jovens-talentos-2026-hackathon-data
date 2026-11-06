import pandas as pd
import numpy as np
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

FILES = {
    "VivaReal": "VivaReal_Itapema.csv",
    "Details": "Details_Itapema.csv",
    "Price_AV": "Price_AV_Itapema.csv",
    "Mesh_Ids": "Mesh_Ids_Data_Itapema.csv",
    "Hosts": "Hosts_ids_Itapema.csv",
}


def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    return pd.read_csv(path, sep=",", quotechar='"', encoding="utf-8", low_memory=False)


def main():
    dfs = {}
    print("=" * 70)
    print("ETAPA 1 - CARGA DOS ARQUIVOS CSV (separador: , com aspas)")
    print("=" * 70)
    for name, fname in FILES.items():
        df = load_csv(fname)
        dfs[name] = df
        print(f"\n[{name}] {fname}")
        print(f" linhas: {len(df):,} colunas: {df.shape[1]}")
        print(f" colunas: {list(df.columns)}")

    vivareal = dfs["VivaReal"]
    print("\n" + "=" * 70)
    print("VERIFICACAO 1 - OUTLIERS - VivaReal (sales_price / usable_area)")
    print("=" * 70)

    for col in ["sale_price", "usable_area"]:
        s = pd.to_numeric(vivareal[col], errors="coerce")
        n_null = s.isna().sum()
        n_total = s.size
        print(f"\n>>> coluna: {col}")
        print(f" não-nulos: {n_total - n_null:,} nulos: {n_null:,} ({(n_null / n_total) * 100:.1f}%)")
        s_drop = s.dropna()
        print(f" descritiva:\n{s_drop.describe().to_string()}")
        q1, q3 = s_drop.quantile(0.25), s_drop.quantile(0.75)
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_out = ((s_drop < low) | (s_drop > high)).sum()
        print(f" regra IQR 1.5x -> limites: [{low:,.2f}, {high:,.2f}]")
        print(f" outliers (IQR): {n_out:,} ({(n_out / len(s_drop)) * 100:.1f}% dos não-nulos)")
        z = np.abs((s_drop - s_drop.mean()) / s_drop.std())
        n_z = (z > 3).sum()
        print(f" outliers (|z-score|>3): {n_z:,} ({(n_z / len(s_drop)) * 100:.1f}% dos não-nulos)")

    details = dfs["Details"]
    print("\n" + "=" * 70)
    print("VERIFICACAO 2 - COORDENADAS - Details (latitude / longitude)")
    print("=" * 70)
    for col in ["latitude", "longitude"]:
        s = pd.to_numeric(details[col], errors="coerce")
        n_zero = (s == 0).sum()
        n_na = s.isna().sum()
        n_null = ((s.isna()) | (s == 0)).sum()
        n_total = s.size
        print(f"\n>>> coluna: {col}")
        print(f" total: {n_total:,} zeradas (0.0): {n_zero:,} ausentes/NA: {n_na:,}")
        print(f" COORDENADA VAZIA/INVÁLIDA (0 ou NA): {n_null:,} ({(n_null / n_total) * 100:.1f}%)")
        print(f" preenchidas corretamente: {n_total - n_null:,} ({(1 - n_null / n_total) * 100:.1f}%)")
        valid = s[(s != 0) & s.notna()]
        if len(valid):
            print(f" range válido: [{valid.min():.6f}, {valid.max():.6f}]")
        else:
            print(" sem coordenadas válidas")

    print("\n" + "=" * 70)
    print("Etapa 1 concluída.")
    print("=" * 70)


if __name__ == "__main__":
    main()
