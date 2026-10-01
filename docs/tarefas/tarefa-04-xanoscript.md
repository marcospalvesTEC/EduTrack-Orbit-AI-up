# Tarefa 04 — Primeiro Pull/Push com XanoScript

## Status

🟡 **Em validação final** — conexão, primeiro Pull e versionamento Git concluídos.

O Push de alteração para o Xano foi iniciado durante a validação, porém abortado
antes da confirmação final por segurança, pois a extensão apresentou um alerta
de possível alteração estrutural da tabela.

## Objetivo

Conectar o ambiente local do **EduTrack Orbit AI** ao backend do Xano utilizando
a extensão **XanoScript** no VS Code, permitindo visualizar e versionar o backend
como código por meio de arquivos `.xs`.

## Ambiente utilizado

| Item | Resultado |
|---|---|
| VS Code | ✅ Utilizado |
| Extensão XanoScript | ✅ Instalada |
| Login no Xano | ✅ Realizado |
| Instância | ✅ Free Instance (`x8ki-letl-twmt`) |
| Branch Xano | ✅ `v1` — Live branch |
| Primeiro Pull | ✅ Concluído |
| Arquivos `.xs` locais | ✅ Recebidos |
| Versionamento Git | ✅ Concluído |
| Push para GitHub | ✅ Concluído |
| Push de alteração para Xano | ⚠️ Abortado por segurança |

## Conexão com o XanoScript

No VS Code foi executado:

`XanoScript: Login to Xano`

A autenticação foi concluída com sucesso.

Em seguida foi selecionada a instância:

`Free Instance (x8ki-letl-twmt)`

Depois foi selecionada a branch do Xano:

`v1 — Live branch`

> A branch `v1` pertence ao Xano e não deve ser confundida com a branch `main`
> utilizada pelo Git/GitHub.

## Primeiro Pull

Após selecionar a branch `v1`, a extensão apresentou a opção:

`Pull Changes`

O Pull foi executado com sucesso e o backend do Xano passou a ser representado
localmente no projeto por arquivos XanoScript (`.xs`).

Entre os diretórios recebidos estão:

- `.xano/`
- `addons/`
- `agents/`
- `apis/`
- `functions/`
- `tables/`
- `tools/`

## Tabelas recebidas

O diretório `tables/` passou a conter:

- `887029_user.xs`
- `887030_event_log.xs`
- `887034_academic_tasks.xs`
- `887035_subjects.xs`

Isso confirmou que a integração entre o backend do Xano e o ambiente local
estava funcionando corretamente.

## APIs e funções

O Pull também trouxe para o projeto os endpoints e funções existentes no Xano.

Entre eles estão endpoints relacionados a:

- autenticação;
- usuários;
- disciplinas;
- tarefas acadêmicas;
- logs de eventos.

Também foram recebidas funções XanoScript existentes no backend.

## Validação do Push para o Xano

Para testar o fluxo de alteração local, o arquivo:

`tables/887035_subjects.xs`

foi aberto no VS Code e recebeu temporariamente um comentário de validação.

Em seguida foi executado:

`XanoScript: Push Stage Changes to Xano`

A extensão detectou a alteração e solicitou o Stage dos arquivos.

Na etapa seguinte, entretanto, o XanoScript apresentou um alerta informando que
a operação envolvia uma tabela e que alterações estruturais poderiam causar
perda de dados.

Por segurança, foi selecionado:

`Abort Push`

O comentário de teste foi posteriormente removido e o arquivo foi restaurado ao
estado recebido originalmente do Xano.

> Nenhuma alteração estrutural foi enviada à tabela `subjects`.

## Segurança

Antes do versionamento, a pasta `.xano/` foi verificada.

O arquivo `.xano/config.json` contém somente as propriedades principais:

- `branch`
- `instanceDisplay`
- `instanceName`
- `paths`
- `workspaceId`
- `workspaceName`

Nenhuma propriedade principal de token ou senha foi identificada nessa
verificação.

O token de autenticação do Xano não foi inserido manualmente no repositório.

## Versionamento no Git

Os arquivos provenientes do Pull foram adicionados seletivamente ao Git.

Commit criado:

```text
a6f451e feat: integra XanoScript e adiciona backend do Xano