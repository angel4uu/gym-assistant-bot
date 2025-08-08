from langchain_google_genai import GoogleGenerativeAI
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def test_gemini():
    chat = GoogleGenerativeAI(
        model="gemini-1.5-flash",
        api_key=config["google_api_key"]
    )

    response = chat.invoke(
        [
            {"role": "user", "content": "¿Cuál es la capital de Francia?"}
        ]
    )

    print(response)

if __name__ == "__main__":
    test_gemini()
