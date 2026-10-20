import requests
from django.core.cache import cache


def get_quote():
    quote = cache.get("quote_of_the_day")          # reuse for 1 hour (don't spam the API)
    if quote:
        return quote
    try:
        r = requests.get("https://zenquotes.io/api/random", timeout=5)
        r.raise_for_status()
        data = r.json()[0]                         # [{"q": "...", "a": "..."}]
        quote = {"text": data["q"], "author": data["a"]}
        cache.set("quote_of_the_day", quote, 60 * 60)
        return quote
    except (requests.RequestException, KeyError, IndexError, ValueError):
        return None 