from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from datetime import datetime
from typing import List, Optional
import uvicorn
import asyncio
import logging

from app.config import settings
from app.bybit_client import bybit_client
from app.models import (
    OrderRequest, OrderResponse, Position, Balance,
    PriceData, Kline, SignalResponse, AccountInfo
)
from app.strategy.simple_sma import sma_strategy

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Bybit Trading Bot",
    description="Trading bot minimalista com estratégia SMA",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "testnet": settings.use_testnet,
        "symbols": settings.symbols_list
    }


@app.get("/api/debug/raw")
async def debug_raw_responses():
    """Debug endpoint to see raw API responses"""
    try:
        results = {}

        try:
            balance = await asyncio.to_thread(bybit_client.get_wallet_balance)
            results['balance'] = {
                'retCode': balance.get('retCode'),
                'retMsg': balance.get('retMsg'),
                'accounts_count': len(balance.get('result', {}).get('list', [])),
                'raw': balance
            }
        except Exception as e:
            results['balance'] = {'error': str(e)}

        try:
            positions = await asyncio.to_thread(bybit_client.get_positions, category="linear")
            results['positions'] = {
                'retCode': positions.get('retCode'),
                'retMsg': positions.get('retMsg'),
                'positions_count': len(positions.get('result', {}).get('list', [])),
                'raw': positions
            }
        except Exception as e:
            results['positions'] = {'error': str(e)}

        try:
            orders = await asyncio.to_thread(bybit_client.get_open_orders, category="linear")
            results['orders'] = {
                'retCode': orders.get('retCode'),
                'retMsg': orders.get('retMsg'),
                'orders_count': len(orders.get('result', {}).get('list', [])),
                'raw': orders
            }
        except Exception as e:
            results['orders'] = {'error': str(e)}

        return results
    except Exception as e:
        return {'error': str(e)}


@app.get("/api/account")
async def get_account():
    try:
        logger.info("Getting account info...")
        response = await asyncio.to_thread(bybit_client.get_account_info)
        logger.info(f"Account response: {response}")

        if response.get("retCode") != 0:
            error_msg = response.get("retMsg", "Unknown error")
            logger.error(f"Account error: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        return response.get("result", {})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Account exception: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/balance")
