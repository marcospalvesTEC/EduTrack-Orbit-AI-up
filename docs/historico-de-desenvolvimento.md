# Histórico de desenvolvimento — EduTrack Orbit AI

> Registro consolidado até 18/09/2026 para acompanhamento acadêmico do projeto.

## 1. Objetivo do registro

Este documento reúne as principais entregas, decisões técnicas, validações e pendências do EduTrack Orbit AI. O histórico de commits e pull requests continua sendo a evidência cronológica oficial; este arquivo oferece uma leitura organizada para apresentação ao professor.

## 2. Tecnologias e organização

- Python 3.12+ e Streamlit no frontend.
- Xano e APIs REST JSON para autenticação e dados acadêmicos.
- OpenSpec para proposta, design, tarefas e rastreabilidade das mudanças.
- Ruff para lint e formatação.
- Pytest para testes automatizados.
- Git e GitHub com desenvolvimento separado por branches e pull requests.
- Temas claro e escuro baseados na identidade visual do EduTrack Orbit AI.

## 3. Linha de evolução

### Fundação do projeto

- Estrutura inicial de aplicação multipágina em Streamlit.
- Separação entre páginas, modelos, serviços, regras acadêmicas, componentes de interface e testes.
- Documentação inicial de arquitetura, negócio, plano de ensino e roteiro de tarefas.
- Definição da identidade “EduTrack Orbit AI” e do slogan “Organize, acompanhe e evolua”.

### Autenticação e integração

- Implementação da autenticação demonstrativa para permitir a apresentação local.
- Proteção das páginas internas por sessão autenticada.
- Integração posterior da autenticação com o Xano.
- Integração das disciplinas com endpoints do Xano e correção dos campos obrigatórios enviados à API.
- Manutenção de dados demonstrativos desacoplados para testes e apresentação.

### Correções de navegação

- Ajuste do recolhimento e reabertura da barra lateral.
- Inclusão progressiva das rotas de Dashboard, Disciplinas, Tarefas, Agenda e Perfil.
- Preservação do acesso às páginas em testes executados isoladamente.

### Dashboard desktop

- Aproximação visual da referência aprovada no Figma.
- Organização de métricas, progresso, gráficos e próximos compromissos.
- Adequação dos componentes aos temas claro e escuro.
- Criação de módulo e CSS específicos para manter a página separada das regras acadêmicas.

### Disciplinas desktop

- Cards de disciplinas com professor, progresso, tarefas e prazo.
- Fluxos de cadastro, resumo, edição, gerenciamento e exclusão.
- Barra de progresso na cor roxa da identidade.
- Correções de quebra de linha e contraste no modo escuro.
- Botão destrutivo de exclusão diferenciado em vermelho.
- Testes dedicados aos helpers e à apresentação de disciplinas.

### Tarefas desktop

- Quadro de tarefas organizado por “A fazer”, “Em andamento” e “Concluídas”.
- Fluxos de nova tarefa, detalhes, edição, conclusão, reabertura e exclusão.
- Ajuste dos campos de data para manter fundo escuro e somente borda clara no modo escuro.
- Indicador roxo na aba ativa dos detalhes da tarefa.
- Testes dedicados ao agrupamento, filtros e componentes da página.

### Agenda desktop

- Criação da página de Agenda e inclusão na navegação autenticada.
- Visualizações de calendário mensal e semana detalhada.
- Conversão de prazos de tarefas em eventos de entrega.
- Cadastro de eventos pessoais mantidos por usuário na sessão do protótipo.
- Categorias visuais para aula, entrega, sessão de foco e trabalho em grupo.
- Navegação entre meses e painel de próximos eventos.
- Correção dos campos de data, horário e seleção no modo escuro: fundo escuro, texto claro e borda clara.
- Cards de dias inteiramente clicáveis no calendário e na semana detalhada.
- Drawer lateral animado da direita para a esquerda, sem escurecer a Agenda.
- Drawer com detalhes completos dos eventos do dia e botão de fechamento ampliado.
- Card de trabalhos em grupo clicável, com listagem de todos os trabalhos no drawer.
- No calendário mensal, limite visual de dois eventos por dia e contador `(+N eventos)` no cabeçalho do card.
- Na semana detalhada, manutenção de todos os eventos visíveis no card.
- Tratamento equivalente nos temas claro e escuro.

