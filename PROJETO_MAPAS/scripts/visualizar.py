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

