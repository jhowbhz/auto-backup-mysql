from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app)

# Variável global para armazenar os dados de progresso
progress_data = {
    'status': 'Aguardando',
    'progress': 0,
    'current_table': '-',
    'total_tables': 0,
    'processed_tables': 0,
    'remaining_tables': 0,
    'upload_progress': 0
}


# Rota para servir o arquivo HTML do dashboard
@app.route('/dashboard')
def dashboard():
    return send_file('View/dashboard/index.html')

# Sua rota existente para atualizar o progresso
@app.route('/progress', methods=['POST'])
def update_progress():
    global progress_data
    data = request.json

    # Substitua '-' por None nos valores das chaves
    for key, value in data.items():
        if value == '-':
            data[key] = None

    progress_data.update(data)
    return jsonify(progress_data)

# Sua rota existente para obter o progresso
@app.route('/progress', methods=['GET'])
def get_progress():
    return jsonify(progress_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
