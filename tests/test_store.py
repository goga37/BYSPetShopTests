import allure
import jsonschema
import requests
from .schemas.store_schema import STORE_SCHEMA
from .schemas.store_schema import INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:

    @allure.title("Размещение заказа")
    def test_post_store_create_order(self):
        with allure.step("Отправка запроса на размещение заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
            response = requests.post(url=f'{BASE_URL}/store/order', json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
        jsonschema.validate(response_json, STORE_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json["id"] == payload["id"], "id заказа не совпадает с ожидаемым"
            assert response_json["petId"] == payload["petId"], "petId питомца не совпадает с ожидаемым"
            assert response_json["quantity"] == payload["quantity"], "quantity не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "status не совпадает с ожидаемым"
            assert response_json["complete"] == payload["complete"], "status не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_post_store_get_order_by_id(self, create_store_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_store_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url=f'{BASE_URL}/store/order/{order_id}')
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
        jsonschema.validate(response_json, STORE_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json["id"] == create_store_order["id"], "id заказа не совпадает с ожидаемым"
            assert response_json["petId"] == create_store_order["petId"], "petId питомца не совпадает с ожидаемым"
            assert response_json["quantity"] == create_store_order["quantity"], "quantity не совпадает с ожидаемым"
            assert response_json["status"] == create_store_order["status"], "status не совпадает с ожидаемым"
            assert response_json["complete"] == create_store_order["complete"], "status не совпадает с ожидаемым"

    @allure.title("Удаление заказа по ID")
    def test_post_store_delete_order_by_id(self, create_store_order):
        with allure.step("Получение ID созданного питомца"):
            order_id = create_store_order["id"]

        with allure.step("Отправка запроса на удаление информации о заказе по ID"):
            response = requests.delete(url=f'{BASE_URL}/store/order/{order_id}')

        with allure.step("Проверка статуса ответа после удаления заказа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response_2 = requests.get(url=f'{BASE_URL}/store/order/{order_id}')

        with allure.step("Проверка статуса ответа на получение инофрмации по заказу после его удаления"):
            assert response_2.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_store_get_nonexisting_order_by_id(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f'{BASE_URL}/store/order/31244124214124124')

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текста ошибки"):
            assert response.text == 'Order not found', "Текст ошибки не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f'{BASE_URL}/store/inventory')
            json_data = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
        jsonschema.validate(json_data, INVENTORY_SCHEMA)
