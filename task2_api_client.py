import logging

import requests

TIMEOUT_SECONDS = 10
API_URL = "https://jsonplaceholder.typicode.com/posts"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def fallback_docs() -> list[dict]:
    """Return fallback documents when request on API URL fails."""
    content_1 = "This came up to handle fallback"
    content_2 = "This is another document for fallback handling."

    return [
        {
            "doc_id": -1,
            "title": "First Fallback",
            "content": content_1,
            "word_count": len(content_1.split()),
        },
        {
            "doc_id": -2,
            "title": "Fallback 2",
            "content": content_2,
            "word_count": len(content_2.split()),
        },
    ]


def fetch_posts(api_url: str = API_URL, posts_limit: int = 5) -> list[dict]:
    """Fetches documents and cleans them.If request fails, falls back to mock documents."""

    logger.info("Starting API request.")
    try:
        response = requests.get(url=api_url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        posts = response.json()[:posts_limit]
        documents = []
        for post in posts:
            documents.append(
                {
                    "doc_id": post["id"],
                    "title": post["title"].strip(),
                    "content": post["body"].replace("\n", " ").strip(),
                    "word_count": len(post["body"].split()),
                }
            )

        logger.info(
            "API request succeeded. %d documents successfully retrieved.",
            len(documents),
        )
        return documents

    except requests.exceptions.Timeout:
        logger.warning(
            "Request timed out after %s seconds. Using fallback.", TIMEOUT_SECONDS
        )
    except requests.exceptions.ConnectionError:
        logger.warning("Connection error. Using fallback.")
    except requests.exceptions.HTTPError as exc:
        logger.warning("HTTP error: %s. Using fallback.", exc)
    except requests.exceptions.JSONDecodeError as exc:
        logger.warning("Invalid JSON: %s. Using fallback.", exc)
    except requests.exceptions.RequestException as exc:
        logger.warning("Request failed: %s. Using fallback.", exc)

    return fallback_docs()


def main() -> None:
    documents = fetch_posts()

    print(f"\nNumber of documents: {len(documents)}")

    for document in documents:
        print(document)


if __name__ == "__main__":
    main()
