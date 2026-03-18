import aiohttp
import asyncio

# ================== YOUR APIs ==================

SHORTLINK_API_LECTURE = "https://arolinks.com/api?api=6d6b19730d806e46dc258768e715e5c4a498fb97&url={url}&alias={alias}"
SHORTLINK_API_BOOK = "https://arolinks.com/api?api=b43087cc2e97e7131232209d2adc98364ecbf21f&url={url}&alias={alias}"

# ================== SHORTLINK GENERATOR ==================

async def generate_shortlink(url: str, alias: str, type_: str = "lecture"):
    api = SHORTLINK_API_LECTURE if type_ == "lecture" else SHORTLINK_API_BOOK
    final_url = api.format(url=url, alias=alias)

    try:
        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(final_url) as resp:
                if resp.status == 200:
                    data = await resp.text()
                    return data.strip()
                else:
                    print(f"Shortlink API Error: {resp.status}")
                    return url

    except asyncio.TimeoutError:
        print("Shortlink timeout")
        return url

    except Exception as e:
        print("Shortlink error:", e)
        return url
