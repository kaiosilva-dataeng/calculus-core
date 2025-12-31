"""
Tests for the Adapters Layer

These tests verify that coefficient providers work correctly
and implement the expected protocols.
"""

import pytest

from calculus_core.adapters.coefficients import (
    AokiVelloso1975Provider,
    AokiVellosoLaprovitera1988Provider,
    DecourtQuaresma1978Provider,
    Teixeira1996Provider,
)

# =============================================================================
# AOKI-VELLOSO PROVIDER TESTS
# =============================================================================


class TestAokiVelloso1975Provider:
    """Tests for the Aoki-Velloso (1975) coefficient provider."""

    @pytest.fixture
    def provider(self):
        return AokiVelloso1975Provider()

    def test_get_k_areia(self, provider):
        assert provider.get_k('areia') == 1000

    def test_get_k_argila(self, provider):
        assert provider.get_k('argila') == 200

    def test_get_k_invalid_solo(self, provider):
        with pytest.raises(ValueError, match='não suportado'):
            provider.get_k('rocha')

    def test_get_alpha_areia(self, provider):
        alpha = provider.get_alpha('areia')
        assert alpha == pytest.approx(0.014)  # 1.4%

    def test_get_alpha_argila(self, provider):
        alpha = provider.get_alpha('argila')
        assert alpha == 0.06  # 6.0%

    def test_get_f1_f2_franki(self, provider):
        f1, f2 = provider.get_f1_f2('franki')
        assert f1 == 2.50
        assert f2 == 5.0  # 2 * F1

    def test_get_f1_f2_pre_moldada_with_diameter(self, provider):
        f1, f2 = provider.get_f1_f2('pré_moldada', diametro=0.4)
        # F1 = 1 + (D/0.8) = 1 + 0.5 = 1.5
        assert f1 == 1.5
        assert f2 == 3.0  # 2 * F1

    def test_get_f1_f2_pre_moldada_requires_diameter(self, provider):
        with pytest.raises(ValueError, match='Diâmetro'):
            provider.get_f1_f2('pré_moldada')

    def test_get_f1_f2_invalid_estaca(self, provider):
        with pytest.raises(ValueError, match='não suportado'):
            provider.get_f1_f2('microestaca')


class TestAokiVellosoLaprovitera1988Provider:
    """Tests for the Aoki-Velloso (Laprovitera 1988) coefficient provider."""

    @pytest.fixture
    def provider(self):
        return AokiVellosoLaprovitera1988Provider()

    def test_get_k_areia(self, provider):
        assert provider.get_k('areia') == 600

    def test_get_alpha_reliable(self, provider):
        alpha = provider.get_alpha('argila_arenosa', confiavel=True)
        assert alpha == 0.04  # 4.0%

    def test_get_alpha_unreliable(self, provider):
        alpha = provider.get_alpha('argila_arenosa', confiavel=False)
        assert alpha == pytest.approx(0.026)  # 2.6% (alpha_star)

    def test_get_f1_f2_pre_moldada(self, provider):
        f1, f2 = provider.get_f1_f2('pré_moldada', diametro=0.3)
        # In Laprovitera, F1 is fixed at 2.0
        assert f1 == 2.0
        assert f2 == 3.5


# =============================================================================
# DECOURT-QUARESMA PROVIDER TESTS
# =============================================================================


class TestDecourtQuaresma1978Provider:
    """Tests for the Décourt-Quaresma (1978) coefficient provider."""

    @pytest.fixture
    def provider(self):
        return DecourtQuaresma1978Provider()

    def test_get_k_argila_deslocamento(self, provider):
        k = provider.get_k('argila', 'deslocamento')
        assert k == 120

    def test_get_k_argila_escavada(self, provider):
        k = provider.get_k('argila', 'escavada')
        assert k == 100

    def test_get_k_areia_deslocamento(self, provider):
        k = provider.get_k('areia', 'deslocamento')
        assert k == 400

    def test_get_alpha_argila_cravada(self, provider):
        alpha = provider.get_alpha('argila', 'cravada')
        assert alpha == 1.0

    def test_get_alpha_areia_escavada(self, provider):
        alpha = provider.get_alpha('areia', 'escavada')
        assert alpha == 0.5

    def test_get_beta_argila_cravada(self, provider):
        beta = provider.get_beta('argila', 'cravada')
        assert beta == 1.0

    def test_get_beta_argila_injetada(self, provider):
        beta = provider.get_beta('argila', 'injetada')
        assert beta == 3.0


# =============================================================================
# TEIXEIRA PROVIDER TESTS
# =============================================================================


class TestTeixeira1996Provider:
    """Tests for the Teixeira (1996) coefficient provider."""

    @pytest.fixture
    def provider(self):
        return Teixeira1996Provider()

    def test_get_alpha_areia_pre_moldada(self, provider):
        alpha = provider.get_alpha('areia', 'pré_moldada')
        assert alpha == 400

    def test_get_alpha_argila_siltosa_escavada(self, provider):
        alpha = provider.get_alpha('argila_siltosa', 'escavada')
        assert alpha == 100

    def test_get_beta_pre_moldada(self, provider):
        beta = provider.get_beta('pré_moldada')
        assert beta == 4

    def test_get_beta_raiz(self, provider):
        beta = provider.get_beta('raiz')
        assert beta == 6

    def test_get_alpha_invalid_solo(self, provider):
        with pytest.raises(ValueError, match='não suportado'):
            provider.get_alpha('rocha', 'pré_moldada')

    def test_get_beta_invalid_estaca(self, provider):
        with pytest.raises(ValueError, match='inválido'):
            provider.get_beta('microestaca')
