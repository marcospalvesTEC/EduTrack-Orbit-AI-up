## Context

O projeto possui um protótipo multipágina em Streamlit, com `app.py` como página Início e páginas de Disciplinas e Tarefas, dados simulados, modelos acadêmicos, cálculos e módulos de interface em `src/ui/`. Consulte `proposal.md` para a motivação e `specs/orbit-interface/spec.md` para os comportamentos exigidos.

A atualização atravessa várias páginas e componentes. Por isso, a identidade visual, a responsividade, a acessibilidade e os estados da interface precisam ser centralizados para evitar estilos divergentes.

As limitações atuais do Streamlit também devem ser consideradas: parte da aparência será controlada pela configuração nativa e parte por estilos aplicados pela aplicação. A solução deve manter o projeto simples, executável localmente e preparado para uma integração futura com Xano.

## Goals / Non-Goals

**Goals:**

- Centralizar cores, tipografia, espaçamentos, bordas, sombras e estados em um sistema visual reutilizável.
- Aplicar a identidade EduTrack Orbit AI às páginas existentes.
- Organizar componentes compartilhados para cabeçalhos, cards, indicadores, status, estados vazios e mascotes.
- Adaptar navegação e conteúdo para computador, tablet e celular.
- Manter gráficos e informações acadêmicas legíveis nos temas claro e escuro.
- Preservar os modelos, cálculos, filtros e dados simulados existentes.
- Criar uma base visual que possa ser reutilizada nas futuras páginas do MVP.

**Non-Goals:**

- Implementar autenticação, banco de dados ou endpoints do Xano.
- Criar funcionalidades completas de Agenda, Relatórios, Perfil, Configurações ou Assistente.
- Implementar inteligência artificial generativa.
- Implementar persistência definitiva das preferências do usuário.
- Alterar as regras acadêmicas ou os modelos de domínio existentes.
- Implementar animações complexas ou modelos tridimensionais em tempo real.

## Decisions

### 1. Evoluir a estrutura Streamlit existente

A atualização será aplicada ao projeto atual, preservando `app.py`, o diretório `pages/` e os módulos em `src/`.

Isso reduz retrabalho e mantém os cálculos, filtros, modelos e dados simulados já validados.

**Alternativa considerada:** reconstruir a interface em outro framework web. Essa opção aumentaria o escopo, exigiria nova arquitetura e atrasaria a validação do MVP.

### 2. Centralizar o sistema visual em `src/ui/theme.py`

Cores, variáveis de tema, tipografia, raios de borda, sombras, espaçamentos e estilos responsivos serão definidos em um único módulo.

As páginas solicitarão a aplicação do tema sem repetir grandes blocos de estilo. A configuração base continuará em `.streamlit/config.toml`.

**Alternativa considerada:** manter estilos independentes em cada página. Essa abordagem facilitaria ajustes locais, mas produziria duplicação e inconsistências.

### 3. Reutilizar componentes em `src/ui/components.py`

Elementos recorrentes serão representados por funções reutilizáveis, incluindo:

- cabeçalho com identidade e slogan;
- cards de métricas;
- indicadores de prioridade e status;
- cards de disciplina e tarefa;
- estados vazios;
- avisos e mensagens;
- bloco de mascote;
- descrição textual de gráficos.

Cada componente receberá dados como entrada e não dependerá diretamente da origem desses dados.

**Alternativa considerada:** construir cada tela somente com chamadas diretas do Streamlit. Isso reduziria a quantidade inicial de abstrações, mas dificultaria a manutenção do padrão visual.

### 4. Separar apresentação, gráficos e regras acadêmicas

`src/ui/` continuará responsável pela apresentação. Regras de progresso, filtros e métricas permanecerão em `src/core/`, enquanto os dados simulados continuarão em `src/services/`.

Os gráficos serão preparados em `src/ui/charts.py` e receberão dados já calculados.

**Alternativa considerada:** calcular indicadores dentro das páginas. Essa opção criaria acoplamento entre interface e regras de negócio.

### 5. Utilizar tokens semânticos de cor

As cores serão identificadas por função, como principal, progresso, sucesso, atenção, prazo vencido, superfície, borda e texto.

As páginas não deverão depender de códigos de cor espalhados pelo projeto. Estados sempre combinarão cor com texto ou ícone.

**Alternativa considerada:** aplicar diretamente a paleta em cada componente. Essa abordagem tornaria futuras mudanças de tema mais trabalhosas.

### 6. Implementar temas claro e escuro por variáveis visuais

Os dois temas compartilharão a mesma estrutura de componentes e usarão conjuntos diferentes de valores para superfícies, textos, bordas e gráficos.

A seleção ficará disponível na interface durante o protótipo. Quando a preferência do dispositivo não puder ser detectada com confiabilidade, será usado um tema padrão legível.

**Alternativa considerada:** depender exclusivamente do tema nativo do Streamlit. Essa escolha não permitiria controlar toda a identidade Orbit de maneira consistente.

