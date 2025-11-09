#!/usr/bin/env python3
"""
API Key Validation Script
This script helps you verify if your Bybit API keys are working correctly
"""

import os
import sys
from pybit.unified_trading import HTTP

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ Loaded environment variables from .env file")
except ImportError:
    print("ℹ️  python-dotenv not installed. Using system environment variables only.")
except Exception as e:
    print(f"⚠️  Could not load .env file: {e}")


def validate_api_keys():
    """Validate API keys by testing basic API calls"""
    
    print("\n" + "="*50)
    print("🔐 API Key Validation Test")
    print("="*50)
    
    api_key = os.getenv('BYBIT_API_KEY')
    api_secret = os.getenv('BYBIT_API_SECRET')
    use_testnet = os.getenv('USE_TESTNET', 'true').lower() == 'true'
    use_demo = os.getenv('USE_DEMO', 'false').lower() == 'true'
    
    if not api_key or not api_secret:
        print("❌ API credentials not found!")
        print("\n📋 Please set your API credentials:")
        print("1. Edit the .env file in this directory")
        print("2. Or set environment variables:")
        print("   BYBIT_API_KEY=your_key")
        print("   BYBIT_API_SECRET=your_secret")
        return False
    
    print(f"✓ API Key found: {api_key[:8]}...{api_key[-4:]}")
    print(f"✓ API Secret found: {api_secret[:8]}...{api_secret[-4:]}")
    
    if use_testnet:
        print("🌐 Using TESTNET")
    elif use_demo:
        print("🎮 Using DEMO TRADING (Mainnet)")
    else:
        print("⚠️  Using LIVE MAINNET")
    
    try:
        if use_testnet:
            client = HTTP(
                testnet=True,
                api_key=api_key,
                api_secret=api_secret
            )
        elif use_demo:
            client = HTTP(
                testnet=False,
                api_key=api_key,
                api_secret=api_secret
            )
            client.endpoint = "https://api-demo.bybit.com"
        else:
            client = HTTP(
                testnet=False,
                api_key=api_key,
                api_secret=api_secret
            )
        print("✓ API client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize API client: {e}")
        return False
    
    print("\n🧪 Test 1: Server Time (No Auth)")
    try:
        server_time = client.get_server_time()
        if server_time['retCode'] == 0:
            print(f"✓ Server time: {server_time['result']['timeSecond']}")
        else:
            print(f"❌ Server time test failed: {server_time['retMsg']}")
            return False
    except Exception as e:
        print(f"❌ Server time test failed: {e}")
        return False
    
    print("\n🧪 Test 2: Account Balance (Auth Required)")
    try:
        balance = client.get_wallet_balance(accountType="UNIFIED", coin="USDT")
        if balance['retCode'] == 0:
            usdt_balance = 0
            if balance['result']['list']:
                for coin in balance['result']['list'][0]['coin']:
                    if coin['coin'] == 'USDT':
                        usdt_balance = float(coin['walletBalance'])
                        break
            print(f"✅ Authentication successful!")
            print(f"💰 USDT Balance: {usdt_balance}")
        else:
            print(f"❌ Balance check failed: {balance['retMsg']}")
            return False
    except Exception as e:
        print(f"❌ Balance test failed: {e}")
        print("💡 This usually means:")
        if use_testnet:
            print("   - Your API keys are for mainnet, but you're using testnet")
            print("   - Your testnet API keys are invalid or expired")
            print("   - API key permissions are insufficient")
        elif use_demo:
            print("   - Your API keys are not configured for demo trading")
            print("   - Your demo API keys are invalid or expired")
            print("   - API key permissions are insufficient")
        else:
            print("   - Your API keys are for testnet/demo, but you're using live mainnet")
            print("   - Your mainnet API keys are invalid or expired")
            print("   - API key permissions are insufficient")
        return False
    
    print("\n🧪 Test 3: Market Data")
    try:
        ticker = client.get_tickers(category="linear", symbol="BTCUSDT")
        if ticker['retCode'] == 0:
            price = ticker['result']['list'][0]['lastPrice']
            print(f"✓ BTCUSDT Price: ${price}")
        else:
            print(f"❌ Market data test failed: {ticker['retMsg']}")
    except Exception as e:
        print(f"❌ Market data test failed: {e}")
    
    print("\n" + "="*50)
    print("🎉 API Key Validation Complete!")
    print("✅ Your API keys are working correctly")
    
    if use_testnet:
        print("🌐 Connected to: TESTNET")
    elif use_demo:
        print("🎮 Connected to: DEMO TRADING (Mainnet)")
    else:
        print("⚠️  Connected to: LIVE MAINNET")
    
    print("="*50)
    
    return True


def main():
    """Main function"""
    print("🚀 Bybit API Key Validator")
    
    success = validate_api_keys()
    
    if success:
        print("\n✅ Ready to start trading bot!")
        print("💡 Run: python run.py")
    else:
        print("\n❌ Please fix the API key issues above before starting the bot")
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
