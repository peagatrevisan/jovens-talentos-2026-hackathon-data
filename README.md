🎥 **Vídeo (3 min):** https://drive.google.com/file/d/1if1MMF3-z4kzed_rSZQTH7tc6gBV3rnE/view?usp=sharing

# Onde investir em Airbnb em Itapema (SC)? Testando uma tese com dados e IA

> **Hackathon Jovens Talentos AI Builder 2026 — Seazone** · análise feita em 1 dia, com um agente de IA (OpenCode) como par de programação
> **Stack:** Python · pandas · NumPy · OpenCode (agente de IA)

**Resposta curta:** a tese interna de que *apartamentos compactos no Centro* são a melhor aposta **não se sustenta nos dados**. O Centro com 1 quarto rende **6,35% ao ano** (6º lugar entre 11 perfis), enquanto **Morretes com 3 quartos** lidera com **9,94%**: custo de compra parecido, diária quase 50% maior.

---

## 1. O desafio

A Seazone pediu uma recomendação de investimento em imóveis para locação por temporada em Itapema, a partir de um snapshot do mercado, e uma posição clara sobre uma tese interna ainda não validada:

> *"Apartamentos compactos (studio/1 quarto) no Centro seriam a aposta mais eficiente."*

## 2. Os dados

| Arquivo | Linhas | Conteúdo |
|---|---|---|
| `VivaReal_Itapema.csv` | 8.329 | Imóveis à venda: preço, área, quartos, bairro, amenidades |
| `Details_Itapema.csv` | 4.441 | Anúncios do Airbnb: quartos, tipo, avaliações |
| `Price_AV_Itapema.csv` | 118.839 | Diárias por anúncio e data |
| `Mesh_Ids_Data_Itapema.csv` | 4.441 | Bairro e coordenadas de cada anúncio do Airbnb |
| `Hosts_ids_Itapema.csv` | 4.440 | Dados dos anfitriões |

## 3. Como cheguei à resposta

### Etapa 1 — Diagnóstico de qualidade antes de qualquer cálculo
Antes de calcular, pedi ao agente que verificasse a base. Dois problemas mudaram a análise:

- **Outliers graves no VivaReal:** área útil de **0 m² a 188.000 m²** e preços de até R$ 44 milhões. A média de área chegava a 197 m², contra mediana de 128 m². → **Decisão: trabalhar com medianas** e aplicar filtro de sanidade de área (20 a 500 m²).
- **Coordenadas 100% zeradas** em `Details` (4.441 de 4.441). → **Decisão: buscar o bairro real** cruzando com `Mesh_Ids` pelo `airbnb_listing_id`. Sem esse cruzamento, não seria possível segmentar o Airbnb por bairro.

### Etapa 2 — Testar a tese exatamente como foi formulada
Para o segmento **Centro + 1 quarto**:

| Premissa | Valor |
|---|---|
| Preço de compra (mediana VivaReal, n = 19) | R$ 890.000 |
| Diária (mediana Airbnb, 116 anúncios, 13.455 diárias) | R$ 471 |
| Ocupação assumida | 120 dias/ano |
| Receita bruta anual | R$ 56.520 |
| **Yield bruto anual** | **6,35%** |

O alto custo de aquisição no Centro achata a rentabilidade.

### Etapa 3 — Procurar a "anomalia de mercado"
Repeti o mesmo cálculo para **todos os bairros × número de quartos**, mantendo só os perfis com **pelo menos 10 imóveis à venda e 10 anúncios no Airbnb**, para evitar conclusões tiradas de 2 ou 3 anúncios. 11 perfis passaram no filtro.

| # | Perfil | Venda (mediana) | Diária (mediana) | Receita anual | **Yield** |
|---|---|---|---|---|---|
| 1 | **Morretes · 3 quartos** | R$ 845.000 | R$ 700 | R$ 84.000 | **9,94%** |
| 2 | Tabuleiro dos Oliveiras · 2q | R$ 780.939 | R$ 523 | R$ 62.760 | 8,04% |
| 3 | Morretes · 2q | R$ 790.000 | R$ 495 | R$ 59.400 | 7,52% |
| 4 | Meia Praia · 1q | R$ 877.500 | R$ 490 | R$ 58.800 | 6,70% |
| 5 | Centro · 2q | R$ 1.105.000 | R$ 600 | R$ 72.000 | 6,52% |
| 6 | *Centro · 1q (tese interna)* | R$ 890.000 | R$ 478 | R$ 57.360 | *6,44%* |

> A diferença entre 6,35% (etapa 2) e 6,44% (etapa 3) vem da remoção de diárias duplicadas (mesmo anúncio e mesma data) no script do ranking.

**Leitura:** Morretes 3 quartos custa praticamente o mesmo que o Centro 1 quarto, mas comporta famílias e grupos, que pagam uma diária quase 50% maior.

### Etapa 4 — Do perfil ao ativo: o que comprar hoje
Filtrei apartamentos de 3 quartos em Morretes abaixo de R$ 600 mil, com 60 a 150 m² e piscina ou churrasqueira, ordenados por preço:

| `listing_id` | Preço | Área | R$/m² | Destaques |
|---|---|---|---|---|
| 2664863504 | R$ 429.000 | 70 m² | R$ 6.129 | piscina, churrasqueira, academia (11 amenidades) |
| **2747933634** | **R$ 450.000** | **70 m²** | **R$ 6.429** | piscina, churrasqueira, ar-condicionado, garagem, elevador (31 amenidades) |
| 2762890210 | R$ 459.000 | 69 m² | R$ 6.652 | piscina, churrasqueira na varanda, elevador (33 amenidades) |

