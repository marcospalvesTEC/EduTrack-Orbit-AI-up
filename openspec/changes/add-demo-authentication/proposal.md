## Why

O protótipo permite acessar diretamente os dados acadêmicos sem identificar o estudante. Para a demonstração de 08/09, o MVP precisa apresentar a jornada básica de acesso e proteger as páginas internas, mesmo antes da integração real com o Xano.

## What Changes

- Adicionar autenticação demonstrativa local, identificada claramente como não produtiva.
- Criar fluxos de cadastro, login, logout, solicitação de recuperação e redefinição simulada de senha.
- Manter a sessão autenticada durante o uso do Streamlit.
- Impedir acesso ao Início acadêmico, Disciplinas e Tarefas enquanto não houver sessão autenticada.
- Disponibilizar uma conta de demonstração e mensagens de validação em português.
- Separar regras de autenticação da interface para permitir substituição futura pelo Xano.
- Adicionar testes unitários e de execução das rotas protegidas.

## Capabilities

### New Capabilities

- `demo-authentication`: Define cadastro local, login, recuperação simulada, redefinição, sessão, logout e proteção das páginas do protótipo.

### Modified Capabilities

Nenhuma. Ainda não existem especificações principais publicadas em `openspec/specs/`.

## Impact

- Novo serviço local de autenticação em `src/services/` e regras auxiliares em `src/core/`.
- Novos componentes de autenticação em `src/ui/` e atualização de `app.py`.
- Proteção das páginas existentes em `pages/`.
- Novos testes em `tests/`.
- Sem novas dependências, envio de e-mail, persistência externa ou integração com Xano.