### Perfil desktop

- Criação da página de Perfil com dados pessoais, preferências acadêmicas, resumo e segurança.
- Edição de nome, curso, instituição, semestre e foto de perfil em painel próprio.
- Formulários do tema escuro com superfície escura, texto claro e somente bordas claras.
- Botões roxos com texto branco nos temas claro e escuro.
- Botão de fechamento ampliado, à direita, preto no tema claro e branco no tema escuro.
- Ações de segurança mantidas na mesma linha, com “Alterar senha” à esquerda e “Encerrar sessões” à direita.
- Testes dedicados ao estado do perfil, métricas, foto e proteções visuais.

## 4. Decisões técnicas relevantes

### Separação entre interface e domínio

As páginas coordenam o fluxo do Streamlit, enquanto `src/ui/` concentra apresentação e CSS. Modelos, cálculos e acesso a dados permanecem separados para facilitar a futura substituição dos dados demonstrativos pelo backend Xano.

### Drawer em vez de navegação ou modal bloqueante

O detalhamento da Agenda inicialmente utilizava navegação e depois um modal central. O fluxo foi substituído por um drawer lateral porque preserva o contexto do calendário, não escurece a tela e permite consultar rapidamente dias com muitos eventos.

### Limite diferente entre as visualizações da Agenda

O calendário mensal exibe somente dois eventos por célula para evitar poluição visual. A semana detalhada utiliza cards mais altos e, portanto, mantém todos os eventos visíveis. Em ambos os casos, o card completo é o alvo de clique.

### Tema escuro

Campos e cards não utilizam preenchimento branco no modo escuro. O padrão adotado mantém superfícies em azul-marinho, textos claros, bordas visíveis e roxo para seleção, progresso e foco.

## 5. Qualidade e validação

Para as entregas de interface foram utilizados:

- `ruff check` para análise estática;
- `ruff format --check` para padronização;
- `pytest -q` para regressão automatizada;
- `git diff --check` para espaços inválidos e problemas de patch;
- revisão visual local nos temas claro e escuro;
- comparação iterativa com as referências do Figma.

Após a implementação do Perfil e o alinhamento das ações de segurança, a suíte registrou **57 testes aprovados**.

## 6. Arquivos principais da Agenda

- `pages/4_Agenda.py`: fluxo da página, cadastro e drawers laterais.
- `src/ui/figma_agenda.py`: modelos de apresentação, filtros, calendário e semana detalhada.
- `src/ui/figma_agenda.css`: temas, cards clicáveis, campos, drawer e responsividade.
- `tests/test_figma_agenda.py`: testes dos helpers e proteções de interação.
- `src/core/auth_session.py`: acesso à Agenda pela navegação autenticada.
- `tests/test_streamlit_auth.py`: verificação de proteção e renderização da rota.

## 7. Pendências conhecidas

- Finalizar os refinamentos menores de espaçamento e responsividade da Agenda.
- Validar o comportamento em diferentes navegadores e larguras de tela.
- Persistir eventos pessoais no Xano; atualmente eles permanecem na sessão do protótipo.
- Implementar edição e exclusão de eventos pessoais.
- Revisar acessibilidade por teclado e leitura por tecnologias assistivas.
- Implementar futuramente a versão mobile do Perfil; a etapa atual cobre somente desktop claro e escuro.
- Persistir dados, preferências e foto do Perfil no Xano; atualmente permanecem na sessão do protótipo.
- Continuar a padronização dos componentes compartilhados para reduzir CSS específico por página.

## 8. Próxima etapa

A próxima etapa prevista é planejar a integração com o **Xano**, mantendo a interface desktop já validada e substituindo gradualmente os dados de sessão por persistência real via API.
