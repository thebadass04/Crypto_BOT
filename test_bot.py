#!/usr/bin/env python3
"""Script de teste rápido para o bot"""

import sys
import os

print("=" * 50)
print("🧪 Testing Bot Configuration")
print("=" * 50)

try:
    print("\n1. Testing config import...")
    from app.config import settings
    print(f"✓ Config loaded")
    print(f"  - API Key: {settings.bybit_api_key[:10]}...{settings.bybit_api_key[-4:]}")
    print(f"  - Testnet: {settings.use_testnet}")
    print(f"  - Demo: {settings.use_demo}")
    print(f"  - Symbols: {settings.symbols_list}")
    
    print("\n2. Testing bybit client import...")
    from app.bybit_client import bybit_client
    print("✓ Bybit client initialized")
    
    print("\n3. Testing API connection...")
    try:
        server_time = bybit_client.get_server_time()
        if server_time.get('retCode') == 0:
            print(f"✓ Server time: {server_time['result']['timeSecond']}")
        else:
            print(f"❌ Server time failed: {server_time.get('retMsg')}")
    except Exception as e:
        print(f"❌ Server time failed: {e}")
    
    print("\n4. Testing account balance...")
    try:
        balance = bybit_client.get_wallet_balance()
        if balance.get('retCode') == 0:
            print("✓ Balance retrieved successfully")
            usdt_balance = 0
            if balance['result']['list']:
                for coin in balance['result']['list'][0]['coin']:
                    if coin['coin'] == 'USDT':
                        usdt_balance = float(coin['walletBalance'])
                        print(f"  💰 USDT Balance: {usdt_balance}")
                        break
        else:
            print(f"❌ Balance failed: {balance.get('retMsg')}")
    except Exception as e:
        print(f"❌ Balance failed: {e}")
    
    print("\n5. Testing market data...")
    try:
        ticker = bybit_client.get_tickers(category="linear", symbol="BTCUSDT")
        if ticker.get('retCode') == 0:
            price = ticker['result']['list'][0]['lastPrice']
            print(f"✓ BTCUSDT Price: ${price}")
        else:
            print(f"❌ Market data failed: {ticker.get('retMsg')}")
    except Exception as e:
        print(f"❌ Market data failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Bot configuration test complete!")
    print("=" * 50)
    print("\n💡 To start the bot, run: python run.py")
    print("   Then open: http://localhost:8000")
    
except Exception as e:
    print(f"\n❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
