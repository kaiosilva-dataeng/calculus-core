# Diário de Evolução: Calculus Core
*De Julho de 2024 ao Estado Atual (Dezembro de 2024)*

Este documento serve como um registro histórico da transformação do `calculus-core`, detalhando como saímos de um conjunto de scripts utilitários para um motor de cálculo de engenharia de fundações robusto, modular e pronto para produção.

---

## 📅 O Ponto de Partida: Julho de 2024
**Estado de Referência (Commit `96211bd`)**

Em julho, o projeto consistia em uma estrutura monolítica e orientada a scripts.

### 🔍 Limitações do Estado Anterior
1. **Acoplamento**: A lógica de cálculo estava misturada com utilitários e definições de dados (ex: `src/calculus_core/core.py`, `models.py`).
2. **Dificuldade de Teste**: Sem uma separação clara entre domínio e infraestrutura, testes automatizados eram escassos e difíceis de manter.
3. **Processos Manuais**: Versionamento, geração de changelogs e deploy eram feitos manualmente, aumentando o risco de erros humanos.
4. **Interface Rígida**: O frontend em Streamlit estava fortemente acoplado aos modelos de dados originais, dificultando a evolução da UI sem quebrar o motor.
5. **Tipagem Limitada**: Cálculos de profundidade eram limitados a inteiros em muitos pontos, o que não refletia a precisão necessária para investigações geotécnicas reais.

---

## 🚀 Fase 1: A Revolução Arquitetural (Agosto - Outubro)
*A transição para Clean Architecture e DDD.*

O passo mais significativo foi a migração para uma arquitetura inspirada no "Cosmic Python" (Clean Architecture + DDD).

### 🛠️ Mudanças Realizadas
- **Domínio Isolado**: Criação de `domain/model.py`, onde as regras de negócio de engenharia (Solos, Estacas, Cálculos) vivem sem conhecimento de interfaces externas.
- **Camada de Serviço**: Introdução de um `service_layer` e um `bootstrap.py` para gerenciar a injeção de dependências e orquestrar fluxos de trabalho.
- **Adaptores e Pontos de Entrada**: Separação clara entre como os dados chegam (Streamlit, CLI) e como são processados.
- **Registro Dinâmico**: Implementação do `CalculationMethodRegistry`, permitindo que novos métodos de cálculo (Aoki-Velloso, Decourt-Quaresma, etc.) sejam adicionados sem modificar o core do sistema.

---

## 🛠️ Fase 2: Excelência Operacional (Novembro)
*Automação e Qualidade de Código.*

Para garantir a sustentabilidade do projeto, implementamos ferramentas de governança de código.

### ✨ Novas Funcionalidades
1. **Commitizen & Conventional Commits**: Padronização de mensagens de commit para facilitar a leitura da evolução do projeto.
2. **Ciclo de Vida Automatizado**: Configuração de GitHub Actions para:
   - Execução de testes em múltiplas versões de Python (3.10 a 3.13).
   - Bump de versão automático baseado em commits.
   - Geração automática de `CHANGELOG.md`.
3. **Pre-commit Hooks**: Garantia de qualidade via `ruff`, `mypy` e `pytest` antes mesmo do código chegar ao repositório.

---

## 💎 Fase 3: Refinamento e UX (Dezembro)
*Foco na precisão técnica e experiência do usuário.*

As atualizações mais recentes focaram em resolver as limitações de "vida real" sentidas pelos usuários.

### 📈 Evolução Técnica e Funcional
- **Release Automático via OIDC**: Implementação de um fluxo de trabalho robusto que publica automaticamente no PyPI e no GitHub Releases ao detectar uma nova tag de versão (`v*`). Utiliza *Trusted Publishing* via OIDC (OpenID Connect), eliminando a necessidade de gerenciar tokens de API inseguros.
- **Suporte a Profundidade Ponto-Flutuante**: Refatoração completa para suportar registros de solo em profundidades como `1.5m` ou `2.75m`, removendo a limitação de números inteiros.
- **Interface Streamlit Premium**: Modernização visual da UI, com melhores gráficos, tabelas dinâmicas e aviso de depreciações corrigidos.
- **Modernização do Ambiente (Python 3.14)**: Pioneirismo na adoção do Python 3.14 para desenvolvimento e CI, garantindo que o motor de cálculo esteja pronto para as futuras otimizações da linguagem.
- **Otimização de Dependências**: Refatoração do `pyproject.toml` para mover dependências pesadas de visualização (`matplotlib`) para grupos opcionais, tornando o core da biblioteca mais leve para integração em outros sistemas.
- **Transparência e Badges**: Implementação de badges automáticos no `README.md` refletindo o status real de CI, cobertura (via SVG dinâmico), versão PyPI e compatibilidade Python.
- **Verificação de Exemplos e Ativos**: Automação que garante que todos os exemplos do `README.md` funcionam e que as imagens da documentação são exibidas corretamente em portais externos como o PyPI via URLs absolutas.
- **Governança de IA**: Estabelecimento de regras estritas de workflow para agentes de IA para garantir integridade do histórico git e revisão humana obrigatória.

---

## 🏁 Estado Atual e Progresso
Hoje, o `calculus-core` não é apenas um software de cálculo; é um ecossistema documentado, testado e evolutivo.

- **Diferença de Estrutura**: De `src/*.py` para uma árvore organizada de `domain`, `adapters` e `service_layer`.
- **Diferença de Confiança**: De "espero que funcione" para "todos os testes passaram no CI e a cobertura está garantida".
- **Diferença de Maturidade**: Um diário de mudanças (`CHANGELOG.md`) que conta a história de cada nova funcionalidade adicionada.

---
