"""Agregação de métricas e formatação do relatório de vendas."""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import Venda
from .parser import LinhaIgnorada


@dataclass(slots=True)
class Relatorio:
    """Resultado agregado do processamento de um arquivo de vendas."""

    vendas_processadas: list[Venda] = field(default_factory=list)
    linhas_ignoradas: list[LinhaIgnorada] = field(default_factory=list)

    @property
    def total_itens_vendidos(self) -> int:
        return sum(v.quantidade for v in self.vendas_processadas)

    @property
    def faturamento_bruto_total(self) -> float:
        return round(sum(v.faturamento for v in self.vendas_processadas), 2)

    @property
    def ticket_medio_por_unidade(self) -> float:
        if self.total_itens_vendidos == 0:
            return 0.0
        return round(self.faturamento_bruto_total / self.total_itens_vendidos, 2)

    @property
    def total_linhas_ignoradas(self) -> int:
        return len(self.linhas_ignoradas)


def construir_relatorio(itens: list[Venda | LinhaIgnorada], filtro: str | None = None) -> Relatorio:
    """Separa itens parseados em vendas válidas (aplicando filtro) e linhas ignoradas."""
    relatorio = Relatorio()
    for item in itens:
        if isinstance(item, LinhaIgnorada):
            relatorio.linhas_ignoradas.append(item)
        elif item.combina_com_filtro(filtro):
            relatorio.vendas_processadas.append(item)
    return relatorio


def formatar_linha_venda(venda: Venda) -> str:
    """Formata uma linha de venda para exibição no terminal."""
    nome_truncado = venda.nome_produto[:18]
    total = f"{venda.faturamento:.2f}"
    return f"-> OK | {nome_truncado:<18} | Qtd: {venda.quantidade:<2} | Total: R$ {total}"


def formatar_resumo(relatorio: Relatorio) -> str:
    """Formata o resumo final do relatório para exibição no terminal."""
    linhas = [
        "=" * 50,
        " RELATÓRIO DE PERFORMANCE ".center(50, " "),
        "=" * 50,
        f"Total de itens vendidos  : {relatorio.total_itens_vendidos}",
        f"Faturamento Bruto Total  : R$ {relatorio.faturamento_bruto_total:.2f}",
        f"Ticket Médio por Unidade : R$ {relatorio.ticket_medio_por_unidade:.2f}",
        f"Linhas ignoradas         : {relatorio.total_linhas_ignoradas}",
        "=" * 50,
    ]
    return "\n".join(linhas)
