import openai
import tiktoken


class Generator:
    def __init__(self, model, prompt, query_signifier=None) -> None:
        self.model = model
        self.prompt = prompt
        self.query_signifier = query_signifier

    def generate(self, query):
        if self.query_signifier:
            query = self.query_signifier + "\n" + query
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": query},
            ],
        )
        return response.choices[0].message.content


def count_tokens(input):
    enc = tiktoken.encoding_for_model("gpt-4")
    return len(enc.encode(input))
