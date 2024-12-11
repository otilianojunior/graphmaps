"""
O código que você compartilhou é responsável por criar um mapa interativo utilizando a biblioteca folium. Esse mapa exibe uma rota entre dois pontos, incluindo informações sobre a origem e o destino. Vamos analisar as funcionalidades:

Função criar_mapa_interativo: A função recebe parâmetros que incluem:

rota: Informações sobre a rota (não utilizadas diretamente no código).
coordenadas_rota: Lista de coordenadas (latitude e longitude) que formam a rota.
distancia_km: Distância da rota em quilômetros.
origem_info e destino_info: Informações sobre a origem e destino, como nome da rua e bairro.
output_path: Caminho para salvar o arquivo HTML do mapa gerado.
Validação de coordenadas: Antes de gerar o mapa, o código verifica se há coordenadas suficientes (pelo menos duas) para criar a rota. Caso contrário, ele lança uma exceção.

Inicialização do mapa: O mapa é criado com a biblioteca folium, sendo centrado na coordenada de origem (primeiro item da lista coordenadas_rota), com um zoom inicial de 14.

Rota: Uma linha (PolyLine) é desenhada no mapa representando a rota, com uma descrição da distância da rota que aparece ao passar o mouse sobre ela.

Marcadores de Origem e Destino:

O marcador de origem é colocado na primeira coordenada da rota, com ícone verde e um popup exibindo o nome da rua e o bairro.
O marcador de destino é colocado na última coordenada da rota, com ícone vermelho e popup similar com as informações de rua e bairro.
Salvar o mapa: O mapa é salvo em um arquivo HTML no caminho especificado pelo parâmetro output_path.
"""



import folium


def criar_mapa_interativo(rota, coordenadas_rota, distancia_km, origem_info, destino_info,
                          output_path="rota_interativa.html"):
    if not coordenadas_rota or len(coordenadas_rota) < 2:
        raise ValueError("Coordenadas insuficientes para criar o mapa.")

    # Inicializa o mapa centralizado no ponto de origem
    mapa = folium.Map(location=coordenadas_rota[0], zoom_start=14)

    # Adiciona a rota ao mapa com a descrição da distância
    folium.PolyLine(
        locations=coordenadas_rota,
        color='blue',
        weight=4,
        opacity=0.7,
        tooltip=f"Distância da rota: {distancia_km:.2f} km"
    ).add_to(mapa)

    # Adiciona marcador de origem com detalhes de rua e bairro
    folium.Marker(
        coordenadas_rota[0],
        popup=(
            f"<b>Origem</b><br>"
            f"Rua: {origem_info['nome_rua']}<br>"
            f"Bairro: {origem_info['bairro']}"
        ),
        icon=folium.Icon(color="green", icon="play", prefix="fa")
    ).add_to(mapa)

    # Adiciona marcador de destino com detalhes de rua e bairro
    folium.Marker(
        coordenadas_rota[-1],
        popup=(
            f"<b>Destino</b><br>"
            f"Rua: {destino_info['nome_rua']}<br>"
            f"Bairro: {destino_info['bairro']}"
        ),
        icon=folium.Icon(color="red", icon="stop", prefix="fa")
    ).add_to(mapa)

    # Salva o mapa em um arquivo HTML
    mapa.save(output_path)
    # print(f"Mapa interativo salvo como '{output_path}'. Abra este arquivo no navegador para visualizar a rota.")

