# Correção focada — Assistente Orbit

**Data:** 28/09/2026

## Escopo

Esta correção altera somente a experiência do Assistente Orbit.

## O que foi corrigido

- Adicionado botão **Nova conversa**.
- Adicionado botão **Limpar histórico**.
- Ao limpar a conversa, também é removida qualquer ação pendente.
- A prévia de uma ação pendente agora aparece **antes do histórico**, evitando que os botões
  `Confirmar` e `Cancelar` fiquem enterrados em uma conversa longa.
- `Confirmar` mantém o fluxo de sessão de foco e adiciona o evento à Agenda.
- `Cancelar` encerra apenas a ação pendente e preserva a conversa.
- O histórico recebeu altura máxima e rolagem própria para não esticar a página indefinidamente.
- As ações rápidas da lateral direita continuam funcionais:
  - Criar tarefa
  - Planejar sessão de foco
  - Adicionar evento à agenda
  - Resumir desempenho
- Estilos novos seguem o roxo Orbit e incluem tratamento para tema escuro.

## Arquivos alterados

```text
pages/6_Assistente.py
src/ui/figma_assistant.py
src/ui/figma_assistant.css
```

## Validação recomendada

1. Abrir o Assistente.
2. Clicar em `Planejar sessão de foco`.
3. Confirmar que a prévia aparece no topo da conversa.
4. Testar `Confirmar`.
5. Testar novamente e usar `Cancelar`.
6. Criar algumas mensagens e clicar em `Limpar histórico`.
7. Confirmar que o histórico some e nenhuma ação pendente permanece.
