import aiohttp
import asyncio

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    url = 'https://bcfp.shenzhen.chinatax.gov.cn/verify/scan?hash=01645d47765dd7aec052188019747d2b9ff4a734a5a7c45ffec86832c070910a19&bill_num=09826096&total_amount=96200'
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        print(html)

asyncio.run(main())
