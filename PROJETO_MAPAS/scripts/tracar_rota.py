"""
Este script calcula a rota mais curta entre dois pontos em uma cidade, utilizando um grafo viário previamente gerado e 
salvo em um arquivo no formato GraphML. A biblioteca OSMnx é usada para carregar o grafo e identificar os nós mais 
próximos às coordenadas de origem e destino, enquanto a biblioteca NetworkX é utilizada para determinar a menor rota 
com base no peso dos arcos (distância).

O fluxo principal do script inclui:
1. Carregar o grafo viário armazenado localmente em "data/map.graphml".
2. Identificar os nós do grafo mais próximos das coordenadas fornecidas para origem e destino.
3. Calcular a rota mais curta entre os nós de origem e destino com base na distância ("length") dos arcos.
4. Retornar a rota, suas coordenadas geográficas e a distância total em quilômetros.
5. Opcionalmente, exibir um gráfico com a rota traçada.

"""

import os

import networkx as nx
import osmnx as ox


def calcular_rota_mais_curta(origem, destino, exibir_plot=False):
    grafo_path = "data/map.graphml"

    if not os.path.exists(grafo_path):
        raise FileNotFoundError(f"Arquivo '{grafo_path}' não encontrado. Execute 'gerar_dados_mapa()' primeiro.")

    grafo = ox.load_graphml(grafo_path)

    try:
        origem_no = ox.distance.nearest_nodes(grafo, X=origem[1], Y=origem[0])
        destino_no = ox.distance.nearest_nodes(grafo, X=destino[1], Y=destino[0])
    except ValueError as e:
        raise ValueError(f"Erro ao encontrar nós próximos: {e}")

    rota = nx.shortest_path(grafo, origem_no, destino_no, weight="length")
    coordenadas_rota = [(grafo.nodes[node]["y"], grafo.nodes[node]["x"]) for node in rota]

    distancia_metros = sum(
        nx.get_edge_attributes(grafo, "length")[(rota[i], rota[i + 1], 0)]
        for i in range(len(rota) - 1)
    )
    distancia_km = distancia_metros / 1000

    if exibir_plot:
        ox.plot_graph_route(grafo, rota, route_linewidth=3, node_size=0, bgcolor="white")

    return rota, coordenadas_rota, distancia_km
