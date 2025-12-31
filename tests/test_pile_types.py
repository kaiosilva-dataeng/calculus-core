"""
Pile Types Tests

Essential tests for extended pile type system.
"""

import math

from calculus_core.domain.pile_types import (
    CATALOGO_PERFIS_METALICOS,
    EstacaCircular,
    EstacaFactory,
    EstacaQuadrada,
)


class TestEstacaCircular:
    """Tests for circular pile type."""

    def test_geometry(self):
        estaca = EstacaCircular(
            _tipo='pré_moldada',
            _processo_construcao='deslocamento',
            diametro=0.4,
            _cota_assentamento=10,
        )
        assert abs(estaca.area_ponta - math.pi * 0.04) < 0.001
        assert abs(estaca.perimetro - math.pi * 0.4) < 0.001


class TestEstacaQuadrada:
    """Tests for square pile type."""

    def test_geometry(self):
        estaca = EstacaQuadrada(
            _tipo='pré_moldada',
            _processo_construcao='deslocamento',
            lado=0.3,
            _cota_assentamento=10,
        )
        assert estaca.area_ponta == 0.09
        assert estaca.perimetro == 1.2


class TestEstacaFactory:
    """Tests for pile factory."""

    def test_criar_circular(self):
        estaca = EstacaFactory.criar_circular(
            'pré_moldada', 'deslocamento', 0.5, 10
        )
        assert estaca.diametro == 0.5

    def test_criar_metalica(self):
        estaca = EstacaFactory.criar_metalica('HP_310x79', 15)
        assert estaca.tipo == 'metálica'


class TestCatalogoMetalicas:
    """Tests for steel pile catalog."""

    def test_has_h_profiles(self):
        assert 'HP_310x79' in CATALOGO_PERFIS_METALICOS
        assert 'HP_360x132' in CATALOGO_PERFIS_METALICOS

    def test_has_tubular_profiles(self):
        assert 'TUBULAR_406.4x9.5' in CATALOGO_PERFIS_METALICOS
