# Correções e estabilização — EduTrack Orbit AI

**Data:** 06/10/2026  
**Projeto:** EduTrack Orbit AI — Innovation Lab

## Objetivo

Registrar as principais correções realizadas antes da entrega, com foco em estabilidade visual, integração com o Xano e preparação das evidências do projeto.

## Correções concluídas

### 1. Renderização de HTML no Dashboard

Foi corrigido o problema em que trechos HTML apareciam como texto na interface, por exemplo:

```html
<div class="orbit-hero-intro">
```

A causa estava relacionada à indentação dos blocos HTML enviados ao `st.markdown(..., unsafe_allow_html=True)`.

A solução aplicada foi normalizar os blocos HTML antes da renderização, preservando o uso de `st.markdown` para manter compatibilidade com os testes existentes.

Arquivos principais envolvidos:

- `src/ui/figma_dashboard.py`
- `src/ui/pets.py`

### 2. Mascotes Orbit

Foi concluída a integração dos mascotes com as preferências do usuário.

Mascotes disponíveis:

- Axalote Mago
- Raposa Feiticeira
- Lagosta Boxeadora
- Caracol Curandeiro

As preferências podem ser definidas por tela:

- Início
- Disciplinas
- Tarefas
- Agenda
- Relatórios
- Assistente
- Perfil
- Configurações

### 3. Persistência no Xano

Foi configurada a tabela:

`user_pet_preferences`

Campos principais:

- `user_id`
- `screen_key`
- `pet_key`

Endpoints utilizados:

```text
GET /profile/pets
POST /profile/pet
```

O endpoint de gravação permite criar ou atualizar a preferência do mascote para cada tela.

### 4. Redução de requisições ao Xano

Foi identificado limite de requisições do plano utilizado no Xano.

Para evitar chamadas desnecessárias durante os reruns do Streamlit, foi utilizado cache em `st.session_state` para dados acadêmicos e preferências já carregadas.

### 5. Configurações

A tela de Configurações recebeu o seletor de mascote por área do sistema.

O usuário pode escolher:

1. a tela;
2. o mascote;
3. salvar a preferência.

A preferência é persistida no Xano.

### 6. Tema claro

Após revisão em vídeo, o modo claro está funcional e visualmente estável para a maior parte das telas.

Foram revisadas principalmente:

- Início
- Disciplinas
- Tarefas
- Agenda
- Relatórios
- Assistente
- Meu Perfil
- Configurações

O erro crítico de HTML visível na interface foi corrigido.

## Validação

A suíte automatizada do projeto permanece como referência de regressão:

```text
88 testes
```

Durante as correções, os patches passaram a incluir:

- backup automático;
- validação de sintaxe;
- execução de testes;
- rollback em caso de falha.

## Pendências visuais finais

Ainda serão feitos pequenos ajustes antes dos prints definitivos da entrega:

- padronizar botões e detalhes de destaque em roxo Orbit;
- remover/ocultar a opção `Deploy` da barra superior do Streamlit sem prejudicar a sidebar;
- melhorar a visualização do campo de pesquisa;
- pequenos ajustes de contraste e espaçamento no modo claro.

## Entrega

Para a entrega no Classroom serão preparadas evidências de:

- todas as telas da aplicação;
- dicionário de dados;
- APIs do modelo de dados;
- CRUD funcionando;
- prints e/ou vídeo demonstrando o funcionamento.

---

Este documento registra o estado das correções realizadas até 06/10/2026 e as pendências finais antes da entrega.
