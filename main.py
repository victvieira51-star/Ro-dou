import argparse
import requests
from bs4 import BeautifulSoup
import time

def buscar_dou(inicio, fim, busca):
    print(f"--- INICIANDO EXTRAÇÃO REAL: {inicio} até {fim} ---")
    
    # Termos do TRF3 e Cargos
    orgaos = ["TRIBUNAL REGIONAL FEDERAL DA 3", "SJMS", "SJSP"]
    base_url = "https://www.in.gov.br"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    for orgao in orgaos:
        print(f"\nVerificando: {orgao}...")
        params = {
            'q': f'"{orgao}" {busca}',
            's': 'do2',
            'publishFrom': inicio,
            'publishTo': fim,
            'limit': '100'
        }
        
        try:
            res = requests.get(base_url, params=params, headers=headers, timeout=30)
            if res.status_code == 200:
                json_data = res.json()
                items = json_data.get('jsonArray', [])
                
                if not items:
                    print(f" > Nenhum resultado para {orgao} neste período.")
                    continue
                
                print(f" > Sucesso! Encontrados {len(items)} atos.")
                for item in items:
                    data = item.get('pubDate')
                    titulo = item.get('title')
                    url = "https://www.in.gov.br" + item.get('urlTitle')
                    print(f"[{data}] - {titulo}")
                    print(f"      Link: {url}")
            else:
                print(f" > Erro no site do Governo: Status {res.status_code}")
            
            time.sleep(2) # Pausa para evitar bloqueio
        except Exception as e:
            print(f" > Erro de conexão: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--inicio')
    parser.add_argument('--fim')
    parser.add_argument('--secao')
    parser.add_argument('--busca')
    args = parser.parse_args()
    
    buscar_dou(args.inicio, args.fim, args.busca)
