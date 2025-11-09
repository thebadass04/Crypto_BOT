# 🤖 Bybit Trading Bot

Bot de trading automatizado para Bybit usando Python (FastAPI) e HTML/JS.

## ✨ Funcionalidades

- ✅ Suporte para BTCUSDT, ETHUSDT, BNBUSDT
- ✅ Estratégia SMA (Simple Moving Average)
- ✅ Interface web responsiva
- ✅ Autenticação HMAC
- ✅ Suporte para Testnet, Demo e Mainnet
- ✅ Visualização de saldo
- ✅ Visualização de posições
- ✅ Visualização de ordens
- ✅ Criação de ordens

## 📁 Estrutura do Projeto

```
BOT_CRYPTO/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configurações
│   ├── models.py            # Modelos Pydantic
│   ├── bybit_client.py      # Cliente Bybit (pybit)
│   └── strategy/
│       ├── __init__.py
│       └── simple_sma.py    # Estratégia SMA
├── static/
│   ├── index.html           # Frontend
│   ├── style.css            # Estilos
│   └── app.js               # Lógica JS
├── .env                     # Credenciais (NÃO COMMITAR!)
├── .env.example             # Exemplo de .env
├── .gitignore
├── requirements.txt         # Dependências Python
├── run.py                   # Script de execução
├── test_bot.py              # Script de teste
├── validate_api_keys.py     # Validação de API keys
└── README.md
```

## 🚀 Instalação

### 1. Clonar o Repositório

