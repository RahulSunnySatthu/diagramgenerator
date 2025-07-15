from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os
import re

# 🟢 Load environment variables from .env
load_dotenv()

# 🟣 Get Groq API Key from env
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("Missing GROQ_API_KEY in environment variables!")

# 🟣 Initialize Groq Client
client = Groq(api_key=api_key)

# Flask setup
app = Flask(__name__)
CORS(app)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "Missing topic"}), 400

    try:
        print("[INFO] Received topic:", topic)

        # 🟢 Query LLM
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Write only a valid blockdiag diagram in the format:\n"
                        f"blockdiag {{ ... }}\n"
                        f"Do not add explanations or markdown fences. "
                        f"Just output the diagram only. "
                        f"Topic: {topic}"
                    )
                }
            ]
        )

        raw_output = response.choices[0].message.content.strip()
        print("[Groq raw output]:", raw_output)

        # Remove code fences if present
        cleaned = re.sub(r"```.*?```", "", raw_output, flags=re.DOTALL).strip()
        print("[After cleanup]:", cleaned)

        # Extract blockdiag block
        match = re.search(r'(blockdiag\s*{[^}]+})', cleaned, re.DOTALL)
        if match:
            diag_code = match.group(1)
        else:
            diag_code = "blockdiag { A -> B; B -> C }"

        print("[Final blockdiag code]:", diag_code)

        return jsonify({"diagram": diag_code})

    except Exception as e:
        print("[ERROR]:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("[INFO] Backend is running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)
