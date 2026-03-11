from fastapi import status


def test_create_order(client):
    response_customer = client.post(
        "/customers",
        json={"name": "jhon doe", "email": "szs@example.com", "age": 20},
    )
    assert response_customer.status_code == status.HTTP_201_CREATED
    customer_id = response_customer.json()["id"]
    response_product = client.post(
        "/products",
        json={
            "name": "balon de futbol",
            "description": "balon super increible de ryan castro awo",
            "price": 20,
            "stock": 20,
        },
    )
    assert response_product.status_code == status.HTTP_201_CREATED
    product_id = response_product.json()["id"]
    response_orders = client.post(
        "/orders",
        json={
            "customer_id": customer_id,
            "items": [{"product_id": product_id, "quantity": 2}],
        },  # se ponen product y quiantiti dentro de llaves {} por que se le pasa un diccionario a items ya que este en models.py esta creado asi items: list[OrderItemCreate] y se pone dentro de corchetes por que necesita que sea una lista
    )
    assert response_orders.status_code == status.HTTP_201_CREATED
    response_read_customer = client.get(f"/customers/{customer_id}")
    response_read_product = client.get(f"/products/{product_id}")
    # de esta manera se ponen los ids dinamicos, primero se crea el response y luego con estas lineas response_read_customer = client.get(f"/customers/{customer_id}") response_read_product = client.get(f"/products/{product_id}") se declaran los ids de forma dinamica para usar arriba
    assert response_read_customer.status_code == status.HTTP_200_OK
    assert response_read_product.status_code == status.HTTP_200_OK
    assert response_orders.json()["total"] == response_product.json()["price"] * 2
    assert response_orders.status_code == status.HTTP_201_CREATED


def test_create_order_customer_not_found(client):
    response_orders = client.post(
        "/orders",
        json={
            "customer_id": 999,
            "items": [{"product_id": 1, "quantity": 2}],
        },
    )
    # esto es un tests de fallo "seguro"
    assert response_orders.status_code == status.HTTP_404_NOT_FOUND
