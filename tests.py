import pytest
from httpx import AsyncClient
from app import app
from src.database.main_db import Database
from src.elastic.main_es import Elastic
import pytest_asyncio
import asyncio


@pytest_asyncio.fixture
async def test_app():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def test_search(test_app):
    await Database.init_db()
    await Database.import_csv()
    await Elastic.fill()
    query = 'Слив'
    result = [{
                    "id": 1,
                    "text": "Слив информации на пассивки:\n\n• Булл (Блокировка боли)\n• Джесси (Массовый шок)\n• Поко (Звукотерапия)\n• Дэррил (Перезарядка на ходу)\n• Карл (Разгром)\n• Биби (Липкая жвачка и Полная готовность)\n• Мортис (Свернувшаяся змея и Неуловимый)\n• Леон (Тайное лекарство)\n• Ворон (Стервятник)\n• Джин (Рука помощи)\n\nВключай уведомления чтобы не пропускать много полезной информации! ✅",
                    "created_date": "2019-07-25T12:42:13",
                    "rubrics": [
                        "VK-1603736028819866",
                        "VK-11879320040",
                        "VK-63192684938"
                    ]
                }]
    response = await test_app.get(f"/search/{query}")
    assert response.status_code == 200
    assert response.json() == result


async def test_search_error(test_app):

    query = 'efdjspoispf'
    result = {
                    "detail": "no matches found",
                }
    response = await test_app.get(f"/search/{query}")
    assert response.status_code == 404
    assert response.json() == result


async def test_delete(test_app):
    id = 1
    result = {
                    "success": "the record was successfully deleted"
                }
    response = await test_app.delete(f"/delete/{id}")
    assert response.status_code == 200
    assert response.json() == result


async def test_delete_error(test_app):
    id = 1
    result = {"detail": "there is no record with this id"}
    response = await test_app.delete(f"/delete/{id}")
    assert response.status_code == 404
    assert response.json() == result

