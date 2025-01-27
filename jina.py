import requests
import time
import os
from datetime import datetime


def scrape_jina_ai(url: str, output_dir: str = "jina_output") -> tuple[float, str]:
    """
    Scrape content from r.jina.ai/<url> and save to markdown file.

    Args:
        url: The URL path to append to r.jina.ai/
        output_dir: Directory to save the markdown file (default: 'jina_output')

    Returns:
        tuple: (execution_time_in_seconds, output_file_path)
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
        response.raise_for_status()  # Raise exception for bad status codes

        # Generate output filename using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"jina_scrape_{timestamp}.md")

        # Save response content to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response.text)

        # End timing
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        return execution_time, output_file

    except requests.RequestException as e:
        raise Exception(f"Failed to scrape {full_url}: {str(e)}")


# Example usage
if __name__ == "__main__":
    # Test URLs
    test_urls = {
        "Wikipedia (Reference)": "en.wikipedia.org/wiki/Formula_One",
        "JS Rendered": "quotes.toscrape.com/js",
        "Table Layout": "quotes.toscrape.com/tableful",
        "Pagination": "quotes.toscrape.com",
        "Infinite Scroll": "quotes.toscrape.com/scroll",
    }

    # Store results
    results = []
    total_time = 0

    # Test each URL
    for site_name, url in test_urls.items():
        try:
            execution_time, output_file = scrape_jina_ai(url)
            results.append(
                {"site": site_name, "time": execution_time, "file": output_file}
            )
            total_time += execution_time
            print(f"Scraped {site_name} in {execution_time:.4f} seconds")
            print(f"Output saved to: {output_file}")
        except Exception as e:
            print(f"Error scraping {site_name}: {str(e)}")

    # Create markdown results table
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join("jina_output", f"scraping_results_{timestamp}.md")

    with open(results_file, "w", encoding="utf-8") as f:
        f.write("# Jina.ai Scraping Test Results\n\n")
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
