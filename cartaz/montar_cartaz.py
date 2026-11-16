# -*- coding: utf-8 -*-
"""
Monta o cartaz a partir de saida/resultados.json e cartaz/config.json.

Gera, dentro da pasta cartaz/:
  cartaz.html        o cartaz pronto (abre no navegador)
  cartaz_A2.pdf      1 página A2 (42 x 59,4 cm), para gráfica; também amplia para A1 sem perder qualidade
  cartaz_4xA4.pdf    4 páginas A4 para imprimir em casa e colar na cartolina em 2 x 2
  cartaz_2xA3.pdf    2 páginas A3 (deitadas) para copiadora, uma em cima da outra

Como rodar (PowerShell, dentro da pasta projeto-un2), depois de editar o config.json:
    python cartaz\\montar_cartaz.py
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path
from string import Template

import fitz  # PyMuPDF: recorta o PDF A2 em A4 e A3 sem perder a qualidade vetorial
import qrcode
import qrcode.image.svg

PASTA = Path(__file__).resolve().parent  # projeto-un2/cartaz
RAIZ = PASTA.parent
R = json.loads((RAIZ / "saida" / "resultados.json").read_text(encoding="utf-8"))
# utf-8-sig: aceita o config.json salvo com ou sem BOM (o Bloco de Notas e o PowerShell às vezes gravam BOM)
CFG = json.loads((PASTA / "config.json").read_text(encoding="utf-8-sig"))
NAVEGADORES = [Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
               Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")]


# ---------------------------------------------------------------- formatação pt-BR
def br(x, casas=2):
    # Arredonda pelo valor decimal, com a regra da ABNT NBR 5891 (empate vai para o algarismo par:
    # 1,625 vira 1,62). O round(x, 10) apaga o erro de ponto flutuante antes: sem ele, o Q1 4,925
    # (guardado como 4.925000000000001) viraria 4,93, contrariando a regra.
    valor = Decimal(repr(round(x, 10))).quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_EVEN)
    return f"{valor:f}".replace(".", ",").replace("-", "−")


def pval(p):
    return "< 0,001" if p < 0.001 else br(p, 3)


# ---------------------------------------------------------------- conferência dos resultados
# Os textos de interpretação do modelo.html foram escritos para ESTES resultados.
# Se alguém mudar a semente ou os dados e as decisões mudarem, o script para aqui,
# para ninguém imprimir um cartaz com texto contradizendo os números.
if 'metodologia' not in R or 'M' not in R['q3_ic']['PB']:
    sys.exit('Execute a análise corrigida antes de gerar o cartaz.')


# ---------------------------------------------------------------- valores para o modelo
d = R["descritivas"]
v = {"semente": str(R["semente"]), "n": str(R["n"]), "n_total": str(2 * R["n"]),
     "N_PB": str(R["tamanho_populacao"]["PB"]), "N_RN": str(R["tamanho_populacao"]["RN"]),
     "B_PB": str(R["tamanho_base_sorteio"]["PB"]), "B_RN": str(R["tamanho_base_sorteio"]["RN"])}

for uf in ("PB", "RN"):
    for tipo, t in (("populacao", "pop"), ("amostra", "am")):
        for var, ests in d[uf][tipo].items():
            for est, val in ests.items():
                chave = f"{var}_{uf.lower()}_{t}_{est}"
                if est == "n":
                    v[chave] = str(val)
                else:
                    v[chave] = br(val, 3 if (est == "variancia" and var != "renda") else 2)
                    v[chave + "_1"] = br(val, 1)

ic, tp = R["q3_ic"], R["q3_teste"]
for uf in ("PB", "RN"):
    v[f"p_{uf.lower()}"] = br(ic[uf]["media"], 1)
    v[f"li_{uf.lower()}"] = br(ic[uf]["li"], 1)
    v[f"ls_{uf.lower()}"] = br(ic[uf]["ls"], 1)
    v[f"real_{uf.lower()}"] = br(ic[uf]["valor_real"], 1)
v["margem"] = br(max(ic[uf]["erro"] for uf in ("PB", "RN")), 1)

t4 = R["q4_ideb"]["t"]
v.update({"ideb_dif": br(t4["diferenca"], 2), "ideb_dif_li": br(t4["ic_dif_li"], 2),
          "ideb_dif_ls": br(t4["ic_dif_ls"], 2), "q4_p": pval(t4["p_valor"])})

# valores atípicos e limites do boxplot (Q3 + 1,5·AIQ)
for uf in ("PB", "RN"):
    atip = R["atipicos_salario"][uf]
    v[f"atipicos_{uf.lower()}"] = ", ".join(f"{a['municipio']} ({uf}, {br(a['salario'], 1)} SM)" for a in atip)
    am = d[uf]["amostra"]["salario"]
    v[f"lim_{uf.lower()}"] = br(am["q3"] + 1.5 * am["aiq"], 2)
    assert all(a["salario"] > am["q3"] + 1.5 * am["aiq"] for a in atip), "texto supõe atípicos só acima"
    # AIQ com 3 casas: com 2 casas, 0,275 viraria 0,27 e não bateria com Q3 − Q1 da tabela
    v[f"salario_{uf.lower()}_am_aiq"] = br(am["aiq"], 3)
salarios_pb = [a["salario"] for a in R["amostras"]["PB"]]
v["pb_entre_16_20"] = str(sum(1.6 - 1e-9 <= s < 2.0 - 1e-9 for s in salarios_pb))


# ---------------------------------------------------------------- tabela descritiva
# Uma linha por estado e por tipo (população/amostra), uma coluna por estatística:
# população e amostra ficam vizinhas, e PB e RN também.
ESTATS = [("n", "n"), ("media", "Média"), ("mediana", "Mediana"), ("variancia", "Variância"),
          ("dp", "Desvio padrão"), ("minimo", "Mínimo"), ("q1", "Q1"), ("q3", "Q3"), ("maximo", "Máximo")]
GRUPOS = [("ideb", "IDEB: anos iniciais, rede pública (0 a 10)"),
          ("renda", "Renda: % da população com renda per capita de até 1/2 SM"),
          ("salario", "Salário médio mensal dos trabalhadores formais (em SM)")]
LINHAS = [("pb", "pop", "PB", "população"), ("pb", "am", "PB", "amostra"),
          ("rn", "pop", "RN", "população"), ("rn", "am", "RN", "amostra")]

linhas = []
for var, titulo in GRUPOS:
    linhas.append(f'<tr class="grupo"><th colspan="{len(ESTATS) + 1}">{titulo}</th></tr>')
    for uf, t, sigla, tipo in LINHAS:
        classe = ' class="amostra"' if t == "am" else ""
        celulas = ""
        for est, _ in ESTATS:
            destaque = ' class="media"' if est == "media" else ""
            celulas += f"<td{destaque}>{v[f'{var}_{uf}_{t}_{est}']}</td>"
        linhas.append(f'<tr{classe}><th><i class="cor {uf}"></i>{sigla} · {tipo}</th>{celulas}</tr>')
cabecalho = "".join(f"<th>{rotulo}</th>" for _, rotulo in ESTATS)
tabela_descritiva = f"""<table class="descritiva">
  <colgroup><col style="width:21%"><col style="width:6%">{'<col>' * (len(ESTATS) - 1)}</colgroup>
  <thead><tr><th></th>{cabecalho}</tr></thead>
  <tbody>{''.join(linhas)}</tbody>
