from flask import Flask, request, jsonify, abort
from functools import wraps
import sqlite3

app = Flask(__name__)

# Identifiants de l'utilisateur
USER_CREDENTIALS = {
    'user': '12345'
}

def check_user_auth(username, password):
    return USER_CREDENTIALS.get(username) == password

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_user_auth(auth.username, auth.password):
            return jsonify({"message": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/fiche_nom/<nom>', methods=['GET'])
@user_required
def get_client_by_name(nom):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE nom = ?", (nom,))
    client = cursor.fetchone()
    conn.close()
    
    if client:
        return jsonify({
            'id': client[0],
            'nom': client[1],
            'prenom': client[2],
            'adresse': client[3]
        })
    else:
        return abort(404, description="Client not found")

if __name__ == '__main__':
    app.run(debug=True)
