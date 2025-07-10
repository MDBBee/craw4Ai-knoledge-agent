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
            session_id = "session1"  # Reuse the same accross all URLs
            for url in urls:
                result = await crawler.arun(
                    url=url,
                    config=crawl_config,
                    session_id=session_id,

                )
                if result.success:
                    print(f"Successfully crawled: {url}")
                    print(f"Markdown length: {len(result.markdown.raw_markdown)}")
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
        # print(result.links)
        if result.success:
            return result.links.get("internal", [])
        else:
            print("Error fetching urls with 'get_urls' func...")
    
async def main():
    links = await get_urls()
    # print(f"Len: {len(links)} \n")
    # print(links[0], type(links[0]))
    urls = [link["href"] for link in links]
    for l in urls:
        print(f"{l}--- \n")
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        await crawl_sequential(urls)
    else:
        print("No urls found to crawl")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
