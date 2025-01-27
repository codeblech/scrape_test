import requests
import time
import os
from datetime import datetime
import numpy as np
from typing import Dict


def scrape_jina_ai(url: str, output_dir: str = "jina_output") -> float:
    """
    Scrape content from r.jina.ai/<url> and save to markdown file.
    Returns execution time in seconds.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Start timing
    start_time = time.perf_counter()

    # Construct full URL
    full_url = f"https://r.jina.ai/{url}"

    try:
        # Send GET request
        response = requests.get(full_url)
        response.raise_for_status()

        # Generate output filename using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"jina_scrape_{timestamp}.md")

        # Save response content to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response.text)

        # End timing and return
        end_time = time.perf_counter()
        return end_time - start_time

    except requests.RequestException as e:
        raise Exception(f"Failed to scrape {full_url}: {str(e)}")


def run_statistical_test(url: str, iterations: int = 5) -> Dict[str, float]:
    """Run multiple iterations of scraping and calculate statistics."""
    times = []

    for _ in range(iterations):
        execution_time = scrape_jina_ai(url)
        times.append(execution_time)

    return {
        "mean": np.mean(times),
        "std": np.std(times),
        "ci_95": 1.96 * np.std(times) / np.sqrt(iterations),
        "min": np.min(times),
        "max": np.max(times),
    }


if __name__ == "__main__":
    # Test URLs
    test_urls = {
        # "Wikipedia (Reference)": "en.wikipedia.org/wiki/Formula_One",
        # "JS Rendered": "quotes.toscrape.com/js",
        # "Table Layout": "quotes.toscrape.com/tableful",
        # "Pagination": "quotes.toscrape.com",
        "Infinite Scroll": "quotes.toscrape.com/scroll",
    }

    results = []
    total_mean_time = 0
    iterations = 5

    # Test each URL
    for site_name, url in test_urls.items():
        try:
            stats = run_statistical_test(url, iterations)
            results.append({"site": site_name, "stats": stats})
            total_mean_time += stats["mean"]
            print(f"Scraped {site_name}:")
            print(f"  Mean time: {stats['mean']:.4f} ± {stats['ci_95']:.4f} seconds")
            print(f"  Range: {stats['min']:.4f} - {stats['max']:.4f} seconds")
        except Exception as e:
            print(f"Error scraping {site_name}: {str(e)}")

    # Create markdown results table
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join("jina_output", f"scraping_results_{timestamp}.md")

    with open(results_file, "w", encoding="utf-8") as f:
        f.write("# Jina.ai Scraping Test Results\n\n")
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
