# 🐛 DEBUGGING GUIDE - Balance & Orders Issues

## 🎯 Problem
You can place orders ✅ but:
- ❌ Balance doesn't appear
- ❌ Open orders don't appear  
- ❌ Error 500 on positions

## ✅ Quick Fixes Applied

### 1. **Added Detailed Logging**
- All endpoints now log requests and responses
- Check terminal/console for detailed error messages

### 2. **Improved Error Handling**
- Frontend now properly handles HTTP errors
- Console logs all API responses

### 3. **Created Debug Tools**
- Debug endpoint: `/api/debug/raw`
- Debug page: http://localhost:8000/static/debug.html

---

## 🔍 How to Debug

### Step 1: Check Server Logs

The server is running in your terminal. Look for these messages:

```
INFO:app.main:Getting wallet balance...
INFO:app.main:Balance response retCode: 0
INFO:app.main:Number of accounts: 1
INFO:app.main:Number of coins in account: 5
INFO:app.main:Returning 2 balances
```

**If you see errors:**
- Check the `retMsg` field
- Look for authentication errors
- Verify API key permissions

### Step 2: Use Debug Page

1. Keep the server running (`python run.py`)
2. Open: http://localhost:8000/static/debug.html
3. Click **"Test All Endpoints"**
4. Check the JSON responses

**What to look for:**
- `retCode: 0` = Success ✅
- `retCode: 10001` = Invalid params ❌
- `retCode: 10003` = Invalid API key ❌
- `retCode: 10004` = Invalid signature ❌
- `retCode: 33004` = No wallet balance ❌

### Step 3: Check Browser Console

1. Open main page: http://localhost:8000
2. Press `F12` (Developer Tools)
3. Go to **Console** tab
4. Refresh the page

**You should see:**
```
Health check: {status: 'healthy', ...}
Loading balance...
Balance data: {balances: [...]}
Loading positions...
Positions data: {positions: [...]}
Loading orders...
Orders data: {orders: [...]}
```

**If you see errors:**
- Red text = API error
- Check the error message
- Look at Network tab for HTTP status codes

---

## 🛠️ Common Issues & Solutions

### Issue 1: "No balance found" but you have balance

**Cause:** Balance is 0 or less than 0.0001

**Solution:**
1. For DEMO account, deposit USDT
2. For TESTNET, get free USDT from faucet:
   - https://testnet.bybit.com/app/user/api-management
   - Click "Get Test USDT"

### Issue 2: Error 500 on positions

**Causes:**
- API returned unexpected response format
- Network timeout
- Permission issue

**Solutions:**
1. Check debug page for exact error
2. Verify API key has "Read Position" permission
3. Check server logs for Python traceback

### Issue 3: Orders don't appear

**Causes:**
- No open orders (all filled/cancelled)
- API key doesn't have "Read Orders" permission

**Solutions:**
1. Place a limit order (won't fill immediately)
2. Check debug page to see actual response
3. Verify API key permissions

### Issue 4: 401 Unauthorized

**Cause:** Invalid API credentials

**Solution:**
```bash
python validate_api_keys.py
```
If this fails, regenerate API keys.

---

## 📋 Debug Checklist

Run through this checklist:

- [ ] Server is running without errors
- [ ] Can access http://localhost:8000
- [ ] Debug page shows retCode: 0 for all endpoints
- [ ] Browser console shows no red errors
- [ ] Have balance > 0 in your account
- [ ] API key has correct permissions

---

## 🔧 Quick Tests

### Test 1: Raw API Response
```bash
# Open browser and go to:
http://localhost:8000/api/debug/raw
```

### Test 2: Balance Endpoint
```bash
# Open browser and go to:
http://localhost:8000/api/balance
```

### Test 3: Server Logs
Check your terminal where `python run.py` is running. You should see:
```
INFO:app.main:Getting wallet balance...
INFO:app.main:Balance response retCode: 0
```

---

## 🎯 Next Steps

1. **Restart the server:**
   ```bash
   # Stop current server (Ctrl+C)
   python run.py
   ```

2. **Open debug page:**
   http://localhost:8000/static/debug.html

3. **Click "Test All Endpoints"**

4. **Check server terminal** for log messages

5. **Take a screenshot** of:
   - Debug page results
   - Server terminal logs
   - Browser console (F12)

---

## 💡 Understanding the Fixes

### What Changed:

1. **Logging Added** - Every endpoint now logs:
   - Request received
   - API response retCode
   - Number of items returned
   - Any errors

2. **Error Handling Improved**:
   - Frontend checks HTTP status codes
   - Shows proper error messages
   - Logs everything to console

3. **Debug Endpoint** - `/api/debug/raw`:
   - Shows raw Bybit API responses
   - Helps identify format issues
   - No processing, just raw data

4. **Empty State Handling**:
   - Balance: Only shows coins with balance > 0
   - Positions: Only shows positions with size > 0
   - Orders: Shows all open orders

---

## 🚨 If Still Not Working

1. **Run debug script:**
   ```bash
   python debug_api.py
   ```

2. **Check API key permissions:**
   - Login to Bybit
   - Go to API Management
   - Verify permissions:
     - ✅ Read Position
     - ✅ Read-Write
     - ✅ Trade

3. **Check account type:**
   - Unified Trading Account (recommended)
   - Not Classic Account

4. **Verify environment:**
   - Demo mode requires mainnet keys
   - Testnet mode requires testnet keys
   - Can't mix them!

---

## 📞 Report Results

After testing, report:
1. What does debug page show?
2. What do server logs say?
3. What does browser console show?
4. Which endpoints work/fail?

This will help pinpoint the exact issue!
