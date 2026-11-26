import re

from nltk.stem import SnowballStemmer

STEMMER = SnowballStemmer("english")

STOP_WORDS = {
    "the",
    "is",
    "on",
    "and",
    "do",
    "i",
    "my",
    "to",
    "from",
    "or",
    "can",
    "how",
    "what",
    "after",
}


def clean_tickets(tickets: list[dict]) -> list[dict]:
    """Remove duplicate tickets based on ticket_id, empty queries and strip HTML tags and whitespaces."""
    cleaned_tickets = []
    seen_ids = set()

    for ticket in tickets:
        if ticket["ticket_id"] in seen_ids:
            continue
        seen_ids.add(ticket["ticket_id"])

        query = ticket["query"]

        if query is None:
            continue

        query = re.sub(r"<[^>]+>", " ", query)
        query = " ".join(query.split())
        if not query:
            continue

        cleaned_tickets.append(
            {
                "ticket_id": ticket["ticket_id"],
                "category": ticket["category"],
                "query": query,
                "status": ticket["status"],
            }
        )

    return cleaned_tickets


def preprocess_text(text: str, stem: bool = True) -> list[str]:
    """Lowercase, strip punctuation, tokenize, remove stop words, and stem the texts."""

    text = text.lower()

    cleaned_text = re.findall(r"[a-z0-9]+", text)

    cleaned_tokens = [word for word in cleaned_text if word not in STOP_WORDS]

    if stem:
        cleaned_tokens = [STEMMER.stem(token) for token in cleaned_tokens]

    return cleaned_tokens
