from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(_name_)


@app.route("/")
def index():
    return jsonify({
        "status": "online",
        "routes": ["/", "/program"]
    })


@app.route('/programacao', methods=['GET'])
def get_programacao():
    try:
        radio_link = "https://93fmrr.com.br/#c"
        headers = {
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        resp = requests.get(radio_link, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        img_tag = soup.find("img", class_="size-full wp-image-640 alignleft")
        p_tag = img_tag.find_next("p")
        raw_text = p_tag.get_text(separator=" ").strip()

        strong = p_tag.find("strong")
        program = strong.get_text(strip=True) if strong else ""
        presenter = raw_text.replace(program, "", 1).strip()

        program_info = {
            "image": img_tag["src"],
            "program": program,
            "presenter": presenter
        }

        return jsonify(program_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if _name_ == '_main_':
    app.run()
