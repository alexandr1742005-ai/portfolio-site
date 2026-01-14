from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Путь к базе данных
DATABASE = 'scores.db'


def init_db():
    """Создаёт таблицу scores, если её нет"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            score INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def save_or_update_score(username, score):
    """Сохраняет или обновляет результат игрока"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Проверяем, есть ли уже такой пользователь
    c.execute('SELECT score FROM scores WHERE username = ?', (username,))
    result = c.fetchone()

    if result:
        old_score = result[0]
        if score > old_score:
            # Обновляем, только если новый результат лучше
            c.execute('UPDATE scores SET score = ?, timestamp = CURRENT_TIMESTAMP WHERE username = ?',
                      (score, username))
    else:
        # Добавляем нового пользователя
        c.execute('INSERT INTO scores (username, score) VALUES (?, ?)', (username, score))

    conn.commit()
    conn.close()


def get_top_scores(limit=10):
    """Получает топ N игроков"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT username, score, timestamp FROM scores ORDER BY score DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows


@app.route('/')
def index():
    top_scores = get_top_scores()
    return render_template('index.html', top_scores=top_scores)


@app.route('/save_score', methods=['POST'])
def save_score_route():
    data = request.json
    username = data.get('username')
    score = data.get('score')

    if username and score is not None:
        save_or_update_score(username, score)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))