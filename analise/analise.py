# -*- coding: utf-8 -*-
"""
Projeto da Unidade II · Métodos Estatísticos Aplicados às Ciências Tecnológicas (UFPB)

Roteiro do script (cada bloco responde a uma parte do enunciado):
  1. Lê as planilhas da professora: todos os municípios da PB (223) e do RN (167).
  2. Sorteia uma amostra aleatória simples (AAS) de 30 municípios por estado.
  3. Salva as amostras em dados/amostras.xlsx (é o arquivo do link pedido no cartaz).
  4. Questão 1: estatísticas descritivas da população e da amostra.
  5. Questão 2: histograma + boxplot do salário em cada amostra.
  6. Questões 3 a 5: intervalos de confiança e testes de hipóteses.
  7. Grava todos os números em saida/resultados.json (o cartaz lê desse arquivo).

Como rodar (PowerShell, dentro da pasta projeto-un2):
    python analise\\analise.py
"""
import json
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

import matplotlib
matplotlib.use("Agg")  # gera as imagens sem abrir janela
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, MultipleLocator

PASTA = Path(__file__).resolve().parent.parent  # pasta projeto-un2
ARQ_PB = PASTA / "dados-originais" / "pb" / "dados_pb.xlsx"
ARQ_RN = PASTA / "dados-originais" / "rn" / "dados_rn.xlsx"
ARQ_AMOSTRAS = PASTA / "dados" / "amostras.xlsx"
SAIDA = PASTA / "saida"

SEMENTE = 20261116  # data da apresentação, fixada ANTES do sorteio: rodar de novo sorteia os mesmos municípios
N = 30              # tamanho de cada amostra (enunciado)
ALFA = 0.05         # nível de significância de todos os testes
VARIAVEIS = ["ideb", "renda", "salario"]
NOMES = {
    "ideb": "IDEB – Anos iniciais do ensino fundamental (rede pública)",
    "renda": "% da população com rendimento nominal mensal per capita de até 1/2 salário mínimo",
    "salario": "Salário médio mensal dos trabalhadores formais (em salários mínimos)",
}

# Cores de identidade (as mesmas no cartaz inteiro): PB = azul, RN = laranja.
COR = {"PB": "#2a78d6", "RN": "#eb6834"}
TINTA, TINTA_2, GRADE, EIXO = "#0b0b0b", "#52514e", "#e1e0d9", "#c3c2b7"


# ----------------------------------------------------------------------------
# 1. Leitura dos dados
# ----------------------------------------------------------------------------
def carregar(arquivo, uf):
    df = pd.read_excel(arquivo)
    df.columns = ["municipio"] + VARIAVEIS
    # Na planilha, "-" quer dizer "sem dado" (o IDEB não foi divulgado para o município).
    # to_numeric(errors="coerce") transforma esse "-" em NaN (valor ausente).
    for v in VARIAVEIS:
        df[v] = pd.to_numeric(df[v], errors="coerce")
    df["uf"] = uf
    return df


def chave_alfabetica(serie):
    # Ordena ignorando acentos ("Água Branca" fica junto do "A", e não depois do "Z").
    return serie.map(lambda s: unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())


# ----------------------------------------------------------------------------
# 2. Amostragem aleatória simples (AAS) sem reposição
# ----------------------------------------------------------------------------
def sortear(pop, rng):
    # Base de sorteio: municípios com as 3 variáveis disponíveis. Os 6 municípios de cada
    # estado sem IDEB ficam de fora, porque a análise usa as 3 variáveis do mesmo município.
    base = pop.dropna(subset=VARIAVEIS).reset_index(drop=True)
    # Sem reposição: todo município da base tem a mesma chance e nenhum sai duas vezes.
    sorteados = rng.choice(len(base), size=N, replace=False)
    amostra = base.iloc[sorteados].copy()
    amostra.insert(0, "ordem_sorteio", np.arange(1, N + 1))
    amostra = amostra.sort_values("municipio", key=chave_alfabetica).reset_index(drop=True)
    return base, amostra


