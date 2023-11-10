import httpx
from utils.singleton import Singleton
# import asyncio


class DjangoRequests(metaclass=Singleton):
    POD_LIST_URL = 'http://localhost:8000/podcasts/'
    POD_EP_LIST_URL = 'http://localhost:8000/podcasts/episodes/' # + pk/
    POD_EP_DETAIL_URL = 'http://localhost:8000/podcasts/episode/detail/' # + pk/


    async def get_podcasts(self, params: dict = None):
        response = await self.aget(self.POD_LIST_URL, params)
        return response
    
    async def get_podcast_episodes(self, pk: int,  params: dict = None):
        url = f'{self.POD_EP_LIST_URL}{pk}/'
        response = await self.aget(url, params)
        return response
    
    async def get_episode(self, pk: int,  params: dict = None):
        url = f'{self.POD_EP_DETAIL_URL}{pk}/'
        response = await self.aget(url, params)
        return response

    async def aget(self, url: str, params: dict):
        async with httpx.AsyncClient() as client:
            return await client.get(url=url, params=params)
        
