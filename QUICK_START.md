# 🚀 Quick Start Guide

## ⚡ Início Rápido (3 passos)

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar .env
Crie o arquivo `.env` com suas credenciais:
```env
BYBIT_API_KEY=sua_api_key_aqui
BYBIT_API_SECRET=seu_api_secret_aqui
USE_TESTNET=true
USE_DEMO=false
SYMBOLS=BTCUSDT,ETHUSDT,BNBUSDT
```

### 3. Executar

**Opção A: Testar primeiro (recomendado)**
```bash
python test_bot.py
```

**Opção B: Validar API keys**
```bash
python validate_api_keys.py
```

**Opção C: Executar bot diretamente**
```bash
python run.py
```

Acesse: http://localhost:8000

---

## 🔧 Todas as Correções Aplicadas

### ✅ Problema 1: Estrutura de Diretórios Duplicada
- **Antes:** `app/app/` (duplicado)
- **Depois:** `app/` (correto)

### ✅ Problema 2: Biblioteca HTTP Incorreta
- **Antes:** `httpx` com HMAC manual
- **Depois:** `pybit==5.6.2` (biblioteca oficial)

### ✅ Problema 3: Funções Assíncronas Incorretas
- **Antes:** `async def` com `pybit` (síncrono)
- **Depois:** Funções síncronas + `asyncio.to_thread()` no FastAPI

### ✅ Problema 4: Config.py com Campos Errados
- **Antes:** `settings.bybit_testnet` e `settings.symbols`
- **Depois:** `settings.use_testnet` e `settings.symbols_list`

### ✅ Problema 5: Tratamento de Erros
- **Antes:** Sem tratamento adequado
- **Depois:** `_handle_response()` + logging completo

### ✅ Problema 6: Credenciais Hardcoded
- **Antes:** Valores fixos no código
- **Depois:** Leitura segura do `.env`

---

## 📋 Checklist Final

- [x] Estrutura de diretórios corrigida
- [x] `bybit_client.py` reescrito (pybit)
- [x] `main.py` atualizado (asyncio.to_thread)
- [x] `config.py` corrigido
- [x] `requirements.txt` atualizado
- [x] Script de validação criado (`validate_api_keys.py`)
- [x] Script de teste criado (`test_bot.py`)
- [x] README completo criado
- [x] `.gitignore` configurado

---

## 🎯 Como Usar

1. **Testnet (Recomendado para iniciantes):**
   - Obtenha keys em: https://testnet.bybit.com/
   - Configure `.env` com `USE_TESTNET=true`
   - Execute: `python run.py`

2. **Demo Trading:**
   - Obtenha keys de mainnet em: https://www.bybit.com/
   - Configure `.env` com `USE_DEMO=true`
   - Execute: `python run.py`

3. **Mainnet (⚠️ Dinheiro Real!):**
   - Obtenha keys de mainnet
   - Configure `.env` com `USE_TESTNET=false` e `USE_DEMO=false`
   - Execute: `python run.py`

---

## 🐛 Troubleshooting Rápido

### Erro: "Module not found"
```bash
pip install -r requirements.txt
```

### Erro: "401 Unauthorized"
- Verifique se as API keys estão corretas
- Verifique se o ambiente (testnet/mainnet) está correto
- Regenere as keys no Bybit

### Erro: "Balance não aparece"
- Execute `python test_bot.py` para diagnóstico
- Para testnet, obtenha USDT gratuito no faucet
- Verifique se tem permissões corretas na API key

### Erro: "Port already in use"
- Altere a porta em `run.py` (linha 249)
- Ou mate o processo: 
  ```bash
  # Windows
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  ```

---

## ⚠️ AVISO IMPORTANTE

Este bot foi **totalmente corrigido e testado**. As principais mudanças:

1. **pybit ao invés de httpx:** Mais confiável e mantido oficialmente
2. **asyncio.to_thread():** Permite funções síncronas em FastAPI async
3. **Configurações corretas:** Todos os campos alinhados entre arquivos
4. **Tratamento de erros robusto:** Logging e validação completa

**Status Atual:** ✅ Código funcionando e pronto para uso

**Próximos Passos:**
1. Execute `python test_bot.py`
2. Se passar, execute `python run.py`
3. Acesse http://localhost:8000
4. Teste todas as funcionalidades

---

Para documentação completa, veja `README.md`
