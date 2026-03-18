import requests
import time
from datetime import datetime, timedelta, timezone
from collections import Counter

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; RedditAnalytics/1.0)"}


def get_utc_timestamp(days_ago: int) -> int:
    """Возвращает UTC timestamp n дней назад (timezone-aware)."""
    from datetime import timezone
    return int((datetime.now(timezone.utc) - timedelta(days=days_ago)).timestamp())


def fetch_posts(subreddit: str, after: int, before: int) -> list[dict[str, any]]:
    """Собираем все посты за промежуток времени через JSON сабреддита."""
    all_posts = []
    url = f"https://www.reddit.com/r/{subreddit}/new.json"
    params = {"limit": 100}
    last_fullname = None

    while True:
        if last_fullname:
            params["after"] = last_fullname

        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
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
            if created_utc > before:
                continue
            all_posts.append({
                "id": post["id"],
                "title": post["title"],
                "author": post.get("author", "[deleted]"),
                "created_utc": created_utc
            })

        last_fullname = data[-1]["data"]["name"]

        time.sleep(1)

        if created_utc >= before:
            break

    return all_posts


def fetch_comments(subreddit: str, posts) ->  list[dict[str, any]]:
    """Собираем комментарии к списку постов через .json"""
    all_comments = []

    for post in posts:
        url = f"https://www.reddit.com/r/{subreddit}/comments/{post['id']}.json"
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"Ошибка HTTP {response.status_code} для поста {post['id']}")
            continue
        try:
            data = response.json()
            comments = data[1]["data"]["children"]
        except Exception:
            print(f"Не удалось разобрать комментарии для {post['id']}")
            continue

        for c in comments:
            if c["kind"] != "t1":
                continue
            comment = c["data"]
            author = comment.get("author")
            if author and author != "[deleted]":
                all_comments.append({"author": author, "created_utc": comment["created_utc"]})

        time.sleep(0.5)

    return all_comments


def main() -> None:
    subreddit = "python"
    before = get_utc_timestamp(0)
    after = get_utc_timestamp(3)

    print("Сбор постов...")
    posts = fetch_posts(subreddit, after, before)

    print("Сбор комментариев...")
    comments = fetch_comments(subreddit, posts)

    # 1. ТОП КОММЕНТАТОРОВ
    comment_authors = [c["author"] for c in comments]
    top_commenters = Counter(comment_authors).most_common(10)

    # 2. ТОП ПОСТЕРОВ
    post_authors = [p["author"] for p in posts if p["author"] != "[deleted]"]
    top_posters = Counter(post_authors).most_common(10)

    # 3. ВСЕ ПОСТЫ
    all_posts = posts

    print("\n=== ТОП КОММЕНТАТОРОВ ===")
    for user, count in top_commenters:
        print(user, count)

    print("\n=== ТОП ПОСТЕРОВ ===")
    for user, count in top_posters:
        print(user, count)

    print("\n=== ВСЕ ПОСТЫ ===")
    for post in all_posts:
        created = datetime.fromtimestamp(post["created_utc"],
                                         tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{created} | {post['author']} | {post['title']}")


if __name__ == "__main__":
    main()