from calculus_core.models import Estaca, PerfilSPT
from calculus_core.utils import normalizar_tipo_estaca, normalizar_tipo_solo


def calcular_Np(perfil_spt: PerfilSPT, cota_asentamento: int):
    """
    Calcula o Np_SPT médio na cota especificada,
    considerando a média do metro acima e abaixo.

    Args:
        perfil_spt: Lista de tuplas (N_SPT, tipo_solo).
        cota: Cota para calcular o N_SPT médio.

    Returns:
        float: N_SPT médio na cota especificada.
    """

    if cota_asentamento not in perfil_spt:
        raise ValueError('Cota asentamento inválida para o perfil SPT.')

    medida_cota_asentamento = perfil_spt.obter_medida(cota_asentamento)

    medida_cota_acima = perfil_spt.obter_medida(
        cota_asentamento - 1, aprox=True
    )
    medida_cota_abaixo = perfil_spt.obter_medida(cota_asentamento + 1)

    return (
        medida_cota_asentamento.N_SPT
        + medida_cota_acima.N_SPT
        + medida_cota_abaixo.N_SPT
    ) / 3


def calcular_Rp(alfa, Np, K, area_ponta):
    """
    Calcula a resistência de ponta da estaca.

    Args:
        alfa: Coeficiente alfa do tipo de solo.
        Np: N_SPT médio na cota de assentamento.
        K: Coeficiente K do tipo de solo.
        area_ponta: Área da ponta da estaca.

    Returns:
        float: Resistência de ponta em kN.
    """
    return alfa * K * Np * area_ponta


def calcular_Nl(perfil_spt: PerfilSPT, cota_asentamento: int):
    """
    Calcula o Nl_SPT médio ao longo do fuste da estaca,
    desconsiderando as cotas utilizadas no Np.
    Args:
        perfil_spt: Lista de tuplas (N_SPT, tipo_solo).
        cota_asentamento: Cota de assentamento para encontrar os indices,
        para desconsiderar no cálculo.

    Returns:
        float: N_SPT médio ao longo do fuste da estaca.
    """

    Nl = 0
    n = 0
    cota_acima = cota_asentamento - 1

    if cota_acima not in perfil_spt:
        return 0

    for i in range(1, cota_acima):
        Nl += perfil_spt.obter_medida(i).N_SPT
        n += 1
    return Nl / n if n > 0 else 0


def calcular_Rl(beta, Nl, perimetro, cota=1):
    """
    Calcula a resistência lateral da estaca.

    Args:
        beta: Coeficiente beta do tipo de solo.
        Nl: N_SPT médio ao longo do fuste da estaca.
        perimetro: Perímetro da seção transversal da estaca.
        cota: Cota até onde calcular a resistência lateral.

    Returns:
        float: Resistência lateral em kN.
    """
    return beta * 10 * (Nl / 3 + 1) * perimetro * cota


def calcular_decourt_quaresma(
    perfil_spt: PerfilSPT,
    estaca: Estaca,
):
    """
    Calcula a capacidade de carga de uma estaca
     pelo método de Décourt-Quaresma (1978).

    Args:
        perfil_spt: Perfil SPT da estaca.
        tipo_estaca: Tipo de estaca (escavada, deslocamento, etc.).
        secao_transversal_estaca: Seção transversal da estaca em metros.
        comprimento_estaca: Comprimento da estaca em metros.

    Returns:
        dict: resistências de ponta, lateral e total em kN.
    """

    coef_K = {
        'argila': {'deslocamento': 120, 'escavada': 100},
        'silte_argiloso': {'deslocamento': 200, 'escavada': 120},
        'silte_arenoso': {'deslocamento': 250, 'escavada': 140},
        'areia': {'deslocamento': 400, 'escavada': 200},
    }
    coef_alfa = {
        'argila': {
            'cravada': 1,
            'escavada': 0.85,
            'escavada_bentonita': 0.85,
            'hélice_contínua': 0.3,
            'raiz': 0.85,
            'injetada': 1,
        },
        'silte': {
            'cravada': 1,
            'escavada': 0.6,
            'escavada_bentonita': 0.6,
            'hélice_contínua': 0.3,
            'raiz': 0.6,
            'injetada': 1,
        },
        'areia': {
            'cravada': 1,
            'escavada': 0.5,
            'escavada_bentonita': 0.5,
            'hélice_contínua': 0.3,
            'raiz': 0.5,
            'injetada': 1,
        },
    }

    coef_beta = {  # noqa
        'argila': {
            'cravada': 1,
            'escavada': 0.8,
            'escavada_bentonita': 0.9,
            'hélice_contínua': 1,
            'raiz': 1.5,
            'injetada': 3,
        },
        'silte': {
            'cravada': 1,
            'escavada': 0.65,
            'escavada_bentonita': 0.75,
            'hélice_contínua': 1,
            'raiz': 1.5,
            'injetada': 3,
        },
        'areia': {
            'cravada': 1,
            'escavada': 0.5,
            'escavada_bentonita': 0.6,
            'hélice_contínua': 1,
            'raiz': 1.5,
            'injetada': 3,
        },
    }
    # Cálculo da Resistência de Ponta (Rp)

    medida_cota_asentamento = perfil_spt.obter_medida(estaca.comprimento)
    cota_asentamento = medida_cota_asentamento.profundidade
    Np = calcular_Np(perfil_spt, cota_asentamento)
    tipo_solo_ponta = normalizar_tipo_solo(
        medida_cota_asentamento.tipo_solo, 'décourt_quaresma'
    )

    K = coef_K[tipo_solo_ponta][estaca.processo_construcao]

    tipo_estaca = normalizar_tipo_estaca(estaca.tipo, 'décourt_quaresma')
    alfa = coef_alfa[tipo_solo_ponta][tipo_estaca]

    Rp = calcular_Rp(alfa, Np, K, estaca.area_ponta())

    # Cálculo da Resistência Lateral (Rl)
    Nl = calcular_Nl(perfil_spt, cota_asentamento)
    tipo_solo_lateral = normalizar_tipo_solo(
        medida_cota_asentamento.tipo_solo, 'décourt_quaresma'
    )
    beta = coef_beta[tipo_solo_lateral][tipo_estaca]
    Rl = calcular_Rl(beta, Nl, estaca.perimetro(), cota_asentamento)

    return {
        'resistencia_ponta': Rp,
        'resistencia_lateral': Rl,
        'resistencia_lateral_total': Rl,
        'capacidade_total': Rp + Rl,
    }
