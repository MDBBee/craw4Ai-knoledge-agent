import asyncio
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, DefaultMarkdownGenerator

async def crawl_sequential(urls: List[str]):
    print("\n=== Sequential Crawling with session Reuse ===")

    browser_config = BrowserConfig(
        headless=True, 
        #   For better performance in Docker or low-memory environments:
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
        )
    crawl_config = CrawlerRunConfig(markdown_generator=DefaultMarkdownGenerator())

    async with AsyncWebCrawler(config=browser_config) as crawler:
        try:
            session_id: "session1"  # Reuse the same accross all URLs
            for url in urls:
                result = await crawler.arun(
                    url=url,
                    config=crawl_config,
                    session_id=session_id,

                )
                if result.success:
                    print(f"Successfully crawled: {url}")
                    print(f"Markdown length: {len(result.markdown_v2.raw_markdown)}")
                else:
                    print(f"Failed: {url} - Error: {result.error_message}")
        finally:
            print("DONE-COMPLETED")
async def get_urls():
    """Fetches all urls in (https://ai.pydantic.dev/)
    """
    async with AsyncWebCrawler() as crawler:
    # Run the crawler on a URL
    result = await crawler.arun(url="https://ai.pydantic.dev/")

    # Print the extracted content
    # print(result.markdown)
    internal_links = result.links.get("internal", [])
    external_links = result.links.get("external", [])
    print(f"Found {len(internal_links)} internal links.")
    for l in internal_links:
        print("\n")
        print(l)
async def main():
    # Create an instance of AsyncWebCrawler

        # print(internal_links)
        # print(f"Found {len(external_links)} external links.")
        # print(external_links)
        # print(f"Found {len(result.media)} media items.")
        # print(result.media)

# Run the async main function
asyncio.run(main())
