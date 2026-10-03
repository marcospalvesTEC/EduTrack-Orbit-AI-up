# Tarefa 06 --- Exploração de Templates Gratuitos

## Status

🟡 **EM ANDAMENTO** --- pesquisa no Figma e no Xano concluída. Restam
adicionar os links diretos dos templates do Figma e realizar o fluxo
Git/PR.

## Objetivo

Explorar referências gratuitas do ecossistema do Figma e do Xano que
possam contribuir para a evolução do **EduTrack Orbit AI**, analisando
soluções existentes sem copiar integralmente outros projetos.

A pesquisa busca identificar boas práticas de interface, organização de
informações acadêmicas, gerenciamento de tarefas e estruturação de
backend que possam ser adaptadas à identidade visual e à arquitetura do
EduTrack Orbit AI.

------------------------------------------------------------------------

## 1. Referências do Figma Community

### 1.1 Student Dashboard LMS Application

**Criadora:** Sakshi Parashar\
**Plataforma:** Figma Community\
**Categoria:** Dashboard acadêmico / LMS\
**Link:** *Adicionar aqui a URL direta do template no Figma Community*

#### O que foi observado

O template apresenta um dashboard acadêmico organizado com informações
importantes para o estudante em uma única tela, incluindo próxima aula,
frequência, quantidade de disciplinas, módulos disponíveis, professor,
horário, conteúdos, materiais e indicadores de progresso.

#### Aplicação no EduTrack Orbit AI

A principal referência é a **hierarquia das informações acadêmicas**. O
template mostra uma forma simples de apresentar primeiro os indicadores
mais importantes e, logo abaixo, detalhar as disciplinas.

No EduTrack, essa referência pode contribuir para a organização do
Dashboard, visualização das disciplinas, indicadores de progresso,
apresentação das informações em cards e acesso rápido aos dados
acadêmicos.

A proposta não é copiar o layout. O EduTrack continuará utilizando sua
própria identidade visual, incluindo a linguagem Orbit, a paleta
predominante em roxo e os elementos visuais próprios do projeto.

#### Evidência

`docs/pesquisa/img/figma-student-dashboard.png`

------------------------------------------------------------------------

### 1.2 Kanban Board Application

**Plataforma:** Figma Community\
**Categoria:** Gerenciamento de tarefas / Kanban\
**Link:** *Adicionar aqui a URL direta do template no Figma Community*

#### O que foi observado

O template organiza tarefas através de um quadro Kanban dividido em **To
Do**, **In Progress**, **Review** e **Done**.

Os cards apresentam informações como prioridade, prazo, categoria,
responsável, comentários e anexos. A interface também possui busca,
filtros, configurações e criação de novas tarefas.

#### Aplicação no EduTrack Orbit AI

Essa referência pode contribuir principalmente para a evolução da área
de **Tarefas**, com separação por status, identificação visual de
prioridades, apresentação clara dos prazos, tags para disciplinas,
filtros, busca rápida e cards mais informativos.

O conceito de Kanban pode ser utilizado futuramente como uma
visualização alternativa das tarefas, sem substituir necessariamente a
visualização atual do EduTrack.

#### Evidência

`docs/pesquisa/img/figma-kanban-board.png`

------------------------------------------------------------------------

## 2. Comparação das referências do Figma

  -----------------------------------------------------------------------
  Referência                          Principal inspiração para o
                                      EduTrack
  ----------------------------------- -----------------------------------
  Student Dashboard LMS Application   Dashboard, disciplinas, indicadores
                                      e progresso acadêmico

  Kanban Board Application            Tarefas, prioridades, prazos,
                                      status, filtros e organização
                                      visual
  -----------------------------------------------------------------------

As duas referências foram escolhidas porque resolvem problemas
diferentes dentro do EduTrack Orbit AI. O primeiro template está mais
relacionado à **experiência acadêmica e ao acompanhamento das
disciplinas**, enquanto o segundo apresenta boas práticas para
**organização e acompanhamento de tarefas**.

------------------------------------------------------------------------

## 3. Exploração do Xano

### 3.1 Pesquisa de templates

Na biblioteca atual de templates do Xano foram realizadas buscas pelos
termos sugeridos na atividade.

-   `Authentication` --- nenhum template encontrado pela busca.
-   `Task` --- nenhum template encontrado pela busca.

Como os termos exatos não retornaram resultados, foi analisado um
template atual que contém elementos de arquitetura relacionados aos
objetivos da atividade.

### 3.2 Sales Pipeline CRM

**Plataforma:** Xano Templates\
**Template:** Sales Pipeline CRM\
**Link:** https://www.xano.com/templates/sales-pipeline-crm/

