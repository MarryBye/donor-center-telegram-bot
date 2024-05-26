import re
import psycopg2.extras as psql_extra

from datetime import datetime
from src.funcs.core import message_translate
from src.classes.Controllers.DatabaseController import DatabaseController


class News:
    def __init__(
        self,
        news_id: int,
        title: str,
        image: str,
        description: str,
        publication_date: datetime,
        news_type: str,
        end_publication_date: datetime,
        link: str,
    ):
        self.news_id = news_id
        self.title = title
        self.image = image
        self.description = description
        self.publication_date = publication_date.strftime("%d-%m-%Y")
        self.news_type = news_type
        self.end_publication_date = end_publication_date.strftime("%d-%m-%Y")
        self.link = link

    def __repr__(self) -> str:
        return f"News(ID={self.news_id}, title='{self.title}', type='{self.news_type}', publication_date='{self.publication_date}')"


class NewsDatabase(DatabaseController):
    def fetch_news(self, limit: int = None) -> list[News]:
        """Получает все новости, сортируя их по типу и дате публикации. Ограничивает количество возвращаемых новостей."""
        try:
            with self.connection.cursor(
                cursor_factory=psql_extra.RealDictCursor
            ) as cur:
                query = """
                SELECT "ID", "title", "image", "description", "publication_date", "type", "end_publication_date", "link"
                FROM "admin".news
                ORDER BY
                    CASE WHEN "type" = 'fundraising' THEN 1 ELSE 2 END,
                    "publication_date" DESC
                """
                if limit is not None:
                    query += " LIMIT %s"
                    cur.execute(query, (limit,))
                else:
                    cur.execute(query)

                rows = cur.fetchall()
                news_list = [
                    News(
                        news_id=row["ID"],
                        title=row["title"],
                        image=row["image"],
                        description=row["description"],
                        publication_date=row["publication_date"],
                        news_type=row["type"],
                        end_publication_date=row["end_publication_date"],
                        link=row["link"],
                    )
                    for row in rows
                ]
            return news_list
        except Exception as e:
            print(f"Ошибка при получении новостей: {e}")
            return []

    def add_news(
        self,
        title: str,
        image: str,
        description: str,
        publication_date: datetime,
        news_type: str,
        end_publication_date: datetime,
        link: str,
    ) -> None:
        """Добавляет новость в базу данных."""
        try:
            with self.connection.cursor(
                cursor_factory=psql_extra.RealDictCursor
            ) as cur:
                query = """
                INSERT INTO "admin".news ("title", "image", "description", "publication_date", "type", "end_publication_date", "link")
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING "ID";
                """
                cur.execute(
                    query,
                    (
                        title,
                        image,
                        description,
                        publication_date,
                        news_type,
                        end_publication_date,
                        link,
                    ),
                )
                news_id = cur.fetchone()["ID"]
                self.connection.commit()
                print(f"Новость успешно добавлена с ID {news_id}.")
        except Exception as e:
            print(f"Ошибка при добавлении новости: {e}")
            self.connection.rollback()

    def escape_markdown_v2(self, text: str) -> str:
        """Экранирует специальные символы для Markdown V2."""
        if not isinstance(text, str):
            text = str(text)
        escape_chars = r"\_*[]()~`>#+-=|{}.!"
        return re.sub(r"([%s])" % re.escape(escape_chars), r"\\\1", text)

    def format_news_for_telegram(self, news_list: list[News], lang: str) -> str:
        """Форматирует список новостей для вывода в Telegram с использованием Markdown V2."""
        formatted_news = []

        _ = lambda text: self.escape_markdown_v2(text)

        for news in news_list:
            news_text = f"*{_(news.title)}*\n"
            if news.link:
                news_text += f"[{_(news.link)}]({_(news.link)})\n"
            news_text += f"{_(news.description)}\n"
            news_text += f"{_(news.publication_date)}\n"
            if news.end_publication_date:
                news_text += f"""_{message_translate("NEWS_END", lang)}_ {_(news.end_publication_date)}\n"""
            news_text += "\n"
            formatted_news.append(news_text)
        return "\n".join(formatted_news)
