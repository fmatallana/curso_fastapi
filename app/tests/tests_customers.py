from fastapi import status


def test_create_customer(client):
    response = client.post(
        "/customers",
        json={"name": "jhon doe", "email": "szs@example.com", "age": 20},
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_read_customer(client):
    response = client.post(
        "/customers",
        json={"name": "jhon doe", "email": "szs@example.com", "age": 20},
    )
    assert response.status_code == status.HTTP_200_OK
    customer_id: int = response.json()["id"]
    response_read = client.get(f"/customers/{customer_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["name"] == "jhon doe"


def test_update_customer(client):
    response = client.post(
        "/customers",
        json={"name": "jhon doe", "email": "szs@example.com", "age": 20},
    )
    assert response.status_code == status.HTTP_201_CREATED
    customer_id: int = response.json()["id"]
    response_read = client.get(f"/customers/{customer_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["name"] == "jhon doe"
    assert response_read.json()["email"] == "szs@example.com"
    assert response_read.json()["age"] == 20
    update_response = client.patch(
        f"/customers/{customer_id}",
        json={"name": "felipe", "email": "felipe@szs.com", "age": 20},
    )
    assert update_response.status_code == status.HTTP_200_OK
    response_update = client.get(f"/customers/{customer_id}")
    assert response_update.status_code == status.HTTP_200_OK
    assert response_update.json()["name"] == "felipe"
    assert response_update.json()["email"] == "felipe@szs.com"
    assert response_update.json()["age"] == 20


def test_delete_customer(client):
    response = client.post(
        "/customers",
        json={"name": "jhon doe", "email": "szs@example.com", "age": 20},
    )
    assert response.status_code == status.HTTP_201_CREATED
    customer_id: int = response.json()["id"]
    response_read = client.get(f"/customers/{customer_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()["name"] == "jhon doe"
    assert response_read.json()["email"] == "szs@example.com"
    assert response_read.json()["age"] == 20
    delete_response = client.delete(
        f"/customers/{customer_id}",
    )
    assert delete_response.status_code == status.HTTP_200_OK
    response_delete = client.get(f"/customers/{customer_id}")
    assert response_delete.status_code == status.HTTP_404_NOT_FOUND

    def test_suscribe_customer(client):
        response = client.post(
            "/customers",
            json={"name": "jhon doe", "email": "szs@example.com", "age": 20},
        )
        assert response.status_code == status.HTTP_201_CREATED
        customer_id: int = response.json()["id"]
        response_read = client.get(f"/customers/{customer_id}")
        assert response_read.status_code == status.HTTP_200_OK
        assert response_read.json()["name"] == "jhon doe"
        assert response_read.json()["email"] == "szs@example.com"
        assert response_read.json()["age"] == 20
        plan_response = client.post(
            "/plans",
            json={
                "name": "premim",
                "price": 12,
                "description": "this is a premium plan for szs.com",
            },
        )
        assert plan_response.status_code == status.HTTP_201_CREATED
        plan_id: int = plan_response.json()["id"]
        response_read = client.get(f"/plans/{plan_id}")
        response_asociacion = client.post(
            f"/customers/{customer_id}/plans/{plan_id}?plan_status=active"
        )
        assert response_asociacion.status_code == status.HTTP_200_OK
        assert (
            response_asociacion.json()["customer_id"] == customer_id
        )  # se pone customer_id por que son las llaves exactas que devuelve el json y dentro del modelo CustomerPlan las llaves se llaman customer_id, plan_id y status
        assert response_asociacion.json()["plan_id"] == plan_id
        assert response_asociacion.json()["status"] == "active"