```bash
git clone <seu-repositorio>
cd BOT_CRYPTO
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar Credenciais

Crie um arquivo `.env` na raiz do projeto:

```env
BYBIT_API_KEY=sua_api_key_aqui
BYBIT_API_SECRET=seu_api_secret_aqui
USE_TESTNET=true
USE_DEMO=false
SYMBOLS=BTCUSDT,ETHUSDT,BNBUSDT
```

#### 🔑 Como Obter API Keys

**Para Testnet (recomendado para testes):**
1. Acesse: https://testnet.bybit.com/
2. Faça login ou crie uma conta
3. Vá em **API Management**
4. Clique em **Create New Key**
5. Selecione permissões:
   - ✅ Read Position
   - ✅ Read-Write
   - ✅ Trade (opcional)
6. Copie a **API Key** e **API Secret**
7. Cole no arquivo `.env`

**Para Mainnet (⚠️ usa dinheiro real!):**
1. Acesse: https://www.bybit.com/
2. Faça login
3. Vá em **API Management**
4. Configure da mesma forma que o testnet
5. Atualize `.env`:
   ```env
   USE_TESTNET=false
   USE_DEMO=false
   ```

## 🧪 Testar Configuração

Antes de executar o bot, valide suas credenciais:

```bash
python validate_api_keys.py
```

Ou use o script de teste completo:

```bash
python test_bot.py
```

Se tudo estiver correto, você verá:

```
✅ Bot configuration test complete!
```

## ▶️ Executar o Bot

```bash
python run.py
```

O bot iniciará em: http://localhost:8000

## 🌐 Usando a Interface

1. Abra o navegador em http://localhost:8000
2. Selecione um símbolo (BTCUSDT, ETHUSDT, BNBUSDT)
3. Visualize:
   - 💰 Saldo da conta
   - 📊 Posições abertas
   - 📝 Ordens abertas
   - 💹 Preço atual
   - 📈 Sinal de trading (SMA)

## 📡 API Endpoints

### Informações da Conta
- `GET /api/account` - Informações da conta
- `GET /api/balance` - Saldo da carteira
- `GET /api/positions` - Posições abertas
- `GET /api/orders` - Ordens abertas

### Dados de Mercado
- `GET /api/price/{symbol}` - Preço atual
- `GET /api/klines/{symbol}?interval=60&limit=100` - Candlesticks

### Trading
- `POST /api/order` - Criar ordem
- `POST /api/signal/{symbol}` - Gerar sinal SMA

### Documentação Interativa
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## ⚙️ Configurações

Edite `.env` para alterar:

| Variável | Descrição | Valores |
|----------|-----------|---------|
| `BYBIT_API_KEY` | Sua API Key | String |
| `BYBIT_API_SECRET` | Seu API Secret | String |
| `USE_TESTNET` | Usar testnet | `true` / `false` |
| `USE_DEMO` | Usar demo trading | `true` / `false` |
| `SYMBOLS` | Símbolos para trade | `BTCUSDT,ETHUSDT,BNBUSDT` |

## 🔧 Estratégia SMA

A estratégia usa duas médias móveis simples:
- **SMA Rápida:** 10 períodos
- **SMA Lenta:** 20 períodos

**Sinais:**
- 🟢 **BUY:** Quando SMA rápida cruza acima da SMA lenta
- 🔴 **SELL:** Quando SMA rápida cruza abaixo da SMA lenta
- ⚪ **HOLD:** Sem cruzamento

## ⚠️ Problemas Comuns

### 1. Erro 401 Unauthorized

**Solução:**
- Verifique se as API keys estão corretas
- Verifique se está usando o ambiente correto (testnet vs mainnet)
- Regenere as API keys no Bybit

### 2. Balance não aparece

**Solução:**
- Execute `python test_bot.py` para verificar
- Verifique se tem saldo na conta (testnet precisa de faucet)
- Para testnet, obtenha USDT gratuito em: https://testnet.bybit.com/app/user/api-management

### 3. ModuleNotFoundError

**Solução:**
```bash
pip install -r requirements.txt
```

### 4. Port 8000 já está em uso

**Solução:**
Edite `run.py` e altere a porta:
```python
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8080,  # Altere para 8080 ou outra porta
    reload=True
)
```

## 📦 Dependências

```
fastapi==0.104.1
uvicorn==0.24.0
pybit==5.6.2
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
pandas==2.1.3
numpy==1.26.2
```

## 🔒 Segurança

- ⚠️ **NUNCA** commite o arquivo `.env`
- ⚠️ **NUNCA** compartilhe suas API keys
- ⚠️ Use permissões mínimas necessárias
- ⚠️ Teste sempre em testnet primeiro
- ⚠️ Use IP whitelisting quando possível

## 📝 TODO

- [ ] Adicionar mais estratégias
- [ ] Implementar backtesting
- [ ] Adicionar notificações
- [ ] Adicionar stop-loss automático
- [ ] Adicionar take-profit automático
- [ ] Implementar WebSocket para dados em tempo real

## 📄 Licença

MIT License

## 🤝 Contribuindo

Pull requests são bem-vindos! Para mudanças importantes, abra uma issue primeiro.

## ⚡ Performance

- Backend: FastAPI (async/await)
- Cliente API: pybit (oficial Bybit)
- Frontend: Vanilla JS (sem frameworks)

## 📊 Status

✅ **Projeto Totalmente Funcional**

- [x] Estrutura do projeto criada
- [x] Backend FastAPI implementado
- [x] Cliente Bybit (pybit) configurado
- [x] Estratégia SMA implementada
- [x] Frontend responsivo criado
- [x] Autenticação HMAC funcionando
- [x] Suporte para Testnet/Demo/Mainnet
- [x] Scripts de validação criados

## 💡 Dicas

1. **Sempre teste em testnet primeiro**
2. **Use stop-loss em trades reais**
3. **Não invista mais do que pode perder**
4. **Monitore o bot regularmente**
5. **Mantenha as dependências atualizadas**

## 📞 Suporte

Para problemas ou dúvidas:
1. Execute `python test_bot.py` para diagnóstico
2. Verifique os logs do servidor
3. Consulte a documentação da API Bybit: https://bybit-exchange.github.io/docs/

---

**⚠️ AVISO:** Este bot é para fins educacionais. Trading de criptomoedas envolve riscos. Use por sua conta e risco.
