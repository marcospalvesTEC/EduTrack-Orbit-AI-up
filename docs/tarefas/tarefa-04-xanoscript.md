# Tarefa 04 — Primeiro Pull/Push com XanoScript

## Status

🟢 **CONCLUÍDA** — integração XanoScript validada nos dois sentidos.

O fluxo **Xano → VS Code** foi validado através do primeiro Pull e o fluxo
**VS Code → Xano** foi validado através da criação e publicação da função isolada
`edutrack_push_test` (#349653), sem alterar as tabelas existentes do EduTrack.

---

## Objetivo

Conectar o ambiente local do **EduTrack Orbit AI** ao backend do Xano utilizando
a extensão **XanoScript** no VS Code, permitindo visualizar, editar e versionar
o backend como código através de arquivos `.xs`.

---

## Ambiente utilizado

| Item | Resultado |
|---|---|
| VS Code | ✅ Utilizado |
| Extensão XanoScript | ✅ Instalada |
| Login no Xano | ✅ Realizado |
| Instância | ✅ Free Instance (`x8ki-letl-twmt`) |
| Branch Xano | ✅ `v1` — Live branch |
| Primeiro Pull | ✅ Concluído |
| Arquivos `.xs` locais | ✅ Recebidos |
| Versionamento Git | ✅ Concluído |
| Push para GitHub | ✅ Concluído |
| Push VS Code → Xano | ✅ Concluído |
| Evidências | ✅ Registradas |

---

## 1. Conexão com o XanoScript

No VS Code foi executado:

`XanoScript: Login to Xano`

A autenticação foi concluída com sucesso.

Em seguida foi selecionada a instância:

`Free Instance (x8ki-letl-twmt)`

Depois foi selecionada a branch do Xano:

`v1 — Live branch`

> A branch `v1` pertence ao Xano e não deve ser confundida com a branch `main`
> utilizada pelo Git/GitHub.

---

## 2. Primeiro Pull

Após selecionar a branch `v1`, a extensão apresentou a opção:

`Pull Changes`

O Pull foi executado com sucesso.

Com isso, o backend existente no Xano passou a ser representado localmente no
projeto através de arquivos XanoScript (`.xs`).

Entre os diretórios recebidos estão:

- `.xano/`
- `addons/`
- `agents/`
- `apis/`
- `functions/`
- `tables/`
- `tools/`

---

## 3. Tabelas recebidas

O diretório `tables/` passou a conter os seguintes arquivos:

- `887029_user.xs`
- `887030_event_log.xs`
- `887034_academic_tasks.xs`
- `887035_subjects.xs`

A presença desses arquivos confirmou que o Pull do backend do Xano para o
ambiente local foi realizado corretamente.

---

## 4. APIs e funções recebidas

O Pull também trouxe para o projeto os endpoints e funções existentes no backend.

Entre os endpoints recebidos estão funcionalidades relacionadas a:

- autenticação;
- usuários;
- disciplinas;
- tarefas acadêmicas;
- logs de eventos.

Também foram recebidas funções XanoScript existentes no backend.

---

## 5. Primeira tentativa de Push

Inicialmente foi utilizado o arquivo:

`tables/887035_subjects.xs`

Foi adicionado temporariamente um comentário para testar o fluxo de alteração
local.

Em seguida foi executado:

`XanoScript: Push Stage Changes to Xano`

A extensão reconheceu a alteração e solicitou que as mudanças fossem adicionadas
ao Stage.

Entretanto, antes da confirmação final, o XanoScript apresentou um alerta
informando que a operação envolvia uma tabela e que alterações estruturais
poderiam causar perda de dados.

Por segurança, foi selecionada a opção:

`Abort Push`

O comentário de teste foi removido e o arquivo `887035_subjects.xs` foi
restaurado ao estado original recebido do Xano.

> Nenhuma alteração estrutural foi enviada para a tabela `subjects`.

---

## 6. Push seguro VS Code → Xano

Para validar o fluxo de Push sem colocar as tabelas existentes do EduTrack em
risco, foi criada uma **Custom Function isolada**.

No VS Code foi executado:

`XanoScript: New Custom Function`

Nome utilizado:

`edutrack_push_test`

A função criada possui a seguinte estrutura:

```xanoscript
function edutrack_push_test {
  input {
    // what is this argument about?
    *text* some_argument? filters=trim
  }

  stack {
    var $some_variable {
      value = "with some value"
    }
  }

  response = $some_variable
}
```

Essa função:

1. recebe opcionalmente o argumento `some_argument`;
2. cria a variável `some_variable`;
3. atribui o valor `"with some value"`;
4. retorna essa variável;
5. não consulta nem modifica nenhuma tabela do EduTrack.

Após salvar o arquivo, foi executado novamente:

`XanoScript: Push Stage Changes to Xano`

As alterações foram adicionadas ao Stage do XanoScript e enviadas ao backend.

---

## 7. Confirmação no Xano

A publicação foi confirmada diretamente através do painel do Xano.

A função passou a aparecer no backend como:

`edutrack_push_test #349653`

A função publicada apresentou a mesma estrutura criada através do VS Code,
confirmando o funcionamento do fluxo:

**VS Code → XanoScript → Xano**

Portanto, o Push foi validado sem modificar as tabelas existentes do
EduTrack Orbit AI.

---

## 8. Segurança

Antes do versionamento, a pasta `.xano/` foi verificada.

O arquivo:

`.xano/config.json`

apresentou as seguintes propriedades principais:

- `branch`
- `instanceDisplay`
- `instanceName`
- `paths`
- `workspaceId`
- `workspaceName`

Nenhuma propriedade principal de token ou senha foi identificada nessa
verificação.

O token de autenticação do Xano não foi inserido manualmente no repositório.

Também foi evitada qualquer alteração estrutural nas tabelas existentes durante
a validação do Push.

---

## 9. Versionamento no Git

Os arquivos provenientes do primeiro Pull foram adicionados seletivamente ao Git.

Commit principal da integração:

```text
a6f451e feat: integra XanoScript e adiciona backend do Xano
```

Resultado:

```text
36 files changed, 1801 insertions(+)
```

Foram versionados arquivos referentes a:

- configuração do Xano;
- tabelas;
- APIs;
- funções;
- agents;
- addons;
- tools.

---

## 10. GitHub

O repositório acadêmico utilizado foi:

`marcospalvesTEC/EduTrack-Orbit-AI-up`

O envio da integração foi realizado através de:

```powershell
git push origin main
```

Resultado:

```text
To https://github.com/marcospalvesTEC/EduTrack-Orbit-AI-up.git
   3f0644e..a6f451e  main -> main
```

Posteriormente, a documentação e a primeira evidência da Tarefa 04 também foram
enviadas ao repositório:

```text
a6f451e..2b3b88c  main -> main
```

Assim, o backend obtido através do XanoScript e a documentação da atividade
estão versionados na branch `main` do repositório acadêmico.

---

## 11. Evidências

### Evidência 01 — Git Push

Arquivo:

`docs/tarefas/evidencias/tarefa-04-git-push.png`

A imagem registra:

- VS Code;
- estrutura XanoScript;
- arquivos `.xs`;
- diretório `tables/`;
- commit da integração;
- comando `git push origin main`;
- confirmação `main -> main`.

### Evidência 02 — Push confirmado no Xano

Arquivo:

`docs/tarefas/evidencias/tarefa-04-xano-push-confirmado.png`

A imagem registra diretamente no painel do Xano:

- branch `v1`;
- ambiente `live`;
- Custom Function `edutrack_push_test`;
- identificação `#349653`;
- estrutura da função;
- argumento `some_argument`;
- variável `some_variable`;
- resposta da função.

Essa evidência confirma o funcionamento do fluxo **VS Code → Xano**.

---

## 12. Resultado final

- [x] Extensão XanoScript instalada.
- [x] Login realizado no Xano.
- [x] Instância Xano selecionada.
- [x] Branch `v1` selecionada.
- [x] Primeiro Pull realizado.
- [x] Diretório `.xano/` criado.
- [x] Arquivos `.xs` disponíveis localmente.
- [x] Tabelas do backend recebidas.
- [x] APIs do backend recebidas.
- [x] Funções do backend recebidas.
- [x] Backend Xano versionado no Git.
- [x] Commit da integração criado.
- [x] Push para o GitHub acadêmico concluído.
- [x] Primeira tentativa de alteração em tabela abortada com segurança.
- [x] Custom Function isolada criada para validação.
- [x] Push VS Code → Xano realizado.
- [x] Função `edutrack_push_test #349653` confirmada no Xano.
- [x] Evidência do Git Push registrada.
- [x] Evidência do Xano Push registrada.

---

## Conclusão

A **Tarefa 04 — Primeiro Pull/Push com XanoScript** foi concluída com sucesso.

Foi validado o fluxo completo:

**Xano → XanoScript → VS Code → Git → GitHub**

e também o fluxo inverso:

**VS Code → XanoScript → Xano**

O primeiro Pull permitiu trazer o backend do EduTrack Orbit AI para o ambiente
local e versioná-lo no Git.

Para testar o Push de maneira segura, foi criada a função isolada
`edutrack_push_test`, posteriormente publicada e confirmada no painel do Xano
como `#349653`.

Nenhuma tabela existente do EduTrack Orbit AI foi removida ou modificada durante
a validação.

**Status final: 🟢 CONCLUÍDA**