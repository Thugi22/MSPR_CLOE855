from flask import Flask, request, jsonify, abort
from functools import wraps
import sqlite3

app = Flask(__name__)

# Identifiants de l'utilisateur
USER_CREDENTIALS = {
    'user': '12345'
}

# Fonction pour vérifier les identifiants utilisateur
def check_user_auth(username, password):
    return USER_CREDENTIALS.get(username) == password

# Décorateur pour protéger les routes avec authentification utilisateur
def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_user_auth(auth.username, auth.password):
            return jsonify({"message": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Nouvelle route pour rechercher un client par nom
@app.route('/fiche_nom/<name>', methods=['GET'])
@user_required
def get_client_by_name(name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE name = ?", (name,))
    client = cursor.fetchone()
    conn.close()
    
    if client:
        return jsonify({
            'id': client[0],
            'name': client[1],
            'other_info': client[2]
        })
    else:
        return abort(404, description="Client not found")

if __name__ == '__main__':
    app.run(debug=True)
