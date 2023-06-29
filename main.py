from flask import Flask, jsonify, request
from sqlalchemy import create_engine
import pandas as pd
import json
import psycopg2
from sqlalchemy import text

app = Flask(__name__)

# Criação da conexão




@app.route('/')
def home():
    return "Seedz"

@app.route('/api/weather', methods=['GET'])
def get_weather_data():
    # Leitura do schema
    query = "SELECT * FROM weather.grid_weather_data"  
    df = pd.read_sql_query(query, con=engine)

    # Converte o DataFrame em um dicionário e, em seguida, em JSON
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/jsondata', methods=['GET'])
def get_json_data():
    with open('grid_weather.json') as f:
        data = json.load(f)

    # Retorna os dados JSON
    return jsonify(data)


@app.route('/api/create_weather', methods=['POST'])
def create_weather_data():
    data = request.get_json()  # Obter dados JSON do corpo da requisição

    df = pd.DataFrame([data])  # Cria um DataFrame com os dados
    df.to_sql('weather.grid_weather_data', con=engine, if_exists='append', index=False)  # Inserir os dados na tabela

    return jsonify({'message': 'Dados inseridos com sucesso!'}), 201

@app.route('/api/update_weather/<int:cod_city>', methods=['PUT'])
def update_weather_data(cod_city):
    data = request.get_json()  # Obter dados JSON do corpo da requisição

    df = pd.DataFrame([data])  # Cria um DataFrame com os dados
    df.to_sql('weather.grid_weather_data', con=engine, if_exists='replace', index=False)  # Atualizar os dados na tabela

    return jsonify({'message': 'Dados atualizados com sucesso!'})

@app.route('/api/delete_weather/<int:cod_city>', methods=['DELETE'])
def delete_weather_data(cod_city):
    with engine.connect() as connection:
        connection.execute(text(f"DELETE FROM weather.grid_weather_data WHERE cod_city = {cod_city};"))  # Exclui os dados na tabela

    return jsonify({'message': 'Dados excluídos com sucesso!'})


if __name__ == "__main__":
    app.run(debug=True)



