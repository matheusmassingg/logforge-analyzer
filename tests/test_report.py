from logforge.models import Venda
from logforge.parser import LinhaIgnorada
from logforge.report import construir_relatorio, formatar_linha_venda, formatar_resumo


def _venda(nome="Produto", qtd=2, preco=10.0, id_="001"):
    return Venda(id_produto=id_, nome_produto=nome, quantidade=qtd, preco_unitario=preco)


def test_totais_do_relatorio():
    itens = [_venda(qtd=2, preco=10.0), _venda(qtd=3, preco=5.0)]
    relatorio = construir_relatorio(itens)
    assert relatorio.total_itens_vendidos == 5
    assert relatorio.faturamento_bruto_total == 35.0
    assert relatorio.ticket_medio_por_unidade == 7.0


def test_relatorio_vazio_nao_gera_divisao_por_zero():
    relatorio = construir_relatorio([])
    assert relatorio.total_itens_vendidos == 0
    assert relatorio.ticket_medio_por_unidade == 0.0


def test_filtro_aplica_case_insensitive():
    itens = [_venda(nome="Sabão em Pó"), _venda(nome="Detergente")]
    relatorio = construir_relatorio(itens, filtro="sabão")
    assert len(relatorio.vendas_processadas) == 1
    assert relatorio.vendas_processadas[0].nome_produto == "Sabão em Pó"


def test_linhas_ignoradas_sao_contabilizadas():
    itens = [_venda(), LinhaIgnorada(numero=2, conteudo="x", motivo="teste")]
    relatorio = construir_relatorio(itens)
    assert relatorio.total_linhas_ignoradas == 1
    assert len(relatorio.vendas_processadas) == 1


def test_formatar_linha_venda_contem_nome_e_total():
    venda = _venda(nome="Sabão", qtd=2, preco=5.0)
    linha = formatar_linha_venda(venda)
    assert "Sabão" in linha
    assert "10.00" in linha


def test_formatar_resumo_contem_metricas():
    relatorio = construir_relatorio([_venda(qtd=2, preco=5.0)])
    resumo = formatar_resumo(relatorio)
    assert "Faturamento Bruto Total" in resumo
    assert "10.00" in resumo