def salvar_amostras(amostras, bases, pops):
    cabecalho = {
        "municipio": "Município",
        "ideb": "IDEB – Anos iniciais (rede pública)",
        "renda": "% da população com renda per capita de até 1/2 salário mínimo",
        "salario": "Salário médio mensal dos trabalhadores formais (salários mínimos)",
        "ordem_sorteio": "Ordem no sorteio",
    }
    sobre = pd.DataFrame({
        "Item": ["Disciplina", "Fonte dos dados", "População", "Base de sorteio", "Amostragem",
                 "Semente", "Variáveis"],
        "Descrição": [
            "Métodos Estatísticos Aplicados às Ciências Tecnológicas (UFPB) · Projeto da Unidade II",
            "IBGE Cidades e Estados (ibge.gov.br/cidades-e-estados), planilhas fornecidas pela docente",
            f"PB: {len(pops['PB'])} municípios · RN: {len(pops['RN'])} municípios",
            f"Municípios com as 3 variáveis disponíveis · PB: {len(bases['PB'])} · RN: {len(bases['RN'])} "
            "(6 municípios de cada estado não têm IDEB divulgado)",
            f"Amostragem aleatória simples sem reposição, n = {N} por estado, sorteio por computador "
            "(Python, numpy.random.default_rng(semente).choice, primeiro PB, depois RN)",
            str(SEMENTE),
            "; ".join(NOMES.values()),
        ],
    })
    ARQ_AMOSTRAS.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(ARQ_AMOSTRAS, engine="openpyxl") as w:
        for aba, uf in [("Amostra 1 - PB", "PB"), ("Amostra 2 - RN", "RN")]:
            t = amostras[uf][["municipio"] + VARIAVEIS + ["ordem_sorteio"]].rename(columns=cabecalho)
            t.insert(0, "Nº", range(1, N + 1))
            t.to_excel(w, sheet_name=aba, index=False)
        sobre.to_excel(w, sheet_name="Sobre os dados", index=False)
        for ws in w.book.worksheets:  # só deixa as colunas largas o bastante para ler
            for col in ws.columns:
                largura = max(len(str(c.value)) for c in col if c.value is not None)
                ws.column_dimensions[col[0].column_letter].width = min(max(8, largura + 2), 95)
            ws.freeze_panes = "A2"


# ----------------------------------------------------------------------------
# 3. Questão 1: estatísticas descritivas
# ----------------------------------------------------------------------------
def descrever(valores, populacao):
    x = valores.dropna().to_numpy(dtype=float)
    # População: divide por N (variância populacional, σ²).
    # Amostra: divide por n − 1 (s², que estima σ² sem viés). É o que o var() do R faz.
    ddof = 0 if populacao else 1
    q1, mediana, q3 = np.quantile(x, [0.25, 0.50, 0.75])  # mesmo método padrão do R (tipo 7)
    dp = x.std(ddof=ddof)
    return {
        "n": int(x.size), "media": x.mean(), "mediana": mediana,
        "variancia": x.var(ddof=ddof), "dp": dp,
        "minimo": x.min(), "q1": q1, "q3": q3, "maximo": x.max(),
        "aiq": q3 - q1,           # amplitude interquartil (tamanho da caixa do boxplot)
        "cv": dp / x.mean(),       # coeficiente de variação: dispersão relativa à média
        # coeficiente de assimetria: > 0 cauda longa à direita, < 0 cauda longa à esquerda
        "assimetria": float(stats.skew(x, bias=populacao)),
        # Moda: não calculada. As 3 variáveis são quantitativas contínuas; valores repetidos
        # só aparecem porque o IBGE arredonda para 1 casa decimal.
    }


# ----------------------------------------------------------------------------
# 4. Questão 2: histograma + boxplot do salário em cada amostra
# ----------------------------------------------------------------------------
def virgula(casas):
    return FuncFormatter(lambda v, _: f"{v:.{casas}f}".replace(".", ","))


def estilo_graficos():
    plt.rcParams.update({
        "font.family": "Segoe UI",
        "font.size": 10.5,
        "svg.fonttype": "none",       # o texto do SVG continua texto (usa a fonte do cartaz)
        "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
        "axes.edgecolor": EIXO, "axes.linewidth": 0.9,
        "xtick.color": TINTA_2, "ytick.color": TINTA_2,
        "xtick.major.size": 0, "ytick.major.size": 0,
        "xtick.major.pad": 5, "ytick.major.pad": 6,
        "axes.labelcolor": TINTA_2, "axes.labelsize": 10.5,
    })


