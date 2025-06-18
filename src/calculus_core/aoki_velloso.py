from calculus_core.models import Estaca, PerfilSPT
from calculus_core.utils import normalizar_tipo_estaca, normalizar_tipo_solo


def obter_fatores_F1_F2(
    fatores_f1_f2: dict, tipo_estaca: str, diametro_estaca: float | None = None
):
    """
    Busca e calcula os fatores F1 e F2 para um dado tipo de estaca.
    """
    if tipo_estaca not in fatores_f1_f2:
        raise ValueError(f"Tipo de estaca '{tipo_estaca}' não reconhecido.")

    dados_fator = fatores_f1_f2[tipo_estaca]
    valor_f1 = dados_fator['F1']
    func_f2 = dados_fator['F2']

    if callable(valor_f1):
        if diametro_estaca is None:
            raise ValueError(
                (
                    f'Diâmetro da estaca é necessário '
                    f'para calcular F1 para estaca {tipo_estaca}.'
                )
            )
        f1_calculado = valor_f1(diametro_estaca)
    else:
        # Se não for uma função, é um número simples
        f1_calculado = valor_f1

    # Calcula F2 usando o valor de F1 já resolvido
    f2_calculado = func_f2(f1_calculado)

    return f1_calculado, f2_calculado


def calcular_Rp(K, Np, f1, area_ponta):
    """
    Calcula a resistência de ponta da estaca.

    Args:
        K: Coeficiente K do tipo de solo.
        Np: N_SPT na cota de apoio da ponta da estaca.
        f1: Fator F1 calculado para o tipo de estaca.
        area_ponta: Área da ponta da estaca.

    Returns:
        float: Resistência de ponta em kN.
    """
    return (K * Np) / f1 * area_ponta


def calcular_Rl_parcial(alfa, K, Nl, f2, perimetro, espessura_camada=1):
    """
    Calcula a resistência lateral parcial da estaca.

    Args:
        alfa: Coeficiente alfa do tipo de solo.
        K: Coeficiente K do tipo de solo.
        Nl: N_SPT medio na camada de solo lateral.
        f2: Fator F2 calculado para o tipo de estaca.
        perimetro: Perímetro da seção transversal da estaca.
        espessura_camada: Espessura da camada de solo em metros.

    Returns:
        float: Resistência lateral parcial em kN.
    """
    return perimetro * espessura_camada * (alfa * K * Nl) / f2


def calcular_aoki_velloso_1975(
    perfil_spt: PerfilSPT,
    estaca: Estaca,
):
    """Calcula a capacidade de carga de estacas segundo Aoki e Velloso (1975).
    Args:
        perfil_spt (PerfilSPT): Objeto representando Perfil SPT do solo.
        estaca (Estaca): Objeto representando a estaca.
    Returns:
        dict: Dicionário com as resistências de ponta, lateral e total.
    """

    coeficientes_aoki_velloso = {
        'areia': {'k_kpa': 1000, 'alpha_perc': 1.4},
        'areia_siltosa': {'k_kpa': 800, 'alpha_perc': 2.0},
        'areia_silto_argilosa': {'k_kpa': 0.70, 'alpha_perc': 2.4},
        'areia_argilosa': {'k_kpa': 600, 'alpha_perc': 3.0},
        'areia_argilo_siltosa': {'k_kpa': 500, 'alpha_perc': 2.8},
        'silte': {'k_kpa': 400, 'alpha_perc': 3.0},
        'silte_arenoso': {'k_kpa': 550, 'alpha_perc': 2.2},
        'silte_areno_argiloso': {'k_kpa': 450, 'alpha_perc': 2.8},
        'silte_argiloso': {'k_kpa': 230, 'alpha_perc': 3.4},
        'silte_argilo_arenoso': {'k_kpa': 250, 'alpha_perc': 3.0},
        'argila': {'k_kpa': 200, 'alpha_perc': 6.0},
        'argila_arenosa': {'k_kpa': 350, 'alpha_perc': 2.4},
        'argila_areno_siltosa': {'k_kpa': 300, 'alpha_perc': 2.8},
        'argila_siltosa': {'k_kpa': 220, 'alpha_perc': 4.0},
        'argila_silto_arenosa': {'k_kpa': 330, 'alpha_perc': 3.0},
    }
    fatores_f1_f2 = {
        'franki': {'F1': 2.50, 'F2': lambda f1: 2 * f1},
        'metálica': {'F1': 1.75, 'F2': lambda f1: 2 * f1},
        'pré_moldada': {
            'F1': lambda D: 1 + (D / 0.8),
            'F2': lambda f1: 2 * f1,
        },
        'escavada': {'F1': 3.00, 'F2': lambda f1: 2 * f1},
        'raiz': {'F1': 2.00, 'F2': lambda f1: 2 * f1},
        'hélice_contínua': {'F1': 2.00, 'F2': lambda f1: 2 * f1},
        'ômega': {'F1': 2.00, 'F2': lambda f1: 2 * f1},
    }
    # Cálculo da Resistência de Ponta (Rp)

    medida_cota_asentamento = perfil_spt.obter_medida(estaca.comprimento)
    Np = medida_cota_asentamento.N_SPT
    tipo_solo_ponta = medida_cota_asentamento.tipo_solo
    tipo_solo_ponta = normalizar_tipo_solo(
        tipo_solo_ponta, 'aoki_velloso_1975'
    )
    K = coeficientes_aoki_velloso[tipo_solo_ponta]['k_kpa']

    tipo_estaca = normalizar_tipo_estaca(estaca.tipo, 'aoki_velloso_1975')
    f1, f2 = obter_fatores_F1_F2(
        fatores_f1_f2, tipo_estaca, estaca.secao_transversal
    )

    Rp = calcular_Rp(K, Np, f1, estaca.area_ponta())

    # Cálculo da Resistência Lateral (Rl)
    Rl = 0
    Rl_parcial = 0
    for cota in range(1, medida_cota_asentamento.profundidade + 1):
        Nl = perfil_spt.obter_medida(cota).N_SPT
        tipo_solo_lateral = perfil_spt.obter_medida(cota).tipo_solo
        K = coeficientes_aoki_velloso[tipo_solo_lateral]['k_kpa']
        alfa = coeficientes_aoki_velloso[tipo_solo_lateral]['alpha_perc'] / 100
        Rl_parcial = calcular_Rl_parcial(
            alfa, K, Nl, f2, estaca.perimetro(), espessura_camada=1
        )
        Rl += Rl_parcial

    return {
        'resistencia_ponta': Rp,
        'resistencia_lateral': Rl_parcial,
        'resistencia_lateral_total': Rl,
        'capacidade_total': Rp + Rl,
    }