O template foi utilizado apenas como **referência de arquitetura**.
Nenhum conteúdo foi instalado ou importado para o workspace do EduTrack
Orbit AI.

#### Estrutura observada

Na página do template são apresentados:

-   **9 tabelas**;
-   **31 APIs**;
-   **10 funções**;
-   uma `auth API` com `login`, `me` e `signup`;
-   APIs separadas por responsabilidade;
-   camada de **Business logic**;
-   camada de dados com diferentes tabelas relacionadas.

A visualização do template demonstra uma separação entre aplicação
cliente, APIs, regras de negócio e armazenamento dos dados.

#### Aplicação no EduTrack Orbit AI

Embora o template seja voltado para CRM, a arquitetura apresentada serve
como referência para a organização do backend do EduTrack.

Uma possível correspondência conceitual é:

  Estrutura observada   Aplicação possível no EduTrack
  --------------------- ---------------------------------------------------
  `auth API`            Login, cadastro e identificação do estudante
  APIs separadas        Disciplinas, tarefas, perfil e demais recursos
  Business logic        Regras acadêmicas e processamento das informações
  Data                  Tabelas e relacionamentos do banco de dados

O principal aprendizado não está nas regras específicas de CRM, mas na
**separação de responsabilidades do backend**.

#### Evidência

`docs/pesquisa/img/xano-sales-pipeline-crm.png`

------------------------------------------------------------------------

## 4. Principais aprendizados

A pesquisa mostrou que referências de frontend e backend podem
contribuir de maneiras diferentes para o EduTrack Orbit AI.

No **Student Dashboard LMS Application**, o principal aprendizado está
na hierarquia das informações acadêmicas e na concentração de dados
relevantes em cards.

No **Kanban Board Application**, o destaque está na visualização do
estado de cada tarefa, permitindo identificar rapidamente atividades
pendentes, em andamento, em revisão e concluídas.

No **Sales Pipeline CRM**, a principal referência está na arquitetura do
backend, especialmente na separação entre autenticação, APIs, regras de
negócio e dados.

Para o EduTrack Orbit AI, essas referências podem ser combinadas sem
abandonar a identidade própria do projeto: uma interface acadêmica
organizada, um gerenciamento de tarefas mais visual e um backend
dividido de forma clara por responsabilidades.

------------------------------------------------------------------------

## 5. Decisões para o EduTrack Orbit AI

A pesquisa não representa uma substituição do design ou da arquitetura
atual do projeto.

As referências serão utilizadas como benchmarking para avaliar possíveis
melhorias em:

-   Dashboard;
-   Disciplinas;
-   Tarefas;
-   indicadores de progresso;
-   filtros e busca;
-   organização das informações;
-   autenticação;
-   separação das APIs;
-   regras de negócio;
-   estrutura de dados.

A identidade visual própria do **EduTrack Orbit AI** será preservada.

------------------------------------------------------------------------

## 6. Evidências

Estrutura planejada para o repositório:

``` text
docs/
└── pesquisa/
    ├── referencias.md
    └── img/
        ├── figma-student-dashboard.png
        ├── figma-kanban-board.png
        └── xano-sales-pipeline-crm.png
```

------------------------------------------------------------------------

## 7. Texto para entrega no Classroom

A principal percepção durante a exploração dos templates foi que
diferentes referências podem contribuir para partes específicas do
EduTrack Orbit AI. O dashboard acadêmico mostrou como organizar
disciplinas, progresso e informações importantes de maneira clara; o
modelo Kanban apresentou uma forma visual de acompanhar tarefas por
status e prioridade; e a análise do template Sales Pipeline CRM no Xano
mostrou a importância de separar autenticação, APIs, regras de negócio e
dados no backend. As referências serão utilizadas como benchmarking, sem
copiar os projetos, preservando a identidade e a arquitetura própria do
EduTrack Orbit AI.

------------------------------------------------------------------------

## Checklist da Tarefa 06

-   [x] Selecionar pelo menos dois templates relevantes no Figma
    Community.
-   [x] Analisar o Student Dashboard LMS Application.
-   [x] Analisar o Kanban Board Application.
-   [ ] Adicionar os links diretos dos dois templates do Figma.
-   [x] Explorar a biblioteca atual de templates do Xano.
-   [x] Registrar as buscas por Authentication e Task.
-   [x] Analisar o Sales Pipeline CRM como referência de arquitetura.
-   [x] Criar a documentação `docs/pesquisa/referencias.md`.
-   [ ] Salvar as três evidências em `docs/pesquisa/img/`.
-   [ ] Criar branch `docs/referencias-templates`.
-   [ ] Fazer commit e push.
-   [ ] Abrir Pull Request.
-   [ ] Fazer merge na `main`.
