import csv
import json

from logforge.exporter import exportar_csv, exportar_json
from logforge.models import Venda


def test_exportar_csv_gera_cabecalho_e_linhas(tmp_path):
    vendas = [Venda("001", "Sabão", 2, 5.0)]
    caminho = exportar_csv(vendas, tmp_path / "saida.csv")

    with caminho.open(encoding="utf-8") as f:
        leitor = csv.DictReader(f, delimiter=";")
        linhas = list(leitor)

    assert linhas[0]["PRODUTO"] == "Sabão"
    assert linhas[0]["FATURAMENTO_TOTAL"] == "10.0"


def test_exportar_csv_sanitiza_campo_com_formula(tmp_path):
    vendas = [Venda("=CMD", "=SOMA(A1:A2)", 1, 1.0)]
    caminho = exportar_csv(vendas, tmp_path / "saida.csv")

    conteudo = caminho.read_text(encoding="utf-8")
    assert "'=CMD" in conteudo
    assert "'=SOMA" in conteudo


def test_exportar_json_gera_lista_valida(tmp_path):
    vendas = [Venda("001", "Detergente", 3, 2.5)]
    caminho = exportar_json(vendas, tmp_path / "saida.json")

    dados = json.loads(caminho.read_text(encoding="utf-8"))
    assert dados[0]["PRODUTO"] == "Detergente"
    assert dados[0]["FATURAMENTO_TOTAL"] == 7.5


def test_exportar_csv_sem_vendas_gera_apenas_cabecalho(tmp_path):
    caminho = exportar_csv([], tmp_path / "vazio.csv")
    conteudo = caminho.read_text(encoding="utf-8").strip()
    assert conteudo == "ID;PRODUTO;QUANTIDADE;PRECO_UNITARIO;FATURAMENTO_TOTAL"
