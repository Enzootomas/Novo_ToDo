def test_api_health_check(client):
    """
    Testa o endpoint de health check /health.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_api_listar_tarefas_inicialmente_vazia(client):
    """
    Testa a listagem de tarefas quando não há tarefas cadastradas.
    """
    response = client.get("/api/todos")
    assert response.status_code == 200
    assert response.get_json() == []


def test_api_criar_tarefa_com_sucesso(client):
    """
    Testa o endpoint POST /api/todos com payload válido.
    """
    payload = {"title": "Comprar café", "description": "100% Arábica"}
    response = client.post("/api/todos", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["title"] == "Comprar café"
    assert data["description"] == "100% Arábica"
    assert data["completed"] is False


def test_api_criar_tarefa_sem_titulo_deve_retornar_400(client):
    """
    Testa a validação de erro ao criar tarefa sem o campo obrigatório 'title'.
    """
    payload = {"description": "Sem título"}
    response = client.post("/api/todos", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_api_obter_tarefa_por_id_existente(client):
    """
    Testa o endpoint GET /api/todos/<id> para tarefa existente.
    """
    res_criacao = client.post("/api/todos", json={"title": "Estudar Testes de Integração"})
    id_criado = res_criacao.get_json()["id"]

    response = client.get(f"/api/todos/{id_criado}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == id_criado
    assert data["title"] == "Estudar Testes de Integração"


def test_api_obter_tarefa_inexistente_deve_retornar_404(client):
    """
    Testa o endpoint GET /api/todos/<id> para tarefa que não existe.
    """
    response = client.get("/api/todos/9999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_api_atualizar_tarefa_com_sucesso(client):
    """
    Testa o endpoint PUT /api/todos/<id> para atualizar status e informações.
    """
    res_criacao = client.post("/api/todos", json={"title": "Tarefa Pendente"})
    id_criado = res_criacao.get_json()["id"]

    res_update = client.put(
        f"/api/todos/{id_criado}",
        json={"completed": True, "title": "Tarefa Concluída"}
    )
    assert res_update.status_code == 200
    data = res_update.get_json()
    assert data["id"] == id_criado
    assert data["title"] == "Tarefa Concluída"
    assert data["completed"] is True


def test_api_deletar_tarefa_com_sucesso(client):
    """
    Testa o endpoint DELETE /api/todos/<id>.
    """
    res_criacao = client.post("/api/todos", json={"title": "Tarefa a Deletar"})
    id_criado = res_criacao.get_json()["id"]

    res_delete = client.delete(f"/api/todos/{id_criado}")
    assert res_delete.status_code == 200
    assert "message" in res_delete.get_json()

    res_busca = client.get(f"/api/todos/{id_criado}")
    assert res_busca.status_code == 404