async def get_balance():
    try:
        logger.info("Getting wallet balance...")
        response = await asyncio.to_thread(bybit_client.get_wallet_balance)
        logger.info(f"Balance response retCode: {response.get('retCode')}")
        
        if response.get("retCode") != 0:
            error_msg = response.get("retMsg", "Unknown error")
            logger.error(f"Balance error: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)

        result = response.get("result", {})
        balances = []

        accounts = result.get("list", [])
        logger.info(f"Number of accounts: {len(accounts)}")
        
        if not accounts:
            logger.warning("No accounts found in balance response")
            logger.warning(f"Full result structure: {result}")
            return {"balances": [], "debug": "No accounts in response"}

        for account in accounts:
            logger.info(f"Account type: {account.get('accountType')}")
            logger.info(f"Full account data: {account}")
            
            coins = account.get("coin", [])
            logger.info(f"Number of coins in account: {len(coins)}")
            
            if not coins:
                logger.warning("No coins found in account!")
                logger.warning(f"Account keys: {list(account.keys())}")
                return {"balances": [], "debug": f"No coins in account. Account has keys: {list(account.keys())}"}

            for coin_data in coins:
                wallet_balance = float(coin_data.get("walletBalance", 0))
                equity = float(coin_data.get("equity", 0))
                available = float(coin_data.get("availableToWithdraw", 0))
                
                logger.info(f"Coin: {coin_data.get('coin')}, Balance: {wallet_balance}, Equity: {equity}, Available: {available}")
                
                balances.append({
                    "coin": coin_data.get("coin"),
                    "wallet_balance": wallet_balance,
                    "available_balance": available,
                    "equity": equity
                })

        logger.info(f"Returning {len(balances)} balances")
        
        if not balances:
            return {"balances": [], "debug": "All coins have 0 balance"}
            
        return {"balances": balances}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Balance exception: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/positions")
async def get_positions(symbol: Optional[str] = None):
    try:
        logger.info(f"Getting positions for symbol: {symbol}")
        response = await asyncio.to_thread(bybit_client.get_positions, category="linear", symbol=symbol)
        logger.info(f"Positions response retCode: {response.get('retCode')}")

        if response.get("retCode") != 0:
            error_msg = response.get("retMsg", "Unknown error")
            logger.error(f"Positions error: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)

        result = response.get("result", {})
        positions = []

        pos_list = result.get("list", [])
        logger.info(f"Number of positions in response: {len(pos_list)}")

        for pos in pos_list:
            size = float(pos.get("size", 0))
            logger.info(f"Position {pos.get('symbol')}: size={size}, side={pos.get('side')}")

            if size > 0:
                positions.append({
                    "symbol": pos.get("symbol"),
                    "side": pos.get("side"),
                    "size": size,
                    "entry_price": float(pos.get("avgPrice", 0)),
                    "mark_price": float(pos.get("markPrice", 0)),
                    "unrealised_pnl": float(pos.get("unrealisedPnl", 0)),
                    "leverage": float(pos.get("leverage", 1))
                })

        logger.info(f"Returning {len(positions)} active positions")
        return {"positions": positions}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Positions exception: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/price/{symbol}")
async def get_price(symbol: str):
    try:
        logger.info(f"Getting price for {symbol}")
        response = await asyncio.to_thread(bybit_client.get_tickers, category="linear", symbol=symbol)

        if response.get("retCode") != 0:
            error_msg = response.get("retMsg", "Unknown error")
            logger.error(f"Price error: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)

        result = response.get("result", {})
        ticker_list = result.get("list", [])

        if not ticker_list:
            logger.warning(f"No ticker found for {symbol}")
            raise HTTPException(status_code=404, detail="Symbol not found")

        ticker = ticker_list[0]
        return {
            "symbol": ticker.get("symbol"),
            "price": float(ticker.get("lastPrice", 0)),
            "timestamp": int(ticker.get("time", 0))
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Price exception: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/klines/{symbol}")
async def get_klines(symbol: str, interval: str = "60", limit: int = 100):
    try:
        response = await asyncio.to_thread(
            bybit_client.get_klines,
            symbol=symbol,
            interval=interval,
            limit=limit
        )

        if response.get("retCode") != 0:
            raise HTTPException(status_code=400, detail=response.get("retMsg"))

        result = response.get("result", {})
        klines_data = result.get("list", [])

        klines = []
        for k in klines_data:
            klines.append({
                "timestamp": int(k[0]),
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5])
            })

        klines.reverse()

        return {"klines": klines}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/signal/{symbol}")
async def generate_signal(symbol: str, interval: str = "60", limit: int = 100):
    try:
        klines_response = await get_klines(symbol, interval, limit)
        klines_data = klines_response["klines"]

        klines = [Kline(**k) for k in klines_data]

        # Run the potentially CPU-bound pandas analysis in a thread to avoid blocking the event loop
        signal, sma_fast, sma_slow = await asyncio.to_thread(sma_strategy.analyze_with_pandas, klines)

        current_price = klines[-1].close if klines else 0

        return {
            "symbol": symbol,
            "signal": signal.value,
            "sma_fast": round(sma_fast, 2),
            "sma_slow": round(sma_slow, 2),
            "current_price": round(current_price, 2),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/order")
async def create_order(order: OrderRequest):
    try:
        response = await asyncio.to_thread(
            bybit_client.place_order,
            category="linear",
            symbol=order.symbol,
            side=order.side.value,
            order_type=order.order_type.value,
            qty=str(order.qty),
            price=str(order.price) if order.price else None
        )

        if response.get("retCode") != 0:
            raise HTTPException(status_code=400, detail=response.get("retMsg"))

        result = response.get("result", {})

        return {
            "order_id": result.get("orderId"),
            "symbol": order.symbol,
            "side": order.side.value,
            "order_type": order.order_type.value,
            "qty": order.qty,
            "price": order.price,
            "status": "created",
            "created_time": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/orders")
async def get_orders(symbol: Optional[str] = None):
    try:
        logger.info(f"Getting open orders for symbol: {symbol}")
        response = await asyncio.to_thread(bybit_client.get_open_orders, category="linear", symbol=symbol)
        logger.info(f"Orders response retCode: {response.get('retCode')}")

        if response.get("retCode") != 0:
            error_msg = response.get("retMsg", "Unknown error")
            logger.error(f"Orders error: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)

        result = response.get("result", {})
        orders = []

        order_list = result.get("list", [])
        logger.info(f"Number of orders in response: {len(order_list)}")

        for order in order_list:
            orders.append({
                "order_id": order.get("orderId"),
                "symbol": order.get("symbol"),
                "side": order.get("side"),
                "order_type": order.get("orderType"),
                "qty": float(order.get("qty", 0)),
                "price": float(order.get("price", 0)),
                "status": order.get("orderStatus"),
                "created_time": order.get("createdTime")
            })

        logger.info(f"Returning {len(orders)} orders")
        return {"orders": orders}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Orders exception: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8080,
        reload=True
    )