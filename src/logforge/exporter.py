"""Exportação dos dados limpos para CSV, JSON ou Excel."""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path

from .models import Venda

logger = logging.getLogger(__name__)

CABECALHO = ["ID", "PRODUTO", "QUANTIDADE", "PRECO_UNITARIO", "FATURAMENTO_TOTAL"]

# Caracteres que, se estiverem no início de um campo, podem ser interpretados
# como fórmulas por Excel/Sheets ao abrir o CSV (CSV injection / fórmula injection).
_CARACTERES_FORMULA = ("=", "+", "-", "@", "\t", "\r")


def _sanitizar_campo(valor: str) -> str:
    """Prefixa um apóstrofo se o campo começar com caractere de fórmula.

    Isso neutraliza ataques de CSV injection quando o arquivo é aberto em
    programas de planilha, sem alterar o valor visualmente para o usuário.
    """
    if valor and valor.startswith(_CARACTERES_FORMULA):
        return f"'{valor}"
    return valor


def _linha_para_dict(venda: Venda) -> dict[str, str | int | float]:
    return {
        "ID": _sanitizar_campo(venda.id_produto),
        "PRODUTO": _sanitizar_campo(venda.nome_produto),
        "QUANTIDADE": venda.quantidade,
        "PRECO_UNITARIO": round(venda.preco_unitario, 2),
        "FATURAMENTO_TOTAL": venda.faturamento,
    }


def exportar_csv(vendas: list[Venda], caminho_saida: str | Path) -> Path:
    """Exporta as vendas para um arquivo CSV usando o módulo csv padrão."""
    caminho = Path(caminho_saida)
    with caminho.open("w", encoding="utf-8", newline="") as f_out:
        escritor = csv.DictWriter(f_out, fieldnames=CABECALHO, delimiter=";")
        escritor.writeheader()
        for venda in vendas:
            escritor.writerow(_linha_para_dict(venda))
    logger.info("Exportado CSV com %d linhas para %s", len(vendas), caminho)
    return caminho


def exportar_json(vendas: list[Venda], caminho_saida: str | Path) -> Path:
    """Exporta as vendas para um arquivo JSON (lista de objetos)."""
    caminho = Path(caminho_saida)
    dados = [_linha_para_dict(venda) for venda in vendas]
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Exportado JSON com %d linhas para %s", len(vendas), caminho)
    return caminho


def exportar_excel(vendas: list[Venda], caminho_saida: str | Path) -> Path:
    """Exporta as vendas para um arquivo .xlsx usando openpyxl.

    Raises:
        ImportError: se openpyxl não estiver instalado.
    """
    try:
        from openpyxl import Workbook
    except ImportError as exc:  # pragma: no cover - depende de dependência opcional
        raise ImportError(
            "Exportar para Excel requer o pacote opcional 'openpyxl'. "
            "Instale com: pip install logforge-analyzer[excel]"
        ) from exc

    caminho = Path(caminho_saida)
    workbook = Workbook()
    planilha = workbook.active
    planilha.title = "Relatorio"
    planilha.append(CABECALHO)
    for venda in vendas:
        linha = _linha_para_dict(venda)
        planilha.append([linha[campo] for campo in CABECALHO])
    workbook.save(caminho)
    logger.info("Exportado Excel com %d linhas para %s", len(vendas), caminho)
    return caminho


EXPORTADORES = {
    "csv": exportar_csv,
    "json": exportar_json,
    "xlsx": exportar_excel,
}
