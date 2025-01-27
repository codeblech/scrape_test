import asyncio
import time
from datetime import datetime
import os
import numpy as np
from typing import Dict

from crawlee.crawlers import BeautifulSoupCrawler, BeautifulSoupCrawlingContext


async def scrape_with_crawlee(url: str) -> float:
    """Scrape a single URL and return execution time."""
    crawler = BeautifulSoupCrawler(
        max_requests_per_crawl=10,
    )

    @crawler.router.default_handler
    async def request_handler(context: BeautifulSoupCrawlingContext) -> None:
        context.log.info(f"Processing {context.request.url} ...")
        data = {
            "url": context.request.url,
            "body": context.soup.contents if context.soup.contents else None,
        }
        await context.push_data(data)

    start_time = time.perf_counter()
    await crawler.run([url])
    end_time = time.perf_counter()
    return end_time - start_time


async def run_statistical_test(url: str, iterations: int = 5) -> Dict[str, float]:
    """Run multiple iterations of scraping and calculate statistics."""
    times = []

    for _ in range(iterations):
        execution_time = await scrape_with_crawlee(url)
        times.append(execution_time)

    return {
        "mean": np.mean(times),
        "std": np.std(times),
        "ci_95": 1.96 * np.std(times) / np.sqrt(iterations),
        "min": np.min(times),
        "max": np.max(times),
    }


async def main() -> None:
    test_urls = {
        "Wikipedia (Reference)": "https://en.wikipedia.org/wiki/Formula_One",
        "JS Rendered": "https://quotes.toscrape.com/js",
        "Table Layout": "https://quotes.toscrape.com/tableful",
        "Pagination": "https://quotes.toscrape.com",
        "Infinite Scroll": "https://quotes.toscrape.com/scroll",
    }

    results = []
    total_mean_time = 0
    iterations = 5

    for site_name, url in test_urls.items():
        try:
            stats = await run_statistical_test(url, iterations)
            results.append({"site": site_name, "stats": stats})
            total_mean_time += stats["mean"]
            print(f"Scraped {site_name}:")
            print(f"  Mean time: {stats['mean']:.4f} ± {stats['ci_95']:.4f} seconds")
            print(f"  Range: {stats['min']:.4f} - {stats['max']:.4f} seconds")
        except Exception as e:
            print(f"Error scraping {site_name}: {str(e)}")

    # Save results to markdown file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("crawlee_output", exist_ok=True)
    results_file = os.path.join("crawlee_output", f"scraping_results_{timestamp}.md")

    with open(results_file, "w", encoding="utf-8") as f:
        f.write("# Crawlee Scraping Test Results\n\n")
        f.write("| Site | Mean Time (s) | 95% CI | Min-Max (s) |\n")
        f.write("|------|---------------|---------|-------------|\n")
        for result in results:
            stats = result["stats"]
            f.write(
                f"| {result['site']} | {stats['mean']:.4f} | ±{stats['ci_95']:.4f} | "
                f"{stats['min']:.4f}-{stats['max']:.4f} |\n"
            )
        f.write("|------|---------------|---------|-------------|\n")
        f.write(f"| **Total Mean** | **{total_mean_time:.4f}** | | |\n\n")

        f.write("## Details\n")
        f.write(f"Number of iterations per URL: {iterations}\n")

    print(f"\nResults summary saved to: {results_file}")


if __name__ == "__main__":
    asyncio.run(main())
