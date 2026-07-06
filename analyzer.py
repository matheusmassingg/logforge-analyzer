#!/usr/bin/env python3
"""Ponto de entrada de compatibilidade.

Mantém o comando original `python analyzer.py dados_brutos.txt ...` funcionando
após a refatoração do código para o pacote `src/logforge`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from logforge.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
