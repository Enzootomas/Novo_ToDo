# Semana 12 — Issues, Projects, Pull Requests e Quality Gates

Este roteiro adapta a atividade da Semana 12 ao repositório `TodoApp_N2S`. Ele conduz uma mudança desde o planejamento até o merge, usando os arquivos, comandos e fluxo que já existem neste projeto.

## Antes de começar: como o projeto está hoje

- O projeto já é um repositório Git; o remoto configurado é `origin` (`profAndreSouza/TodoApp_N2S`) e a branch atual de trabalho é `main`. Não execute `git init` nem crie outro repositório.
- A API Flask fica em `app/`. Os testes ficam em `tests/unit`, `tests/integration` e `tests/e2e`.
- `requirements.txt` já inclui Flask, pytest, pytest-cov e Flake8.
- `.github/workflows/ci.yml` roda os três grupos de testes quando há `push` para `main`. No momento, não roda em Pull Requests, não faz lint e não verifica cobertura.
- A aplicação já rejeita título de tarefa vazio ou composto por espaços. Os testes de integração já cobrem a ausência do campo `title`; a atividade prática deste guia acrescentará cobertura explícita para título formado apenas por espaços.
- GitHub Projects, PRs e regras de proteção são configurados no GitHub. O guia não cria Issues, branches ou regras remotamente; ele dá os passos para a equipe fazê-lo.

## Passo 1 — Abrir uma Issue com objetivo e aceite verificável

### 1.1 Criar a Issue

1. Acesse o repositório `profAndreSouza/TodoApp_N2S` no GitHub.
2. Abra **Issues** e selecione **New issue**. Se o repositório oferecer templates, escolha um template de tarefa ou bug; caso contrário, use **Open a blank issue**.
3. Use este título, que corresponde a uma lacuna real nos testes atuais:

   **`test(api): cobrir rejeição de título vazio ou composto por espaços`**

4. Cole e ajuste esta descrição:

```markdown
## Problema
A API já rejeita a criação de tarefas sem título, e o modelo rejeita títulos vazios ou formados apenas por espaços. Porém, o teste de integração existente cobre a ausência do campo, mas não deixa explícito o contrato HTTP para um título contendo somente espaços.

## História
Como consumidor da API To-Do, quero receber uma resposta HTTP 400 com um erro em JSON quando envio um título vazio ou composto por espaços, para entender por que a tarefa não foi criada.

## Critérios de aceite
- [ ] Um POST para `/api/todos` sem `title` retorna HTTP 400 e um JSON com a chave `error`.
- [ ] Um POST para `/api/todos` com `title` igual a `"   "` retorna HTTP 400 e um JSON com a chave `error`.
- [ ] A tentativa inválida não cria uma tarefa; a listagem permanece sem essa tarefa.
- [ ] Os testes de integração cobrem os dois casos de entrada inválida.
- [ ] Os testes unitários, de integração e E2E passam.
- [ ] O workflow de CI executa em Pull Request e reprova se lint, testes ou cobertura mínima falharem.

## Fora do escopo
Mudar o formato das respostas da API, alterar o armazenamento em memória ou adicionar banco de dados.

## Evidências esperadas
Link da Pull Request e link da execução de CI com todos os checks verdes.
```

5. Em **Assignees**, atribua a pessoa responsável. Em **Labels**, selecione labels existentes que façam sentido, como `tests`, `enhancement` ou `good first issue`; não crie labels duplicadas sem necessidade.
6. Defina prioridade se o repositório usar esse campo. Registre o número da Issue criada (por exemplo, `#12`); nos exemplos seguintes substitua `12` pelo número real.
7. Confira que o título, os critérios de aceite e o escopo estão visíveis na Issue. A Issue deve dizer como reconhecer a conclusão sem depender de uma avaliação vaga como “ficou melhor”.

## Passo 2 — Criar/usar um Project e acompanhar o trabalho