</table>"""


# ---------------------------------------------------------------- tabela dos testes
def decisao(rejeita, se_rejeita, se_nao):
    return se_rejeita if rejeita else se_nao


f4, f5, t5 = R["q4_ideb"]["f"], R["q5_salario"]["f"], R["q5_salario"]["t"]
H0 = lambda s: f'<span class="h0">H<sub>0</sub>: {s}</span>'
REJ, NAO = "Rejeita H<sub>0</sub>", "Não rejeita H<sub>0</sub>"
testes = []
for titulo, teste in [('Renda: média municipal (%)', tp), ('IDEB: média', t4), ('Salário: média (SM)', t5)]:
    testes.append(('', titulo, H0('μ<sub>PB</sub> = μ<sub>RN</sub>'),
        f"t aprox. + CPF ({br(teste['gl'], 1)} gl)",
        f"t = {br(teste['t'])}<br>p = {pval(teste['p_valor'])}",
        decisao(teste['rejeita_h0'], f'{REJ}: PB maior' if teste['diferenca'] > 0 else f'{REJ}: RN maior',
                f'{NAO}: evidência insuficiente'), teste['rejeita_h0']))
for titulo, f in [('IDEB: variâncias*', f4), ('Salário: variâncias*', f5)]:
    testes.append(('var-f', titulo, H0('σ²<sub>PB</sub> = σ²<sub>RN</sub>'), 'F clássico (29; 29 gl)',
        f"F = {br(f['f'])}<br>p = {pval(f['p_valor'])}",
        decisao(f['rejeita_h0'], 'Rejeita igualdade*', 'Não rejeita igualdade*'), False))
linhas = []
for classe, o_que, h0, teste, resultado, dec, rejeita in testes:
    classes = " ".join(c for c in (classe, "rejeita" if rejeita else "") if c)
    linhas.append(f'<tr class="{classes}"><td><b>{o_que}</b>{h0}</td><td>{teste}</td>'
                  f'<td>{resultado}</td><td class="decisao">{dec}</td></tr>')
tabela_testes = f"""<table class="testes">
  <colgroup><col style="width:28%"><col style="width:26%"><col style="width:19%"><col style="width:27%"></colgroup>
  <thead><tr><th>Comparação PB × RN</th><th>Teste</th><th>Resultado</th><th>Decisão</th></tr></thead>
  <tbody>{''.join(linhas)}</tbody>
