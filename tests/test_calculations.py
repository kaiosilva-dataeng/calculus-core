"""
Tests for the Calculation Strategies

These tests verify that the calculation methods work correctly
by using mocked coefficient providers.
"""

import pytest

from calculus_core.adapters.coefficients import (
    AokiVelloso1975Provider,
    DecourtQuaresma1978Provider,
    Teixeira1996Provider,
)
from calculus_core.domain.calculation import (
    AokiVellosoCalculator,
    DecourtQuaresmaCalculator,
    TeixeiraCalculator,
)
from calculus_core.domain.model import Estaca, PerfilSPT

# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def perfil_spt():
    """Standard SPT profile for testing."""
    perfil = PerfilSPT(nome_sondagem='SP-01')
    perfil.adicionar_medidas(
        [
            (1, 3, 'argila_arenosa'),
            (2, 3, 'argila_arenosa'),
            (3, 5, 'argila_arenosa'),
            (4, 6, 'argila_arenosa'),
            (5, 8, 'argila_arenosa'),
            (6, 13, 'areia_argilosa'),
            (7, 17, 'areia_argilosa'),
            (8, 25, 'areia_argilosa'),
            (9, 27, 'areia_silto_argilosa'),
            (10, 32, 'areia'),
            (11, 36, 'areia'),
        ]
    )
    return perfil


@pytest.fixture
def estaca_circular():
    """Standard circular pile for testing."""
    return Estaca(
        tipo='pré_moldada',
        processo_construcao='deslocamento',
        formato='circular',
        secao_transversal=0.3,
        cota_assentamento=5,
    )


@pytest.fixture
def estaca_quadrada():
    """Standard square pile for testing."""
    return Estaca(
        tipo='pré_moldada',
        processo_construcao='deslocamento',
        formato='quadrada',
        secao_transversal=0.3,
        cota_assentamento=5,
    )


# =============================================================================
# AOKI-VELLOSO CALCULATOR TESTS
# =============================================================================


class TestAokiVellosoCalculator:
    """Tests for AokiVellosoCalculator."""

    @pytest.fixture
    def calculator(self):
        provider = AokiVelloso1975Provider()
        return AokiVellosoCalculator(provider)

    def test_calcular_returns_resultado(
        self, calculator, perfil_spt, estaca_circular
    ):
        resultado = calculator.calcular(perfil_spt, estaca_circular)
        assert resultado.cota == 5
        assert resultado.resistencia_ponta > 0
        assert resultado.resistencia_lateral >= 0
        assert resultado.capacidade_carga > 0

    def test_calcular_resistencia_ponta_formula(
        self, calculator, perfil_spt, estaca_quadrada
    ):
        # For cota 5, tip layer is layer 6 (areia_argilosa, N=13)
        # K = 600 for areia_argilosa
        # F1 = 1 + (0.3/0.8) = 1.375 for pre_moldada with D=0.3
        # Rp = (K * Np) / F1 * Area = (600 * 13) / 1.375 * 0.09
        resultado = calculator.calcular(perfil_spt, estaca_quadrada)
        assert resultado.resistencia_ponta > 0

    def test_cota_parada(self, calculator, perfil_spt):
        cota = calculator.cota_parada(perfil_spt)
        # Should be last layer - 1
        assert cota == 10  # 11 layers, last layer index 10

    def test_calcular_np(self, calculator, perfil_spt):
        np = calculator.calcular_np(perfil_spt, cota_assentamento=5)
        # Tip layer is at depth 6, N_SPT = 13
        assert np == 13


# =============================================================================
# DECOURT-QUARESMA CALCULATOR TESTS
# =============================================================================


class TestDecourtQuaresmaCalculator:
    """Tests for DecourtQuaresmaCalculator."""

    @pytest.fixture
    def calculator(self):
        provider = DecourtQuaresma1978Provider()
        return DecourtQuaresmaCalculator(provider)

    def test_calcular_returns_resultado(
        self, calculator, perfil_spt, estaca_circular
    ):
        resultado = calculator.calcular(perfil_spt, estaca_circular)
        assert resultado.cota == 5
        assert resultado.resistencia_ponta >= 0
        assert resultado.resistencia_lateral >= 0

    def test_calcular_np_averaging(self, calculator, perfil_spt):
        # Np is average of cota and cota+1
        # For cota 5: (8 + 13) / 2 = 10.5
        np = calculator.calcular_np(perfil_spt, cota_assentamento=5)
        assert np == 10.5

    def test_cota_parada(self, calculator, perfil_spt):
        cota = calculator.cota_parada(perfil_spt)
        assert cota == 10

    def test_calcular_rp_formula(self, calculator):
        # Rp = alpha * Np * K * Area
        rp = DecourtQuaresmaCalculator.calcular_rp(
            alpha=1.0,
            Np=10.0,
            K=120,
            area_ponta=0.09,
        )
        expected = 1.0 * 10.0 * 120 * 0.09
        assert abs(rp - expected) < 0.001


# =============================================================================
# TEIXEIRA CALCULATOR TESTS
# =============================================================================


class TestTeixeiraCalculator:
    """Tests for TeixeiraCalculator."""

    @pytest.fixture
    def calculator(self):
        provider = Teixeira1996Provider()
        return TeixeiraCalculator(provider)

    def test_calcular_returns_resultado(
        self, calculator, perfil_spt, estaca_quadrada
    ):
        resultado = calculator.calcular(perfil_spt, estaca_quadrada)
        assert resultado.cota == 5
        assert resultado.resistencia_ponta >= 0
        assert resultado.resistencia_lateral >= 0

    def test_cota_parada(self, calculator, perfil_spt):
        cota = calculator.cota_parada(perfil_spt)
        assert cota == 10

    def test_calcular_rp_formula(self, calculator):
        rp = TeixeiraCalculator.calcular_rp(
            alpha=300,
            Np=15.0,
            area_ponta=0.09,
        )
        expected = 300 * 15.0 * 0.09
        assert abs(rp - expected) < 0.001

    def test_calcular_carga_adm_uses_minimum(self, calculator):
        # Q_adm = min((Rp+Rl)/2, Rp/4 + Rl/1.5)
        Rp = 100
        Rl = 60
        nbr = (Rp + Rl) / 2  # 80
        decourt = Rp / 4 + Rl / 1.5  # 25 + 40 = 65
        expected = min(nbr, decourt)
        assert (
            TeixeiraCalculator.calcular_carga_adm_teixeira(Rp, Rl) == expected
        )


# =============================================================================
# INTEGRATION TESTS WITH REAL PROVIDERS
# =============================================================================


class TestCalculatorIntegration:
    """Integration tests using real providers."""

    def test_all_calculators_return_valid_results(
        self, perfil_spt, estaca_circular
    ):
        from calculus_core.bootstrap import create_calculator

        calculators = [
            create_calculator('aoki_velloso_1975'),
            create_calculator('decourt_quaresma_1978'),
            create_calculator('teixeira_1996'),
        ]

        for calc in calculators:
            resultado = calc.calcular(perfil_spt, estaca_circular)
            assert resultado.capacidade_carga > 0
            assert resultado.capacidade_carga_adm > 0
