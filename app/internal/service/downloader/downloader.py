import aiohttp


async def download_object(url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.read()
                return data
            else:
                raise Exception('Could not download provided image')