</table>"""


# ---------------------------------------------------------------- gráficos SVG embutidos
def svg_embutido(arquivo, prefixo):
    svg = (RAIZ / "saida" / "graficos" / arquivo).read_text(encoding="utf-8")
    svg = svg[svg.index("<svg"):]  # tira o cabeçalho XML
    svg = re.sub(r'<svg([^>]*?) width="[^"]+" height="[^"]+"', r'<svg\1 class="grafico"', svg, count=1)
    # ids únicos por gráfico (vários SVGs na mesma página não podem repetir id)
    svg = re.sub(r'id="([^"]+)"', rf'id="{prefixo}-\1"', svg)
    svg = re.sub(r'url\(#([^)]+)\)', rf'url(#{prefixo}-\1)', svg)
    svg = re.sub(r'href="#([^"]+)"', rf'href="#{prefixo}-\1"', svg)
    return svg


# ---------------------------------------------------------------- link e QR code das planilhas
link = CFG.get("link_planilhas", "").strip()
if link:
    qr_svg = qrcode.make(link, image_factory=qrcode.image.svg.SvgPathImage, border=0).to_string(encoding="unicode")
    qr_svg = re.sub(r'<svg([^>]*?) width="[^"]+" height="[^"]+"', r"<svg\1", qr_svg, count=1)
    qr = f'<div class="qr">{qr_svg}</div>'
    link_texto = html.escape(link)
else:
    qr = '<div class="qr vazio">QR code<br>do link</div>'
    link_texto = "FALTA O LINK: cole o link da planilha em cartaz/config.json e rode o script de novo."

v.update({
    "renda_dif": br(tp['diferenca']), 'renda_p': pval(tp['p_valor']),
    'salario_p': pval(t5['p_valor']),
    'cpf_pb': br(ic['PB']['fpc'], 3), 'cpf_rn': br(ic['RN']['fpc'], 3),
    "grupo": html.escape(CFG["grupo"]),
    "integrantes": " · ".join(html.escape(nome) for nome in CFG["integrantes"]),
    "tabela_descritiva": tabela_descritiva, "tabela_testes": tabela_testes,
    "grafico_salario": svg_embutido("salario_hist_boxplot.svg", "g1"),
    "grafico_ic": svg_embutido("ic_renda_media.svg", "g2"),
    "grafico_medias": svg_embutido("medias_ic.svg", "g3"),
    "qr": qr, "link_texto": link_texto,
})

pagina = Template((PASTA / "modelo.html").read_text(encoding="utf-8")).substitute(v)
ARQ_HTML = PASTA / "cartaz.html"
ARQ_HTML.write_text(pagina, encoding="utf-8")


# ---------------------------------------------------------------- PDF pelo navegador (Chrome ou Edge)
navegador = next((p for p in NAVEGADORES if p.exists()), None)
if navegador is None:
    sys.exit("Não achei Chrome nem Edge. Abra o cartaz.html no navegador e use Ctrl+P > Salvar como PDF.")

with tempfile.TemporaryDirectory(dir=os.environ.get('PROJETO_TMP')) as perfil:
    base = [str(navegador), "--headless=new", "--disable-gpu", f"--user-data-dir={perfil}",
            "--window-size=1600,2250"]
    if os.environ.get('PROJETO_HEADLESS_COMPAT') == '1':
        base += ['--no-sandbox', '--disable-crash-reporter', '--disable-breakpad']
    dom = subprocess.run(base + ["--dump-dom", ARQ_HTML.as_uri()], capture_output=True, text=True,
                         encoding="utf-8", timeout=120).stdout
    ARQ_A2 = PASTA / "cartaz_A2.pdf"
    subprocess.run(base + ["--no-pdf-header-footer", "--print-to-pdf-no-header", f"--print-to-pdf={ARQ_A2}",
                           ARQ_HTML.as_uri()], capture_output=True, timeout=120, check=True)

avisos = []
m = re.search(r'data-transbordando="([^"]*)"', dom)
if m is None:
    avisos.append("não consegui conferir se o texto coube nos quadrantes")
elif m.group(1):
    avisos.append(f"conteúdo passou da borda nos quadrantes: {html.unescape(m.group(1))}")

# ---------------------------------------------------------------- recortes A4 (2 x 2) e A3 (2 x 1)
a2 = fitz.open(ARQ_A2)
if len(a2) != 1:
    avisos.append(f"o PDF A2 saiu com {len(a2)} páginas (esperado: 1)")
L, A = a2[0].rect.width, a2[0].rect.height


def recortar(destino, quadros):
    novo = fitz.open()
    for x0, y0, x1, y1 in quadros:
        pag = novo.new_page(width=x1 - x0, height=y1 - y0)
        pag.show_pdf_page(pag.rect, a2, 0, clip=fitz.Rect(x0, y0, x1, y1))
    novo.save(destino)


recortar(PASTA / "cartaz_4xA4.pdf", [(0, 0, L / 2, A / 2), (L / 2, 0, L, A / 2),
                                    (0, A / 2, L / 2, A), (L / 2, A / 2, L, A)])
recortar(PASTA / "cartaz_2xA3.pdf", [(0, 0, L, A / 2), (0, A / 2, L, A)])

# ---------------------------------------------------------------- pendências do grupo
if "?" in CFG["grupo"] or any(nome.startswith("Integrante") for nome in CFG["integrantes"]):
    avisos.append("faltam o número do grupo e/ou os nomes dos integrantes (cartaz/config.json)")
if not link:
    avisos.append("falta o link das planilhas (cartaz/config.json); o enunciado exige esse link no cartaz")

print("Cartaz gerado em", PASTA)
for aviso in avisos:
    print("  ATENÇÃO:", aviso)

if avisos and any('borda' in a or 'páginas' in a for a in avisos):
    sys.exit(1)
