from flask import Flask, request, send_file, jsonify, send_from_directory
import io
import qrcode
import barcode
from barcode.writer import ImageWriter

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    if not data or 'type' not in data or 'text' not in data:
        return jsonify({'error': 'invalid payload'}), 400

    t = data['type']
    text = data['text']
    buf = io.BytesIO()

    try:
        if t == 'qrcode':
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')
            img.save(buf, format='PNG')
            buf.seek(0)
            return send_file(buf, mimetype='image/png', download_name='qrcode.png')

        elif t == 'barcode':
            code = barcode.get('code128', text, writer=ImageWriter())
            code.write(buf)
            buf.seek(0)
            return send_file(buf, mimetype='image/png', download_name='barcode.png')

        else:
            return jsonify({'error': 'unknown type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
