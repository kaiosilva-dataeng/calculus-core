import math


class Estaca:
    def __init__(
        self,
        tipo,
        processo_construcao,
        formato,
        secao_transversal,
        comprimento,
    ):
        if formato not in ['circular', 'quadrada']:
            raise ValueError(
                'Formato de estaca deve ser "circular" ou "quadrada".'
            )
        self.tipo = tipo
        self.processo_construcao = processo_construcao
        self.formato = formato
        self.secao_transversal = secao_transversal
        self.comprimento = comprimento

    def area_ponta(self):
        if self.formato == 'circular':
            raio = self.secao_transversal / 2
            return math.pi * (raio**2)
        elif self.formato == 'quadrada':
            largura = self.secao_transversal
            return largura**2

    def perimetro(self):
        if self.formato == 'circular':
            raio = self.secao_transversal / 2
            return 2 * math.pi * raio
        elif self.formato == 'quadrada':
            largura = self.secao_transversal
            return 4 * largura

    def area_lateral(self):
        if self.formato == 'circular':
            raio = self.secao_transversal / 2
            return math.pi * raio * self.comprimento
        elif self.formato == 'quadrada':
            largura = self.secao_transversal
            return largura * self.comprimento


def calcular_Np(perfil_spt, cota_asentamento):
    """
    Calcula o Np_SPT médio na cota especificada,
    considerando a média do metro acima e abaixo.

    Args:
        perfil_spt: Lista de tuplas (N_SPT, tipo_solo).
        cota: Cota para calcular o N_SPT médio.

    Returns:
        float: N_SPT médio na cota especificada.
    """
    index_cota_asentamento = cota_asentamento - 1  # Index baseado em 0

    if index_cota_asentamento < 0 or index_cota_asentamento >= len(perfil_spt):
        raise ValueError('Cota asentamento inválida para o perfil SPT.')

    Nspt_cota_asentamento = perfil_spt[index_cota_asentamento][0]

    if index_cota_asentamento - 1 < 0:
        Nspt_cota_acima = perfil_spt[index_cota_asentamento][0]
    elif index_cota_asentamento - 1 >= 0:
        Nspt_cota_acima = perfil_spt[index_cota_asentamento - 1][0]

    if index_cota_asentamento + 1 >= len(perfil_spt):
        Nspt_cota_abaixo = 50
    elif index_cota_asentamento + 1 < len(perfil_spt):
        Nspt_cota_abaixo = perfil_spt[index_cota_asentamento + 1][0]

    return (Nspt_cota_asentamento + Nspt_cota_acima + Nspt_cota_abaixo) / 3


def normalizar_tipo_solo(tipo_solo, metodo):
    """
    Normaliza o tipo de solo para um formato padrão.

    Args:
        tipo_solo: Tipo de solo como string.

    Returns:
        str: Tipo de solo normalizado.
    """
    if metodo == 'decourt_quaresma':
        tipo_solo = tipo_solo.lower().replace(' ', '_').replace('-', '_')
        if tipo_solo in ['argila', 'argila_arenosa', 'argila_areno_siltosa']:
            return 'argila'
        elif tipo_solo in ['silte', 'silte_argiloso', 'silte_arenoso']:
            return 'silte'
        elif tipo_solo in ['areia', 'areia_argilosa', 'areia_areno_siltosa']:
            return 'areia'
    return tipo_solo


def calcular_decourt_quaresma(
    perfil_spt,
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
            'helice_continua': 0.3,
            'raiz': 0.85,
            'injetada': 1,
        },
        'silte': {
            'cravada': 1,
            'escavada': 0.6,
            'escavada_bentonita': 0.6,
            'helice_continua': 0.3,
            'raiz': 0.6,
            'injetada': 1,
        },
        'areia': {
            'cravada': 1,
            'escavada': 0.5,
            'escavada_bentonita': 0.5,
            'helice_continua': 0.3,
            'raiz': 0.5,
            'injetada': 1,
        },
    }

    coef_beta = {  # noqa
        'argila': {
            'cravada': 1,
            'escavada': 0.8,
            'escavada_bentonita': 0.9,
            'helice_continua': 1,
            'raiz': 1.5,
            'injetada': 3,
        },
        'silte': {
            'cravada': 1,
            'escavada': 0.65,
            'escavada_bentonita': 0.75,
            'helice_continua': 1,
            'raiz': 1.5,
            'injetada': 3,
        },
        'areia': {
            'cravada': 1,
            'escavada': 0.5,
            'escavada_bentonita': 0.6,
            'helice_continua': 1,
            'raiz': 1.5,
            'injetada': 3,
        },
    }
    # Cálculo da Resistência de Ponta (Rp)

    cota_asentamento = estaca.comprimento
    Np = calcular_Np(perfil_spt, cota_asentamento)
    tipo_solo_ponta = perfil_spt[cota_asentamento - 1][1]
    tipo_solo_ponta = normalizar_tipo_solo(tipo_solo_ponta, 'decourt_quaresma')

    K = coef_K[tipo_solo_ponta][estaca.processo_construcao]

    alfa = coef_alfa[tipo_solo_ponta][estaca.tipo]
    q_p = alfa * K * Np * estaca.area_ponta()

    return {
        'resistencia_ponta': q_p,
        'resistencia_lateral': 0,
        'capacidade_total': 0,
    }


if __name__ == '__main__':
    # Exemplo de uso
    resultado = calcular_decourt_quaresma(
        perfil_spt=[
            (3, 'areia_argilosa'),
            (3, 'areia_argilosa'),
            (5, 'areia_argilosa'),
            (6, 'argila_arenosa'),
            (8, 'argila_arenosa'),
            (13, 'argila_arenosa'),
            (17, 'argila_arenosa'),
            (25, 'argila_arenosa'),
            (27, 'argila_areno_siltosa'),
            (32, 'argila_areno_siltosa'),
            (36, 'argila_areno_siltosa'),
        ],
        estaca=Estaca(
            tipo='cravada',
            processo_construcao='deslocamento',
            formato='quadrada',
            secao_transversal=0.3,
            comprimento=11,
        ),
    )
    print(resultado)
