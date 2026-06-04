from __future__ import annotations

import aiohttp

from .const import BASE_URLS


class CrystalApiError(Exception):
    pass


class CrystalAuthError(CrystalApiError):
    pass


class CrystalRateLimitError(CrystalApiError):
    pass


class CrystalMaintenanceError(CrystalApiError):
    pass


class CrystalNotFoundError(CrystalApiError):
    pass


class CrystalApiClient:
    def __init__(self, api_key: str, environment: str, session: aiohttp.ClientSession) -> None:
        self._api_key = api_key
        self._base_url = BASE_URLS[environment]
        self._session = session

    def _headers(self) -> dict[str, str]:
        return {"x-api-key": self._api_key}

    async def _get(self, path: str) -> dict:
        url = f"{self._base_url}{path}"
        async with self._session.get(url, headers=self._headers()) as resp:
            if resp.status == 401 or resp.status == 403:
                raise CrystalAuthError("Invalid API key")
            if resp.status == 429:
                raise CrystalRateLimitError("Rate limit exceeded")
            if resp.status == 404:
                raise CrystalNotFoundError("Resource not found")
            if resp.status == 503:
                raise CrystalMaintenanceError("API is in maintenance mode")
            resp.raise_for_status()
            return await resp.json()

    async def list_vessels(self) -> list[dict]:
        data = await self._get("/connect/v1/vessels")
        return data.get("vessels", [])

    async def get_vessel(self, vessel_id: int) -> dict:
        return await self._get(f"/connect/v1/vessels/{vessel_id}")
