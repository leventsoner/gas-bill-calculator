from flask import Flask, render_template, request, jsonify
import datetime as dt
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from core.nat_gas_bill import calculate_gas_bill, LANGUAGES

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        first_index = float(data['first_index'])
        last_index = float(data['last_index'])
        start_date = dt.date.fromisoformat(data['start_date'])
        end_date = dt.date.fromisoformat(data['end_date'])
        lang = data.get('language', 'en')

        result = calculate_gas_bill(
            first_index, last_index, 
            start_date, end_date, 
            lang
        )
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True) 