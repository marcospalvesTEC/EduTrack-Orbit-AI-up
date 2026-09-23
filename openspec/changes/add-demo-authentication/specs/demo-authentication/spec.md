## Purpose

Permitir que o protótipo demonstre uma jornada completa de acesso e restrinja as áreas acadêmicas, deixando explícito que os dados e a recuperação são locais e temporários.

## ADDED Requirements

### Requirement: Identificação demonstrativa

O sistema SHALL identificar claramente que a autenticação é demonstrativa e SHALL disponibilizar credenciais de teste na tela de entrada.

#### Scenario: Visualização das credenciais de teste
- **WHEN** o visitante acessar a tela de login
- **THEN** o sistema exibirá a conta demonstrativa e informará que não se trata de autenticação produtiva

### Requirement: Cadastro local

O sistema SHALL permitir cadastrar nome, e-mail e senha válidos durante a sessão atual e MUST rejeitar e-mails duplicados ou campos inválidos.

#### Scenario: Cadastro válido
- **WHEN** o visitante informar nome, e-mail válido, senha com pelo menos oito caracteres e confirmação correspondente
- **THEN** o sistema criará a conta local e permitirá o acesso

#### Scenario: Cadastro inválido
- **WHEN** o visitante informar dados incompletos, e-mail inválido, e-mail existente ou senhas divergentes
- **THEN** o sistema rejeitará o cadastro e exibirá uma mensagem específica sem revelar senhas

### Requirement: Login local

O sistema SHALL autenticar uma conta demonstrativa ou uma conta criada na sessão e MUST rejeitar credenciais incorretas com mensagem genérica.

#### Scenario: Login válido
- **WHEN** o visitante informar e-mail e senha correspondentes a uma conta disponível
- **THEN** o sistema iniciará uma sessão autenticada e exibirá a área acadêmica

#### Scenario: Login inválido
- **WHEN** o visitante informar credenciais incorretas
- **THEN** o sistema permanecerá na entrada e informará que e-mail ou senha são inválidos

### Requirement: Proteção das páginas

O sistema MUST impedir que visitantes sem sessão autenticada utilizem o Início acadêmico, Disciplinas e Tarefas.

#### Scenario: Acesso sem autenticação
- **WHEN** um visitante abrir diretamente uma página acadêmica
- **THEN** o sistema exibirá uma orientação para realizar login e interromperá a renderização dos dados da página

### Requirement: Sessão e logout

O sistema SHALL manter o usuário autenticado durante a sessão atual e SHALL oferecer logout em todas as áreas protegidas.

#### Scenario: Encerramento de sessão
- **WHEN** o estudante acionar o logout
- **THEN** o sistema removerá a sessão autenticada e voltará a proteger as páginas acadêmicas

### Requirement: Recuperação e redefinição simuladas

O sistema SHALL simular a solicitação de recuperação e permitir redefinir a senha de uma conta local existente sem enviar mensagens externas.

#### Scenario: Solicitação para conta existente
- **WHEN** o visitante solicitar recuperação para um e-mail cadastrado
- **THEN** o sistema informará que a recuperação demonstrativa está disponível e exibirá o fluxo de redefinição local

#### Scenario: Solicitação para e-mail desconhecido
- **WHEN** o visitante solicitar recuperação para um e-mail não cadastrado
- **THEN** o sistema exibirá uma resposta neutra que não confirme a existência da conta

#### Scenario: Redefinição válida
- **WHEN** o visitante autorizado no fluxo demonstrativo informar e confirmar uma nova senha válida
- **THEN** o sistema atualizará a senha local e permitirá novo login

### Requirement: Limites da demonstração

O sistema MUST informar que contas, senhas e alterações da autenticação local não constituem persistência segura nem substituem a integração futura com o Xano.

#### Scenario: Reinício do protótipo
- **WHEN** o processo ou a sessão demonstrativa for reiniciada
- **THEN** o sistema poderá restaurar apenas a conta de demonstração e SHALL manter visível o aviso sobre dados temporários
