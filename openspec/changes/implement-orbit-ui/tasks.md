## 1. Base visual e identidade

- [ ] 1.1 Revisar `src/ui/theme.py` e `.streamlit/config.toml`, registrar os tokens de cores, superfícies, textos, bordas, sombras e espaçamentos dos temas claro e escuro e verificar visualmente que ambos mantêm contraste legível
- [x] 1.2 Atualizar o nome para “EduTrack Orbit AI” e o slogan para “Organize, acompanhe e evolua” e verificar que a identidade aparece corretamente na página inicial
- [ ] 1.3 Adicionar o recurso otimizado do robô cúbico pixelado e verificar que a imagem carrega sem distorção ou impacto perceptível no carregamento
- [ ] 1.4 Preparar a estrutura de recursos para as skins de axolote, raposa e lagosta-boxeadora e verificar que o componente aceita cada opção sem alterar o layout

## 2. Componentes compartilhados

- [ ] 2.1 Refatorar `src/ui/components.py` para oferecer cabeçalho, card de métrica, indicador de status, estado vazio e bloco de mascote reutilizáveis e verificar seu uso em pelo menos duas páginas
- [x] 2.2 Implementar indicadores semânticos de prioridade e status combinando cor com texto ou ícone e verificar todos os estados disponíveis com dados simulados
- [ ] 2.3 Implementar estados vazios com orientação e ação de primeiro cadastro e verificar a renderização com listas vazias de disciplinas e tarefas
- [ ] 2.4 Padronizar botões, formulários, avisos, bordas e estados de foco e verificar consistência visual nas páginas principais

## 3. Navegação e responsividade

- [x] 3.1 Atualizar a navegação para apresentar barra lateral em telas amplas e verificar acesso à página inicial, Disciplinas e Tarefas
- [ ] 3.2 Criar uma apresentação compacta da navegação para telas reduzidas e verificar que os destinos principais continuam acessíveis
- [ ] 3.3 Adaptar colunas, cards, tabelas e blocos informativos para reorganização em telas menores e verificar o aplicativo em larguras de celular, tablet e computador
- [ ] 3.4 Verificar que nenhuma imagem, gráfico, texto ou mascote produz rolagem horizontal desnecessária nas páginas principais

## 4. Atualização das páginas

- [x] 4.1 Atualizar `app.py` com a identidade Orbit, introdução do protótipo e acesso claro às áreas principais e verificar a página inicial em ambos os temas
- [x] 4.2 Remover `pages/1_Dashboard.py` e consolidar a visão geral acadêmica na página Início
- [x] 4.3 Atualizar `pages/2_Disciplinas.py` com componentes consistentes para nome, professor, progresso e informações disponíveis e verificar a listagem em diferentes quantidades de disciplinas
- [x] 4.4 Atualizar `pages/3_Tarefas.py` com título, disciplina, prazo, prioridade e status claramente identificados e verificar a exibição de tarefas pendentes, concluídas e com prazo vencido
- [x] 4.5 Manter os dados simulados desacoplados das páginas e verificar que os serviços atuais continuam abastecendo a interface sem conexão com o Xano
- [x] 4.6 Criar `pages/4_Agenda.py` com calendário mensal, semana detalhada, cadastro de eventos, próximos eventos e navegação autenticada
- [x] 4.7 Implementar detalhes da Agenda em drawer lateral não bloqueante, com cards completos clicáveis, suporte aos temas claro e escuro e detalhamento de trabalhos em grupo
- [x] 4.8 Limitar o calendário mensal a dois eventos por célula com contador de excedentes, mantendo todos os eventos na semana detalhada
- [x] 4.9 Implementar a página de Perfil desktop nos temas claro e escuro, com edição de dados, foto, preferências e senha
- [x] 4.10 Alinhar as ações de segurança do Perfil na mesma linha, em extremos opostos do card
- [x] 4.11 Implementar a tela de Cadastro desktop nos temas claro e escuro, com formulário funcional e acesso pelo portal de autenticação
- [x] 4.12 Implementar a tela de Recuperação de senha desktop nos temas claro e escuro, com resposta neutra, suporte e retorno ao login
- [x] 4.13 Implementar a tela de Redefinição de senha desktop nos temas claro e escuro, com critérios de senha e fluxo demonstrativo funcional
- [x] 4.14 Implementar Relatórios desktop nos temas claro e escuro, com filtros, métricas, insight, histórico e exportação funcional em PDF
- [x] 4.15 Implementar o Assistente Orbit desktop nos temas claro e escuro, com conversa demonstrativa, contexto acadêmico e confirmação antes de ações que alterem dados
- [x] 4.16 Implementar Configurações desktop nos temas claro e escuro, com preferências funcionais, exportação segura e sincronização com o Perfil
- [x] 4.17 Alinhar a página Início aos frames claro e escuro do Figma
- [x] 4.18 Remover o Dashboard analítico da navegação e adicionar proteção automatizada contra o retorno da rota
- [x] 4.19 Substituir o Login genérico por uma tela desktop em duas colunas, com temas claro e escuro e atalhos funcionais
- [x] 4.20 Implementar páginas públicas de Termos de Uso e Política de Privacidade, acessíveis pelo Login e pelo Cadastro
- [x] 4.21 Implementar Suporte e Contato desktop público, com formulário demonstrativo, FAQ, atalhos seguros e temas claro e escuro
- [x] 4.22 Refinar o Perfil para que Preferências e Segurança ocupem a largura completa, mantendo Alterar senha e Encerrar sessões em extremidades opostas da mesma linha
- [x] 4.23 Integrar a barra lateral autenticada ao shell desktop do Figma, com marca no topo, navegação unificada, tema, conta, logout e ferramentas demonstrativas recolhíveis

## 5. Gráficos e acessibilidade

- [x] 5.1 Atualizar `src/ui/charts.py` para utilizar as cores semânticas dos temas e verificar legibilidade de títulos, eixos, rótulos e legendas
- [ ] 5.2 Fornecer resumo textual para cada gráfico principal e verificar que a informação essencial permanece compreensível sem depender apenas da visualização
- [ ] 5.3 Revisar rótulos, ordem de foco e acionamento por teclado dos controles principais e verificar a navegação sem uso do mouse
- [ ] 5.4 Revisar contraste, ampliação de texto e identificação não baseada apenas em cores nos temas claro e escuro e registrar os ajustes necessários

## 6. Verificação e documentação

- [x] 6.1 Executar `python -m pytest` e verificar que os testes existentes de modelos, filtros, métricas e dados simulados continuam passando
- [x] 6.2 Executar o aplicativo com `python -m streamlit run app.py` e verificar que a página inicial, Disciplinas e Tarefas abrem sem exceções
- [ ] 6.3 Realizar revisão visual comparando as páginas implementadas com as referências aprovadas do kit Orbit e registrar diferenças relevantes
- [x] 6.4 Executar `openspec.cmd validate implement-orbit-ui --strict` e verificar que todos os artefatos da mudança permanecem válidos
- [ ] 6.5 Revisar os arquivos alterados com `git diff --check` e `git status` e verificar que não existem erros de espaços, arquivos temporários ou mudanças fora do escopo
- [x] 6.6 Registrar as entregas, decisões, verificações e pendências em `docs/historico-de-desenvolvimento.md`
