import ollama

response = ollama.chat(
    model="qwen3:4b",
    messages=[
        {"role": "user", "content": "Explain prompt injection in simple terms."}
    ]
)

print(response["message"]["content"])