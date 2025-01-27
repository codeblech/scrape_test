import asyncio
import time
from datetime import datetime
import os

from crawlee.crawlers import BeautifulSoupCrawler, BeautifulSoupCrawlingContext


async def main() -> None:
    # Setup crawler
    crawler = BeautifulSoupCrawler(
        # Limit the crawl to max requests. Remove or increase it for crawling all links.
        max_requests_per_crawl=10,
    )

    # Define the default request handler, which will be called for every request.
    @crawler.router.default_handler
    async def request_handler(context: BeautifulSoupCrawlingContext) -> None:
        context.log.info(f"Processing {context.request.url} ...")

        # Extract data from the page.
        data = {
            "url": context.request.url,
            "body": context.soup.contents if context.soup.contents else None,
        }

        # Push the extracted data to the default dataset.
        await context.push_data(data)

        # Enqueue all links found on the page.
        # await context.enqueue_links()

    # Start timing the crawling operation
    start_time = time.perf_counter()

    # Run the crawler with the initial list of URLs
    await crawler.run(["https://en.wikipedia.org/wiki/Formula_One"])

    # End timing and calculate execution time
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    print(f"Crawling completed in {execution_time:.4f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
