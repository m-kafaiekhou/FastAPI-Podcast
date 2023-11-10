from typing import Dict
from fastapi import Body, Depends, HTTPException, Query, APIRouter, Response

from schemas.schemas import *
from services.authentications import JWTBearer
from services.django import DjangoRequests
from utils.auth import generate_token
from services.redis import get_redis


router = APIRouter(prefix='/podcast')


@router.get('/list', response_model=Dict)
async def podcast_list(page: str = Query(None)):
    adapter = DjangoRequests()

    params = {'page': page} if page else None
    response = await adapter.get_podcasts(params)
    
    return response.json()
    


@router.get('/{podcast_id}/episodes', response_model=Dict)
async def podcast_episode_list(podcast_id: int, page: str = Query(None)):
    adapter = DjangoRequests()

    params = {'page': page} if page else None
    response = await adapter.get_podcast_episodes(podcast_id, params)
    print(response.json())
    return response.json()


@router.get('/episode/{episode_id}', response_model=Dict)
async def episode_detail(episode_id: int, page: str = Query(None)):
    adapter = DjangoRequests()

    params = {'page': page} if page else None
    response = await adapter.get_episode(episode_id, params)
    print(response.json())
    return response.json()
