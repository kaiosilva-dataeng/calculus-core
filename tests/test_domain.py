"""
Core Domain Tests

Essential tests for the domain model entities and value objects.
"""

import math

import pytest

from calculus_core.domain.model import Estaca, MedidaSPT, PerfilSPT
from calculus_core.domain.value_objects import (
    CoeficienteSolo,
    ResultadoCalculo,
    TipoSolo,
)


class TestTipoSolo:
    """Tests for TipoSolo value object."""

    def test_creates_and_normalizes(self):
        solo = TipoSolo(nome='Argila Arenosa')
        assert solo.nome == 'Argila Arenosa'
        assert solo.normalizado == 'argila_arenosa'

    def test_rejects_empty_nome(self):
        with pytest.raises(ValueError, match='não pode ser vazio'):
            TipoSolo(nome='')


class TestResultadoCalculo:
    """Tests for ResultadoCalculo value object."""

    def test_creates_valid_resultado(self):
        resultado = ResultadoCalculo(
            cota=5,
            resistencia_ponta=100.0,
            resistencia_lateral=50.0,
            capacidade_carga=150.0,
            capacidade_carga_adm=75.0,
        )
        assert resultado.capacidade_carga == 150.0
        assert resultado.to_dict()['cota'] == 5

    def test_validates_inputs(self):
        with pytest.raises(ValueError):
            ResultadoCalculo(
                cota=0,  # Invalid
                resistencia_ponta=100.0,
                resistencia_lateral=50.0,
                capacidade_carga=150.0,
                capacidade_carga_adm=75.0,
            )

    def test_is_immutable(self):
        resultado = ResultadoCalculo(
            cota=5,
            resistencia_ponta=100.0,
            resistencia_lateral=50.0,
            capacidade_carga=150.0,
            capacidade_carga_adm=75.0,
        )
        with pytest.raises(AttributeError):
            resultado.cota = 10


class TestCoeficienteSolo:
    """Tests for CoeficienteSolo value object."""

    def test_alpha_conversion(self):
        coef = CoeficienteSolo(
            k_kpa=500,
            alpha_perc=3.0,
            alpha_star_perc=2.0,
        )
        assert coef.alpha == 0.03
        assert coef.get_alpha(confiavel=True) == 0.03
        assert coef.get_alpha(confiavel=False) == 0.02


class TestEstaca:
    """Tests for Estaca entity."""

    def test_geometry_calculations(self):
        estaca = Estaca(
            tipo='pré_moldada',
            processo_construcao='deslocamento',
            formato='circular',
            secao_transversal=0.4,
            cota_assentamento=5.5,
        )
        # Area = pi * r^2
        assert abs(estaca.area_ponta - math.pi * 0.04) < 0.0001
        # Perimeter = pi * d
        assert abs(estaca.perimetro - math.pi * 0.4) < 0.0001
        # Supports fractional cota
        assert estaca.cota_assentamento == 5.5

    def test_quadrada_geometry(self):
        estaca = Estaca(
            tipo='pré_moldada',
            processo_construcao='deslocamento',
            formato='quadrada',
            secao_transversal=0.3,
            cota_assentamento=5,
        )
        assert estaca.area_ponta == 0.09
        assert estaca.perimetro == 1.2

    def test_validates_formato(self):
        with pytest.raises(ValueError, match='circular.*quadrada'):
            Estaca(
                tipo='pré_moldada',
                processo_construcao='deslocamento',
                formato='triangular',
                secao_transversal=0.3,
                cota_assentamento=5,
            )


class TestMedidaSPT:
    """Tests for MedidaSPT value object."""

    def test_creates_with_fractional_depth(self):
        medida = MedidaSPT(profundidade=1.5, N_SPT=8, tipo_solo='argila')
        assert medida.profundidade == 1.5
        assert medida.N_SPT == 8

    def test_is_impenetravel(self):
        assert MedidaSPT(10, 50, 'areia').is_impenetravel
        assert MedidaSPT(10, 45, 'impenetravel').is_impenetravel
        assert not MedidaSPT(5, 25, 'areia').is_impenetravel


class TestPerfilSPT:
    """Tests for PerfilSPT aggregate."""

    @pytest.fixture
    def perfil(self):
        """Create a sample SPT profile."""
        perfil = PerfilSPT(nome_sondagem='SP-01')
        perfil.adicionar_medidas(
            [
                (1.0, 5, 'argila'),
                (2.0, 10, 'areia'),
                (3.0, 15, 'areia'),
                (4.0, 20, 'areia'),
            ]
        )
        return perfil

    def test_basic_operations(self, perfil):
        assert len(perfil) == 4
        assert perfil.profundidade_minima == 1.0
        assert perfil.profundidade_maxima == 4.0
        assert 2.0 in perfil
        assert 5.0 not in perfil

    def test_obter_medida_strategies(self, perfil):
        # Exact match
        assert perfil.obter_medida(2.0, 'exata').N_SPT == 10

        # Closest match
        assert perfil.obter_medida(2.3, 'mais_proxima').profundidade == 2.0

        # Previous layer
        assert perfil.obter_medida(2.5, 'anterior').profundidade == 2.0

        # Interpolation
        interp = perfil.obter_medida(2.5, 'interpolar')
        assert 12 <= interp.N_SPT <= 13

    def test_obter_n_spt_intervalo(self, perfil):
        media = perfil.obter_n_spt_intervalo(1.0, 4.0, 'media')
        assert media == 12.5  # (5+10+15+20) / 4

    def test_iterar_profundidades(self):
        perfil = PerfilSPT(intervalo_padrao=0.5)
        perfil.adicionar_medidas(
            [
                (1.0, 5, 'argila'),
                (2.0, 10, 'areia'),
            ]
        )
        profs = [p for p, _ in perfil.iterar_profundidades()]
        assert profs == [1.0, 1.5, 2.0]

    def test_impenetravel_beyond_profile(self, perfil):
        medida = perfil.obter_medida(5.0)
        assert medida.is_impenetravel
