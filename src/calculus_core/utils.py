def normalizar_tipo_solo(tipo_solo: str, metodo: str) -> str:
    """
    Normaliza o tipo de solo para um formato padrão.

    Args:
        tipo_solo: Tipo de solo como string.

    Returns:
        str: Tipo de solo normalizado.
    """
    tipo_solo = tipo_solo.lower().replace(' ', '_').replace('-', '_')
    if metodo == 'décourt_quaresma':
        if tipo_solo in ['argila', 'argila_arenosa', 'argila_areno_siltosa']:
            return 'argila'
        elif tipo_solo in ['silte', 'silte_argiloso', 'silte_arenoso']:
            return 'silte'
        elif tipo_solo in ['areia', 'areia_argilosa', 'areia_areno_siltosa']:
            return 'areia'
    return tipo_solo


def normalizar_tipo_estaca(tipo_estaca: str, metodo: str) -> str:
    """
    Normaliza o tipo de estaca para um formato padrão.

    Args:
        tipo_estaca: Tipo de estaca como string.

    Returns:
        str: Tipo de estaca normalizado.
    """
    tipo_estaca = tipo_estaca.lower().replace(' ', '_').replace('-', '_')
    if metodo == 'décourt_quaresma':
        if tipo_estaca in [
            'cravada',
            'franki',
            'pré_moldada',
            'metálica',
            'ômega',
        ]:
            return 'cravada'
        elif tipo_estaca in [
            'escavada',
            'escavada_bentonita',
            'hélice_contínua',
            'raiz',
            'injetada',
        ]:
            return tipo_estaca
    return tipo_estaca
