"""
Soil Investigation Tests

Essential tests for CPT profiles and CPT-SPT conversion.
"""

import pytest

from calculus_core.domain.model import PerfilSPT
from calculus_core.domain.soil_investigation import (
    CPTtoSPTConverter,
    MedidaCPT,
    PerfilCPT,
    SoilTestType,
    converter_cpt_para_spt,
    listar_correlacoes_cpt_spt,
)


class TestMedidaCPT:
    """Tests for CPT measurement."""

    def test_creates_valid_medida(self):
        medida = MedidaCPT(profundidade=2.0, qc=5.0, fs=50.0)
        assert medida.profundidade == 2.0
        assert medida.qc == 5.0
        assert medida.qc_kpa == 5000.0

    def test_calculates_friction_ratio(self):
        medida = MedidaCPT(profundidade=2.0, qc=10.0, fs=100.0)
        assert medida.Rf == 1.0  # (100 / 10000) * 100

    def test_detects_cohesive_soil(self):
        assert not MedidaCPT(2.0, 10.0, 50.0, Rf=0.5).is_cohesive
        assert MedidaCPT(2.0, 2.0, 100.0, Rf=5.0).is_cohesive

    def test_test_type_detection(self):
        assert MedidaCPT(2.0, 5.0, 50.0).test_type == SoilTestType.CPT
        assert (
            MedidaCPT(2.0, 5.0, 50.0, u2=100.0).test_type == SoilTestType.CPTU
        )


class TestPerfilCPT:
    """Tests for CPT profile."""

    @pytest.fixture
    def perfil(self):
        perfil = PerfilCPT(nome_sondagem='CPT-01')
        perfil.adicionar_medidas(
            [
                (1.0, 2.0, 30.0),
                (2.0, 5.0, 50.0),
                (3.0, 10.0, 60.0),
            ]
        )
        return perfil

    def test_basic_operations(self, perfil):
        assert len(perfil) == 3
        assert perfil.profundidade_minima == 1.0
        assert perfil.profundidade_maxima == 3.0

    def test_obter_qc_intervalo(self, perfil):
        media = perfil.obter_qc_intervalo(1.0, 3.0, 'media')
        assert abs(media - 5.67) < 0.1  # (2+5+10) / 3


class TestCPTtoSPTConverter:
    """Tests for CPT to SPT conversion."""

    @pytest.fixture
    def perfil_cpt(self):
        perfil = PerfilCPT()
        perfil.adicionar_medidas(
            [
                (1.0, 2.0, 20.0),  # Low qc
                (2.0, 5.0, 40.0),  # Medium
                (3.0, 10.0, 50.0),  # High
            ]
        )
        return perfil

    def test_conversion_produces_spt(self, perfil_cpt):
        converter = CPTtoSPTConverter()
        perfil_spt = converter.convert(perfil_cpt)
        assert isinstance(perfil_spt, PerfilSPT)
        assert len(perfil_spt) >= 1

    def test_nspt_values_are_reasonable(self, perfil_cpt):
        converter = CPTtoSPTConverter()
        perfil_spt = converter.convert(perfil_cpt)
        for medida in perfil_spt:
            assert 1 <= medida.N_SPT <= 60


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_converter_cpt_para_spt(self):
        perfil_cpt = PerfilCPT()
        perfil_cpt.adicionar_medidas(
            [
                (1.0, 5.0, 50.0),
                (2.0, 10.0, 60.0),
            ]
        )
        perfil_spt = converter_cpt_para_spt(perfil_cpt, 'robertson_1983')
        assert isinstance(perfil_spt, PerfilSPT)

    def test_listar_correlacoes(self):
        correlacoes = listar_correlacoes_cpt_spt()
        assert 'robertson_1983' in correlacoes
        assert 'aoki_velloso_1975' in correlacoes


class TestIntegracao:
    """Integration test: CPT → SPT → Calculation."""

    def test_cpt_to_spt_to_aoki_velloso(self):
        from calculus_core.bootstrap import create_calculator
        from calculus_core.domain.model import Estaca

        # Create CPT
        perfil_cpt = PerfilCPT()
        perfil_cpt.adicionar_medidas(
            [
                (1.0, 2.0, 20.0),
                (2.0, 5.0, 40.0),
                (3.0, 10.0, 50.0),
                (4.0, 15.0, 60.0),
                (5.0, 20.0, 80.0),
            ]
        )

        # Convert
        perfil_spt = converter_cpt_para_spt(perfil_cpt, 'robertson_1983')

        # Create pile
        estaca = Estaca(
            tipo='pré_moldada',
            processo_construcao='deslocamento',
            formato='circular',
            secao_transversal=0.3,
            cota_assentamento=4.0,
        )

        # Calculate
        calc = create_calculator('aoki_velloso_1975')
        resultado = calc.calcular(perfil_spt, estaca)

        assert resultado.capacidade_carga > 0
