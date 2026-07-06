"""Leitura e parsing do arquivo de dados brutos."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from .models import Venda

logger = logging.getLogger(__name__)

CAMPOS_ESPERADOS = 4
PREFIXO_IGNORAR = "ERROR_LOG"


class ArquivoNaoEncontradoError(FileNotFoundError):
    """Lançado quando o arquivo de entrada não existe."""


@dataclass(slots=True)
class LinhaIgnorada:
    """Guarda o motivo de uma linha ter sido ignorada, para relatórios verbosos."""

    numero: int
    conteudo: str
    motivo: str


def _tentar_detectar_encoding(caminho: Path) -> str:
    """Tenta ler o arquivo como utf-8; recua para latin-1 se falhar.

    Muitos arquivos de log/relatório gerados no Brasil vêm em latin-1 (cp1252),
    então evitamos que acentos quebrem o processamento inteiro.
    """
    amostra = caminho.read_bytes()[:4096]
    try:
        amostra.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        logger.warning(
            "Não foi possível decodificar %s como utf-8; usando latin-1.", caminho
        )
        return "latin-1"


def _parsear_linha(numero: int, linha_bruta: str) -> Venda | LinhaIgnorada:
    """Converte uma linha de texto em um objeto Venda ou um registro de linha ignorada."""
    linha = linha_bruta.strip()

    if not linha:
        return LinhaIgnorada(numero, linha_bruta, "linha vazia")

    if linha.startswith(PREFIXO_IGNORAR):
        return LinhaIgnorada(numero, linha_bruta, "linha de log de erro")

    partes = linha.split(";")
    if len(partes) < CAMPOS_ESPERADOS:
        return LinhaIgnorada(
            numero, linha_bruta, f"esperado {CAMPOS_ESPERADOS} campos, encontrado {len(partes)}"
        )

    id_prod, nome_prod, qtd_str, preco_str = (p.strip() for p in partes[:CAMPOS_ESPERADOS])

    if not id_prod or not nome_prod:
        return LinhaIgnorada(numero, linha_bruta, "id ou nome do produto vazio")

    if not qtd_str or not preco_str:
        return LinhaIgnorada(numero, linha_bruta, "quantidade ou preço vazio")

    try:
        quantidade = int(qtd_str)
    except ValueError:
        return LinhaIgnorada(numero, linha_bruta, f"quantidade inválida: {qtd_str!r}")

    try:
        preco = float(preco_str)
    except ValueError:
        return LinhaIgnorada(numero, linha_bruta, f"preço inválido: {preco_str!r}")

    if quantidade <= 0:
        return LinhaIgnorada(numero, linha_bruta, f"quantidade não positiva: {quantidade}")

    if preco <= 0:
        return LinhaIgnorada(numero, linha_bruta, f"preço não positivo: {preco}")

    return Venda(
        id_produto=id_prod, nome_produto=nome_prod, quantidade=quantidade, preco_unitario=preco
    )


def ler_vendas(caminho_arquivo: str | Path) -> Iterator[Venda | LinhaIgnorada]:
    """Lê o arquivo linha a linha e produz Venda ou LinhaIgnorada para cada uma.

    Usa um generator para não carregar arquivos grandes inteiros em memória.

    Raises:
        ArquivoNaoEncontradoError: se o caminho não existir.
    """
    caminho = Path(caminho_arquivo)
    if not caminho.exists():
        raise ArquivoNaoEncontradoError(f"Arquivo {caminho} não encontrado.")

    encoding = _tentar_detectar_encoding(caminho)

    with caminho.open("r", encoding=encoding) as arquivo:
        for numero, linha in enumerate(arquivo, start=1):
            yield _parsear_linha(numero, linha)
