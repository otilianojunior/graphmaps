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
