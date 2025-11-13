from openai import OpenAI

client = OpenAI(
    api_key="fw_3ZLyBejzBgSzRwAADs9vkXFu",  # ← замени!
    base_url="https://api.fireworks.ai/inference/v1"
)

response = client.chat.completions.create(
    model="accounts/fireworks/models/qwen3-235b-a22b",
    messages=[{"role": "user", "content": "Какой предудущий вопрос был? Ответь кратко на русском."}],
    max_tokens=256,
    temperature=0.7
)

print("🤖 Ответ:", response.choices[0].message.content.strip())
