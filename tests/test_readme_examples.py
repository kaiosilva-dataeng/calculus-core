import re
from pathlib import Path

import pytest


def extract_python_code_blocks(readme_path: Path) -> list[str]:
    """Exrai todos os blocos de código Python do README."""
    content = readme_path.read_text(encoding='utf-8')
    # Regex para encontrar blocos ```python ... ```
    pattern = re.compile(r'```python\n(.*?)\n```', re.DOTALL)
    return pattern.findall(content)


def test_readme_python_examples():
    """
    Lê o README.md, extrai os exemplos Python e os executa.

    Os exemplos são executados em um contexto compartilhado (globals)
    pois frequentemente um bloco depende de variáveis definidas no anterior
    (ex: o objeto 'perfil' ou 'estaca').
    """
    readme_path = Path(__file__).parent.parent / 'README.md'
    assert readme_path.exists(), 'README.md não encontrado'

    code_blocks = extract_python_code_blocks(readme_path)
    assert len(code_blocks) > 0, (
        'Nenhum bloco de código Python encontrado no README'
    )

    # Contexto compartilhado para execução
    global_context = {}

    for i, block in enumerate(code_blocks, 1):
        try:
            # Executa o bloco de código
            exec(block, global_context)
        except Exception as e:
            pytest.fail(
                f'Erro ao executar o bloco de código {i} do README:\n\n{block}\n\nErro: {e}'
            )


if __name__ == '__main__':
    # Permite rodar o script diretamente para debug
    test_readme_python_examples()
    print('Todos os blocos de código do README foram executados com sucesso!')
