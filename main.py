import argparse
import requests
import json
import time

def buscar_dou_trf3(inicio, fim, orgao, termos):
    print(f"--- INICIANDO BUSCA REAL: {orgao} ({inicio} a {fim}) ---")
    
    # URL da API de busca da Imprensa Nacional
    url = "https://www.in.gov.br"
    
    # Filtros exatos para o buscador do governo
    # do2 = Seção 2 (Atos de Pessoal)
    query = f'"{orgao}" {termos}'
    
    params = {
        'q': query,
        's': 'do2',
        'publishFrom': inicio,
        'publishTo': fim,
        'limit': 100
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            dados = response.json()
            items = dados.get('jsonArray', [])
            
            if not items:
                print("Nenhum resultado encontrado para este período/órgão.")
                return

            print(f"Sucesso! Encontrados {len(items)} atos no período.")
            print("-" * 60)
            print("DATA | ATO | NOME/CARGO | LOCALIDADE | LINK")
            print("-" * 60)

            for item in items:
                titulo = item.get('title', 'Sem Título')
                data = item.get('pubDate', 'Sem Data')
                url_pdf = "https://www.in.gov.br" + item.get('urlTitle', '')
                
                # Exibe o resultado formatado no log
                print(f"{data} | {titulo} | {url_pdf}")
        else:
            print(f"Erro no servidor do governo: {response.status_code}")
            
    except Exception as e:
        print(f"Erro na conexão: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--inicio')
    parser.add_argument('--fim')
    parser.add_argument('--orgao')
    parser.add_argument('--busca')
    args, unknown = parser.parse_known_args()
    
    # Rodar busca para cada variação de órgão para garantir
    orgaos = ["TRIBUNAL REGIONAL FEDERAL DA 3ª REGIAO", "SJMS", "SJSP"]
    for o in orgaos:
        buscar_dou_trf3(args.inicio, args.fim, o, args.busca)
        time.sleep(2) # Pausa para não ser bloqueado
