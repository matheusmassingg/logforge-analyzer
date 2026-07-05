# LogForge Analyzer 🚀

Bem-vindo ao meu primeiro projeto prático com dados! O **LogForge Analyzer** é um script em Python que faz a "faxina" automática de relatórios de vendas brutos, eliminando linhas vazias e erros do sistema de forma resiliente.

## 💡 O que ele faz:
- **Faxina Automática:** Ignora linhas de erro (`ERROR_LOG`) e espaços vazios.
- **Busca Rápida:** Filtra as vendas por um produto específico via terminal.
- **Exportação:** Salva os dados limpos em um arquivo `.csv` pronto para o Excel.

## 🚀 Como rodar:
- Relatório Geral: `python analyzer.py dados_brutos.txt`
- Filtrar Produto: `python analyzer.py dados_brutos.txt --filtro "Sabão"`
- Exportar para CSV: `python analyzer.py dados_brutos.txt --exportar`

*Projeto desenvolvido para consolidação de fundamentos em Python, Git e Terminal Linux.*
