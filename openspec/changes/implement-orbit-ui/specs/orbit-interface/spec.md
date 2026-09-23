## Purpose

Definir a experiência visual, responsiva e acessível do EduTrack Orbit AI, garantindo que estudantes consigam navegar e interpretar informações acadêmicas com consistência em diferentes dispositivos e temas.

## ADDED Requirements

### Requirement: Identidade do produto

O sistema SHALL apresentar o nome “EduTrack Orbit AI”, o slogan “Organize, acompanhe e evolua” e um robô cúbico pixelado como elemento principal da identidade visual.

#### Scenario: Exibição da identidade

- **WHEN** o estudante acessar a página inicial
- **THEN** o sistema exibirá o nome EduTrack Orbit AI, o slogan definido e o elemento visual da marca

### Requirement: Sistema visual consistente

O sistema SHALL aplicar uma identidade visual consistente em páginas, cards, botões, formulários, indicadores, gráficos, mensagens e estados de tarefas.

#### Scenario: Navegação entre páginas

- **WHEN** o estudante navegar entre Início, Disciplinas e Tarefas
- **THEN** o sistema manterá padrões consistentes de cores, tipografia, espaçamento, bordas e componentes

### Requirement: Cores semânticas

O sistema SHALL utilizar azul-petróleo como cor principal, roxo para progresso e inteligência, verde para conclusão, laranja para atenção e vermelho para prazo vencido.

#### Scenario: Exibição de status

- **WHEN** o sistema apresentar o status de uma tarefa
- **THEN** a cor correspondente será acompanhada por texto ou ícone que permita identificar o significado sem depender somente da cor

### Requirement: Temas de interface

O sistema SHALL oferecer temas claro e escuro e SHALL permitir a seleção do tema pelo estudante.

#### Scenario: Alteração manual de tema

- **WHEN** o estudante selecionar o tema claro ou escuro
- **THEN** o sistema aplicará o tema escolhido aos componentes visíveis da interface

#### Scenario: Preferência inicial do dispositivo

- **WHEN** não existir uma preferência de tema definida pelo estudante
- **THEN** o sistema utilizará a preferência disponível no dispositivo ou apresentará um tema padrão legível

### Requirement: Navegação responsiva

O sistema SHALL adaptar sua navegação ao espaço disponível na tela, mantendo acesso às páginas principais.

#### Scenario: Navegação em tela ampla

- **WHEN** o aplicativo for exibido em uma tela ampla
- **THEN** o sistema apresentará a navegação principal em uma barra lateral

#### Scenario: Navegação em tela reduzida

- **WHEN** o aplicativo for exibido em uma tela reduzida
- **THEN** o sistema apresentará uma navegação compacta adequada ao dispositivo

### Requirement: Visão geral acadêmica no Início

O sistema SHALL apresentar na página Início um resumo visual das disciplinas, tarefas, progresso acadêmico e próximos prazos disponíveis nos dados atuais.

#### Scenario: Início com dados

- **WHEN** existirem dados acadêmicos disponíveis
- **THEN** o estudante visualizará indicadores e gráficos organizados por importância e com identificação textual

#### Scenario: Início sem dados

- **WHEN** não existirem dados acadêmicos disponíveis
- **THEN** o sistema exibirá uma orientação e uma ação para cadastrar o primeiro item

### Requirement: Listagem de disciplinas

O sistema SHALL apresentar as disciplinas de forma legível, permitindo que o estudante identifique nome, professor, progresso e informações acadêmicas disponíveis.

#### Scenario: Consulta de disciplinas

- **WHEN** o estudante acessar a página de Disciplinas
- **THEN** o sistema exibirá as disciplinas em componentes consistentes e adaptáveis ao tamanho da tela

### Requirement: Listagem de tarefas

O sistema SHALL apresentar as tarefas com título, disciplina, prazo, prioridade e status disponíveis, destacando os itens que requerem atenção.

#### Scenario: Consulta de tarefas

- **WHEN** o estudante acessar a página de Tarefas
- **THEN** o sistema exibirá as tarefas com seus estados e informações essenciais claramente identificados

#### Scenario: Tarefa com prazo vencido

- **WHEN** uma tarefa ultrapassar seu prazo sem estar concluída
- **THEN** o sistema a identificará como “Prazo vencido” ou “Requer atenção” com texto ou ícone e indicação visual correspondente

### Requirement: Acessibilidade da interface

O sistema MUST permitir navegação por teclado, manter contraste legível e fornecer identificação textual para informações transmitidas visualmente.

#### Scenario: Navegação por teclado

- **WHEN** o estudante utilizar somente o teclado
- **THEN** os controles interativos principais poderão receber foco e ser acionados em uma ordem compreensível

#### Scenario: Interpretação de gráfico

- **WHEN** um gráfico for apresentado
- **THEN** o sistema disponibilizará título, rótulos ou descrição textual que comunique sua informação principal

### Requirement: Estados vazios orientados

O sistema SHALL apresentar orientação contextual e uma ação útil quando uma página não possuir dados.

#### Scenario: Página sem registros

- **WHEN** uma listagem não possuir registros
- **THEN** o sistema exibirá uma mensagem explicativa, um elemento visual apropriado e uma ação para cadastrar o primeiro item

### Requirement: Mascotes de apoio

O sistema SHALL permitir o uso de robôs cúbicos com skins de mascotes como elementos de apoio visual, incluindo axolote, raposa e lagosta-boxeadora.

#### Scenario: Exibição de mascote

- **WHEN** um mascote for exibido em uma página
- **THEN** ele reforçará a comunicação da interface sem ocultar conteúdo, impedir navegação ou substituir informações textuais

### Requirement: Dados de demonstração identificáveis

O sistema SHALL continuar operando com dados simulados durante esta etapa da interface.

#### Scenario: Uso do protótipo visual

- **WHEN** o estudante acessar uma tela abastecida com dados simulados
- **THEN** o sistema permitirá avaliar a interface sem exigir conexão com o Xano
