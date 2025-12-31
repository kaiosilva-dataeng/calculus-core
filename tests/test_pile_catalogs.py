"""
Pile Catalog Tests

Essential tests for pile catalogs and factory integration.
"""

import pytest

from calculus_core.domain.pile_catalogs import (
    CATALOGO_ESCAVADAS,
    CATALOGO_FRANKI,
    CATALOGO_HELICE_CONTINUA,
    CATALOGO_PRE_MOLDADAS,
    CATALOGO_RAIZ,
    listar_tipos_estaca,
    obter_perfil,
    resumo_catalogos,
)
from calculus_core.domain.pile_types import EstacaFactory


class TestCatalogosExistem:
    """Verify catalogs are properly populated."""

    @pytest.mark.parametrize(
        ('catalogo', 'min_count'),
        [
            (CATALOGO_PRE_MOLDADAS, 10),
            (CATALOGO_ESCAVADAS, 8),
            (CATALOGO_HELICE_CONTINUA, 8),
            (CATALOGO_RAIZ, 6),
            (CATALOGO_FRANKI, 5),
        ],
    )
    def test_catalog_has_profiles(self, catalogo, min_count):
        assert len(catalogo) >= min_count


class TestFactoryCatalogIntegration:
    """Tests for factory integration with catalogs."""

    @pytest.mark.parametrize(
        ('tipo', 'perfil', 'expected_tipo'),
        [
            ('pre_moldada', 'CIRCULAR_330', 'pré_moldada'),
            ('escavada', 'ESCAVADA_600_REV', 'escavada'),
            ('helice_continua', 'HELICE_500', 'hélice_contínua'),
            ('raiz', 'RAIZ_200', 'raiz'),
            ('franki', 'FRANKI_450', 'franki'),
            ('metalica', 'HP_310x79', 'metálica'),
        ],
    )
    def test_criar_de_catalogo(self, tipo, perfil, expected_tipo):
        estaca = EstacaFactory.criar_de_catalogo(tipo, perfil, 10)
        assert estaca.tipo == expected_tipo
        assert estaca.cota_assentamento == 10


class TestCatalogUtilities:
    """Tests for catalog utility functions."""

    def test_listar_tipos(self):
        tipos = listar_tipos_estaca()
        assert set(tipos) >= {
            'pre_moldada',
            'escavada',
            'helice_continua',
            'raiz',
            'franki',
            'omega',
        }

    def test_obter_perfil(self):
        perfil = obter_perfil('escavada', 'ESCAVADA_600_REV')
        assert perfil.diametro == 0.60

    def test_resumo_catalogos(self):
        resumo = resumo_catalogos()
        assert len(resumo) >= 6
        for tipo, perfis in resumo.items():
            assert len(perfis) >= 1
