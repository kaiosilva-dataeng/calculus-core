"""
Soil Types Tests

Essential tests for soil type mapping between methods.
"""

import pytest

from calculus_core.domain.soil_types import (
    AokiVellosoSoilMapper,
    DecourtQuaresmaSoilMapper,
    SoilMapperRegistry,
    TeixeiraSoilMapper,
    TipoSoloCanonical,
    map_soil_type,
)


class TestTipoSoloCanonical:
    """Tests for canonical soil types."""

    @pytest.mark.parametrize(
        ('input_str', 'expected'),
        [
            ('argila', TipoSoloCanonical.ARGILA),
            ('argila arenosa', TipoSoloCanonical.ARGILA_ARENOSA),
            ('AREIA_SILTOSA', TipoSoloCanonical.AREIA_SILTOSA),
            ('pedregulho', TipoSoloCanonical.AREIA_COM_PEDREGULHOS),
        ],
    )
    def test_from_string(self, input_str, expected):
        assert TipoSoloCanonical.from_string(input_str) == expected

    def test_from_string_invalid(self):
        with pytest.raises(ValueError, match='não reconhecido'):
            TipoSoloCanonical.from_string('solo_inventado')


class TestSoilMappers:
    """Tests for method-specific soil mappers."""

    def test_aoki_velloso_preserves_types(self):
        mapper = AokiVellosoSoilMapper()
        assert (
            mapper.map_soil_type(TipoSoloCanonical.ARGILA_ARENOSA)
            == 'argila_arenosa'
        )
        assert (
            mapper.map_soil_type(TipoSoloCanonical.AREIA_COM_PEDREGULHOS)
            == 'areia'
        )

    def test_decourt_quaresma_groups_types(self):
        mapper = DecourtQuaresmaSoilMapper()
        # Décourt-Quaresma groups all clay variants to 'argila'
        assert mapper.map_soil_type(TipoSoloCanonical.ARGILA) == 'argila'
        assert (
            mapper.map_soil_type(TipoSoloCanonical.ARGILA_ARENOSA) == 'argila'
        )
        assert mapper.map_soil_type(TipoSoloCanonical.AREIA) == 'areia'

    def test_teixeira_specific_mappings(self):
        mapper = TeixeiraSoilMapper()
        assert (
            mapper.map_soil_type(TipoSoloCanonical.ARGILA_SILTOSA)
            == 'argila_siltosa'
        )


class TestSoilMapperRegistry:
    """Tests for soil mapper registry."""

    def test_has_builtin_mappers(self):
        assert SoilMapperRegistry.has('aoki_velloso')
        assert SoilMapperRegistry.has('decourt_quaresma')
        assert SoilMapperRegistry.has('teixeira')

    def test_get_mapper(self):
        mapper = SoilMapperRegistry.get('aoki_velloso')
        assert mapper is not None


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_map_soil_type(self):
        assert (
            map_soil_type('argila_arenosa', 'aoki_velloso') == 'argila_arenosa'
        )
        assert map_soil_type('argila_arenosa', 'decourt_quaresma') == 'argila'
