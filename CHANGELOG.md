# Changelog

## [3.0.0]

### Alterado (breaking)
- Código reorganizado do script único `analyzer.py` para o pacote `src/logforge`
  (`models`, `parser`, `report`, `exporter`, `cli`).
- `analyzer.py` na raiz agora é um wrapper de compatibilidade que chama `logforge.cli.main`.

### Adicionado
- Suporte a exportação em JSON e Excel (`--formato csv|json|xlsx`), além do CSV original.
- Flag `-o/--saida` para customizar o caminho do arquivo exportado.
- Flag `-v/--verbose` para listar o motivo de cada linha ignorada.
- Flag `-q/--quiet` para suprimir a listagem linha a linha no terminal.
- Flag `--version`.
- Detecção automática de encoding (utf-8 com fallback para latin-1).
- Validação de quantidade/preço não positivos.
- Sanitização contra CSV injection (fórmulas iniciadas por `= + - @`).
- Suíte de testes com `pytest` (parser, relatório, exportação e CLI).
- CI no GitHub Actions (lint com `ruff`, type check com `mypy`, testes em 3 versões de Python).
- `pyproject.toml` com metadados de pacote, entry point `logforge` e dependências opcionais.

### Corrigido
- Divisão por zero no ticket médio quando não há itens processados (já existia proteção,
  mantida e testada explicitamente agora).
- Tratamento de erro deixou de ser um `except` genérico silencioso.

## [2.1.0] (versão original)
- Script único `analyzer.py` com leitura, filtro e exportação básica para CSV.
