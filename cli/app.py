"""CLI interface backed by the shared intelligence services."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from backend.config import BRAND_QUERIES, get_settings
from backend.services.analytics import build_summary_from_articles
from backend.services.common import AnalysedArticle
from backend.services.news_fetcher import GoogleNewsFetcher, NewsFetchError
from backend.services.sentiment import SentimentAnalysisError, SentimentClassifier
from backend.services.topics import TopicClassificationError, TopicClassifier


cli = typer.Typer(add_completion=False)
console = Console()


def shorten_headline(headline: str, limit: int = 90) -> str:
    clean_headline = " ".join(headline.split())
    if len(clean_headline) <= limit:
        return clean_headline
    return f"{clean_headline[: limit - 3]}..."


def render_summary_table(summary: dict[str, dict[str, float | int]]) -> None:
    table = Table(title="TYRE BRAND SENTIMENT ANALYSIS (NEWS)", show_lines=False)
    table.add_column("Brand", style="bold cyan")
    table.add_column("Articles", justify="right")
    table.add_column("Positive", justify="right", style="green")
    table.add_column("Neutral", justify="right", style="yellow")
    table.add_column("Negative", justify="right", style="red")
    table.add_column("Score", justify="right")

    for brand, stats in summary.items():
        table.add_row(
            brand.upper(),
            str(stats["articles"]),
            str(stats["positive"]),
            str(stats["neutral"]),
            str(stats["negative"]),
            f"{float(stats['score']):.2f}",
        )

    console.print(table)


def analyse_brand(
    brand: str,
    limit: int,
    news_fetcher: GoogleNewsFetcher,
    sentiment: SentimentClassifier,
    topics: TopicClassifier,
) -> list[AnalysedArticle]:
    articles = news_fetcher.fetch_news(brand=brand, query=BRAND_QUERIES[brand], limit=limit)
    if not articles:
        console.print(f"[yellow]No articles found for {brand}.[/yellow]")
        return []

    console.print(f"Analysing {len(articles)} headlines for [bold]{brand}[/bold]...")

    analysed: list[AnalysedArticle] = []
    with console.status(f"[cyan]Starting analysis for {brand}...[/cyan]", spinner="dots") as status:
        for index, article in enumerate(articles, start=1):
            status.update(
                f"[cyan]{brand}[/cyan] [{index}/{len(articles)}] "
                f"[white]{shorten_headline(article.headline)}[/white]"
            )
            analysed.append(
                AnalysedArticle(
                    brand=article.brand,
                    headline=article.headline,
                    source=article.source,
                    url=article.url,
                    sentiment=sentiment.classify(article.headline),
                    topic=topics.classify(article.headline),
                    published_date=article.published_date,
                )
            )
    console.print(f"[green]Completed[/green] {brand}: analysed {len(articles)} headlines.")
    return analysed


@cli.command()
def analyse(
    limit: int = typer.Option(100, min=1, help="Maximum number of news articles to analyse per brand."),
    days: int = typer.Option(3, min=1, max=7, help="Compatibility option retained from the previous interface."),
) -> None:
    """Fetch news, classify sentiment, and print the summary table."""

    del days

    try:
        settings = get_settings()
        news_fetcher = GoogleNewsFetcher(settings)
        sentiment = SentimentClassifier(settings.openai_api_key, settings.openai_model)
        topics = TopicClassifier(settings.openai_api_key, settings.openai_model)

        analysed: list[AnalysedArticle] = []
        for brand in BRAND_QUERIES:
            analysed.extend(analyse_brand(brand, limit, news_fetcher, sentiment, topics))

        render_summary_table(build_summary_from_articles(analysed))
    except ValueError as exc:
        console.print(f"[red]Configuration error:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    except (NewsFetchError, SentimentAnalysisError, TopicClassificationError) as exc:
        console.print(f"[red]Analysis error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


def run() -> None:
    """Run the CLI preserving the original `python app.py` behavior."""

    try:
        analyse()
    except typer.Exit as exc:
        raise SystemExit(exc.exit_code) from exc
