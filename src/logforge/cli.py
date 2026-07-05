"""Interface de linha de comando do LogForge Analyzer."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from . import __version__
from .exporter import EXPORTADORES
from .parser import ArquivoNaoEncontradoError, ler_vendas
from .report import construir_relatorio, formatar_linha_venda, formatar_resumo

logger = logging.getLogger("logforge")


def _configurar_logging(verbose: bool) -> None:
    nivel = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=nivel, format="[%(levelname)s] %(message)s")


def _construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="logforge",
        description="LogForge Analyzer - CLI de processamento de dados de vendas.",
    )
    parser.add_argument("arquivo", help="Caminho do arquivo de logs brutos.")
    parser.add_argument(
        "-f", "--filtro", default=None, help="Filtra o relatório por nome de produto."
    )
    parser.add_argument(
        "-e", "--exportar", action="store_true", help="Exporta os dados tratados."
    )
    parser.add_argument(
        "--formato",
        choices=sorted(EXPORTADORES.keys()),
        default="csv",
        help="Formato de exportação (usado apenas com --exportar). Padrão: csv.",
    )
    parser.add_argument(
        "-o",
        "--saida",
        default=None,
        help="Caminho do arquivo de saída (padrão: relatorio_limpo.<formato>).",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Mostra detalhes de linhas ignoradas."
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suprime a listagem de vendas no terminal."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def executar(argv: list[str] | None = None) -> int:
    """Ponto de entrada principal. Retorna o código de saída do processo."""
    parser = _construir_parser()
    args = parser.parse_args(argv)
    _configurar_logging(args.verbose)

    try:
        itens = list(ler_vendas(args.arquivo))
    except ArquivoNaoEncontradoError as exc:
        print(f"[ERRO] {exc}")
        return 1

    relatorio = construir_relatorio(itens, filtro=args.filtro)

    print("\n" + "=" * 50)
    print(" LOGFORGE ANALYZER v3.0 ".center(50, " "))
    print("=" * 50)
    if args.filtro:
        print(f"Filtro ativo: buscando por '{args.filtro}'")
    print("-" * 50)

    if not args.quiet:
        for venda in relatorio.vendas_processadas:
            print(formatar_linha_venda(venda))

    print(formatar_resumo(relatorio))

    if args.verbose and relatorio.linhas_ignoradas:
        print("\nLinhas ignoradas:")
        for ignorada in relatorio.linhas_ignoradas:
            print(f"  linha {ignorada.numero}: {ignorada.motivo} -> {ignorada.conteudo!r}")

    if args.exportar:
        if not relatorio.vendas_processadas:
            print("[AVISO] Nenhuma venda válida para exportar.")
        else:
            caminho_saida = args.saida or f"relatorio_limpo.{args.formato}"
            exportador = EXPORTADORES[args.formato]
            try:
                caminho_final = exportador(relatorio.vendas_processadas, caminho_saida)
            except ImportError as exc:
                print(f"[ERRO] {exc}")
                return 1
            print(f"[PROCESSO] Dados exportados para: {caminho_final}")

    return 0


def main() -> None:
    sys.exit(executar())


if __name__ == "__main__":
    main()