def outliers(x):
    # Regra do boxplot: atípico é o valor abaixo de Q1 − 1,5·AIQ ou acima de Q3 + 1,5·AIQ.
    q1, q3 = np.quantile(x, [0.25, 0.75])
    aiq = q3 - q1
    return q1 - 1.5 * aiq, q3 + 1.5 * aiq


def grafico_salario(amostras, desc):
    estilo_graficos()
    valores = {uf: amostras[uf]["salario"].to_numpy() for uf in ("PB", "RN")}
    todos = np.concatenate(list(valores.values()))
    # Classes de largura 0,2 salário mínimo, fechadas à esquerda: [1,2; 1,4), [1,4; 1,6) ...
    # O deslocamento de 0,001 evita que 1,4 caia na classe errada por arredondamento do computador.
    ini = np.floor(todos.min() * 5) / 5
    fim = np.ceil((todos.max() + 1e-9) * 5) / 5 + 0.2
    bordas = np.round(np.arange(ini, fim + 1e-9, 0.2), 1)
    contagens = {uf: np.histogram(valores[uf], bins=bordas - 0.001)[0] for uf in valores}
    ymax = max(c.max() for c in contagens.values())

    largura_mm, altura_mm = 176, 102
    fig = plt.figure(figsize=(largura_mm / 25.4, altura_mm / 25.4))
    gs = fig.add_gridspec(5, 1, height_ratios=[3.1, 1.25, 1.8, 3.1, 1.25], hspace=0,
                          left=0.075, right=0.985, top=1 - 9 / altura_mm, bottom=19 / altura_mm)
    blocos = {"PB": (gs[0], gs[1]), "RN": (gs[3], gs[4])}
    rotulo = {"PB": "Paraíba · Amostra 1", "RN": "Rio Grande do Norte · Amostra 2"}
    atipicos = {}

    for uf, (g_hist, g_box) in blocos.items():
        x, cor, d = valores[uf], COR[uf], desc[uf]["amostra"]["salario"]
        ax = fig.add_subplot(g_hist)
        # 2 px de "respiro" entre as barras (a cor do fundo separa, sem contorno)
        ax.bar(bordas[:-1] + 0.0045, contagens[uf], width=0.2 - 0.009, align="edge",
               color=cor, zorder=3)
        ax.set_xlim(bordas[0] - 0.05, bordas[-1] + 0.05)
        ax.set_ylim(0, ymax + 2.2)
        ax.yaxis.set_major_locator(MultipleLocator(4 if ymax > 10 else 2))
        ax.grid(axis="y", color=GRADE, linewidth=0.8, zorder=0)
        ax.tick_params(axis="x", labelbottom=False)
        ax.set_ylabel("municípios")
        for i, c in enumerate(contagens[uf]):
            if c:
                ax.text(bordas[i] + 0.1, c + 0.35, str(c), ha="center", va="bottom",
                        fontsize=9.5, color=TINTA_2)
        # título do painel: quadradinho na cor do estado + nome em tinta (texto nunca na cor da série)
        pos = ax.get_position()
        lado_pt = 8.2  # quadradinho da altura das maiúsculas do título
        base_y = pos.y1 + 3.5 / altura_mm
        fig.patches.append(plt.Rectangle((pos.x0, base_y), lado_pt / 72 * 25.4 / largura_mm,
                                         lado_pt / 72 * 25.4 / altura_mm,
                                         transform=fig.transFigure, color=cor, zorder=5))
        fig.text(pos.x0 + 0.024, base_y, f"{rotulo[uf]}  (n = {d['n']})",
                 fontsize=11.5, fontweight="bold", color=TINTA, va="baseline")

        bx = fig.add_subplot(g_box, sharex=ax)
        bx.boxplot(x, vert=False, widths=0.62, positions=[0], patch_artist=True, whis=1.5,
                   boxprops=dict(facecolor=cor + "2e", edgecolor=cor, linewidth=1.4),
                   medianprops=dict(color=cor, linewidth=3.0, solid_capstyle="butt"),
                   whiskerprops=dict(color=TINTA_2, linewidth=1.2),
                   capprops=dict(color=TINTA_2, linewidth=1.2),
                   flierprops=dict(marker="o", markersize=7.5, markerfacecolor=cor,
                                   markeredgecolor="white", markeredgewidth=1.4))
        bx.plot([x.mean()], [0], marker="D", markersize=6.5, color=TINTA,
                markeredgecolor="white", markeredgewidth=1.2, zorder=6)
        bx.set_ylim(-0.75, 0.75)
        bx.set_yticks([])
        bx.xaxis.set_major_locator(MultipleLocator(0.2))
        bx.xaxis.set_major_formatter(virgula(1))
        bx.spines["bottom"].set_color(EIXO)
        bx.grid(axis="x", color=GRADE, linewidth=0.6, zorder=0)
        # rótulo dos valores atípicos (seletivo: só eles recebem nome)
        lim_inf, lim_sup = outliers(x)
        fora = amostras[uf][(amostras[uf]["salario"] < lim_inf) | (amostras[uf]["salario"] > lim_sup)]
        atipicos[uf] = fora[["municipio", "salario"]].to_dict("records")
        for valor, grupo in fora.groupby("salario"):
            nomes = ", ".join(grupo["municipio"])
            bx.text(valor + 0.045, 0, f"{nomes} ({valor:.1f})".replace(".", ","), ha="left", va="center",
                    fontsize=9.5, color=TINTA)

    fig.axes[-1].set_xlabel("Salário médio mensal dos trabalhadores formais (em salários mínimos)")
    # o eixo x também aparece embaixo do boxplot da PB, para cada bloco ser lido sozinho
    fig.axes[1].tick_params(axis="x", labelbottom=True)
    # legenda de como ler o boxplot (símbolos neutros: descrevem formas, não estados)
    simbolos = [
        Patch(facecolor="#e9e8e3", edgecolor=TINTA_2, linewidth=1, label="caixa: de Q1 a Q3"),
        Line2D([], [], color=TINTA_2, linewidth=3, label="mediana"),
        Line2D([], [], marker="D", color=TINTA, linestyle="", markersize=6.5,
               markeredgecolor="white", label="média"),
        Line2D([], [], marker="o", color=TINTA_2, linestyle="", markersize=7,
               markeredgecolor="white", label="valor atípico (a mais de 1,5·AIQ da caixa)"),
    ]
    fig.legend(handles=simbolos, loc="lower center", bbox_to_anchor=(0.53, 0.0), ncol=4, frameon=False,
               fontsize=9, handlelength=1.3, handletextpad=0.5, columnspacing=1.3, labelcolor=TINTA_2)
    SAIDA.joinpath("graficos").mkdir(parents=True, exist_ok=True)
    fig.savefig(SAIDA / "graficos" / "salario_hist_boxplot.svg")
    fig.savefig(SAIDA / "graficos" / "salario_hist_boxplot.png", dpi=200)
    plt.close(fig)
    return atipicos


