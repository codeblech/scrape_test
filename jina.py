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
    try:
        execution_time, output_file = scrape_jina_ai("en.wikipedia.org/wiki/Formula_One")
        print(f"Scraping completed in {execution_time:.4f} seconds")
        print(f"Output saved to: {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
