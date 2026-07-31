from ollama import chat

MODEL_NAME = "qwen2:1.5b"


def ask_ai(messages):

    try:

        response = chat(
            model=MODEL_NAME,
            messages=messages
        )

        return response["message"]["content"]

    except Exception as e:

        return f"Error: {e}"