def test_api_health_check(client):
    """Testa o endpoint de health check."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_api_listar_tarefas_inicialmente_vazia(client):
    """Testa a listagem sem tarefas cadastradas."""
    response = client.get("/api/todos")

    assert response.status_code == 200
    assert response.get_json() == []


def test_api_criar_tarefa_com_sucesso(client):
    """Testa a criacao de uma tarefa com dados validos."""
    payload = {"title": "Comprar café", "description": "100% Arábica"}
    response = client.post("/api/todos", json=payload)

    assert response.status_code == 201

    data = response.get_json()
    assert "id" in data
    assert data["title"] == "Comprar café"
    assert data["description"] == "100% Arábica"
    assert data["completed"] is False


def test_api_criar_tarefa_sem_titulo_deve_retornar_400(client):
    """Testa a rejeicao de uma tarefa sem o campo title."""
    payload = {"description": "Sem título"}
    response = client.post("/api/todos", json=payload)

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_api_obter_tarefa_por_id_existente(client):
    """Testa a consulta de uma tarefa existente."""
    res_criacao = client.post(
        "/api/todos",
        json={"title": "Estudar Testes de Integração"},
    )
    id_criado = res_criacao.get_json()["id"]

    response = client.get(f"/api/todos/{id_criado}")

    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == id_criado
    assert data["title"] == "Estudar Testes de Integração"


def test_api_obter_tarefa_inexistente_deve_retornar_404(client):
    """Testa a consulta de uma tarefa inexistente."""
    response = client.get("/api/todos/9999")

    assert response.status_code == 404
    assert "error" in response.get_json()


def test_api_atualizar_tarefa_com_sucesso(client):
    """Testa a atualizacao do titulo e do status da tarefa."""
    res_criacao = client.post(
        "/api/todos",
        json={"title": "Tarefa Pendente"},
    )
    id_criado = res_criacao.get_json()["id"]

    res_update = client.put(
        f"/api/todos/{id_criado}",
        json={"completed": True, "title": "Tarefa Concluída"},
    )

    assert res_update.status_code == 200

    data = res_update.get_json()
    assert data["id"] == id_criado
    assert data["title"] == "Tarefa Concluída"
    assert data["completed"] is True


def test_api_deletar_tarefa_com_sucesso(client):
    """Testa a exclusao de uma tarefa."""
    res_criacao = client.post(
        "/api/todos",
        json={"title": "Tarefa a Deletar"},
    )
    id_criado = res_criacao.get_json()["id"]

    res_delete = client.delete(f"/api/todos/{id_criado}")

    assert res_delete.status_code == 200
    assert "message" in res_delete.get_json()

    res_busca = client.get(f"/api/todos/{id_criado}")

    assert res_busca.status_code == 404


def test_api_criar_tarefa_com_titulo_ausente_ou_em_branco_deve_retornar_400(client):
    """Rejeita titulos invalidos sem adicionar tarefas a listagem."""
    lista_antes = client.get("/api/todos")

    assert lista_antes.status_code == 200
    tarefas_antes = lista_antes.get_json()

    payloads_invalidos = [
        {"description": "Sem título"},
        {"title": ""},
        {"title": "   "},
    ]

    for payload in payloads_invalidos:
        response = client.post("/api/todos", json=payload)

        assert response.status_code == 400
        assert "error" in response.get_json()

        lista_depois = client.get("/api/todos")

        assert lista_depois.status_code == 200
        assert lista_depois.get_json() == tarefas_antes