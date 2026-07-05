"""Modelos de dados usados pelo LogForge Analyzer."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Venda:
    """Representa uma única linha de venda já validada e limpa.

    Attributes:
        id_produto: Identificador do produto (string, pode ter zeros à esquerda).
        nome_produto: Nome do produto.
        quantidade: Quantidade vendida (inteiro positivo).
        preco_unitario: Preço unitário (float positivo).
    """

    id_produto: str
    nome_produto: str
    quantidade: int
    preco_unitario: float

    @property
    def faturamento(self) -> float:
        """Faturamento total da linha (quantidade * preço unitário)."""
        return round(self.quantidade * self.preco_unitario, 2)

    def combina_com_filtro(self, filtro: str | None) -> bool:
        """Retorna True se o produto satisfaz o filtro de nome (case-insensitive)."""
        if not filtro:
            return True
        return filtro.lower() in self.nome_produto.lower()