1. No repositório, abra **Projects**. Se já existir um Project da equipe, reutilize-o. Se não existir, escolha **New project**, dê um nome como `ToDoApp — Planejamento` e selecione a visualização **Board**.
2. Na visualização do Project, adicione a Issue recém-criada pelo número ou pelo título. Em projetos ligados ao repositório, também é possível abrir a Issue e usar **Projects → Add to project**.
3. Configure as colunas de status para representar o fluxo usado pela equipe: `Backlog`, `Pronto`, `Em andamento`, `Em revisão` e `Concluído`. Se o Project recém-criado vier com `Todo`, `In Progress` e `Done`, renomeie ou mapeie esses estados; não é necessário manter colunas equivalentes duplicadas.
4. Adicione campos que a equipe realmente preencherá: `Priority`, `Assignee` e, se houver planejamento por ciclos, `Iteration`. Evite campos sem responsável ou uso definido.
5. Mova o cartão da Issue para `Pronto` quando o escopo estiver claro. Mova para `Em andamento` ao começar a implementação, para `Em revisão` quando abrir a PR e para `Concluído` depois do merge e do fechamento da Issue.
6. Combine um limite de trabalho em andamento se a equipe trabalhar em várias Issues simultâneas; por exemplo, manter no máximo uma tarefa por pessoa em `Em andamento` antes de iniciar outra.

O cartão acompanha o trabalho. A branch, os commits, a PR e os checks registram a mudança no código. Ao longo da atividade, mantenha ambos coerentes.

## Passo 3 — Configurar proteção para que o gate seja obrigatório

Configure esta regra antes de criar a branch de trabalho. Exija Pull Request para qualquer alteração em `main`. Ative **Require status checks to pass before merging**. Se o check `Testes e Quality Gate` ainda não aparecer na lista, salve a regra exigindo PR e retorne assim que o workflow publicar o check. Selecione o check exibido para o job `qualidade` e conclua essa seleção antes de qualquer merge. Um check obrigatório pendente ou com falha impede o merge; até ele ser selecionado, a regra ainda não bloqueia especificamente por falha nos testes.

1. No GitHub, abra **Settings** do repositório. Procure **Rules → Rulesets** ou **Branches → Branch protection rules**, conforme a interface disponível e as permissões da conta.
2. Crie uma regra direcionada à branch `main` (por padrão, branch alvo `main`; não aplique acidentalmente a todas as branches sem decisão da equipe).
3. Ative a exigência de Pull Request antes do merge. Defina uma aprovação mínima — por exemplo, uma — e habilite resolução de conversas se essa for a política da equipe.
4. Esta regra exige que os checks obrigatórios passem antes do merge. Se o workflow ainda não tiver publicado o check, deixe essa seleção para quando ele aparecer; não faça merge antes disso.
5. Se houver a opção **Require branches to be up to date before merging**, decida se querem que a branch de PR incorpore os commits mais recentes de `main` antes do merge. Ative-a somente se o time puder manter esse fluxo.
6. Considere impedir force push e exclusão da branch protegida. Decida explicitamente se administradores e mantenedores também devem estar sujeitos à regra.
7. Salve e confira o resumo da regra, branch alvo e bypass list antes de concluir.
8. Salve a regra e confira se `main` é o único alvo.

Quando o workflow executar em uma PR, confira se o check correto aparece como obrigatório e foi publicado para o último commit. Filtros incorretos ou um nome de check errado podem deixar o merge bloqueado aguardando um check inexistente.


## Passo 4 — Preparar o ambiente e criar uma branch rastreável

### 4.1 Sincronizar a branch base

No terminal, na raiz do repositório:

```bash
git status --short
git switch main
git pull --ff-only origin main
```

Antes de trocar de branch, confira `git status --short`. Se houver alterações locais que não pertencem a esta atividade, salve-as em um commit próprio ou use `git stash push -m "trabalho em andamento"` e recupere-as depois. Não descarte trabalho local sem revisar.

### 4.2 Criar a branch da Issue

Substitua `12` pelo número real da Issue:

```bash
git switch -c feature/12-cobrir-titulo-com-espacos
```

