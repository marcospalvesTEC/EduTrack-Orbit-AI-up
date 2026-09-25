# Tarefa 05 — Exercícios Básicos de Git: Branches e Pull Requests

## Status

✅ **Concluída**

## Objetivo

Aplicar um fluxo profissional de desenvolvimento utilizando branches, commits, Pull Requests e merges.

## Implementação no EduTrack Orbit AI

O EduTrack Orbit AI utiliza branches separadas para novas funcionalidades, documentação e correções.

Exemplos de branches presentes no projeto:

```text
develop
docs/development-history
feat/xano-auth-integration
feat/xano-subjects-integration
feature/demo-authentication
feature/figma-desktop-agenda
feature/figma-desktop-profile
feature/figma-desktop-registration
feature/figma-desktop-subjects
feature/figma-desktop-tasks
feature/setup-project-foundation
fix/mvp-interactions-mobile
fix/sidebar-navigation
fix/sidebar-reopen-button
fix/theme-toggle
fix/xano-subject-required-fields
```

O projeto também utiliza mensagens de commit compatíveis com Conventional Commits, incluindo prefixos como:

```text
feat:
fix:
docs:
chore:
```

## Observação sobre a migração do repositório

Os commits, branches e histórico Git foram preservados na migração para a conta acadêmica.

Pull Requests são objetos do GitHub e não são transferidos apenas com `git push --all`. Por isso, novos Pull Requests acadêmicos devem ser criados no repositório:

`marcospalvesTEC/EduTrack-Orbit-AI-up`

A própria branch usada para adicionar esta documentação pode servir como uma nova evidência prática do fluxo Branch → Push → Pull Request → Merge.

## Fluxo utilizado

```text
main
  ↓
nova branch
  ↓
alterações
  ↓
git add
  ↓
git commit
  ↓
git push
  ↓
Pull Request
  ↓
revisão
  ↓
merge
```

## Evidências

Adicionar:

```text
docs/tarefas/evidencias/tarefa-05-branch.png
docs/tarefas/evidencias/tarefa-05-pull-request.png
docs/tarefas/evidencias/tarefa-05-merge.png
```

## Resultado

- [x] Uso de branches.
- [x] Commits organizados.
- [x] Uso de prefixos `feat:`, `fix:`, `docs:` e `chore:`.
- [x] Merge de funcionalidades utilizado no histórico do projeto.
- [ ] Criar novo Pull Request no repositório acadêmico.
- [ ] Adicionar screenshot do PR acadêmico.
- [ ] Adicionar screenshot do merge acadêmico.
