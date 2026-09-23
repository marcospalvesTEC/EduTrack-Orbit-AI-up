## Why

O protótipo atual em Streamlit possui a estrutura funcional inicial, mas ainda não representa a identidade visual, a navegação responsiva e a experiência planejada para o EduTrack Orbit AI. Esta mudança transforma o protótipo em uma interface acadêmica consistente, acessível e preparada para a evolução das funcionalidades do MVP.

## What Changes

- Atualizar a identidade do aplicativo para **EduTrack Orbit AI**, acompanhada do slogan “Organize, acompanhe e evolua”.
- Aplicar um sistema visual consistente com azul-petróleo, roxo, verde, laranja e vermelho para estados e indicadores.
- Criar temas claro e escuro, respeitando a preferência do dispositivo quando possível.
- Padronizar cards, botões, formulários, indicadores, gráficos, mensagens e estados vazios.
- Implementar navegação responsiva com barra lateral em telas maiores e navegação adaptada em telas menores.
- Atualizar as telas existentes de Início, Disciplinas e Tarefas.
- Preparar a navegação e a identidade visual para Agenda, Relatórios, Perfil, Configurações e Assistente.
- Incorporar o robô cúbico e pixelado como elemento da marca.
- Preparar componentes visuais para futuras skins de mascotes, incluindo axolote, raposa e lagosta-boxeadora.
- Melhorar acessibilidade com contraste adequado, identificação textual de estados, navegação por teclado e descrições para gráficos.
- Manter os dados simulados nesta etapa, deixando a integração com Xano para uma mudança posterior.

## Capabilities

### New Capabilities

- `orbit-interface`: Define a identidade visual, os temas, a navegação responsiva, os componentes reutilizáveis, os estados de interface, a acessibilidade e a apresentação das telas acadêmicas do EduTrack Orbit AI.

### Modified Capabilities

Nenhuma. O projeto ainda não possui especificações principais publicadas em `openspec/specs/`.

## Impact

- Código Streamlit em `app.py` e no diretório `pages/`.
- Componentes, gráficos e temas existentes em `src/ui/`.
- Configuração visual em `.streamlit/config.toml`.
- Recursos de marca e mascotes que forem adicionados ao projeto.
- Testes relacionados à renderização, navegação e comportamento dos componentes.
- Não haverá alteração de APIs ou integração com o Xano nesta mudança.
