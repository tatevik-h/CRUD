import math
import asyncio
from typing import Any

from collections import OrderedDict
from starlette.requests import Request

from config.core.settings import settings
from src.api.schemas import FeedbackRetrieve


class Paginator:
    DEFAULT_PAGE = 1
    DEFAULT_PAGE_SIZE = settings.FEEDBACK_DEFAULT_PAGE_SIZE

    def __init__(self, request: Request):
        self.request = request
        self._page_param = "page"
        self._page_size_param = "per_page"
        self._filter_param = "filter"

    async def _get_self_link(self, view_args: dict) -> str:
        url = self.request.url.include_query_params(
            page=view_args[self._page_param], per_page=view_args[self._page_size_param]
        )
        if view_args[self._filter_param]:
            url = url.include_query_params(filter=view_args[self._filter_param])
        return str(url)

    async def _get_first_page_link(self, first_page: int, view_args: dict) -> str:
        url = self.request.url.include_query_params(
            page=first_page,
            per_page=view_args[self._page_size_param],
        )
        if view_args[self._filter_param]:
            url = url.include_query_params(filter=view_args[self._filter_param])
        return str(url)

    async def _get_last_page_link(self, last_page: int, view_args: dict) -> str:
        url = self.request.url.include_query_params(
            page=last_page,
            per_page=view_args[self._page_size_param],
        )
        if view_args[self._filter_param]:
            url = url.include_query_params(filter=view_args[self._filter_param])
        return str(url)

    async def _get_prev_page_link(self, prev_page: int, view_args: dict) -> str:
        url = self.request.url.include_query_params(
            page=prev_page,
            per_page=view_args[self._page_size_param],
        )
        if view_args[self._filter_param]:
            url = url.include_query_params(filter=view_args[self._filter_param])
        return str(url)

    async def _get_next_page_link(self, next_page: int, view_args: dict) -> str:
        url = self.request.url.include_query_params(
            page=next_page,
            per_page=view_args[self._page_size_param],
        )
        if view_args[self._filter_param]:
            url = url.include_query_params(filter=view_args[self._filter_param])
        return str(url)

    async def paginate(
        self,
        query_model,
        collection_name: str,
        document_count: int,
        page: int = DEFAULT_PAGE,
        per_page: int = DEFAULT_PAGE_SIZE,
        filter_param: str = "",
    ) -> dict:
        prev_page, next_page = page - 1, page + 1
        first_page, last_page = 1, math.ceil(document_count / per_page)
        query_items = query_model.limit(per_page).offset((page - 1) * per_page)

        items = query_items.all()
        view_args = {
            self._page_param: page,
            self._page_size_param: per_page,
            self._filter_param: filter_param,
        }

        pagination_schema = {"self": {"href": await self._get_self_link(view_args)}}

        if items:
            pagination_schema["first"] = {
                "href": await self._get_first_page_link(first_page, view_args)
            }
            pagination_schema["last"] = {
                "href": await self._get_last_page_link(last_page, view_args)
            }
        if page > first_page:
            pagination_schema["prev"] = {
                "href": await self._get_prev_page_link(prev_page, view_args)
            }
        if page < last_page:
            pagination_schema["next"] = {
                "href": await self._get_next_page_link(next_page, view_args)
            }
        return {
            "total": last_page,
            "count": document_count,
            "_links": OrderedDict(sorted(pagination_schema.items())),
            "_embedded": {
                collection_name: [
                    FeedbackRetrieve(
                        id=item.id,
                        full_name=item.full_name,
                        phone_number=item.phone_number,
                        email=item.email,
                        time_created=item.time_created,
                        comment=item.comment,
                        score=item.score,
                        waiter_name=(item.waiter.name if item.waiter else None),
                    )
                    for item in items
                ]
            },
        }