Use Gitflow sem `develop`: branches de trabalho partem de `main` e usam `feature/<número>-<descrição>` para funcionalidades e melhorias, incluindo mudanças de teste, ou `hotfix/<número>-<descrição>` para correções urgentes. Nesta atividade, use `feature/12-cobrir-titulo-com-espacos`. Não crie `develop`. Para conferir:

```bash
git branch --show-current
```

### 4.3 Reproduzir o cenário e implementar a cobertura

O arquivo a alterar é `tests/integration/test_routes.py`. Acrescente um teste para `POST /api/todos` com `json={"title": "   "}`. Verifique o status HTTP 400, a presença da chave `error` no JSON e que uma consulta posterior à listagem não contém uma tarefa criada pela requisição inválida. Mantenha também o teste existente para ausência do campo.

Execute primeiro a camada afetada:

```bash
python -m pytest -v tests/integration/test_routes.py
```

Depois rode as três camadas e o mesmo gate de cobertura que será usado no CI:

```bash
python -m pytest -v tests/unit
python -m pytest -v tests/integration
python -m pytest -v tests/e2e
python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=80 tests/
```

O último comando só deve passar se a cobertura calculada em `app` for igual ou superior a 80%. Se o comportamento já estiver correto e apenas faltava o teste, não mude a lógica da aplicação sem necessidade. Se um teste expuser um defeito, corrija a causa e registre a mudança na PR.

### 4.4 Registrar mudanças em commits pequenos

Confira o diff e os arquivos que serão enviados:

```bash
git diff --check
git diff
git status --short
```

Adicione os arquivos intencionais e faça commit. Exemplo para a cobertura:

```bash
git add tests/integration/test_routes.py
git commit -m "test(api): cobrir título composto por espaços"
```

O workflow é uma alteração lógica separada; quando estiver pronta, faça outro commit:

```bash
git add .github/workflows/ci.yml
git commit -m "ci: executar quality gate em pull requests"
```

Se a equipe preferir um único commit para uma mudança pequena, isso também é válido. Não use `git add .` sem conferir `git status`, para evitar incluir `.coverage`, caches, ambiente virtual ou arquivos da IDE. O `.gitignore` já ignora vários desses artefatos.

Envie a branch ao remoto:

```bash
git push -u origin feature/12-cobrir-titulo-com-espacos
```

## Passo 5 — Atualizar o workflow de CI para atuar como Quality Gate

Edite `.github/workflows/ci.yml`. O arquivo atual já possui jobs separados para unitários, integração e E2E, mas só dispara em `push` para `main`. Para começar com o fluxo existente, adicione execução em PR para `main`, permissões mínimas de leitura, lint e cobertura. Abaixo está uma versão compacta, em um único job, usando ferramentas que já constam em `requirements.txt` e Python 3.11, que o workflow atual já utiliza:

```yaml
name: Pipeline CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  qualidade:
    name: Testes e Quality Gate
    runs-on: ubuntu-latest
    steps:
      - name: Baixar código
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip

      - name: Instalar dependências
        run: python -m pip install -r requirements.txt

      - name: Lint essencial
        run: flake8 app tests --count --select=E9,F63,F7,F82 --show-source --statistics

      - name: Testes unitários
        run: python -m pytest -v tests/unit

      - name: Testes de integração
        run: python -m pytest -v tests/integration

      - name: Testes E2E
        run: python -m pytest -v tests/e2e

      - name: Cobertura mínima de 80%
        run: python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=80 tests/
```

Lint é análise estática: Flake8 lê o código sem executá-lo e aplica regras. `E9` aponta erros graves de sintaxe; `F63` e `F7`, construções inválidas; `F82`, nomes usados sem definição. Esse gate não formata o código nem mede a qualidade dos testes. Se falhar, o job fica vermelho e o check obrigatório bloqueia o merge. Depois de corrigir os avisos existentes, a equipe pode ampliar para `flake8 app tests --statistics`, que inclui regras de estilo e outros possíveis defeitos.

