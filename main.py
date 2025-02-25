from os import getenv
import requests
from openai import OpenAI
from dotenv import load_dotenv

# https://api.telegram.org/bot<API_KEY>/getUpdates -> pegar chat ID do telegram

load_dotenv()

OPENAI_KEY = getenv("OPENAI_KEY")
TELEGRAM_BOT_KEY = getenv("TELEGRAM_BOT_KEY")
TELEGRAM_CHAT_ID = getenv("TELEGRAM_CHAT_ID")


def send_telegram_common_message(api_key, chat_id, message):
    try:
        url = f"https://api.telegram.org/bot{api_key}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
        }

        response = requests.post(url, json=payload)

        if response.status_code != 200:
            print(f"Erro ao enviar mensagem: {response.status_code}, {response.text}")
            return None

        print("Mensagem enviada com sucesso!")
        return response.status_code

    except requests.exceptions.RequestException as req_err:
        print(f"Erro de rede ao enviar mensagem: {req_err}")
        return None

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None


def get_random_message_openai(api_key: str, theme: str) -> str:
    client = OpenAI(api_key=api_key)

    prompt = (
        f"me mande uma mensagem curta sobre ${theme}, estou testando a api da openai"
    )

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente especializado em mensagens aleatorias",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
        )

        content = chat_completion.choices[0].message.content

        return content

    except Exception as e:
        print(f"Erro ao gerar post de blog: {e}")
        return None


if __name__ == "__main__":
    message = get_random_message_openai(api_key=OPENAI_KEY, theme="café gelado")
    send_telegram_common_message(
        api_key=TELEGRAM_BOT_KEY, chat_id=TELEGRAM_CHAT_ID, message=message
    )
    print("Finalizado.")
