import re


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
