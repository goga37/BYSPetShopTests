import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f'{BASE_URL}/pet/9999')
            print(response)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexisting_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f'{BASE_URL}/pet', json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexisting_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f'{BASE_URL}/pet/9999')

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_post_pet_with_data(self):
        with allure.step("Отправка запроса на добавление нового питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "name питомца не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "status питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца c полными данными")
    def test_post_pet_with_full_data(self):
        with allure.step("Отправка запроса на добавление нового питомца c полными данными"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": [
                    "string"
                ],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "name питомца не совпадает с ожидаемым"
            assert response_json["category"]["id"] == payload["category"][
                "id"], "category_id питомца не совпадает с ожидаемым"
            assert response_json["category"]["name"] == payload["category"][
                "name"], "category_name питомца не совпадает с ожидаемым"
            assert response_json["photoUrls"][0] == payload["photoUrls"][
                0], "photoUrls_0 питомца не совпадает с ожидаемым"
            assert response_json["tags"][0]["id"] == payload["tags"][0][
                "id"], "tags_id питомца не совпадает с ожидаемым"
            assert response_json["tags"][0]["name"] == payload["tags"][0][
                "name"], "tags_name питомца не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "status питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_update_existing_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на обновление информации о питомце"):
            response = requests.put(url=f'{BASE_URL}/pet/{pet_id}')
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == create_pet["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == create_pet["name"], "name питомца не совпадает с ожидаемым"
            assert response_json["status"] == create_pet["status"], "status питомца не совпадает с ожидаемым"

    @allure.title("Обновление информации о питомце")
    def test_update_existing_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на обновление информации о питомце"):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }
            response = requests.put(url=f'{BASE_URL}/pet', json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "name питомца не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "status питомца не совпадает с ожидаемым"

    @allure.title("Удаление питомца по ID")
    def test_delete_existing_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на удаления питомца по ID"):
            response = requests.delete(url=f'{BASE_URL}/pet/{pet_id}')

        with allure.step("Проверка статуса ответа после удаления питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получения информации по удаленому питомцу"):
            response_2 = requests.get(url=f'{BASE_URL}/pet/{pet_id}')

        with allure.step("Проверка статуса ответа после удаления питомца"):
            assert response_2.status_code == 404, "Код ответа не совпал с ожидаемым"