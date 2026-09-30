# EduTrack Orbit AI - Backend Xano & XanoScript

Este diretório armazena especificações, schemas de banco e scripts **XanoScript** versionados da aplicação.

## Fonte versionada dos schemas

Os arquivos `.xs` baixados pela extensão **XanoScript** ficam na raiz do repositório:

```text
tables/    arquivos .xs gerados pelo XanoScript (uma tabela por arquivo)
.xano/     metadados de workspace e branch usados pela extensão
```

Este diretório (`xano/`) é apenas documentação. A verdade sobre o schema real do
backend são os arquivos `tables/*.xs`.

> O token de acesso do Xano **não** é versionado. A extensão o guarda no Secret
> Storage do VS Code, fora da pasta do projeto. Nunca cole o token em arquivos
> do repositório.

## Convenções Oficiais

- **Padrão de Nomenclatura:** Obrigatório o uso de `snake_case` para todos os endpoints, tabelas e nomes de coluna.
- **Isolamento de Dados (Multiusuário):** Todas as queries e mutations no Xano devem filtrar estritamente por `user_id` autenticado via JWT.
- **Formato de Resposta:** JSON padronizado com códigos HTTP adequados (200, 201, 400, 401, 403, 404, 500).

## Tabelas Canônicas Principais

> **Divergência conhecida:** a tabela de autenticação criada pelo Xano chama-se
> `user` (nome padrão da plataforma). O schema canônico deste projeto prevê
> `users`. A tabela real, gerada pelo XanoScript, é a referência até que
> `subjects` e `academic_tasks` sejam criadas nas Tarefas 11 e 13.

1. **`users`**:
   - `id` (integer / auto-increment)
   - `created_at` (timestamp)
   - `name` (text)
   - `email` (text / unique)
   - `password` (text / hash seguro)
   - `role` (text / student)

2. **`subjects`**:
   - `id` (integer / auto-increment)
   - `created_at` (timestamp)
   - `user_id` (integer / fk users)
   - `name` (text)
   - `workload_hours` (integer / decimal)
   - `color` (text / hex color)

3. **`academic_tasks`**:
   - `id` (integer / auto-increment)
   - `created_at` (timestamp)
   - `user_id` (integer / fk users)
   - `subject_id` (integer / fk subjects)
   - `title` (text)
   - `description` (text)
   - `due_date` (timestamp)
   - `priority` (text / low, medium, high)
   - `status` (text / draft, pending, in_progress, completed, overdue)
   - `subtasks` (json array)