# ----------------------------------------------------------------------------
# 5. Questões 3 a 5: inferência
# ----------------------------------------------------------------------------
def ic_proporcao(p, n, conf=0.95):
    # IC para proporção: p̂ ± z·√(p̂(1 − p̂)/n)
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    ep = np.sqrt(p * (1 - p) / n)
    return {"p": p, "n": n, "z": z, "ep": ep, "erro": z * ep, "li": p - z * ep, "ls": p + z * ep}


def teste_duas_proporcoes(p1, n1, p2, n2):
    # H0: p1 = p2 contra H1: p1 ≠ p2. Sob H0, as amostras se juntam numa proporção comum.
    p_comum = (p1 * n1 + p2 * n2) / (n1 + n2)
    ep = np.sqrt(p_comum * (1 - p_comum) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / ep
    return {"p_comum": p_comum, "ep": ep, "z": z, "z_critico": stats.norm.ppf(1 - ALFA / 2),
            "p_valor": 2 * stats.norm.sf(abs(z)), "rejeita_h0": bool(2 * stats.norm.sf(abs(z)) < ALFA)}


def teste_f(x1, x2):
    # H0: σ1² = σ2² contra H1: σ1² ≠ σ2². F = s1²/s2² tem distribuição F(n1 − 1, n2 − 1) sob H0.
    s1, s2 = np.var(x1, ddof=1), np.var(x2, ddof=1)
    gl1, gl2 = len(x1) - 1, len(x2) - 1
    f = s1 / s2
    p = 2 * min(stats.f.cdf(f, gl1, gl2), stats.f.sf(f, gl1, gl2))
    return {"s2_1": s1, "s2_2": s2, "f": f, "gl1": gl1, "gl2": gl2,
            "f_crit_inf": stats.f.ppf(ALFA / 2, gl1, gl2), "f_crit_sup": stats.f.ppf(1 - ALFA / 2, gl1, gl2),
            "p_valor": p, "rejeita_h0": bool(p < ALFA)}


def teste_t(x1, x2, variancias_iguais):
    # H0: μ1 = μ2 contra H1: μ1 ≠ μ2.
    # Variâncias iguais -> t com variância combinada (gl = n1 + n2 − 2).
    # Variâncias diferentes -> t de Welch (gl pela fórmula de Welch-Satterthwaite).
    r = stats.ttest_ind(x1, x2, equal_var=variancias_iguais)
    gl = float(r.df)
    ic = r.confidence_interval(confidence_level=1 - ALFA)
    return {"variancias_iguais": variancias_iguais, "media_1": float(np.mean(x1)), "media_2": float(np.mean(x2)),
            "diferenca": float(np.mean(x1) - np.mean(x2)), "t": float(r.statistic), "gl": gl,
            "t_critico": float(stats.t.ppf(1 - ALFA / 2, gl)), "p_valor": float(r.pvalue),
            "ic_dif_li": float(ic.low), "ic_dif_ls": float(ic.high), "rejeita_h0": bool(r.pvalue < ALFA)}


def comparar_medias(x1, x2):
    # A dica do enunciado: primeiro o teste F decide a suposição sobre as variâncias,
    # depois o teste t adequado compara as médias.
    f = teste_f(x1, x2)
    t = teste_t(x1, x2, variancias_iguais=not f["rejeita_h0"])
    # Conferências para o relatório (não vão para o cartaz):
    # o outro teste t, o teste de Levene (não exige normalidade) e o Shapiro-Wilk (normalidade).
    outro_t = teste_t(x1, x2, variancias_iguais=f["rejeita_h0"])
    levene_p = float(stats.levene(x1, x2, center="median").pvalue)
    normal = {k: float(stats.shapiro(x).pvalue) for k, x in (("PB", x1), ("RN", x2))}
    return {"f": f, "t": t, "outro_t": outro_t, "levene_p": levene_p, "shapiro_p": normal}


def ic_media(x, valor_real):
    # IC de 95% para a média com σ desconhecido: x̄ ± t·s/√n (t com n − 1 graus de liberdade)
    li, ls = stats.t.interval(0.95, len(x) - 1, loc=np.mean(x), scale=stats.sem(x))
    return {"media": float(np.mean(x)), "li": float(li), "ls": float(ls), "valor_real": float(valor_real),
            "contem_valor_real": bool(li <= valor_real <= ls)}


def grafico_medias(ic_medias):
    # Complemento visual dos testes t: médias das amostras com IC de 95% (PB e RN lado a lado)
    estilo_graficos()
    altura_mm = 44
    fig, eixos = plt.subplots(1, 2, figsize=(176 / 25.4, altura_mm / 25.4), sharey=True)
    fig.subplots_adjust(left=0.065, right=0.985, top=1 - 8.5 / altura_mm, bottom=13.5 / altura_mm, wspace=0.10)
    paineis = [("ideb", "IDEB médio (anos iniciais)", 0.25), ("salario", "Salário médio (em salários mínimos)", 0.05)]
    for ax, (var, titulo, passo) in zip(eixos, paineis):
        for y, uf in [(1, "PB"), (0, "RN")]:
            ic, cor = ic_medias[var][uf], COR[uf]
            ax.plot([ic["li"], ic["ls"]], [y, y], color=cor, linewidth=3.2, solid_capstyle="butt", zorder=3)
            for borda in (ic["li"], ic["ls"]):
                ax.plot([borda, borda], [y - 0.13, y + 0.13], color=cor, linewidth=2.2, zorder=3)
                ax.text(borda, y - 0.22, f"{borda:.2f}".replace(".", ","), ha="center", va="top",
                        fontsize=9, color=TINTA_2)
            ax.plot([ic["media"]], [y], marker="o", markersize=10, color=cor, markeredgecolor="white",
                    markeredgewidth=1.8, zorder=5)
            ax.text(ic["media"], y - 0.22, f"{ic['media']:.2f}".replace(".", ","), ha="center", va="top",
                    fontsize=9.5, color=TINTA, fontweight="bold")
            ax.plot([ic["valor_real"]], [y + 0.22], marker="v", markersize=8, color=TINTA,
                    markeredgecolor="white", markeredgewidth=1.2, zorder=6)
        lo = min(ic_medias[var][uf]["li"] for uf in ("PB", "RN"))
        hi = max(ic_medias[var][uf]["ls"] for uf in ("PB", "RN"))
        folga = (hi - lo) * 0.12
        ax.set_xlim(lo - folga, hi + folga)
        ax.xaxis.set_major_locator(MultipleLocator(passo))
        ax.xaxis.set_major_formatter(virgula(2))
        ax.grid(axis="x", color=GRADE, linewidth=0.6, zorder=0)
        ax.set_xlabel(titulo)
    eixos[0].set_yticks([1, 0], ["PB", "RN"], fontsize=11, fontweight="bold", color=TINTA)
    eixos[0].set_ylim(-0.65, 1.45)
    simbolos = [
        Line2D([], [], marker="o", color=TINTA_2, linestyle="", markersize=8, markeredgecolor="white",
               label="média da amostra"),
        Line2D([], [], color=TINTA_2, linewidth=3, label="IC de 95% da média"),
        Line2D([], [], marker="v", color=TINTA, linestyle="", markersize=8, markeredgecolor="white",
               label="média real da população"),
    ]
    fig.legend(handles=simbolos, loc="upper center", bbox_to_anchor=(0.53, 1.0), ncol=3, frameon=False,
               fontsize=9, handlelength=1.4, handletextpad=0.5, columnspacing=1.5, labelcolor=TINTA_2)
    fig.savefig(SAIDA / "graficos" / "medias_ic.svg")
    fig.savefig(SAIDA / "graficos" / "medias_ic.png", dpi=200)
    plt.close(fig)


def grafico_ic(ics, parametros):
    estilo_graficos()
    altura_mm = 42
    fig, ax = plt.subplots(figsize=(176 / 25.4, altura_mm / 25.4))
    fig.subplots_adjust(left=0.075, right=0.985, top=1 - 8.5 / altura_mm, bottom=13.5 / altura_mm)
    for y, uf in [(1, "PB"), (0, "RN")]:
        ic, cor = ics[uf], COR[uf]
        li, ls, p = ic["li"] * 100, ic["ls"] * 100, ic["p"] * 100
        ax.plot([li, ls], [y, y], color=cor, linewidth=3.2, solid_capstyle="butt", zorder=3)
        for borda in (li, ls):
            ax.plot([borda, borda], [y - 0.12, y + 0.12], color=cor, linewidth=2.2, zorder=3)
            ax.text(borda, y - 0.2, f"{borda:.1f}%".replace(".", ","), ha="center", va="top",
                    fontsize=9.5, color=TINTA_2)
        ax.plot([p], [y], marker="o", markersize=10, color=cor, markeredgecolor="white",
                markeredgewidth=1.8, zorder=5)
        ax.text(p, y - 0.2, f"{p:.1f}%".replace(".", ","), ha="center", va="top",
                fontsize=10, color=TINTA, fontweight="bold")
        # valor real da população: triângulo apontando para a linha, por cima (não esconde a bolinha)
        ax.plot([parametros[uf] * 100], [y + 0.2], marker="v", markersize=8, color=TINTA,
                markeredgecolor="white", markeredgewidth=1.2, zorder=6)
    ax.set_yticks([1, 0], ["PB", "RN"], fontsize=11, fontweight="bold", color=TINTA)
    ax.set_ylim(-0.62, 1.42)
    simbolos = [
        Line2D([], [], marker="o", color=TINTA_2, linestyle="", markersize=8, markeredgecolor="white",
               label="estimativa da amostra"),
        Line2D([], [], color=TINTA_2, linewidth=3, label="IC de 95%"),
        Line2D([], [], marker="v", color=TINTA, linestyle="", markersize=8, markeredgecolor="white",
               label="valor real da população"),
    ]
    fig.legend(handles=simbolos, loc="upper center", bbox_to_anchor=(0.53, 1.0), ncol=3, frameon=False,
               fontsize=9, handlelength=1.4, handletextpad=0.5, columnspacing=1.5, labelcolor=TINTA_2)
    lo = min(ic["li"] for ic in ics.values()) * 100
    hi = max(ic["ls"] for ic in ics.values()) * 100
    ax.set_xlim(np.floor(lo / 5) * 5 - 2, np.ceil(hi / 5) * 5 + 2)
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.grid(axis="x", color=GRADE, linewidth=0.6, zorder=0)
    ax.set_xlabel("Proporção da população com renda per capita de até 1/2 salário mínimo")
    fig.savefig(SAIDA / "graficos" / "ic_proporcoes.svg")
    fig.savefig(SAIDA / "graficos" / "ic_proporcoes.png", dpi=200)
    plt.close(fig)


# ----------------------------------------------------------------------------
# Execução
# ----------------------------------------------------------------------------
def para_json(obj):
    # numpy -> tipos simples do Python, para o json conseguir gravar
    if isinstance(obj, dict):
        return {k: para_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [para_json(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def main():
    pops = {"PB": carregar(ARQ_PB, "PB"), "RN": carregar(ARQ_RN, "RN")}

    rng = np.random.default_rng(SEMENTE)
    bases, amostras = {}, {}
    for uf in ("PB", "RN"):  # a ordem importa: o mesmo gerador sorteia primeiro a PB, depois o RN
        bases[uf], amostras[uf] = sortear(pops[uf], rng)
    salvar_amostras(amostras, bases, pops)

    desc = {uf: {"populacao": {v: descrever(pops[uf][v], populacao=True) for v in VARIAVEIS},
                 "amostra": {v: descrever(amostras[uf][v], populacao=False) for v in VARIAVEIS}}
            for uf in ("PB", "RN")}

    atipicos = grafico_salario(amostras, desc)

    # Questão 3: a proporção de cada amostra é a média das 30 proporções municipais (em 0 a 1)
    p_hat = {uf: amostras[uf]["renda"].mean() / 100 for uf in ("PB", "RN")}
    p_real = {uf: pops[uf]["renda"].mean() / 100 for uf in ("PB", "RN")}  # valor da população inteira
    ics = {uf: ic_proporcao(p_hat[uf], N) for uf in ("PB", "RN")}
    for uf in ics:
        ics[uf]["contem_valor_real"] = bool(ics[uf]["li"] <= p_real[uf] <= ics[uf]["ls"])
        ics[uf]["valor_real"] = p_real[uf]
    teste_prop = teste_duas_proporcoes(p_hat["PB"], N, p_hat["RN"], N)
    grafico_ic(ics, p_real)

    # Conferência (não é o método pedido): tratar a proporção municipal como variável
    # quantitativa e usar o IC t da média. Fica no relatório para responder possíveis perguntas.
    conferencia_renda = {uf: {"media": amostras[uf]["renda"].mean(),
                              "ic": stats.t.interval(0.95, N - 1, loc=amostras[uf]["renda"].mean(),
                                                     scale=stats.sem(amostras[uf]["renda"]))}
                         for uf in ("PB", "RN")}
    conferencia_renda["teste"] = comparar_medias(amostras["PB"]["renda"].to_numpy(),
                                                 amostras["RN"]["renda"].to_numpy())

    # Questões 4 e 5
    ideb = comparar_medias(amostras["PB"]["ideb"].to_numpy(), amostras["RN"]["ideb"].to_numpy())
    salario = comparar_medias(amostras["PB"]["salario"].to_numpy(), amostras["RN"]["salario"].to_numpy())
    ic_medias = {var: {uf: ic_media(amostras[uf][var].to_numpy(), pops[uf][var].mean()) for uf in ("PB", "RN")}
                 for var in ("ideb", "salario")}
    grafico_medias(ic_medias)

    resultados = {
        "semente": SEMENTE, "n": N, "alfa": ALFA,
        "tamanho_populacao": {uf: len(pops[uf]) for uf in pops},
        "tamanho_base_sorteio": {uf: len(bases[uf]) for uf in bases},
        "sem_ideb": {uf: pops[uf].loc[pops[uf]["ideb"].isna(), "municipio"].tolist() for uf in pops},
        "amostras": {uf: amostras[uf].drop(columns="uf").to_dict("records") for uf in amostras},
        "descritivas": desc,
        "atipicos_salario": atipicos,
        "q3_ic": ics, "q3_teste": teste_prop, "q3_conferencia_t": conferencia_renda,
        "q4_ideb": ideb, "q5_salario": salario, "ic_medias": ic_medias,
    }
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "resultados.json").write_text(json.dumps(para_json(resultados), ensure_ascii=False, indent=2),
                                           encoding="utf-8")
    print("OK: dados/amostras.xlsx, saida/resultados.json e saida/graficos/ atualizados")


if __name__ == "__main__":
    main()
