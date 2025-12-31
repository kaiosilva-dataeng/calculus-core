"""
Method Registry Tests

Essential tests for the calculation method registry.
"""

import pytest

from calculus_core.domain.method_registry import (
    CalculationMethodRegistry,
    get_calculator,
    list_available_methods,
)


class TestCalculationMethodRegistry:
    """Tests for the calculation method registry."""

    def test_builtin_methods_registered(self):
        ids = CalculationMethodRegistry.list_ids()
        assert set(ids) >= {
            'aoki_velloso_1975',
            'aoki_velloso_laprovitera_1988',
            'decourt_quaresma_1978',
            'teixeira_1996',
        }

    def test_get_method_info(self):
        info = CalculationMethodRegistry.get('aoki_velloso_1975')
        assert info.name == 'Aoki e Velloso (1975)'
        assert 'Aoki' in info.authors[0]
        assert 'AOKI' in info.reference.upper()

    def test_create_calculator(self):
        calc = CalculationMethodRegistry.create_calculator('aoki_velloso_1975')
        assert calc is not None
        assert hasattr(calc, 'calcular')

    def test_get_nonexistent_method(self):
        with pytest.raises(ValueError, match='não encontrado'):
            CalculationMethodRegistry.get('metodo_inexistente')


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    def test_get_calculator(self):
        calc = get_calculator('teixeira_1996')
        assert calc is not None

    def test_list_available_methods(self):
        methods = list_available_methods()
        assert len(methods) >= 4
        assert all('id' in m for m in methods)
