import os
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, ConfigDict

class Settings(BaseSettings):
    # Use Field with env= to map to existing environment variable names
    bybit_api_key: str = Field("", env="BYBIT_API_KEY")
    bybit_api_secret: str = Field("", env="BYBIT_API_SECRET")
    use_testnet: bool = Field(True, env="USE_TESTNET")
    use_demo: bool = Field(False, env="USE_DEMO")
    symbols: str = Field("BTCUSDT,ETHUSDT,BNBUSDT", env="SYMBOLS")

    # Pydantic v2 style config for BaseSettings
    model_config = ConfigDict(env_file=".env", case_sensitive=False)

    @field_validator("symbols", mode="before")
    def _normalize_symbols(cls, v: Union[str, List[str], None]) -> str:
        """
        Accept a comma separated string or a list of symbols and normalize:
        - strip whitespace
        - uppercase symbols
        - join back into a comma separated string
        """
        if v is None:
            return ""
        if isinstance(v, list):
            parts = v
        else:
            parts = str(v).split(",")
        normalized = [p.strip().upper() for p in parts if p and str(p).strip()]
        return ",".join(normalized)

    @property
    def symbols_list(self) -> List[str]:
        """Retorna lista de símbolos como lista de strings limpas/uppercase"""
        if not self.symbols:
            return []
        return [s for s in (item.strip() for item in self.symbols.split(",")) if s]

    @property
    def base_url(self) -> str:
        """Retorna URL base da API Bybit"""
        if self.use_testnet:
            return "https://api-testnet.bybit.com"
        if self.use_demo:
            return "https://api-demo.bybit.com"
        return "https://api.bybit.com"


settings = Settings()
