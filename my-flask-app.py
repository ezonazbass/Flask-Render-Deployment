from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

# Flask uygulamasını başlat
app = Flask(__name__)
CORS(app)

# Google Generative AI yapılandırması
genai.configure(api_key="AIzaSyANY9CZz7W7VRh8hObUhJMdAWTyLD3ngrk")  # API anahtarınızı buraya yazın

# Model yapılandırması
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
    system_instruction=(
        "You are a Survey Generator that produces JSON outputs based on given prompts. \n\n"
        "Guidelines:\n"
        "1. Always return only JSON.\n"
        "2. Create surveys with exactly 9 questions.\n"
        "3. Use the following JSON structure:\n\n"
        "{\n"
        "  \"title\": \"Survey Title\",\n"
        "  \"description\": \"Brief survey description.\",\n"
        "  \"exp_date\": \"YYYY-MM-DD\",\n"
        "  \"fields\": [\n"
        "    {\n"
        "      \"type\": \"Type ID\",\n"
        "      \"label\": \"Question text\",\n"
        "      \"required\": true/false\n"
        "    },\n"
        "    ...\n"
        "  ]\n"
        "}\n\n"
        "Field Type IDs:\n"
        "- 3: Emoji Rating  \n"
        "- 4: Multiple Choice (Static: No, Maybe, Probably, 100% Sure)  \n"
        "- 5: Range Number (0-1000)  \n"
        "- 6: Yes/No  \n"
        "- 7: Short Text  \n"
        "- 8: Long Text  \n"
        "- 9: Number (no limit)  \n"
        "- 10: Rate 1-5  \n"
        "- 11: Rate 0-10  \n\n"
        "Example:\n"
        "{\n"
        "  \"title\": \"Customer Satisfaction Survey\",\n"
        "  \"description\": \"This survey measures customer satisfaction with our services.\",\n"
        "  \"exp_date\": \"2024-01-15\",\n"
        "  \"fields\": [\n"
        "    { \"type\": \"7\", \"label\": \"What is your name?\", \"required\": true },\n"
        "    { \"type\": \"11\", \"label\": \"Rate your satisfaction from 1 to 10.\", \"required\": true },\n"
        "    { \"type\": \"4\", \"label\": \"Would you use our service again?\", \"required\": false }\n"
        "  ]\n"
        "}\n\n"
        "Ensure all surveys follow this structure.\n"
    ),
)

# Ana rotayı tanımla
@app.route('/', methods=['GET'])
def welcome():
    return "<h1>Hello World</h1>"

# AI'dan anket üretmek için rota
@app.route('/generate-survey', methods=['POST'])  # Parantez hatası düzeltildi
def generate_survey():
    try:
        # İstekten prompt'u al
        data = request.get_json()
        prompt = data.get('prompt')

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Chat oturumunu başlat
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)

        # AI'dan gelen cevabı döndür
        return jsonify({"survey": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask uygulamasını çalıştır
if __name__ == '__main__':
    app.run(debug=True)
