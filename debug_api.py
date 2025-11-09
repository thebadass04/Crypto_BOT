#!/usr/bin/env python3
"""Debug script to test API responses"""

import json
from app.bybit_client import bybit_client

print("=" * 60)
print("🔍 API RESPONSE DEBUGGER")
print("=" * 60)

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}")
    print(json.dumps(response, indent=2))
    print()

try:
    print("\n1️⃣  Testing Balance...")
    try:
        balance = bybit_client.get_wallet_balance(account_type="UNIFIED", coin="USDT")
        print_response("BALANCE RESPONSE", balance)
        
        if balance.get('retCode') == 0:
            result = balance.get('result', {})
            accounts = result.get('list', [])
            print(f"✓ Number of accounts: {len(accounts)}")
            
            if accounts:
                print(f"✓ First account structure:")
                print(json.dumps(accounts[0], indent=2))
                
                coins = accounts[0].get('coin', [])
                print(f"✓ Number of coins: {len(coins)}")
                
                for coin in coins:
                    print(f"  💰 {coin.get('coin')}: {coin.get('walletBalance')}")
        else:
            print(f"❌ Balance error: {balance.get('retMsg')}")
    except Exception as e:
        print(f"❌ Balance exception: {e}")
        import traceback
        traceback.print_exc()

    print("\n2️⃣  Testing Positions...")
    try:
        positions = bybit_client.get_positions(category="linear", symbol=None)
        print_response("POSITIONS RESPONSE", positions)
        
        if positions.get('retCode') == 0:
            result = positions.get('result', {})
            pos_list = result.get('list', [])
            print(f"✓ Number of positions: {len(pos_list)}")
            
            if pos_list:
                print(f"✓ First position structure:")
                print(json.dumps(pos_list[0], indent=2))
                
                for pos in pos_list:
                    size = float(pos.get('size', 0))
                    if size > 0:
                        print(f"  📊 {pos.get('symbol')}: Size={size}, Side={pos.get('side')}")
            else:
                print("ℹ️  No positions found")
        else:
            print(f"❌ Positions error: {positions.get('retMsg')}")
    except Exception as e:
        print(f"❌ Positions exception: {e}")
        import traceback
        traceback.print_exc()

    print("\n3️⃣  Testing Open Orders...")
    try:
        orders = bybit_client.get_open_orders(category="linear", symbol=None)
        print_response("ORDERS RESPONSE", orders)
        
        if orders.get('retCode') == 0:
            result = orders.get('result', {})
            order_list = result.get('list', [])
            print(f"✓ Number of orders: {len(order_list)}")
            
            if order_list:
                print(f"✓ First order structure:")
                print(json.dumps(order_list[0], indent=2))
                
                for order in order_list:
                    print(f"  📝 {order.get('symbol')}: {order.get('side')} {order.get('qty')} @ {order.get('price')}")
            else:
                print("ℹ️  No open orders")
        else:
            print(f"❌ Orders error: {orders.get('retMsg')}")
    except Exception as e:
        print(f"❌ Orders exception: {e}")
        import traceback
        traceback.print_exc()

    print("\n4️⃣  Testing Market Price...")
    try:
        ticker = bybit_client.get_tickers(category="linear", symbol="BTCUSDT")
        print_response("TICKER RESPONSE (BTCUSDT)", ticker)
        
        if ticker.get('retCode') == 0:
            result = ticker.get('result', {})
            ticker_list = result.get('list', [])
            if ticker_list:
                print(f"✓ BTCUSDT Price: ${ticker_list[0].get('lastPrice')}")
        else:
            print(f"❌ Ticker error: {ticker.get('retMsg')}")
    except Exception as e:
        print(f"❌ Ticker exception: {e}")

except KeyboardInterrupt:
    print("\n\n⚠️  Interrupted by user")
except Exception as e:
    print(f"\n\n❌ Fatal error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ Debug complete!")
print("=" * 60)
