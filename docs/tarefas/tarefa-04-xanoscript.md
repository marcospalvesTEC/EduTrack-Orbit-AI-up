# Tarefa 04 — Primeiro Pull/Push com XanoScript

## Status

🟡 **Em validação** — ambiente local preparado; Pull ainda não executado.

## Objetivo

Conectar o ambiente local (VS Code) ao backend do Xano utilizando a extensão
**XanoScript**, permitindo gerenciar o backend como código e versioná-lo no Git.

## Conceitos

- **Xano:** plataforma de backend No-Code que gerencia banco de dados e APIs.
- **XanoScript (`.xs`):** representação da lógica do Xano em texto, o que permite
  versionar o backend com Git.
- **Pull:** baixar do painel do Xano as tabelas e configurações para o computador.
- **Push:** enviar as alterações feitas nos arquivos `.xs` locais para o painel.

## Estado verificado do ambiente

Verificações executadas em 30/09/2026 na máquina de desenvolvimento:

| Item | Resultado |
|---|---|
| Extensão XanoScript instalada | ✅ `xano.xanoscript-0.5.12` |
| Login na extensão | ❌ Sem estado em `globalStorage` |
| Pastas `tables/` e `.xano/` no repositório | ❌ Ainda não existem |
| `*.xs` normalizado para LF | ✅ `.gitattributes` linha 15 |
| `tables/` e `.xano/` versionáveis | ✅ `.gitignore` não os bloqueia |

Comandos usados:

```powershell
Get-ChildItem "$env:USERPROFILE\.vscode\extensions" -Directory | Where-Object Name -match 'xano'
Test-Path "$env:APPDATA\Code\User\globalStorage\xano.xanoscript"
Test-Path tables; Test-Path .xano
```

## Procedimento a executar

### 1. Conta e workspace no Xano

1. Criar conta em [xano.com](https://www.xano.com/) (plano gratuito).
2. Criar o workspace `edutrack-ai` na instância.
3. Em **Instances** → engrenagem da **Free Instance** → **Metadata API & MCP
   Server** → **Manage Access Tokens** → **New Access Token**.
4. Nomear como `VS Code` e selecionar os escopos: **Database** (CRUD),
   **API Groups** (CRUD), **Functions** (CRUD) e **Content** (Read).
5. Copiar o token imediatamente — ele aparece uma única vez.

> O token **não** deve ser salvo no repositório. A extensão o guarda no Secret
> Storage do VS Code, fora da pasta do projeto.

### 2. Conexão com o VS Code

1. `Ctrl + Shift + P` → **XanoScript: Login to Xano**.
2. Escolher **Login via Browser** (primeira vez) ou **Enter Access Token**.
3. `Ctrl + Shift + P` → **XanoScript: Select workspace** → `edutrack-ai`.
4. Se aparecer o aviso de pull, escolher **Pull Changes**.

### 3. Primeiro Pull

1. `Ctrl + Shift + P` → **XanoScript: Pull latest changes from Xano**.
2. Isso cria `tables/` com os arquivos `.xs` e a pasta oculta `.xano/`.
3. Para exibir `.xano/`, usar `Ctrl + Shift + .` no explorador do VS Code.

### 4. Alteração e Push

1. Abrir um `.xs` e adicionar o comentário `// Meu primeiro comentário via VS Code`.
2. Salvar com `Ctrl + S`.
3. `Ctrl + Shift + P` → **XanoScript: Push Stage Changes to Xano**.
4. Conferir o comentário no painel do Xano.

### 5. Commitar antes de deletar (ordem obrigatória)

O passo de remoção de tabelas padrão é **irreversível**. O commit precisa existir
**antes** da deleção para que a recuperação sugerida no roteiro funcione:

```powershell
git add tables .xano
git commit -m "feat: pull inicial do XanoScript"
```

Só depois de remover os `.xs` indesejados e executar o Push, commitar a remoção:

```powershell
git add tables
git commit -m "chore: remove tabelas padrao do Xano"
```

> A ordem sugerida no roteiro (deletar → depois commitar) quebra a rede de
> segurança de `git checkout HEAD~1 -- tables/`. Por isso o commit antecede a
> deleção.

### 6. Remoção das tabelas padrão

Manter apenas a tabela de autenticação. Na instância atual a tabela é `user`
(nome padrão do Xano), e não `users` como descreve `xano/README.md`. A divergência
está documentada e será resolvida nas Tarefas 11 e 13, quando forem criadas
`subjects` e `academic_tasks`.

1. Deletar os arquivos `.xs` de `account`, `agent_conversation`, `agent_message`,
   `event_log` e demais tabelas geradas automaticamente.
2. Manter o `.xs` da tabela `user`.
3. **XanoScript: Push Stage Changes to Xano** e conferir no painel.

## Segurança aplicada nesta preparação

- URL real da instância removida de `.env.example` e
  `.streamlit/secrets.toml.example`, substituída por placeholder.
- `.gitignore` ignora arquivos de token e credenciais dentro de `tables/` e
  `.xano/`, mas mantém esses diretórios versionáveis.
- Commits separados para que a mudança de segurança fique identificável no
  histórico (`1f2454f`).

## Comandos de verificação

```powershell
git ls-files tables .xano
Test-Path tables; Test-Path .xano
```

## Resultado

- [x] Extensão XanoScript instalada (`0.5.12`).
- [x] `*.xs` preparado no `.gitattributes` para LF.
- [x] `tables/` e `.xano/` liberados no `.gitignore`.
- [x] URL privada do Xano removida do versionamento.
- [ ] Workspace Xano criado e token gerado.
- [ ] Login realizado na extensão do VS Code.
- [ ] Pull executado e `tables/` com arquivos `.xs` visível.
- [ ] Comentário de teste enviado via Push e conferido no painel.
- [ ] Tabelas padrão removidas, mantendo apenas `user`.
- [ ] Evidências (screenshots) adicionadas.
