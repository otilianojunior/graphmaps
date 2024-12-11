def calcular_preco_km():
    preco_combustivel = 6  # R$/litro
    consumo_veiculo = 10  # km/litro
    margem_lucro = 0.50  # R$/km
    return (preco_combustivel / consumo_veiculo) + margem_lucro


def calcular_preco_corrida(distancia_km, preco_km, aplicar_taxa_noturna=False,
                           aplicar_taxa_pico=False, aplicar_taxa_excesso_corridas=False,
                           aplicar_taxa_limpeza=False, aplicar_taxa_cancelamento=False):
    # Taxas fixas
    TAXA_NOTURNA = 5  # R$
    TAXA_MANUTENCAO = 2  # R$
    TAXA_PICO_PERCENTUAL = 20  # %
    TAXA_EXCESSO_CORRIDAS = 3  # R$
    TAXA_LIMPEZA = 10  # R$ (valor fictício para exemplo)
    TAXA_CANCELAMENTO = 7  # R$ (valor fictício para exemplo)

    # Cálculo básico: preço por km vezes distância
    preco_basico = preco_km * distancia_km

    # Adicionar taxas baseadas nos parâmetros booleanos
    adicional_pico = (preco_basico * (TAXA_PICO_PERCENTUAL / 100)) if aplicar_taxa_pico else 0
    taxa_noturna = TAXA_NOTURNA if aplicar_taxa_noturna else 0
    taxa_excesso_corridas = TAXA_EXCESSO_CORRIDAS if aplicar_taxa_excesso_corridas else 0
    taxa_limpeza = TAXA_LIMPEZA if aplicar_taxa_limpeza else 0
    taxa_cancelamento = TAXA_CANCELAMENTO if aplicar_taxa_cancelamento else 0

    # Somar todas as taxas adicionais
    preco_total = (
            preco_basico
            + taxa_noturna
            + TAXA_MANUTENCAO
            + adicional_pico
            + taxa_excesso_corridas
            + taxa_limpeza
            + taxa_cancelamento
    )

    return preco_total