**Escolha: `2747933634`.** Custa só R$ 21 mil a mais que o mais barato e traz ar-condicionado, garagem e elevador, itens que pesam na avaliação e na ocupação no Airbnb. Está cerca de 46% abaixo da mediana do bairro.

Aplicando a diária mediana do perfil (R$ 700 × 120 dias = R$ 84.000), o yield bruto projetado seria de **18,7%**. Esse número é um **teto otimista**, pelos motivos da seção 5.

## 4. Recomendação final

1. **Melhor perfil:** apartamento de 3 quartos, imóvel inteiro para temporada.
2. **Melhor localização em eficiência de capital:** Morretes. Meia Praia fatura mais em valor absoluto (R$ 159 mil/ano no 4 quartos), mas exige R$ 3,6 milhões de compra (4,43% de yield).
3. **O que explica as melhores receitas:** capacidade para famílias e grupos, e o pacote piscina + churrasqueira, complementado por garagem, elevador e ar-condicionado.
4. **O que comprar:** o imóvel `2747933634`, condicionado à verificação da seção 6.
5. **Tese interna:** **não se sustenta.** Centro 1 quarto fica em 6º lugar de 11.

## 5. Limitações (o que eu checaria antes de investir dinheiro de verdade)

- **Yield bruto, não líquido.** Não desconta condomínio, IPTU, limpeza, taxa da plataforma, gestão e manutenção. O ranking entre bairros tende a se manter, mas os percentuais caem.
- **Ocupação de 120 dias igual para todos os bairros.** Bairros mais afastados da praia podem ter ocupação menor. É a premissa que mais pode mudar o ranking.
- **Amostra de Morretes 3q no Airbnb no limite:** exatamente 10 anúncios, o mínimo do filtro. Um ranking com mínimo de 20 anúncios mostraria se o resultado se mantém.
- **O 18,7% compara coisas diferentes:** o preço de um imóvel abaixo da mediana com a diária mediana do perfil inteiro. Um 3 quartos de 70 m² provavelmente cobra menos que a mediana. Imóveis muito abaixo da mediana com longas listas de amenidades também podem ser lançamentos na planta, sem renda imediata.
- **Sazonalidade:** se as diárias capturadas se concentram na alta temporada, multiplicar a mediana por 120 dias superestima a receita anual.
- **Cobertura do Airbnb:** `Price_AV` tem diárias de 1.005 dos 4.441 anúncios.
- **Grafias diferentes entre bases** ("Alto São Bento" vs "Alto Sao Bento") impediram o cruzamento de alguns bairros menores.

## 6. Próximos passos

- Calcular o yield líquido com condomínio e IPTU (o VivaReal tem `monthly_condo_fee` e `yearly_iptu`).
- Estimar ocupação por bairro a partir do calendário de disponibilidade, em vez de assumir 120 dias.
- Usar a diária de anúncios comparáveis (mesma área e quartos) para o imóvel escolhido.
- Padronizar os nomes de bairro antes do cruzamento.
- Verificar no anúncio se o imóvel escolhido está pronto ou na planta.

## 7. Como trabalhei com IA

Toda a análise foi feita em parceria com um agente de IA (OpenCode), e a conversa completa está no arquivo **Hackathon Seazone – AI Log**, na raiz deste repositório. A divisão de papéis foi:

- **O agente** escreveu e executou os scripts, inspecionou as colunas e resolveu problemas técnicos (encoding, parsing das amenidades).
- **As decisões de análise foram minhas:** validar a base antes de calcular, trocar média por mediana após o outlier de 188.000 m², exigir amostra mínima de 10 imóveis, formular a hipótese da "anomalia de mercado" e decidir como testar a tese interna.

Cada etapa foi um pedido curto e verificável, com o resultado conferido antes de passar à próxima.

## 8. Como rodar

```bash
git clone https://github.com/peagatrevisan/jovens-talentos-2026-hackathon-data.git
cd jovens-talentos-2026-hackathon-data
pip install pandas numpy

# rode a partir da raiz do repositório

python scripts/etl_load_data.py         # etapa 1: carga e diagnóstico de qualidade
python scripts/yield_centro_1q.py       # etapa 2: yield do segmento Centro + 1 quarto
python scripts/ranking_yield_bairros.py # etapa 3: ranking de todos os bairros x quartos
python scripts/morretes_3q_top3.py      # etapa 4: top 3 imóveis para compra
```

## 9. Estrutura

```
├── data/                         # bases fornecidas pela Seazone
├── scripts/
│   ├── etl_load_data.py          # etapa 1: carga e diagnóstico
│   ├── yield_centro_1q.py        # etapa 2: teste da tese interna
│   ├── ranking_yield_bairros.py  # etapa 3: ranking de perfis
│   └── morretes_3q_top3.py       # etapa 4: escolha do ativo
├── Hackathon Seazone - AI Log    # conversa completa com o agente de IA
├── index.html                    # enunciado do desafio
└── README.md
```

---

**Autor:** Pedro Henrique Trevisan · [LinkedIn](https://www.linkedin.com/in/pedro-henrique-trevisan) · [GitHub](https://github.com/peagatrevisan)
