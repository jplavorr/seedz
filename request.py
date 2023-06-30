import requests
import concurrent.futures

data_to_post = {
    "cod_city": 123456,
    "date": "2023-06-29",
    "hour": 12,
    "precipitation": 1.0,
    "dry_bulb_temperature": 25.0,
    # adicione o restante dos campos aqui
}

data_to_put = {
    "cod_city": 123456,
    "date": "2023-06-29",
    "hour": 13,
    "precipitation": 2.0,
    "dry_bulb_temperature": 26.0,
    # adicione o restante dos campos aqui
}

cod_city_to_delete = 123456

def create_weather_data(url, data):
    response = requests.post(url, json=data)
    print(f'Response from POST {url}: status code - {response.status_code}, response - {response.json()}')

def get_weather_data(url):
    response = requests.get(url)
    print(f'Response from GET {url}: status code - {response.status_code}, response - {response.json()}')

def update_weather_data(url, data):
    response = requests.put(url, json=data)
    print(f'Response from PUT {url}: status code - {response.status_code}, response - {response.json()}')

def delete_weather_data(url):
    response = requests.delete(url)
    print(f'Response from DELETE {url}: status code - {response.status_code}, response - {response.json()}')


# Crie um executor de thread pool
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Inicie várias threads que irão executar as operações CRUD
    executor.submit(create_weather_data, 'http://34.31.67.203:5000/api/create_weather', data_to_post)
    executor.submit(get_weather_data, 'http://34.31.67.203:5000/api/weather')
    executor.submit(update_weather_data, f'http://34.31.67.203:5000/api/update_weather/{data_to_put["cod_city"]}', data_to_put)
    executor.submit(delete_weather_data, f'http://34.31.67.203:5000/api/delete_weather/{cod_city_to_delete}')


