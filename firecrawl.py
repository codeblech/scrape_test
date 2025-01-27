import requests
import time
import os
from datetime import datetime


def scrape_firecrawl(url: str, output_dir: str = "fire_output") -> tuple[float, str]:
    """Scrape content using Firecrawl API and save to markdown file."""
    os.makedirs(output_dir, exist_ok=True)

    payload = {
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": True,
        "includeTags": ["body"],
        "excludeTags": [],
        "headers": {},
        "waitFor": 0,
        "mobile": False,
        "skipTlsVerification": False,
        "timeout": 30000,
        "actions": [{"type": "wait", "milliseconds": 2}],
        "location": {"country": "US", "languages": ["en-US"]},
        "removeBase64Images": True,
    }

    start_time = time.perf_counter()
    response = requests.request(
        "POST",
        "http://localhost:3002/v1/scrape",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"firecrawl_scrape_{timestamp}.md")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(response.text)

    return execution_time, output_file


if __name__ == "__main__":
    test_urls = {
        "Wikipedia (Reference)": "https://en.wikipedia.org/wiki/Formula_One",
        "JS Rendered": "https://quotes.toscrape.com/js",
        "Table Layout": "https://quotes.toscrape.com/tableful",
        "Pagination": "https://quotes.toscrape.com",
        "Infinite Scroll": "https://quotes.toscrape.com/scroll",
    }

    results = []
    total_time = 0

    for site_name, url in test_urls.items():
        try:
            execution_time, output_file = scrape_firecrawl(url)
            results.append(
                {"site": site_name, "time": execution_time, "file": output_file}
            )
            total_time += execution_time
            print(f"Scraped {site_name} in {execution_time:.4f} seconds")
            print(f"Output saved to: {output_file}")
        except Exception as e:
            print(f"Error scraping {site_name}: {str(e)}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join("fire_output", f"scraping_results_{timestamp}.md")

    with open(results_file, "w", encoding="utf-8") as f:
        f.write("# Firecrawl Scraping Test Results\n\n")
        f.write("| Site | Time (seconds) |\n")
        f.write("|------|---------------|\n")
        for result in results:
            f.write(f"| {result['site']} | {result['time']:.4f} |\n")
        f.write("|------|---------------|\n")
        f.write(f"| **Total** | **{total_time:.4f}** |\n\n")

        f.write("## Details\n")
        for result in results:
            f.write(f"* {result['site']}: Output saved to `{result['file']}`\n")

    print(f"\nResults summary saved to: {results_file}")
