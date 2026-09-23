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
- Inclusão progressiva das rotas de Disciplinas, Tarefas, Agenda e Perfil.
- Preservação do acesso às páginas em testes executados isoladamente.

### Início desktop

- Alinhamento da página inicial aos frames visuais `Dashboard / Desktop / Light` e `Dashboard / Desktop / Dark` do Figma, cuja navegação marca a opção Início como ativa.
- Hero com progresso real, próxima entrega e foco recomendado calculados a partir das tarefas da sessão.
- Cards de disciplinas, tarefas prioritárias, Agenda de hoje e progresso semanal abastecidos pelos dados reais do estudante.
- Links funcionais de acesso às telas completas de Disciplinas e Tarefas e painel clicável de dicas.
- Tema escuro com superfícies azul-marinho, textos claros, bordas visíveis e destaque roxo conforme o frame aprovado.
- Estados vazios preservados para contas novas sem disciplinas, tarefas ou eventos.

### Login desktop

- Substituição do portal genérico com três abas por uma tela dedicada em duas colunas.
- Formulário de acesso com campos organizados, botão roxo e atalhos funcionais para cadastro e recuperação de senha.
- Painel visual Orbit alinhado à identidade já aplicada no Cadastro.
- Temas claro e escuro com campos escuros, bordas claras e textos brancos no modo escuro.
- Rodapé funcional com Política de Privacidade, Termos de Uso e acesso à marca.
- Preservação da autenticação demonstrativa e da integração existente com o Xano.

### Termos de Uso e Política de Privacidade

- Criação de páginas públicas dedicadas para os Termos de Uso e a Política de Privacidade.
- Conteúdo organizado em seções legíveis, com identificação da versão e contexto acadêmico do protótipo.
- Navegação funcional a partir do Login e do Cadastro, com retorno direto à tela de acesso.
- Temas claro e escuro alinhados ao sistema visual Orbit, mantendo superfícies escuras, textos claros e bordas visíveis no modo escuro.
- Ligação entre os dois documentos para facilitar a consulta do estudante.

### Remoção do Dashboard analítico

- Remoção da rota `pages/1_Dashboard.py` e do respectivo item da navegação lateral.
- Consolidação da visão geral acadêmica na página Início, evitando destinos concorrentes com conteúdo semelhante.
- Manutenção das métricas internas compartilhadas pelo Início, Perfil, Assistente e Relatórios.
- Preservação da página Relatórios como área específica para análises, filtros, histórico e exportação.
- Atualização dos testes de autenticação e navegação para impedir o retorno acidental da rota removida.

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

### Cadastro desktop

- Implementação dos frames `Cadastro / Desktop / Light` e `Cadastro / Desktop / Dark` do Figma.
- Tela dedicada com identidade Orbit, formulário em duas colunas e painel visual da jornada acadêmica.
- Cadastro funcional preservando o serviço demonstrativo e a integração existente com o Xano.
- Campos de nome, e-mail, curso, instituição, senha, confirmação e aceite dos termos.
- Curso e instituição iniciais enviados ao estado do Perfil após a criação da conta.
- No tema escuro, superfícies e campos permanecem escuros, com textos e bordas claras.
- Botão principal roxo com texto branco nos dois temas.
- Pequeno espaçamento entre os campos para preservar leitura e áreas de clique independentes.
- Marca Orbit AI, Política de Privacidade e Termos de Uso transformados em controles clicáveis.
- Testes dedicados aos helpers, proteções visuais e composição completa do formulário.

### Recuperação de senha desktop

- Implementação dos frames `Recuperação / Desktop / Light` e `Recuperação / Desktop / Dark` do Figma.
- Tela dedicada com formulário de e-mail, aviso de link temporário e painel visual das três etapas.
- Resposta neutra para endereços conhecidos e desconhecidos, evitando revelar a existência de contas.
- Integração com o estado demonstrativo para liberar futuramente a etapa de redefinição local.
- No tema escuro, superfícies e campo permanecem escuros, com textos e bordas claras.
- Botão principal roxo com texto branco nos dois temas.
- Marca, retorno ao login, suporte, Política de Privacidade e Termos de Uso clicáveis.
- Ação de suporte reposicionada logo após o retorno ao login e botão de envio fixado em roxo.
- Testes dedicados à composição da tela, às regras visuais e à neutralidade da resposta.

### Redefinição de senha desktop

- Implementação dos frames `Redefinição / Desktop / Light` e `Redefinição / Desktop / Dark` do Figma.
- Tela dedicada com nova senha, confirmação, critérios em tempo real e aviso de sessão temporária.
- Fluxo demonstrativo conectado à recuperação, alterando de fato a senha da conta durante a sessão.
- Sessões ausentes ou expiradas são recusadas sem alterar credenciais.
- No tema escuro, campos e superfícies permanecem escuros, com bordas e textos claros.
- Botão principal roxo com texto branco nos dois temas e retorno funcional ao login.
- Testes dedicados aos critérios, à composição visual e à alteração da senha demonstrativa.

### Relatórios desktop

- Implementação dos frames `Relatórios / Desktop / Light` e `Relatórios / Desktop / Dark` do Figma.
- Inclusão da rota protegida de Relatórios na navegação autenticada.
- Filtros funcionais de período e disciplina, aplicados às métricas e aos demais blocos.
- Métricas calculadas com dados reais da sessão: progresso, tarefas concluídas, horas de estudo e média por disciplina.
- Desempenho por disciplina, distribuição das tarefas, insight do Orbit e histórico recente.
- Plano recomendado acessível por diálogo e construído conforme disciplinas e pendências atuais.
- Exportação funcional de relatório acadêmico em PDF, utilizando ReportLab.
- Suporte aos temas claro e escuro, com cards escuros, bordas visíveis e ações roxas no tema escuro.
- Testes dedicados aos cálculos, distribuição, geração do PDF e composição completa da página.

