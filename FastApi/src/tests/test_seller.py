import pytest
from fastapi import status
from sqlalchemy import select

from src.models import books, seller


# Тест создания продавца
@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {"first_name": "Robert", "last_name": "Martin", "email": "qew@123.com", "password": "201307"}

    response = await async_client.post("/api/v1/seller/", json=data)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data == {"first_name": "Robert", "last_name": "Martin", "email": "qew@123.com", "id": 6}


# Тест на ручку получения списка продавцов
@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):

    seller_1 = seller.Seller(first_name="Ivan", last_name="Ivanov", email="qwe@mail.com", password="password1")
    seller_2 = seller.Seller(first_name="Petr", last_name="Petrov", email="zxc@mail.com", password="password2")

    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/seller/")

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["sellers"]) == 2  # Опасный паттерн! Если в БД есть данные, то тест упадет

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        "sellers": [
            {"first_name": "Ivan", "last_name": "Ivanov", "email": "qwe@mail.com", "id": seller_1.id},
            {"first_name": "Petr", "last_name": "Petrov", "email": "zxc@mail.com", "id": seller_2.id},
        ]
    }


# Тест на ручку получения одного продавца
@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):

    seller_1 = seller.Seller(first_name="Ivan", last_name="Ivanov", email="qwe@mail.com", password="password1")
    seller_2 = seller.Seller(first_name="Petr", last_name="Petrov", email="zxc@mail.com", password="password2")

    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    book = books.Book(author="Pushkin", title="Eugeny Onegin", year=2001, count_pages=104, seller_id=seller_1.id)
    db_session.add_all([book])
    await db_session.flush()

    r

    response = await async_client.get(f"/api/v1/seller/{seller_1.id}")

    assert response.status_code == status.HTTP_200_OK

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        "id": seller_1.id,
        "first_name": "Ivan",
        "last_name": "Ivanov",
        "email": "qwe@mail.com",
        "books": [{"title": "Eugeny Onegin", "author": "Pushkin", "year": 2001, "id": book.id, "count_pages": 104}],
    }


# Тест на ручку удаления продавца
@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    # Создаем книги вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    seller_1 = seller.Seller(first_name="Ivan", last_name="Ivanov", email="qwe@mail.com", password="password1")

    db_session.add(seller_1)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/seller/{seller_1.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_books = await db_session.execute(select(books.Book))
    res = all_books.scalars().all()
    assert len(res) == 0


# Тест на ручку обновления продавцов
@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    seller_1 = seller.Seller(first_name="Ivan", last_name="Ivanov", email="qwe@mail.com", password="password1")

    db_session.add(seller_1)
    await db_session.flush()

    response = await async_client.put(
        f"/api/v1/seller/{seller_1.id}",
        json={"first_name": "Petr", "last_name": "Petrov", "email": "qew@123.com", "id": seller_1.id},
    )

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    # Проверяем, что обновились все поля
    res = await db_session.get(seller.Seller, seller_1.id)
    assert res.first_name == "Petr"
    assert res.last_name == "Petrov"
    assert res.email == "qew@123.com"
    assert res.id == seller_1.id