from flask import Flask, render_template, request, jsonify
import logging
import os

app = Flask(__name__)

# Настройка логирования
if not os.path.exists('logs'):
    os.makedirs('logs')

user_action_logger = logging.getLogger('user_actions')
user_action_logger.setLevel(logging.INFO)
user_action_handler = logging.FileHandler('logs/user_actions.log')
user_action_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
user_action_logger.addHandler(user_action_handler)

computation_logger = logging.getLogger('computations')
computation_logger.setLevel(logging.INFO)
computation_handler = logging.FileHandler('logs/computations.log')
computation_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
computation_logger.addHandler(computation_handler)

@app.route('/')
def index():
    return render_template('index.html')

from sympy import sympify

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expression = data.get('expression')
    user_action_logger.info(f"Expression entered: {expression}")
    try:
        # Использование sympy для безопасного выполнения вычислений
        result = sympify(expression)
        computation_logger.info(f"Computed result for '{expression}' = {result}")
        return jsonify(result=str(result))
    except Exception as e:
        computation_logger.error(f"Error computing expression '{expression}': {e}")
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)
