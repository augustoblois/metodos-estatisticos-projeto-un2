# Execute dentro da pasta do projeto; requer Python 3.12 e Chrome ou Edge.
$ErrorActionPreference = 'Stop'
python -m venv .venv
if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar ambiente Python' }
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar dependências' }
foreach ($etapa in @('analise/analise.py', 'analise/gerar_relatorio.py', 'cartaz/montar_cartaz.py', 'falas/gerar_falas.py', 'analise/verificar.py')) {
    & .\.venv\Scripts\python.exe -X utf8 $etapa
    if ($LASTEXITCODE -ne 0) { throw "Falha na etapa $etapa" }
}
