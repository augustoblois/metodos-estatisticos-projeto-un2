# -*- coding: utf-8 -*-
"""
Gera um PDF de falas para cada integrante do grupo.

Lê os nomes de cartaz/config.json e as imagens do cartaz pronto (cartaz/cartaz_A2.pdf).
Gera, dentro da pasta falas/:
  falas (Nome Sobrenome).pdf   um por integrante, em A5 (lê bem no celular e imprime bem)

A ordem de quem fala segue a ordem dos nomes no config.json: o 1º nome faz a parte 1
(quadrante superior esquerdo), o 2º a parte 2, e assim por diante.

Como rodar (PowerShell, dentro da pasta projeto-un2), depois de gerar o cartaz:
    python falas\\gerar_falas.py
"""
import base64
import html
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from string import Template

import fitz  # PyMuPDF: tira as imagens do cartaz e confere os PDFs

PASTA = Path(__file__).resolve().parent  # projeto-un2/falas
RAIZ = PASTA.parent
CFG = json.loads((RAIZ / "cartaz" / "config.json").read_text(encoding="utf-8-sig"))
CARTAZ = RAIZ / "cartaz" / "cartaz_A2.pdf"
NAVEGADORES = [Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
               Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")]
PALAVRAS_POR_MINUTO = 140  # ritmo calmo de apresentação

# ---------------------------------------------------------------- conteúdo
# {p1} a {p4} viram o primeiro nome de quem faz cada parte; {todos} vira a lista dos primeiros nomes.
# Os números são os do cartaz (saida/resultados.json, semente 20261116).
from conteudo import PARTES, COMUM, DICAS


# ---------------------------------------------------------------- integrantes
nomes = [n.strip() for n in CFG["integrantes"]]
if len(nomes) != len(PARTES):
    sys.exit(f"O roteiro está dividido em {len(PARTES)} partes, e o config.json tem {len(nomes)} integrantes. "
             "Ajuste a divisão em falas/gerar_falas.py (lista PARTES).")
primeiros = [n.split()[0] for n in nomes]
lista = ", ".join(primeiros[:-1]) + " e " + primeiros[-1]
NOMES = {f"p{i + 1}": p for i, p in enumerate(primeiros)} | {"todos": lista}


def texto(t):
    return html.escape(t.format_map(NOMES))


def segundos_de_fala(parte):
    palavras = sum(len(t.format_map(NOMES).split()) for _, t in parte["fala"])
    return round(palavras / PALAVRAS_POR_MINUTO * 60 / 15) * 15  # arredonda para 15 s


def tempo(segundos):
    minutos, resto = divmod(segundos, 60)
    return f"cerca de {minutos} min" + (f" {resto} s" if resto else "")


# ---------------------------------------------------------------- imagens do cartaz
if not CARTAZ.exists():
    sys.exit("Não achei o cartaz/cartaz_A2.pdf. Rode antes: python cartaz\\montar_cartaz.py")
cartaz = fitz.open(CARTAZ)
pagina = cartaz[0]
L, A = pagina.rect.width, pagina.rect.height
QUADROS = [fitz.Rect(0, 0, L / 2, A / 2), fitz.Rect(L / 2, 0, L, A / 2),
           fitz.Rect(0, A / 2, L / 2, A), fitz.Rect(L / 2, A / 2, L, A)]


def imagem(dpi, clip=None):
    jpeg = pagina.get_pixmap(dpi=dpi, clip=clip).tobytes("jpeg", jpg_quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(jpeg).decode()


miniatura = imagem(32)

# ---------------------------------------------------------------- montagem das páginas
navegador = next((p for p in NAVEGADORES if p.exists()), None)
if navegador is None:
    sys.exit("Não achei Chrome nem Edge para gerar os PDFs.")

modelo = Template((PASTA / "modelo_falas.html").read_text(encoding="utf-8"))
tempos = [segundos_de_fala(p) for p in PARTES]  # o total é a soma das partes já arredondadas
with tempfile.TemporaryDirectory(dir=os.environ.get('PROJETO_TMP')) as temp:
    temp = Path(temp)
    for i, (nome, parte) in enumerate(zip(nomes, PARTES)):
        mapa = "".join(f'<span class="q q{k + 1}{" voce" if k == i else ""}"><b>{k + 1}</b></span>'
                       for k in range(len(PARTES)))
        destaque = ['class="voce"' if k == i else "" for k in range(len(PARTES))]
        ordem = "".join(
            f'<li {destaque[k]}><span class="n">{k + 1}</span>'
            f'<span><b>{html.escape(primeiros[k])}</b> · {html.escape(p["curto"])}</span></li>'
            for k, p in enumerate(PARTES))
        if i == 0:
            entrada = f"Você abre a apresentação. No fim da sua fala, passe a palavra para {primeiros[1]}."
        elif i == len(PARTES) - 1:
            entrada = f"Você fala depois de {primeiros[i - 1]} e fecha a apresentação, abrindo para perguntas."
        else:
            entrada = (f"Você fala depois de {primeiros[i - 1]}. No fim da sua fala, passe a palavra para "
                       f"{primeiros[i + 1]}.")
        fala = "".join(f'<div class="bloco"><p class="gesto">→ {texto(g)}</p><p class="texto">{texto(t)}</p></div>'
                       for g, t in parte["fala"])
        conceitos = "".join(f"<dt>{texto(c)}</dt><dd>{texto(e)}</dd>" for c, e in parte["conceitos"])
        numeros = "".join(f"<tr><th>{texto(r)}</th><td>{texto(v)}</td></tr>" for r, v in parte["numeros"])
        perguntas = "".join(f'<div class="pergunta"><p class="p">“{texto(p)}”</p><p class="r">{texto(r)}</p></div>'
                            for p, r in parte["perguntas"])
        pagina_html = modelo.substitute(
            nome=html.escape(nome), parte=i + 1, total_partes=len(PARTES), tema=html.escape(parte["tema"]),
            quadrante=parte["quadrante"], miniatura=miniatura, mapa=mapa, ordem=ordem,
            tempo=tempo(tempos[i]), tempo_total=tempo(sum(tempos)), entrada=html.escape(entrada),
            fala=fala, conceitos=conceitos, numeros=numeros, perguntas=perguntas,
            comum="".join(f"<li>{texto(c)}</li>" for c in COMUM),
            dicas="".join(f"<li>{texto(d)}</li>" for d in DICAS),
            quadro=imagem(150, QUADROS[i]))
        roteiro = f"# Fala de {nome}\n\nParte {i+1}: {parte['tema']}\n\n"
        for gesto, trecho in parte['fala']:
            roteiro += f"*{gesto}*\n\n{trecho.format_map(NOMES)}\n\n"
        roteiro += "Memorize: barras → caixa → PB concentrada → RN disperso → atípicos → renda municipal → limites.\n" if 'Luy' in nome else ''
        (PASTA / f'fala_simples_{nome.split()[0]}.md').write_text(roteiro, encoding='utf-8')
        arq_html = PASTA / f"falas_{i + 1}.html"
        arq_html.write_text(pagina_html, encoding="utf-8")
        arq_pdf = PASTA / f"falas ({nome}).pdf"
        extras = ['--no-sandbox', '--disable-crash-reporter', '--disable-breakpad'] if os.environ.get('PROJETO_HEADLESS_COMPAT') == '1' else []
        subprocess.run([str(navegador), "--headless=new", "--disable-gpu", *extras, f"--user-data-dir={temp / 'perfil'}",
                        "--no-pdf-header-footer", "--print-to-pdf-no-header", f"--print-to-pdf={arq_pdf}",
                        arq_html.as_uri()], capture_output=True, timeout=120, check=True)
        paginas = len(fitz.open(arq_pdf))
        print(f"{arq_pdf.name}: parte {i + 1}, {paginas} páginas, fala de {tempo(tempos[i])}")
