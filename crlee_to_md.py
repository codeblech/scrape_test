import os
import json
import tempfile
import asyncio
import time
from datetime import datetime
import numpy as np
from typing import Dict
from markitdown import MarkItDown
from crawlee.crawlers import BeautifulSoupCrawler, BeautifulSoupCrawlingContext

# Define paths
input_directory = (
    "/home/malik/Documents/work/scrape test/scrape_test/storage/datasets/default"
)
output_directory = "/home/malik/Documents/work/scrape test/scrape_test/crawlee_output"

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)


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


async def process_and_convert_to_markdown():
    total_start_time = time.perf_counter()

    # Initialize MarkItDown
    md = MarkItDown()

    # Process each file in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".json") and filename != "__metadata__.json":
            input_path = os.path.join(input_directory, filename)

            # Read the JSON file
            with open(input_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Extract URL and HTML body
            url = data.get("url", "")
            html_content = "".join(data.get("body", []))

            # Create a temporary HTML file
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".html", delete=False, encoding="utf-8"
            ) as temp_file:
                temp_file.write(html_content)
                temp_path = temp_file.name

            try:
                # Convert HTML to Markdown using the temporary file path
                markdown_content = md.convert(temp_path).text_content

                # Prepare the Markdown with URL at the top
                markdown_with_url = f"# URL: {url}\n\n{markdown_content}"

                # Define output file path
                output_filename = f"{os.path.splitext(filename)[0]}.md"
                output_path = os.path.join(output_directory, output_filename)

                # Write the Markdown content to a file
                with open(output_path, "w", encoding="utf-8") as output_file:
                    output_file.write(markdown_with_url)

            finally:
                # Clean up the temporary file
                os.unlink(temp_path)

    total_end_time = time.perf_counter()
    return total_end_time - total_start_time


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


async def main():
    test_urls = {
        "Wikipedia (Reference)": "https://en.wikipedia.org/wiki/Formula_One",
        "JS Rendered": "https://quotes.toscrape.com/js",
        "Table Layout": "https://quotes.toscrape.com/tableful",
        "Pagination": "https://quotes.toscrape.com",
        "Infinite Scroll": "https://quotes.toscrape.com/scroll",
    }

    # First, perform the statistical scraping
    print("Starting web scraping with statistical analysis...")
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

    # Save statistical results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stats_file = os.path.join(output_directory, f"scraping_results_to_md{timestamp}.md")

    with open(stats_file, "w", encoding="utf-8") as f:
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

    # Then, convert all scraped content to markdown
    print("\nConverting scraped content to Markdown...")
    conversion_time = await process_and_convert_to_markdown()

    print(f"\nEntire process completed in {conversion_time:.4f} seconds")
    print(f"Statistical results saved to: {stats_file}")
    print("Markdown files are saved in the 'crawlee_output' directory.")


if __name__ == "__main__":
    asyncio.run(main())
