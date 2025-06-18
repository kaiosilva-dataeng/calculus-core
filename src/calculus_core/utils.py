from collections.abc import Callable

from calculus_core.models import Estaca, PerfilSPT


def normalizar_tipo_solo(tipo_solo: str, metodo: str) -> str:
    """
    Normaliza o tipo de solo para um formato padrão.

    Args:
        tipo_solo: Tipo de solo como string.

    Returns:
        str: Tipo de solo normalizado.
    """
    tipo_solo = tipo_solo.lower().replace(' ', '_').replace('-', '_')
    if metodo == 'décourt_quaresma':
        if tipo_solo in ['argila', 'argila_arenosa', 'argila_areno_siltosa']:
            return 'argila'
        elif tipo_solo in ['silte', 'silte_argiloso', 'silte_arenoso']:
            return 'silte'
        elif tipo_solo in ['areia', 'areia_argilosa', 'areia_areno_siltosa']:
            return 'areia'
    return tipo_solo


def normalizar_tipo_estaca(tipo_estaca: str, metodo: str) -> str:
    """
    Normaliza o tipo de estaca para um formato padrão.

    Args:
        tipo_estaca: Tipo de estaca como string.

    Returns:
        str: Tipo de estaca normalizado.
    """
    tipo_estaca = tipo_estaca.lower().replace(' ', '_').replace('-', '_')
    if metodo == 'décourt_quaresma':
        if tipo_estaca in [
            'cravada',
            'franki',
            'pré_moldada',
            'metálica',
            'ômega',
        ]:
            return 'cravada'
        elif tipo_estaca in [
            'escavada',
            'escavada_bentonita',
            'hélice_contínua',
            'raiz',
            'injetada',
        ]:
            return tipo_estaca
    return tipo_estaca


def calcular_capacidade_estaca(
    metodo_calculo: Callable[[PerfilSPT, Estaca], dict],
    perfil_spt: PerfilSPT,
    tipo_estaca: str,
    processo_construcao: str,
    formato: str,
    secao_transversal: float,
):
    """
    Calcula a capacidade de carga de uma estaca metro a metro
    usando o método especificado.

    Args:
        metodo_calculo (callable): Método de cálculo a ser utilizado.
        perfil_spt: Perfil SPT da estaca.
        tipo_estaca: Tipo de estaca (cravada, franki, pré_moldada, metálica,
            ômega, escavada, escavada_bentonita, hélice_contínua, raiz,
            injetada).
        processo_construcao: escavada, deslocamento.
        formato: Formato da estaca (circular, quadrada).
        secao_transversal: Seção transversal da estaca em metros.

    Returns:
        dict: Resistências de ponta, lateral e total em kN.
    """

    resultado: list[dict] = []
    for i in range(1, len(perfil_spt) + 1):
        estaca = Estaca(
            tipo=tipo_estaca,
            processo_construcao=processo_construcao,
            formato=formato,
            secao_transversal=secao_transversal,
            comprimento=i,
        )

        resultado_estaca = metodo_calculo(
            perfil_spt,
            estaca,
        )
        resultado.append(
            {
                'cota': i,
                'resistencia_ponta': resultado_estaca['resistencia_ponta'],
                'resistencia_lateral': resultado_estaca['resistencia_lateral'],
                'resistencia_lateral_total': resultado_estaca[
                    'resistencia_lateral_total'
                ],
                'capacidade_total': resultado_estaca['capacidade_total'],
            }
        )
    return resultado
