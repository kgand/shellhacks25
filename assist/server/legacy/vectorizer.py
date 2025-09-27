import cohere

class Vectorizer:
    def __init__(self, token: str):
        self._token = token

    def encode(self, text: str):
        client = cohere.Client(api_key=self._token)
        out = client.embed(texts=[text])
        return out["embeddings"][0]

def cosine_score(a, b):
    s = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return s / (na * nb)
