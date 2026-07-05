from pathlib import Path

import pytest

from logforge.models import Venda
from logforge.parser import ArquivoNaoEncontradoError, LinhaIgnorada, ler_vendas

FIXTURE = Path(__file__).parent / "fixtures" / "amostra_pequena.txt"


def test_arquivo_inexistente_levanta_erro():
    with pytest.raises(ArquivoNaoEncontradoError):
        list(ler_vendas("caminho/que/nao/existe.txt"))


def test_linha_valida_e_parseada_corretamente():
    resultados = list(ler_vendas(FIXTURE))
    vendas = [r for r in resultados if isinstance(r, Venda)]
    primeira = vendas[0]
    assert primeira.id_produto == "001"
    assert primeira.nome_produto == "Sabão em Pó"
    assert primeira.quantidade == 10
    assert primeira.preco_unitario == 5.50
    assert primeira.faturamento == 55.0


def test_linha_error_log_e_ignorada():
    resultados = list(ler_vendas(FIXTURE))
    ignoradas = [r for r in resultados if isinstance(r, LinhaIgnorada)]
    motivos = [i.motivo for i in ignoradas]
    assert any("log de erro" in m for m in motivos)


def test_linha_vazia_e_ignorada():
    resultados = list(ler_vendas(FIXTURE))
    ignoradas = [r for r in resultados if isinstance(r, LinhaIgnorada)]
    assert any(i.motivo == "linha vazia" for i in ignoradas)


def test_quantidade_nao_numerica_e_ignorada():
    resultados = list(ler_vendas(FIXTURE))
    ignoradas = [r for r in resultados if isinstance(r, LinhaIgnorada)]
    assert any("quantidade inválida" in i.motivo for i in ignoradas)


def test_quantidade_negativa_e_ignorada():
    resultados = list(ler_vendas(FIXTURE))
    ignoradas = [r for r in resultados if isinstance(r, LinhaIgnorada)]
    assert any("quantidade não positiva" in i.motivo for i in ignoradas)


def test_preco_zero_e_ignorado():
    resultados = list(ler_vendas(FIXTURE))
    ignoradas = [r for r in resultados if isinstance(r, LinhaIgnorada)]
    assert any("preço não positivo" in i.motivo for i in ignoradas)


def test_preco_vazio_e_ignorado():
    resultados = list(ler_vendas(FIXTURE))
    ignoradas = [r for r in resultados if isinstance(r, LinhaIgnorada)]
    assert any(i.motivo == "quantidade ou preço vazio" for i in ignoradas)
