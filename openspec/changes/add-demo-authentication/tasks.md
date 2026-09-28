## 1. Serviço de autenticação

- [x] 1.1 Implementar armazenamento em memória, conta padrão e hash de senha em `src/services/demo_auth.py` e verificar cadastro e autenticação com testes unitários
- [x] 1.2 Implementar validações de nome, e-mail, senha, duplicidade e confirmação e verificar todos os retornos de erro com testes
- [x] 1.3 Implementar recuperação e redefinição locais com resposta neutra e verificar contas existentes e desconhecidas com testes

## 2. Sessão e proteção

- [x] 2.1 Implementar inicialização, leitura e encerramento da sessão em `src/core/auth_session.py` e verificar transições de estado com testes
- [x] 2.2 Implementar guard reutilizável para páginas protegidas e verificar que interrompe a renderização sem usuário autenticado
- [x] 2.3 Aplicar o guard ao Início acadêmico, Disciplinas e Tarefas e verificar cada rota pelo teste de aplicação do Streamlit

## 3. Interface demonstrativa

- [x] 3.1 Implementar componentes reutilizáveis de login, cadastro e recuperação em `src/ui/auth.py` e verificar rótulos, validações e mensagens
- [x] 3.2 Atualizar `app.py` para alternar entre portal de autenticação e página inicial autenticada e verificar os dois estados
- [x] 3.3 Adicionar conta de demonstração, aviso de dados temporários e logout e verificar que as informações aparecem sem expor hashes ou estado interno
- [x] 3.4 Verificar que formulários e ações ocupam a largura disponível sem rolagem horizontal em telas reduzidas
- [x] 3.5 Implementar o Cadastro desktop claro e escuro conforme os frames aprovados do Figma, preservando o serviço demonstrativo e a integração disponível com o Xano
- [x] 3.6 Implementar a Recuperação de senha desktop clara e escura conforme os frames aprovados do Figma, com resposta neutra e acesso dedicado pelo portal
- [x] 3.7 Implementar a Redefinição de senha desktop clara e escura, conectada à recuperação e à troca local da credencial demonstrativa

## 4. Qualidade e entrega

- [x] 4.1 Executar Ruff e corrigir todos os erros de lint e formatação
- [x] 4.2 Executar Pytest e verificar que testes novos e existentes passam
- [x] 4.3 Executar `compileall` e as quatro rotas pelo AppTest e verificar ausência de erros de sintaxe e exceções
- [x] 4.4 Subir o servidor Streamlit e verificar resposta `ok` no endpoint de saúde
- [x] 4.5 Validar `add-demo-authentication` com OpenSpec em modo estrito e registrar o progresso real das tarefas
