from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os
import re

# 🟢 Load environment variables from .env
load_dotenv()

# 🟣 Get your Groq API key securely
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("Missing GROQ_API_KEY in environment variables!")

# 🟣 Initialize Groq client with API key
client = Groq(api_key=api_key)

# Flask app
app = Flask(__name__)
CORS(app)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "Missing topic"}), 400

    try:
        # 🟢 1️⃣ Call Groq LLM with prompt
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

        # 🟢 2️⃣ Get LLM raw text
        raw_output = response.choices[0].message.content.strip()
        print("[Groq raw output]:", raw_output)

        # 🟢 3️⃣ Clean markdown fences
        cleaned = re.sub(r"```.*?```", "", raw_output, flags=re.DOTALL).strip()
        print("[After fence removal]:", cleaned)

        # 🟢 4️⃣ Extract only blockdiag { ... }
        match = re.search(r'(blockdiag\s*{[^}]+})', cleaned, re.DOTALL)
        if match:
            diag_code = match.group(1)
        else:
            diag_code = "blockdiag { A -> B; B -> C }"

        print("[Final blockdiag code]:", diag_code)

        # 🟢 5️⃣ Return JSON
        return jsonify({"diagram": diag_code})

    except Exception as e:
        print("[ERROR]:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
