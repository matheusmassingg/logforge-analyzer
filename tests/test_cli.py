from pathlib import Path

from logforge.cli import executar

FIXTURE = str(Path(__file__).parent / "fixtures" / "amostra_pequena.txt")


def test_cli_retorna_0_em_execucao_normal(capsys):
    codigo = executar([FIXTURE])
    saida = capsys.readouterr().out
    assert codigo == 0
    assert "RELATÓRIO DE PERFORMANCE" in saida


def test_cli_retorna_1_para_arquivo_inexistente(capsys):
    codigo = executar(["nao_existe.txt"])
    saida = capsys.readouterr().out
    assert codigo == 1
    assert "ERRO" in saida


def test_cli_exportar_gera_arquivo(tmp_path, capsys):
    destino = tmp_path / "saida.csv"
    codigo = executar([FIXTURE, "--exportar", "--saida", str(destino)])
    assert codigo == 0
    assert destino.exists()


def test_cli_filtro_reduz_resultados(capsys):
    executar([FIXTURE, "--filtro", "Detergente"])
    saida = capsys.readouterr().out
    assert "Detergente" in saida
    assert "Amaciante" not in saida
