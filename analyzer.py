import os
import argparse

def analisar_dados(caminho_arquivo, filtro=None, exportar=False):
    if not os.path.exists(caminho_arquivo):
        print(f"[ERRO] Arquivo {caminho_arquivo} não encontrado.")
        return

    print("\n" + "="*50)
    print("   LOGFORGE ANALYZER v2.0 - PRODUÇÃO   ")
    print("="*50)
    if filtro:
        print(f"Filtro Ativo: Aplicando busca por '{filtro}'")
        print("-"*50)
    
    total_faturamento = 0.0
    itens_processados = 0
    linhas_ignoradas = 0
    linhas_limpas = []

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        for num_linha, linha in enumerate(arquivo, 1):
            linha = linha.strip()
            
            if not linha or linha.startswith("ERROR_LOG"):
                linhas_ignoradas += 1
                continue
                
            partes = linha.split(";")
            
            try:
                id_prod = partes[0].strip()
                nome_prod = partes[1].strip()
                quantidade_str = partes[2].strip()
                preco_unitario_str = partes[3].strip()
                
                if not quantidade_str or not preco_unitario_str:
                    linhas_ignoradas += 1
                    continue
                    
                qty = int(quantidade_str)
                preco = float(preco_unitario_str)
                
                if filtro and filtro.lower() not in nome_prod.lower():
                    continue

                faturamento_linha = qty * preco
                total_faturamento += faturamento_linha
                itens_processados += qty
                
                linhas_limpas.append(f"{id_prod};{nome_prod};{qty};{preco};{faturamento_linha}\n")
                print(f"-> OK | {nome_prod[:18]:<18} | Qtd: {qty:<2} | Total: R$ {faturamento_linha:.2f}")
                
            except (ValueError, IndexError):
                linhas_ignoradas += 1
                continue

    print("="*50)
    print("           RELATÓRIO DE PERFORMANCE            ")
    print("="*50)
    print(f"Total de itens vendidos : {itens_processados}")
    print(f"Faturamento Bruto Total : R$ {total_faturamento:.2f}")
    if itens_processados > 0:
        print(f"Ticket Médio por Unidade: R$ {(total_faturamento / itens_processados):.2f}")
    print("="*50)

    if exportar and linhas_limpas:
        arquivo_saida = "relatorio_limpo.csv"
        with open(arquivo_saida, "w", encoding="utf-8") as f_out:
            f_out.write("ID;PRODUTO;QUANTIDADE;PRECO_UNITARIO;FATURAMENTO_TOTAL\n")
            f_out.writelines(linhas_limpas)
        print(f"[PROCESSO] Dados limpos exportados para: {arquivo_saida}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LogForge Analyzer - CLI de Processamento de Dados.")
    parser.add_argument("arquivo", help="Caminho do arquivo de logs brutos.")
    parser.add_argument("-f", "--filtro", help="Filtra o relatório por nome de produto.", default=None)
    parser.add_argument("-e", "--exportar", help="Exporta os dados tratados para CSV.", action="store_true")
    
    args = parser.parse_args()
    analisar_dados(args.arquivo, args.filtro, args.exportar)