Antes de enviar, valide o YAML e o diff. A configuração mede cobertura de `app/`, não `src/`. Cobertura é a proporção de linhas executáveis da aplicação percorridas pelos testes. O limite de 80% exige que pelo menos 80 de cada 100 linhas contabilizadas sejam exercitadas; pytest-cov encerra com falha abaixo desse valor. Isso não significa que 80% dos testes passaram nem garante bons cenários: asserções relevantes continuam necessárias. `term-missing` lista linhas não cobertas para orientar novos testes. A versão do Python está alinhada ao workflow atual.

Neste roteiro, `main` é a branch base e destino das PRs. Branches `feature/*` e `hotfix/*` partem da `main` atualizada e retornam por Pull Request para `main`; não há branch `develop`.

### Alternativa: manter jobs separados

Jobs independentes podem dar diagnóstico paralelo e preservar a organização atual do workflow. Nesse caso, adicione o lint e cobertura como jobs ou steps com nomes claros e faça o job de cobertura depender dos três grupos de teste, se quiser um check agregador. A proteção de branch deverá exigir o check agregador que realmente aparecer na PR. Evite duplicar todos os testes sem uma razão de feedback ou isolamento.

## Passo 6 — Abrir a Pull Request e ligar as evidências

1. No GitHub, abra a página do repositório. A notificação da branch enviada costuma oferecer **Compare & pull request**; alternativamente, abra **Pull requests → New pull request**.
2. Selecione a branch de destino `main` e a branch de origem `feature/12-cobrir-titulo-com-espacos`. Confira a direção: a branch de trabalho deve entrar em `main`.
3. Use um título claro, por exemplo **`test(api): cobrir rejeição de título composto por espaços`**.
4. Preencha o corpo. Substitua o número da Issue e remova itens que não se aplicam:

```markdown
## Issue relacionada
Closes #12

## O que mudou
- Adiciona cobertura de integração para título composto apenas por espaços.
- Atualiza o CI para executar em Pull Requests e verificar lint, testes e cobertura.

## Como validar
- `python -m pytest -v tests/integration/test_routes.py`
- `python -m pytest -v tests/unit`
- `python -m pytest -v tests/integration`
- `python -m pytest -v tests/e2e`
- `python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=80 tests/`

## Riscos e reversão
- Risco: o limite de cobertura pode revelar cobertura geral abaixo de 80%.
- Reversão: reverter o merge da PR.

## Checklist
- [ ] Critérios de aceite da Issue atendidos
- [ ] Testes e documentação atualizados, quando aplicável
- [ ] Diff revisado e sem arquivos locais ou segredos
- [ ] Checks do CI concluídos
```

5. `Closes #12` associa a PR à Issue e a fecha quando a PR entra em `main`.
6. Crie a PR como **Draft** se o trabalho ainda não estiver pronto para revisão; marque como **Ready for review** quando estiver completo.
7. Confira se o cartão do Project foi movido para `Em revisão` e se a PR aparece relacionada à Issue. Registre o link da PR para a auditoria.

## Passo 7 — Revisar a mudança, acompanhar checks e corrigir falhas

### 6.1 Revisão humana

Peça a uma pessoa revisora para verificar:

- se o novo teste exercita a requisição com título em branco e confirma status e corpo de resposta;
- se a asserção verifica o efeito esperado sem depender de detalhes frágeis;
- se a alteração do workflow usa os diretórios, dependências e versão Python corretos;
- se cobertura é medida na aplicação (`app`) e se o limite é o combinado;
- se o escopo da PR corresponde à Issue e não contém arquivos de cache, configuração local ou credenciais.

Comente as dúvidas na linha relevante do diff. A autora deve responder e marcar conversas resolvidas depois que a correção for revisada.

### 6.2 Acompanhar o CI

