import os
import sys
import requests
import time
import concurrent.futures
import asyncio
import aiohttp
from multiprocessing import Pool


def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = url.split("/")[-1]
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename, None
        else:
            return None, f"Failed to download image from {url}"
    except Exception as e:
        return None, str(e)


async def download_image_async(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                filename = url.split("/")[-1]
                with open(filename, 'wb') as f:
                    f.write(await response.read())
                return filename, None
            else:
                return None, f"Failed to download image from {url}"
    except Exception as e:
        return None, str(e)


def download_images_multithread(urls):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as executor:
        future_to_url = {executor.submit(download_image, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                filename, error = future.result()
                if error is not None:
                    print(error)
                else:
                    print(f"Downloaded {filename}")
            except Exception as e:
                print(f"Exception occurred: {str(e)}")
    end_time = time.time()
    print(f"Total time taken for multithreaded download: {end_time - start_time} seconds")


def download_images_multiprocess(urls):
    start_time = time.time()
    with Pool(len(urls)) as p:
        results = p.map(download_image, urls)
        for filename, error in results:
            if error is not None:
                print(error)
            else:
                print(f"Downloaded {filename}")
    end_time = time.time()
    print(f"Total time taken for multiprocess download: {end_time - start_time} seconds")


async def download_images_async(urls):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_async(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        for filename, error in results:
            if error is not None:
                print(error)
            else:
                print(f"Downloaded {filename}")
    end_time = time.time()
    print(f"Total time taken for asynchronous download: {end_time - start_time} seconds")


if __name__ == "__main__":
    # Задаем URL-адреса непосредственно в коде
    urls = [
        "https://example.com/images/image1.jpg",
        "https://example.com/images/image2.jpg"
    ]

    print("URLs to be processed:", urls)

    print("Starting multithreaded download...")
    download_images_multithread(urls)

    print("\nStarting multiprocess download...")
    download_images_multiprocess(urls)

    print("\nStarting asynchronous download...")
    asyncio.run(download_images_async(urls))
