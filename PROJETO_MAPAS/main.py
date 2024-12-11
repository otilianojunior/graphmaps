import os

import pandas as pd

from scripts.gerar_mapa import gerar_dados_mapa
from scripts.tracar_rota import calcular_rota_mais_curta
from scripts.valor_corrida import calcular_preco_corrida, calcular_preco_km
from scripts.visualizar import criar_mapa_interativo


def escolher_pontos_aleatorios():
    # Verificar se o arquivo de localizações existe
    if not os.path.exists("data/localizacoes.csv"):
        raise FileNotFoundError(
            "Arquivo 'data/localizacoes.csv' não encontrado. Execute 'gerar_dados_mapa()' primeiro."
        )

    # Carregar o CSV com as localizações
    df_nodes = pd.read_csv("data/localizacoes.csv")

    # Filtrar locais onde o bairro não é "Desconhecido"
    df_nodes_filtrado = df_nodes[df_nodes["bairro"] != "Desconhecido"]

    # Verificar se há localizações válidas
    if df_nodes_filtrado.empty:
        raise ValueError("Não há locais com bairros válidos para selecionar.")

    # Escolher aleatoriamente a origem e o destino entre locais com bairros válidos
    origem = df_nodes_filtrado.sample(n=1).iloc[0]
    destino = df_nodes_filtrado.sample(n=1).iloc[0]

    # Garantir que a origem e o destino sejam diferentes
    while origem["node_id"] == destino["node_id"]:
        destino = df_nodes_filtrado.sample(n=1).iloc[0]

    # Extrair as informações necessárias
    origem_coord = (origem["latitude"], origem["longitude"])
    destino_coord = (destino["latitude"], destino["longitude"])

    origem_info = {
        "coordenadas": origem_coord,
        "nome_rua": origem["nome_rua"],
        "bairro": origem["bairro"],
    }

    destino_info = {
        "coordenadas": destino_coord,
        "nome_rua": destino["nome_rua"],
        "bairro": destino["bairro"],
    }

    return origem_info, destino_info


def main():
    # Gerar dados do mapa se necessário
    gerar_dados_mapa()

    # Escolher pontos de origem e destino aleatórios
    origem_info, destino_info = escolher_pontos_aleatorios()
    print(
        f"Origem escolhida: {origem_info['coordenadas']} - Rua: {origem_info['nome_rua']} - Bairro: {origem_info['bairro']}")
    print(
        f"Destino escolhido: {destino_info['coordenadas']} - Rua: {destino_info['nome_rua']} - Bairro: {destino_info['bairro']}")

    # Calcular a rota entre origem e destino
    rota, coordenadas_rota, distancia_km = calcular_rota_mais_curta(
        origem_info["coordenadas"],
        destino_info["coordenadas"],
        exibir_plot=True
    )
    #AQUI ROTA NÓS
    print(f"Rota calculada: {coordenadas_rota}")
    print(f"Distância total: {distancia_km:.2f} km")

    # Cálculo do preço por km
    preco_km = calcular_preco_km()

    # Parâmetros booleanos para aplicar taxas
    aplicar_taxa_noturna = True
    aplicar_taxa_pico = False
    aplicar_taxa_excesso_corridas = True
    aplicar_taxa_limpeza = False
    aplicar_taxa_cancelamento = False

    # Calcular o preço total da corrida
    preco_total = calcular_preco_corrida(
        distancia_km,
        preco_km,
        aplicar_taxa_noturna,
        aplicar_taxa_pico,
        aplicar_taxa_excesso_corridas,
        aplicar_taxa_limpeza,
        aplicar_taxa_cancelamento,
    )

    print(f"Preço total da corrida: R${preco_total:.2f}")

    # Criar e salvar o mapa interativo
    criar_mapa_interativo(
        rota=rota,
        coordenadas_rota=coordenadas_rota,
        distancia_km=distancia_km,
        origem_info=origem_info,
        destino_info=destino_info,
        output_path="rota_interativa.html"
    )


if __name__ == "__main__":
    main()
