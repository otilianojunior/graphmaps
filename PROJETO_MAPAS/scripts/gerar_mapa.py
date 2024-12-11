"""
Este script tem como objetivo gerar dados geográficos relacionados à cidade de Vitória da Conquista, Brasil, utilizando
a biblioteca OSMnx para obter o grafo da cidade e a biblioteca Geopy para realizar geocodificação reversa (converter 
coordenadas geográficas em nomes de ruas e bairros). 

O fluxo principal do script inclui:
1. Verificar se os dados do grafo e das localizações já existem em arquivos armazenados localmente.
2. Caso os dados não existam, criar o grafo da cidade com base na malha viária para veículos (tipo "drive").
3. Processar cada nó (node) do grafo, extraindo latitude, longitude, nome da rua e bairro.
4. Utilizar multithreading para acelerar o processamento dos nós do grafo.
5. Salvar os dados processados em um arquivo CSV para uso posterior.

"""


import os
from concurrent.futures import ThreadPoolExecutor

import osmnx as ox
import pandas as pd
from geopy.geocoders import Nominatim


def obter_nome_rua_bairro(coordenada):
    geolocator = Nominatim(user_agent="mapa_interativo")
    location = geolocator.reverse(coordenada, language='pt', exactly_one=True)

    if location:
        address = location.raw.get("address", {})
        return address.get("road", "Desconhecido"), address.get("suburb", "Desconhecido")
    return "Desconhecido", "Desconhecido"


def processar_no(node, grafo, nodes_data):
    latitude = grafo.nodes[node]["y"]
    longitude = grafo.nodes[node]["x"]
    nome_rua, bairro = obter_nome_rua_bairro((latitude, longitude))

    nodes_data["node_id"].append(node)
    nodes_data["latitude"].append(latitude)
    nodes_data["longitude"].append(longitude)
    nodes_data["nome_rua"].append(nome_rua)
    nodes_data["bairro"].append(bairro)


def gerar_dados_mapa():
    if os.path.exists("data/map.graphml") and os.path.exists("data/localizacoes.csv"):
        print("Arquivos existentes encontrados. Carregando dados...")
        return

    cidade = "Vitória da Conquista, Brasil"
    print("Gerando novos dados do mapa...")
    grafo = ox.graph_from_place(cidade, network_type="drive")
    ox.save_graphml(grafo, filepath="data/map.graphml")

    nodes_data = {"node_id": [], "latitude": [], "longitude": [], "nome_rua": [], "bairro": []}

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda node: processar_no(node, grafo, nodes_data), grafo.nodes)

    pd.DataFrame(nodes_data).to_csv("data/localizacoes.csv", index=False)
    print("Dados do mapa gerados e localizações salvas.")
