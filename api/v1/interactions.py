from datetime import datetime, timedelta
from typing import Dict
from uuid import uuid4
from fastapi import Body, Depends, HTTPException, Header, APIRouter, Response

from schemas.schemas import *
from services.authentications import JWTBearer
from services.mongo import get_mongo


router = APIRouter(prefix='/interactions')

podcast_collection = get_mongo()["podcast"]


@router.post("/like/{channel_id}/{episode_id}")
async def like(channel_id: int, episode_id: int, payload: dict = Depends(JWTBearer())):

    user_id = payload["user_identifier"]

    filter = {"channel_id": channel_id}

    doc = {"$pull": {f"episodes.{episode_id}.likes": user_id}}

    data = await podcast_collection.update_one(filter=filter, update=doc, upsert=True)

    if data.modified_count == 0:
        doc = {"$push": {f"episodes.{episode_id}.likes": user_id}}

        await podcast_collection.update_one(filter=filter, update=doc, upsert=True)

        return {"liked"}

    return {"unliked"}


@router.post("/comment/{channel_id}/{episode_id}")
async def create_comment(channel_id: int, episode_id: int, comment: Comment,
                         payload: dict = Depends(JWTBearer())
                         ):
    user_id = payload["user_identifier"]
    username = payload["username"]

    filter = {"channel_id": channel_id}
    current_dt = datetime.utcnow() + timedelta(hours=3.5)
    doc = {"$push": {f"episodes.{episode_id}.comment": {uuid4().hex: {'user_id': user_id, 'username': username, 'comment': comment.comment, 'dt': current_dt}}}}

    await podcast_collection.update_one(filter=filter, update=doc, upsert=True)
    return {"comment created"}


@router.post("/rmcomment/{channel_id}/{episode_id}/{comment_id}")
async def remove_comment(channel_id: int, episode_id: int, comment_id: str,
                         payload: dict = Depends(JWTBearer())
                         ):
    user_id = payload["user_identifier"]

    filter = {"channel_id": channel_id}
    doc = {"$pull": {f"episodes.{episode_id}.comment": {f"{comment_id}.user_id": user_id}}}

    await podcast_collection.update_one(filter=filter, update=doc)
    return {"comment removed"}


@router.post("/bookmark/{channel_id}")
async def bookmark(channel_id: int, payload: dict = Depends(JWTBearer())):
    user_id = payload["user_identifier"]

    filter = {"channel_id": channel_id}
    doc = {"$pull": {"bookmark": user_id}}

    data = await podcast_collection.update_one(filter=filter, update=doc, upsert=True)

    if data.modified_count == 0:
        doc = {"$push": {"bookmark": user_id}}
        await podcast_collection.update_one(filter=filter, update=doc, upsert=True)

        return {"channel bookmarked"}
    return {"bookmark removed"}
