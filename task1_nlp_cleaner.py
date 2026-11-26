import json
import re
from collections import Counter
from pathlib import Path

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
DATA_DIR = Path("data")


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


def analyze_tickets(cleaned_tickets: list[dict]) -> dict[str, int]:
    """Count tickets in each category, print top 5 words, save token records in json format."""

    category_count = Counter(ticket["category"] for ticket in cleaned_tickets)

    query_tokens = []
    tokens_record = []

    for ticket in cleaned_tickets:
        tokens = preprocess_text(ticket["query"])
        query_tokens.extend(tokens)
        tokens_record.append({**ticket, "tokens": tokens})

    keyword_count = Counter(query_tokens)

    most_frequent = keyword_count.most_common(5)

    print(f"Counts per category: {dict(category_count)}")
    print(f"Top 5 most frequent words: {most_frequent}")

    DATA_DIR.mkdir(exist_ok=True)

    with open(DATA_DIR / "cleaned_tickets.json", "w", encoding="utf-8") as file:
        json.dump(
            tokens_record,
            file,
            indent=4,
            ensure_ascii=False,
        )

    return dict(category_count)



def main() -> None:
    with open(DATA_DIR / "support_tickets.json", encoding="utf-8") as f:
        tickets = json.load(f)

    cleaned = clean_tickets(tickets)
    analyze_tickets(cleaned)


if __name__ == "__main__":
    main()