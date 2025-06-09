import requests
from fastapi import HTTPException
from typing import Dict, Any

class NaturalistAPIClient:
    def __init__(self):
        self.base_url = "https://api.inaturalist.org/v1"
        self.gbif_url = "https://api.gbif.org/v1"
        self.wikipedia_url = "https://pt.wikipedia.org/w/api.php"
    
    def buscar_dados_especie(self, scientific_name: str) -> Dict[str, Any]:
        """
        Busca dados de espécies no iNaturalist e GBIF com fallbacks robustos.
        Retorna um dicionário com taxonomia, links e descrição.
        """
        try:
            # 1. Busca no iNaturalist
            inat_response = requests.get(
                f"{self.base_url}/taxa",
                params={
                    "q": scientific_name,
                    "is_active": "true",
                    "rank": "species",
                    "per_page": 1
                },
                timeout=10
            )
            inat_data = inat_response.json().get("results", [{}])[0]
            
            if not inat_data.get("id"):
                raise ValueError("Espécie não encontrada no iNaturalist")

            # 2. Busca taxonomia no GBIF
            gbif_response = requests.get(
                f"{self.gbif_url}/species/match",
                params={"name": scientific_name, "strict": "true"},
                timeout=10
            )
            gbif_data = gbif_response.json()

            # 3. Montagem da taxonomia com fallbacks
            taxonomy = {
                "reino": gbif_data.get("kingdom") or inat_data.get("iconic_taxon_name", "Desconhecido"),
                "filo": gbif_data.get("phylum", "Desconhecido"),
                "classe": gbif_data.get("class", "Desconhecido"),
                "ordem": gbif_data.get("order", "Desconhecido"),
                "familia": gbif_data.get("family") or inat_data.get("ancestry", "").split("/")[-2:][0] or "Desconhecido",
                "genero": gbif_data.get("genus") or scientific_name.split()[0],
                "especie": gbif_data.get("species") or scientific_name
            }

            # 4. Retorno padronizado
            return {
                "taxonomy": taxonomy,
                "inaturalist": inat_data,
                "inaturalist_link": f"https://www.inaturalist.org/taxa/{inat_data['id']}",
                "wikipedia_url": inat_data.get("wikipedia_url", ""),
                "description": ""  # Campo vazio para ser preenchido posteriormente
            }

        except Exception as e:
            print(f"Erro na API para {scientific_name}: {str(e)}")
            # Fallback mínimo para fungos (ajuste conforme seu domínio)
            return {
                "taxonomy": {
                    "reino": "Fungi",
                    "filo": "Desconhecido",
                    "classe": "Desconhecido",
                    "ordem": "Desconhecido",
                    "familia": "Desconhecido",
                    "genero": scientific_name.split()[0],
                    "especie": scientific_name
                },
                "inaturalist": {},
                "inaturalist_link": "",
                "wikipedia_url": "",
                "description": "Descrição não disponível."
            }

# Instância global do cliente (mantida para compatibilidade)
api_client = NaturalistAPIClient()