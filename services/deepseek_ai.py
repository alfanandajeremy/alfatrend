import requests

DEEPSEEK_URL = (
    "https://api.deepseek.com/chat/completions"
)


def analyze_trends(api_key, text):

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Kamu adalah AI analis trend Indonesia.

    Analisa data berikut dan cari:

    1. Topik paling viral
    2. Keyword trending
    3. Sentimen publik
    4. Prediksi trend berikutnya
    5. Ringkasan singkat

    DATA:
    {text}
    """

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Kamu adalah analis "
                    "trend internet Indonesia."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.5,
        "max_tokens": 1500
    }

    response = requests.post(
        DEEPSEEK_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    data = response.json()

    if "choices" not in data:

        return str(data)

    return data["choices"][0]["message"]["content"]