1. Na PR, consulte a seção **Checks** ou a aba **Actions** para ver a execução iniciada pelo evento `pull_request`.
2. Espere cada job terminar. `Success` significa que aquele comando passou naquele commit; um workflow executado não bloqueia merge automaticamente até que a regra de proteção exija seu check.
3. Abra os logs do step que falhou e identifique a primeira mensagem de erro relevante. Não esconda falhas com `continue-on-error`.
4. Reproduza localmente o comando que falhou, a partir da raiz do projeto, usando o mesmo Python e as dependências do `requirements.txt`.
5. Corrija a causa. Para uma regressão de código, corrija implementação ou teste conforme o comportamento acordado; não altere um teste apenas para fazê-lo passar sem justificativa.
6. Faça commit e envie para a mesma branch:

```bash
git add <arquivos-alterados>
git commit -m "fix(api): corrigir validação de título"
git push
```

7. A PR será atualizada e os checks rodarão novamente para o novo commit. Confirme que a revisão continua válida e que todos os checks exigidos estão verdes.

## Passo 8 — Fazer uma falha controlada e provar recuperação

Faça a simulação em uma branch descartável separada, ligada a uma Issue de exercício, para não misturar a regressão com a mudança real:

1. Crie uma branch como `feature/13-demonstrar-bloqueio-ci` a partir da branch base atualizada.
2. Introduza uma falha temporária e pequena, por exemplo, altere em um teste uma expectativa de status HTTP para um valor que a API não retorna. Não mude comportamento de produção para criar a falha.
3. Abra uma PR de exercício contra a branch protegida e confirme que o check falha e que a regra impede o merge.
4. Registre o link da PR e o nome do check que a bloqueou.
5. Corrija a expectativa no mesmo branch, faça novo commit e push, e confirme que o workflow executa novamente para o novo commit.
6. Confirme que os checks ficam verdes. Feche a PR de demonstração sem merge, a menos que ela contenha trabalho real aprovado.
7. Exclua a branch de exercício no GitHub e localmente após confirmar que não há trabalho necessário nela:

```bash
git switch main
git branch -d feature/13-demonstrar-bloqueio-ci
```

Não use `git branch -D` como rotina: a opção forçada pode apagar commits ainda não integrados.

## Passo 9 — Integrar a mudança real e fechar o ciclo

Antes do merge, confirme todos os pontos:

- Critérios de aceite da Issue foram atendidos e demonstrados na PR.
- Revisão humana foi aprovada e conversas estão resolvidas.
- Lint, testes unitários, integração, E2E e cobertura passaram no commit mais recente.
- Branch base e branch de origem estão corretas.
- O check obrigatório da proteção de branch está aprovado.

Use o método de merge permitido pela equipe (merge commit, squash ou rebase). Se a equipe não tiver uma convenção, squash merge é uma opção simples para manter a branch principal com um commit por PR; combine a regra antes de padronizá-la. Depois do merge, confirme que `Closes #<número>` encerrou a Issue. Se não encerrou, feche-a manualmente com uma nota apontando para a PR. Mova o cartão para `Concluído` e registre os links da Issue, PR, revisão e execução do workflow.

## Entrega e checklist da atividade

O resultado da atividade é uma cadeia que possa ser auditada:

`Issue com aceite → cartão no Project → branch com número → commits → PR → revisão → checks obrigatórios verdes → merge → Issue e cartão concluídos`

- [ ] Issue criada com o título sugerido (ou título equivalente) e critérios verificáveis.
- [ ] Issue adicionada ao Project com prioridade e estado atualizado.
- [ ] Branch numerada criada a partir da branch base correta.
- [ ] Teste de integração para título composto por espaços incluído.
- [ ] CI acionado em PR e configurado para lint, unitários, integração, E2E e cobertura mínima de 80%.
- [ ] PR vinculada à Issue e preenchida com resumo e validação.
- [ ] Uma revisão humana registrada e conversas resolvidas.
- [ ] Check real do CI exigido pela regra de proteção de `main`.
- [ ] Bloqueio por falha demonstrado e depois recuperado sem merge da regressão.
- [ ] PR real integrada, Issue fechada e cartão concluído.
- [ ] Links da Issue, Project, PR e workflow guardados como evidências da atividade.