### Assistente Orbit desktop

- Implementação dos frames `Assistente / Desktop / Light` e `Assistente / Desktop / Dark` do Figma.
- Inclusão da rota protegida do Assistente na navegação autenticada.
- Conversa demonstrativa funcional com respostas determinísticas construídas a partir das disciplinas e tarefas da sessão.
- Sugestões rápidas clicáveis para planejamento semanal, consulta de atrasos e criação de sessão de foco.
- Painel lateral com contexto acadêmico, ações disponíveis e aviso explícito sobre confirmação prévia.
- Fluxo seguro de escrita: o Orbit apresenta uma prévia e somente adiciona a sessão de foco à Agenda depois da confirmação do estudante.
- Histórico da conversa e ações pendentes isolados por usuário durante a sessão.
- Suporte aos temas claro e escuro, mantendo superfícies e campos escuros, bordas claras e botões roxos com texto branco no tema escuro.
- Testes dedicados às respostas, isolamento por usuário, regras visuais e confirmação do evento na Agenda.

### Configurações desktop

- Implementação dos frames `Configurações / Desktop / Light` e `Configurações / Desktop / Dark` do Figma.
- Inclusão da rota protegida de Configurações na navegação autenticada.
- Preferências funcionais de aparência, notificações, Assistente Orbit AI, idioma, região e acessibilidade.
- Sincronização de tema, idioma e notificações com as preferências exibidas no Perfil.
- Confirmação antes de ações do Orbit e navegação por teclado mantidas como proteções obrigatórias.
- Pré-visualização imediata dos temas claro e escuro, com campos escuros, bordas claras e textos legíveis no tema escuro.
- Exportação funcional dos dados públicos, disciplinas, tarefas e preferências em JSON, sem senha ou token de sessão.
- Ações de privacidade, revisão de dispositivos e exclusão protegida com retorno visível ao usuário.
- Configurações isoladas por conta durante a sessão demonstrativa.
- Testes dedicados à persistência, exportação segura, regras visuais e sincronização com o Perfil.

### Suporte e Contato desktop

- Implementação da página pública `Suporte / Desktop` nos temas claro e escuro.
- Formulário com nome, e-mail, categoria, assunto e descrição da solicitação.
- Categorias de suporte para acesso, disciplinas, tarefas, agenda, perfil e outros assuntos.
- Validação local do e-mail e do conteúdo mínimo antes de registrar a solicitação.
- Envio estritamente demonstrativo, com aviso explícito de que nenhuma mensagem externa foi enviada.
- Perguntas frequentes sobre acesso, dados da sessão demonstrativa e comunicação segura de erros.
- Atalhos funcionais para recuperação de senha, Termos de Uso, Política de Privacidade e retorno ao Login.
- Substituição do antigo diálogo de suporte da Recuperação por navegação para a nova página pública.
- Tema escuro com superfícies e campos escuros, bordas claras, textos brancos e botão roxo com texto branco.
- Testes dedicados à renderização pública, validação do formulário, envio demonstrativo, tema escuro e integração com a Recuperação.

### Refinamento final do Perfil desktop

- Ajuste da grade para que os cards de Preferências acadêmicas e Segurança ocupem toda a largura disponível.
- Correção da causa que mantinha `Encerrar sessões` visualmente no centro da página: o card de Segurança estava limitado à coluna direita da grade.
- Manutenção das duas ações de segurança na mesma linha, com `Alterar senha` na extremidade esquerda e `Encerrar sessões` na extremidade direita.
- Preservação dos botões roxos com texto branco nos temas claro e escuro.
- Teste de regressão atualizado para proteger a largura dos cards e o alinhamento horizontal das ações.

### Integração da barra lateral Orbit

- Substituição da composição longa e fragmentada do Streamlit por uma barra lateral compartilhada entre todas as páginas autenticadas.
- Marca EduTrack Orbit AI posicionada no topo com logotipo oficial e o slogan `Organize, acompanhe e evolua`.
- Controle de tema reposicionado dentro do shell autenticado, mantendo a preferência durante a sessão.
- Navegação unificada para Início, Disciplinas, Tarefas, Agenda, Relatórios, Assistente, Perfil e Configurações.
- Ícones padronizados com Material Symbols e destaque roxo para a rota ativa.
- Ferramentas de demonstração recolhidas em um único expansor para reduzir a altura e a poluição visual da barra.
- Conta ativa e botão roxo de saída mantidos na parte inferior da estrutura.
- Estilos compartilhados para os temas claro e escuro, incluindo bordas, textos, estados de foco e botão de reabertura da barra.
- Teste de regressão para marca, tema, destinos, ferramentas demonstrativas e logout.
- Validação visual automatizada registrada como bloqueada porque o navegador da sessão recusou o servidor Streamlit local; a conferência final permanece para o navegador local.

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

Após a remoção do Dashboard analítico e consolidação da visão geral no Início, a suíte registrou **80 testes aprovados**.

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
- Corrigir no refinamento final a responsividade das telas de Cadastro, Recuperação e Redefinição.

## 8. Próxima etapa

A próxima etapa prevista é executar o **refinamento visual conjunto das telas desktop**, corrigindo diferenças menores de espaçamento e alinhamento registradas durante a implementação. A responsividade e as versões mobile permanecem para a etapa posterior.
