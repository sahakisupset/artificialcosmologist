import json

from openai import OpenAI


class DeepSeekClient:
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com", model: str = "deepseek-reasoner"):
        if not api_key:
            raise ValueError("A DeepSeek API key is required")
        self.model = model
        self._client = OpenAI(api_key=api_key, base_url=base_url)

    def reason(self, prompt: str, system: str | None = None, temperature: float = 0.2) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content or ""

    def reason_json(self, prompt: str, system: str | None = None) -> dict:
        text = self.reason(prompt, system=system, temperature=0)
        text = text.strip()
        if text.startswith("```"):
            text = text.split("```", 2)[1]
            if text.startswith("json"):
                text = text[4:].strip()
        return json.loads(text)
