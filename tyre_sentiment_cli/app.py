"""Typer CLI entrypoint for tyre brand sentiment analysis."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from aggregator import build_summary
from config import BRAND_QUERIES, get_settings
from fetch_news import NewsFetchError, GoogleNewsClient
from models import ArticleResult, NewsArticle
from sentiment import SentimentAnalysisError, SentimentClassifier


app = typer.Typer(help="Analyze news sentiment for tyre brands.")
console = Console()


def shorten_headline(headline: str, limit: int = 90) -> str:
    """Shorten long headlines so the status line stays readable."""

    clean_headline = " ".join(headline.split())
    if len(clean_headline) <= limit:
        return clean_headline
    return f"{clean_headline[: limit - 3]}..."


def render_summary_table(summary: dict[str, dict[str, float | int]]) -> None:
    """Render the Rich output table."""

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


def analyse_brand_articles(
    brand: str,
    articles: list[NewsArticle],
    classifier: SentimentClassifier,
) -> list[ArticleResult]:
    """Classify articles for a single brand with live CLI status updates."""

    results: list[ArticleResult] = []
    total_articles = len(articles)

    with console.status(
        f"[cyan]Starting analysis for {brand}...[/cyan]",
        spinner="dots",
    ) as status:
        for index, article in enumerate(articles, start=1):
            status.update(
                f"[cyan]{brand}[/cyan] [{index}/{total_articles}] "
                f"[white]{shorten_headline(article.title)}[/white]"
            )
            sentiment = classifier.classify_sentiment(article.title)
            results.append(
                ArticleResult(
                    brand=article.brand,
                    title=article.title,
                    sentiment=sentiment,
                )
            )

    console.print(f"[green]Completed[/green] {brand}: analysed {total_articles} headlines.")
    return results


@app.command()
def analyse(
    limit: int = typer.Option(200, min=1, help="Maximum number of news articles to analyse per brand."),
    days: int = typer.Option(3, min=1, max=7, help="Compatibility option retained from the previous interface."),
) -> None:
    """Fetch news headlines, classify sentiment, and print the summary table."""

    try:
        settings = get_settings()
        news_client = GoogleNewsClient(settings)
        classifier = SentimentClassifier(settings.openai_api_key, settings.openai_model)

        all_articles = news_client.fetch_all_brands(limit=limit)
        combined_results = []

        for brand in BRAND_QUERIES:
            articles = all_articles.get(brand, [])
            if not articles:
                console.print(f"[yellow]No articles found for {brand}.[/yellow]")
                continue

            console.print(f"Analysing {len(articles)} headlines for [bold]{brand}[/bold]...")
            combined_results.extend(analyse_brand_articles(brand, articles, classifier))

        summary = build_summary(combined_results)
        render_summary_table(summary)
    except ValueError as exc:
        console.print(f"[red]Configuration error:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    except NewsFetchError as exc:
        console.print(f"[red]News fetch error:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    except SentimentAnalysisError as exc:
        console.print(f"[red]Sentiment analysis error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


if __name__ == "__main__":
    app()
