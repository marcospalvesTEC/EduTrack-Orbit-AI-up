# Patch — Tema Claro, Navegação e Funcionalidade

**Data:** 28/09/2026  
**Projeto:** EduTrack Orbit AI

## Escopo

Correções levantadas na validação do tema claro, preservando a arquitetura e as funcionalidades já construídas.

## Alterações

### Busca global e notificações
- O campo `Buscar...` deixa de ser apenas decorativo.
- Busca por disciplinas, tarefas e páginas principais.
- Resultados usam navegação nativa do Streamlit para preservar a sessão.
- O sino mostra tarefas atrasadas e prazos dos próximos 7 dias.
- Elementos decorativos antigos do cabeçalho são ocultados.
- `Deploy` e o menu nativo do Streamlit são ocultados da interface final.

### Dashboard
- Navegação HTML antiga deixa de ser usada para evitar perda de sessão.
- Atalhos nativos para Disciplinas e Tarefas preservam a autenticação.

### Agenda
- O título de qualquer mês usa o roxo Orbit com maior destaque.
- O card `Trabalho em grupo` recebe contorno roxo completo.

### Assistente Orbit
- Ações rápidas passam a funcionar.
- Sugestões rápidas recebem mais espaçamento interno.
- Botão `Enviar` usa roxo Orbit com texto branco.

### Perfil
- Ações principais dos modais usam roxo Orbit + texto branco.
- Upload, controles `+/-` e indicadores interativos seguem a identidade Orbit.

### Configurações
- Setas dos selects recebem alinhamento e cor roxa.
- Toggles ativos usam roxo Orbit.
- `Salvar configurações` mantém confirmação visível após o rerun.
- `Gerenciar privacidade` e `Revisar dispositivos` exibem resposta visível.
- `Excluir conta` permanece protegido e não apaga a conta demonstrativa.
- `Baixar meus dados` foi preservado.

## Segurança

Nenhuma exclusão real de conta foi adicionada. A conta de teste permanece disponível.

## Validação

```powershell
python -m pytest -q
python -m streamlit run app.py
git status
git diff
```


## Validação automatizada

Após adicionar Busca Global e trocar os links HTML do Dashboard por navegação
nativa do Streamlit, dois testes antigos precisaram ser atualizados:

- O Assistente agora possui dois campos de texto: Busca Global e pergunta ao Orbit.
- O Dashboard passa a validar `st.page_link` para Disciplinas e Tarefas, evitando
  navegação HTML direta que podia perder a sessão autenticada.

Essas mudanças atualizam os testes para o comportamento funcional novo, sem remover
a cobertura das funcionalidades anteriores.