### 7. Adaptar o layout com colunas flexíveis e estilos responsivos

As páginas usarão contêineres e colunas que possam reorganizar o conteúdo conforme a largura disponível.

Em telas amplas, a navegação permanecerá lateral. Em telas reduzidas, a apresentação será compactada e os principais destinos ficarão acessíveis por uma navegação adequada ao espaço disponível.

Conteúdos secundários poderão ser empilhados abaixo dos conteúdos principais.

**Alternativa considerada:** manter o mesmo layout em todas as larguras. Isso prejudicaria a leitura e a interação em celulares.

### 8. Atualizar primeiro as páginas já funcionais

A implementação seguirá esta ordem:

1. tema e tokens visuais;
2. componentes compartilhados;
3. página inicial e identidade;
4. Disciplinas;
5. Tarefas;
6. ajustes responsivos e de acessibilidade.

As páginas futuras poderão aparecer como destinos planejados somente quando houver uma experiência clara para o usuário, sem simular funcionalidades concluídas.

**Alternativa considerada:** criar todas as páginas do questionário nesta mudança. Isso misturaria atualização visual com diversos módulos funcionais ainda não especificados.

### 9. Tratar os robôs como recursos de apresentação

O robô principal e as skins de axolote, raposa e lagosta-boxeadora serão armazenados como recursos estáticos otimizados.

Os componentes responsáveis por exibi-los deverão receber texto alternativo e limitar suas dimensões para que não bloqueiem controles ou informações.

**Alternativa considerada:** usar animações ou modelos 3D em tempo real. Essa opção aumentaria carregamento, complexidade e dependências sem benefício necessário para o protótipo.

### 10. Manter os dados simulados desacoplados da interface

A interface continuará consumindo os serviços simulados atuais. Componentes receberão estruturas de dados que possam futuramente ser abastecidas pelo Xano sem reformulação visual completa.

Elementos que representem dados demonstrativos deverão ser apresentados dentro do contexto de protótipo.

**Alternativa considerada:** integrar Xano durante esta mudança. Isso dificultaria separar falhas visuais de falhas de autenticação ou rede.

### 11. Incorporar acessibilidade desde os componentes base

Controles deverão possuir rótulos compreensíveis, foco visível e ordem coerente. Gráficos terão títulos, rótulos e resumo textual. Status não dependerão apenas de cores.

O contraste será revisado nos dois temas e o layout deverá continuar utilizável com ampliação de texto.

**Alternativa considerada:** revisar acessibilidade somente ao final. Essa abordagem exigiria retrabalho em todos os componentes.

### 12. Evitar novas dependências sem necessidade comprovada

A implementação priorizará Streamlit e as bibliotecas já declaradas no projeto. Uma dependência adicional só será incluída caso resolva uma necessidade que não possa ser atendida de forma sustentável pela estrutura atual.

**Alternativa considerada:** adicionar bibliotecas para cada componente visual. Isso elevaria o custo de manutenção e o risco de incompatibilidades.

## Risks / Trade-offs

- [Estilos personalizados podem ser afetados por atualizações do Streamlit] → Concentrar seletores e estilos em `src/ui/theme.py` e testar as páginas principais após mudanças de versão.
- [A navegação inferior pode ter limitações no Streamlit] → Priorizar uma navegação compacta e funcional, mantendo rotas acessíveis mesmo quando a apresentação exata precisar ser adaptada.
- [Tema automático pode não detectar o dispositivo em todos os ambientes] → Disponibilizar seleção manual e aplicar um tema padrão legível.
- [Imagens dos mascotes podem aumentar o tempo de carregamento] → Otimizar dimensões e formatos e carregar somente os recursos necessários para cada tela.
- [Personalização visual excessiva pode prejudicar acessibilidade] → Validar contraste, foco, texto alternativo e leitura sem dependência exclusiva de cor.
- [Dados simulados podem ser confundidos com dados reais] → Manter contexto claro de protótipo até a integração com Xano.
- [Alterações compartilhadas podem afetar todas as páginas] → Aplicar mudanças de maneira incremental e revisar cada página após ajustes nos componentes base.
- [A interface móvel pode divergir das referências visuais] → Preservar hierarquia, legibilidade e acesso às funções como critérios principais da adaptação.

## Migration Plan

1. Registrar o estado atual da aplicação e confirmar que a branch ativa é `feature/implement-orbit-ui`.
2. Atualizar os tokens e temas compartilhados.
3. Refatorar componentes reutilizáveis sem alterar as regras acadêmicas.
4. Aplicar a nova identidade à página inicial.
5. Migrar Início, Disciplinas e Tarefas individualmente.
6. Adicionar e otimizar os recursos visuais da marca.
7. Revisar responsividade, contraste, navegação por teclado e descrições de gráficos.
8. Executar os testes existentes e realizar validação visual das páginas principais.
9. Validar os artefatos OpenSpec antes do commit.
10. Em caso de regressão, reverter os commits da interface na branch sem alterar os modelos e serviços existentes.
