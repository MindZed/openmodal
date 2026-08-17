from openai import OpenAI

client = OpenAI(
    base_url="https://<YOUR_WORKSPACE_NAME>--gemma-4-e4b-server-server-web-app.modal.run/v1",
    api_key="<YOUR_API_KEY>",
)

try:
    response = client.chat.completions.create(
        model="google/gemma-4-E4B-it",
        messages=[{"role": "user", "content": "Explain what Modal is in one sentence."}],
        max_tokens=128
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
