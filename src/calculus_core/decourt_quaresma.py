from calculus_core.models import Estaca, MetodoCalculo, PerfilSPT
from calculus_core.utils import normalizar_tipo_estaca, normalizar_tipo_solo

coef_K_decourt_quaresma_1978 = {
    'argila': {'deslocamento': 120, 'escavada': 100},
    'silte_argiloso': {'deslocamento': 200, 'escavada': 120},
    'silte_arenoso': {'deslocamento': 250, 'escavada': 140},
    'areia': {'deslocamento': 400, 'escavada': 200},
}
coef_alfa_decourt_quaresma_1996 = {
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
coef_beta_decourt_quaresma_1996 = {
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


class DecourtQuaresma(MetodoCalculo):
    """
    Classe para calcular a capacidade de carga de estacas
     pelo método de Décourt-Quaresma (1978).
    """

    def __init__(self, coef_K: dict, coef_alfa: dict, coef_beta: dict):
        """
        Inicializa a classe com os coeficientes necessários para o cálculo.

        Args:
            coef_K: Coeficientes K (kPa) por tipo de solo e processo de
                construção.
            coef_alfa: Coeficientes alfa por tipo de solo e tipo de estaca.
            coef_beta: Coeficientes beta por tipo de solo e tipo de estaca.
        """
        self._coef_K = coef_K
        self._coef_alfa = coef_alfa
        self._coef_beta = coef_beta

    @staticmethod
    def calcular_Np(perfil_spt: PerfilSPT, cota_assentamento: int):
        """
            Calcula o Np_SPT médio na cota especificada,
            considerando a média do metro acima e abaixo.

        Args:
            perfil_spt: Lista de tuplas (N_SPT, tipo_solo).
            cota: Cota para calcular o N_SPT médio.

        Returns:
            float: N_SPT médio na cota especificada.
        """

        if cota_assentamento not in perfil_spt:
            raise ValueError('Cota assentamento inválida para o perfil SPT.')

        medida_cota_assentamento = perfil_spt.obter_medida(cota_assentamento)

        medida_cota_acima = perfil_spt.obter_medida(
            cota_assentamento - 1, aprox=True
        )
        medida_cota_abaixo = perfil_spt.obter_medida(cota_assentamento + 1)

        return (
            medida_cota_assentamento.N_SPT
            + medida_cota_acima.N_SPT
            + medida_cota_abaixo.N_SPT
        ) / 3

    @staticmethod
    def calcular_Nl(perfil_spt: PerfilSPT, cota_assentamento: int):
        """
        Calcula o Nl_SPT médio ao longo do fuste da estaca,
        desconsiderando as cotas utilizadas no Np.
        Args:
            perfil_spt: Lista de tuplas (N_SPT, tipo_solo).
            cota_assentamento: Cota de assentamento para encontrar os indices,
            para desconsiderar no cálculo.

        Returns:
            float: N_SPT médio ao longo do fuste da estaca.
        """

        Nl = 0
        n = 0
        cota_acima = cota_assentamento - 1

        if cota_acima not in perfil_spt:
            return 0

        for i in range(1, cota_acima):
            Nl += perfil_spt.obter_medida(i).N_SPT
            n += 1
        return Nl / n if n > 0 else 0

    @staticmethod
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

    @staticmethod
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

    def coef_K(self, tipo_solo: str, processo_construcao: str) -> float:
        """
        Obtém o coeficiente K para o tipo de solo e processo de construção.

        Args:
            tipo_solo: Tipo de solo (argila, silte, areia).
            processo_construcao: Processo de construção
                (deslocamento, escavada, etc).

        Returns:
            float: Coeficiente K correspondente.
        """
        tipo_solo = normalizar_tipo_solo(tipo_solo, 'décourt_quaresma', 'K')

        if tipo_solo not in self._coef_K:
            raise ValueError(f'Tipo de solo inválido: {tipo_solo}')
        if processo_construcao not in self._coef_K[tipo_solo]:
            raise ValueError(
                f'Processo de construção inválido: {processo_construcao}'
            )

        return self._coef_K[tipo_solo][processo_construcao]

    def coef_alfa(self, tipo_solo: str, tipo_estaca: str) -> float:
        """
        Obtém o coeficiente alfa para o tipo de solo e tipo de estaca.

        Args:
            tipo_solo: Tipo de solo (argila, silte, areia).
            tipo_estaca: Tipo de estaca
            (cravada, escavada, hélice contínua, etc.).

        Returns:
            float: Coeficiente alfa correspondente.
        """
        tipo_solo = normalizar_tipo_solo(tipo_solo, 'décourt_quaresma', 'alfa')
        tipo_estaca = normalizar_tipo_estaca(tipo_estaca, 'décourt_quaresma')

        if tipo_solo not in self._coef_alfa:
            raise ValueError(f'Tipo de solo inválido: {tipo_solo}')
        if tipo_estaca not in self._coef_alfa[tipo_solo]:
            raise ValueError(f'Tipo de estaca inválido: {tipo_estaca}')

        return self._coef_alfa[tipo_solo][tipo_estaca]

    def coef_beta(self, tipo_solo: str, tipo_estaca: str) -> float:
        """
        Obtém o coeficiente beta para o tipo de solo e tipo de estaca.

        Args:
            tipo_solo: Tipo de solo (argila, silte, areia).
            tipo_estaca: Tipo de estaca
            (cravada, escavada, hélice contínua, etc.).

        Returns:
            float: Coeficiente beta correspondente.
        """
        tipo_solo = normalizar_tipo_solo(tipo_solo, 'décourt_quaresma', 'beta')
        tipo_estaca = normalizar_tipo_estaca(tipo_estaca, 'décourt_quaresma')

        if tipo_solo not in self._coef_beta:
            raise ValueError(f'Tipo de solo inválido: {tipo_solo}')
        if tipo_estaca not in self._coef_beta[tipo_solo]:
            raise ValueError(f'Tipo de estaca inválido: {tipo_estaca}')

        return self._coef_beta[tipo_solo][tipo_estaca]

    def calcular(self, perfil_spt: PerfilSPT, estaca: Estaca) -> dict:
        """
        Calcula a capacidade de carga de estacas
        pelo método de Décourt-Quaresma (1978).

        Args:
            perfil_spt: Perfil SPT contendo as medidas de N_SPT e tipo de solo.
            estaca: Objeto Estaca contendo informações sobre a estaca.

        Returns:
            dict: Dicionário contendo as resistências de ponta,
            resistência lateral parcial,
            resistência lateral total e total da estaca.
        """

        # Cálculo da Resistência de Ponta (Rp)
        medida_cota_assentamento = perfil_spt.obter_medida(estaca.comprimento)
        Np = self.calcular_Np(
            perfil_spt, medida_cota_assentamento.profundidade
        )
        K = self.coef_K(
            medida_cota_assentamento.tipo_solo, estaca.processo_construcao
        )
        alfa = self.coef_alfa(medida_cota_assentamento.tipo_solo, estaca.tipo)

        Rp = self.calcular_Rp(alfa, Np, K, estaca.area_ponta())

        # Cálculo da Resistência Lateral (Rl)
        Nl = self.calcular_Nl(
            perfil_spt, medida_cota_assentamento.profundidade
        )
        beta = self.coef_beta(medida_cota_assentamento.tipo_solo, estaca.tipo)

        Rl = self.calcular_Rl(
            beta, Nl, estaca.perimetro(), medida_cota_assentamento.profundidade
        )

        return {
            'resistencia_ponta': Rp,
            'resistencia_lateral': Rl,
            'resistencia_lateral_total': Rl,
            'capacidade_total': Rp + Rl,
        }


decort_quaresma_1978_revisado = DecourtQuaresma(
    coef_K=coef_K_decourt_quaresma_1978,
    coef_alfa=coef_alfa_decourt_quaresma_1996,
    coef_beta=coef_beta_decourt_quaresma_1996,
)
