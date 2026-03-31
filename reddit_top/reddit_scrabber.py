import requests
import time
from datetime import datetime, timedelta, timezone
from collections import Counter
from typing import Any

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; RedditAnalytics/1.0)"}
LIMIT = 100
BEFORE_UTC = 0
AFTER_UTC = 3
REQUEST_TIMEOUT = 10
POSTS_DELAY = 1
COMMENTS_DELAY = 0.5
TOP_COUNT = 10


def get_utc_timestamp(days_ago: int) -> int:
    """Возвращает UTC timestamp n дней назад (timezone-aware)."""
    return int((datetime.now(timezone.utc) - timedelta(days=days_ago)).timestamp())


def fetch_posts(subreddit: str, after: int, before: int) -> list[dict[str, Any]]:
    """Собираем все посты за промежуток времени через JSON сабреддита."""
    all_posts = []
    url = f"https://www.reddit.com/r/{subreddit}/new.json"
    params = {"limit": LIMIT}
    last_fullname = None

    while True:
        if last_fullname:
            params["after"] = last_fullname

        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=REQUEST_TIMEOUT)
        except requests.RequestException as e:
            print(f"Ошибка сети: {e}")
            break

        if response.status_code != 200:
            print(f"Ошибка HTTP {response.status_code}: {response.text[:200]}")
            break

        try:
            data = response.json()["data"]["children"]
        except Exception:
            print("Ошибка разбора JSON")
            break

        if not data:
            break

        for item in data:
            post = item["data"]
            created_utc = post["created_utc"]
            if created_utc < after:
                continue
            all_posts.append({
                "id": post["id"],
                "title": post["title"],
                "author": post.get("author", "[deleted]"),
                "created_utc": created_utc
            })

        last_fullname = data[-1]["data"]["name"]

        time.sleep(POSTS_DELAY)

        if created_utc < after:
            break

    return all_posts


def _extract_comments(children: list[dict[str, Any]], result: list[dict[str, Any]]) -> None:
    """Рекурсивно извлекает комментарии, включая вложенные replies."""
    for c in children:
        if c["kind"] != "t1":
            continue

        comment = c["data"]
        author = comment.get("author")

        if author and author != "[deleted]":
            result.append({"author": author, "created_utc": comment["created_utc"]})

        replies = comment.get("replies")

        if isinstance(replies, dict):
            _extract_comments(replies["data"]["children"], result)


def fetch_comments(subreddit: str, posts) ->  list[dict[str, Any]]:
    """Собираем комментарии к списку постов через .json"""
    all_comments = []

    for post in posts:
        url = f"https://www.reddit.com/r/{subreddit}/comments/{post['id']}.json"
        try:
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        except requests.RequestException as e:
            print(f"Ошибка сети для поста {post['id']}: {e}")
            continue

        if response.status_code != 200:
            print(f"Ошибка HTTP {response.status_code} для поста {post['id']}")
            continue
        try:
            data = response.json()
            comments = data[1]["data"]["children"]
        except Exception:
            print(f"Не удалось разобрать комментарии для {post['id']}")
            continue

        _extract_comments(comments, all_comments)

        time.sleep(COMMENTS_DELAY)

    return all_comments


def main() -> None:
    subreddit = input("Введите сабреддит: ").strip().lower()
    before = get_utc_timestamp(BEFORE_UTC)
    after = get_utc_timestamp(AFTER_UTC)

    print("Сбор постов...")
    posts = fetch_posts(subreddit, after, before)

    print("Сбор комментариев...")
    comments = fetch_comments(subreddit, posts)

    top_commenters = Counter([c["author"] for c in comments]).most_common(TOP_COUNT)

    top_posters = Counter([p["author"] for p in posts if p["author"] != "[deleted]"]).most_common(TOP_COUNT)

    print("\n=== ТОП КОММЕНТАТОРОВ ===")
    for user, count in top_commenters:
        print(user, count)

    print("\n=== ТОП ПОСТЕРОВ ===")
    for user, count in top_posters:
        print(user, count)

    print("\n=== ВСЕ ПОСТЫ ===")
    for post in posts:
        created = datetime.fromtimestamp(post["created_utc"],
                                         tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{created} | {post['author']} | {post['title']}")


if __name__ == "__main__":
    main()