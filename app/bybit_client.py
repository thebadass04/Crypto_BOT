from typing import Optional, Dict, Any, List
from pybit.unified_trading import HTTP
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BybitClient:
    """Cliente para interagir com a API v5 da Bybit usando pybit"""
    
    def __init__(self):
        """Inicializa o cliente Bybit"""
        try:
            if not settings.bybit_api_key or not settings.bybit_api_secret:
                raise ValueError("API credentials not configured. Please check your .env file.")
            
            if settings.use_testnet:
                self.client = HTTP(
                    testnet=True,
                    api_key=settings.bybit_api_key,
                    api_secret=settings.bybit_api_secret
                )
                logger.info("✓ Connected to Bybit TESTNET")
            elif settings.use_demo:
                self.client = HTTP(
                    testnet=False,
                    api_key=settings.bybit_api_key,
                    api_secret=settings.bybit_api_secret
                )
                self.client.endpoint = "https://api-demo.bybit.com"
                logger.info("✓ Connected to Bybit DEMO")
            else:
                self.client = HTTP(
                    testnet=False,
                    api_key=settings.bybit_api_key,
                    api_secret=settings.bybit_api_secret
                )
                logger.info("⚠️  Connected to Bybit MAINNET")
                
        except Exception as e:
            logger.error(f"Failed to initialize Bybit client: {e}")
            raise

    def _handle_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Processa resposta da API e trata erros"""
        if response.get('retCode') != 0:
            error_msg = response.get('retMsg', 'Unknown error')
            logger.error(f"API Error: {error_msg}")
            raise Exception(f"Bybit API Error: {error_msg}")
        return response

    def get_server_time(self) -> Dict[str, Any]:
        """Obtém tempo do servidor"""
        try:
            response = self.client.get_server_time()
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting server time: {e}")
            raise

    def get_account_info(self) -> Dict[str, Any]:
        """Obtém informações da conta"""
        try:
            response = self.client.get_account_info()
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            raise

    def get_wallet_balance(self, account_type: str = "UNIFIED", coin: Optional[str] = None) -> Dict[str, Any]:
        """Obtém saldo da carteira"""
        try:
            params = {"accountType": account_type}
            if coin:
                params["coin"] = coin
            response = self.client.get_wallet_balance(**params)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting wallet balance: {e}")
            raise

    def get_positions(self, category: str = "linear", symbol: Optional[str] = None, settle_coin: str = "USDT") -> Dict[str, Any]:
        """Obtém posições abertas"""
        try:
            params = {"category": category}
            if symbol:
                params["symbol"] = symbol
            else:
                params["settleCoin"] = settle_coin
            response = self.client.get_positions(**params)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            raise

    def get_tickers(self, category: str = "linear", symbol: Optional[str] = None) -> Dict[str, Any]:
        """Obtém preços atuais (tickers)"""
        try:
            params = {"category": category}
            if symbol:
                params["symbol"] = symbol
            response = self.client.get_tickers(**params)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting tickers: {e}")
            raise

    def get_klines(
        self,
        category: str = "linear",
        symbol: str = "BTCUSDT",
        interval: str = "60",
        limit: int = 200
    ) -> Dict[str, Any]:
        """Obtém dados de candlestick (klines)"""
        try:
            response = self.client.get_kline(
                category=category,
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting klines: {e}")
            raise

    def place_order(
        self,
        category: str,
        symbol: str,
        side: str,
        order_type: str,
        qty: str,
        price: Optional[str] = None,
        time_in_force: str = "GTC",
        position_idx: int = 0
    ) -> Dict[str, Any]:
        """Cria uma ordem"""
        try:
            params = {
                "category": category,
                "symbol": symbol,
                "side": side,
                "orderType": order_type,
                "qty": qty,
                "timeInForce": time_in_force,
                "positionIdx": position_idx
            }

            if price and order_type == "Limit":
                params["price"] = price

            response = self.client.place_order(**params)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            raise

    def get_open_orders(self, category: str = "linear", symbol: Optional[str] = None) -> Dict[str, Any]:
        """Lista ordens abertas"""
        try:
            params = {"category": category}
            if symbol:
                params["symbol"] = symbol
            response = self.client.get_open_orders(**params)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error getting open orders: {e}")
            raise

    def cancel_order(self, category: str, symbol: str, order_id: str) -> Dict[str, Any]:
        """Cancela uma ordem"""
        try:
            response = self.client.cancel_order(
                category=category,
                symbol=symbol,
                orderId=order_id
            )
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            raise


bybit_client = BybitClient()