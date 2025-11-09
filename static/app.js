const API_BASE = '';

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();

        console.log('Health check:', data);

        document.getElementById('status-indicator').classList.add('online');
        document.getElementById('status-text').textContent = 'Conectado';

        if (!data.testnet) {
            document.getElementById('testnet-badge').textContent = 'MAINNET';
            document.getElementById('testnet-badge').style.background = '#ef4444';
            document.getElementById('testnet-badge').style.color = 'white';
        }

        return true;
    } catch (error) {
        console.error('Health check error:', error);
        document.getElementById('status-indicator').classList.add('offline');
        document.getElementById('status-text').textContent = 'Desconectado';
        return false;
    }
}

async function loadBalance() {
    try {
        console.log('Loading balance...');
        const response = await fetch(`${API_BASE}/api/balance`);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}`);
        }

        const data = await response.json();
        console.log('Balance data:', data);

        const container = document.getElementById('balance-container');

        if (data.balances && data.balances.length > 0) {
            container.innerHTML = data.balances.map(balance => `
                <div class="balance-item">
                    <h3>${balance.coin}</h3>
                    <div class="info-row">
                        <span class="info-label">Saldo:</span>
                        <span class="info-value">${balance.wallet_balance.toFixed(4)}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Disponível:</span>
                        <span class="info-value">${balance.available_balance.toFixed(4)}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Equity:</span>
                        <span class="info-value">${balance.equity.toFixed(4)}</span>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<div class="empty-state">Nenhum saldo encontrado</div>';
        }
    } catch (error) {
        console.error('Balance error:', error);
        document.getElementById('balance-container').innerHTML =
            `<div class="empty-state">Erro ao carregar saldo: ${error.message}</div>`;
    }
}

async function loadPositions() {
    try {
        console.log('Loading positions...');
        const response = await fetch(`${API_BASE}/api/positions`);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}`);
        }

        const data = await response.json();
        console.log('Positions data:', data);

        const container = document.getElementById('positions-container');

        if (data.positions && data.positions.length > 0) {
            container.innerHTML = data.positions.map(pos => `
                <div class="position-item">
                    <h3>${pos.symbol}</h3>
                    <div class="info-row">
                        <span class="info-label">Lado:</span>
                        <span class="info-value">${pos.side}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Tamanho:</span>
                        <span class="info-value">${pos.size}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Preço de Entrada:</span>
                        <span class="info-value">${pos.entry_price.toFixed(2)}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Preço Atual:</span>
                        <span class="info-value">${pos.mark_price.toFixed(2)}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">PnL:</span>
                        <span class="info-value ${pos.unrealised_pnl >= 0 ? 'positive' : 'negative'}">
                            ${pos.unrealised_pnl.toFixed(2)}
                        </span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Alavancagem:</span>
                        <span class="info-value">${pos.leverage}x</span>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<div class="empty-state">Nenhuma posição aberta</div>';
        }
    } catch (error) {
        console.error('Positions error:', error);
        document.getElementById('positions-container').innerHTML =
            `<div class="empty-state">Erro ao carregar posições: ${error.message}</div>`;
    }
}

async function loadPrices() {
    try {
        const symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT'];
        const pricesPromises = symbols.map(symbol => 
            fetch(`${API_BASE}/api/price/${symbol}`).then(r => r.json())
        );
        
        const prices = await Promise.all(pricesPromises);
        
        const container = document.getElementById('prices-container');
        container.innerHTML = prices.map(price => `
            <div class="price-item">
                <h3>${price.symbol}</h3>
                <div class="info-row">
                    <span class="info-label">Preço:</span>
                    <span class="info-value">${parseFloat(price.price).toFixed(2)} USDT</span>
                </div>
            </div>
        `).join('');
    } catch (error) {
        document.getElementById('prices-container').innerHTML = 
            `<div class="empty-state">Erro ao carregar preços: ${error.message}</div>`;
    }
}

async function generateSignal() {
    const symbol = document.getElementById('signal-symbol').value;
    const btn = document.getElementById('generate-signal-btn');
    const resultDiv = document.getElementById('signal-result');
    
    btn.disabled = true;
    btn.textContent = 'Gerando...';
    
    try {
        const response = await fetch(`${API_BASE}/api/signal/${symbol}`, {
            method: 'POST'
        });
        const data = await response.json();
        
        resultDiv.className = `signal-result ${data.signal.toLowerCase()} show`;
        resultDiv.innerHTML = `
            <div class="signal-badge ${data.signal.toLowerCase()}">${data.signal}</div>
            <div class="info-row">
                <span class="info-label">SMA Rápida (9):</span>
                <span class="info-value">${data.sma_fast}</span>
            </div>
            <div class="info-row">
                <span class="info-label">SMA Lenta (21):</span>
                <span class="info-value">${data.sma_slow}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Preço Atual:</span>
                <span class="info-value">${data.current_price}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Timestamp:</span>
                <span class="info-value">${new Date(data.timestamp).toLocaleString('pt-BR')}</span>
            </div>
        `;
    } catch (error) {
        resultDiv.className = 'signal-result error show';
        resultDiv.textContent = `Erro: ${error.message}`;
    } finally {
        btn.disabled = false;
        btn.textContent = 'Gerar Sinal SMA';
    }
}

async function createOrder() {
    const symbol = document.getElementById('order-symbol').value;
    const side = document.getElementById('order-side').value;
    const orderType = document.getElementById('order-type').value;
    const qty = parseFloat(document.getElementById('order-qty').value);
    const price = orderType === 'Limit' ? parseFloat(document.getElementById('order-price').value) : null;
    
    if (!qty || qty <= 0) {
        alert('Por favor, insira uma quantidade válida');
        return;
    }
    
    if (orderType === 'Limit' && (!price || price <= 0)) {
        alert('Por favor, insira um preço válido para ordem limitada');
        return;
    }
    
    const btn = document.getElementById('create-order-btn');
    const resultDiv = document.getElementById('order-result');
    
    btn.disabled = true;
    btn.textContent = 'Criando...';
    
    try {
        const orderData = {
            symbol,
            side,
            order_type: orderType,
            qty
        };
        
        if (price) {
            orderData.price = price;
        }
        
        const response = await fetch(`${API_BASE}/api/order`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao criar ordem');
        }
        
        const data = await response.json();
        
        resultDiv.className = 'order-result success show';
        resultDiv.innerHTML = `
            <strong>✅ Ordem criada com sucesso!</strong><br>
            <div class="info-row">
                <span class="info-label">Order ID:</span>
                <span class="info-value">${data.order_id}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Símbolo:</span>
                <span class="info-value">${data.symbol}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Lado:</span>
                <span class="info-value">${data.side}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Quantidade:</span>
                <span class="info-value">${data.qty}</span>
            </div>
        `;
        
        loadOrders();
    } catch (error) {
        resultDiv.className = 'order-result error show';
        resultDiv.innerHTML = `<strong>❌ Erro:</strong> ${error.message}`;
    } finally {
        btn.disabled = false;
        btn.textContent = 'Criar Ordem';
    }
}

async function loadOrders() {
    try {
        console.log('Loading orders...');
        const response = await fetch(`${API_BASE}/api/orders`);

        if (!response.ok) {
            let errorMsg = `HTTP ${response.status}`;
            try {
                const errData = await response.json();
                errorMsg = errData.detail || errData.message || errorMsg;
            } catch (e) {
                // ignore JSON parse errors, keep default message
            }
            throw new Error(errorMsg);
        }

        const data = await response.json();
        console.log('Orders data:', data);

        const container = document.getElementById('orders-container');

        if (data.orders && data.orders.length > 0) {
            container.innerHTML = data.orders.map(order => `
                <div class="order-item">
                    <div class="info-row">
                        <span class="info-label">Símbolo:</span>
                        <span class="info-value">${order.symbol}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Lado:</span>
                        <span class="info-value">${order.side}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Tipo:</span>
                        <span class="info-value">${order.order_type}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Quantidade:</span>
                        <span class="info-value">${order.qty}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Preço:</span>
                        <span class="info-value">${order.price}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Status:</span>
                        <span class="info-value">${order.status}</span>
                    </div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<div class="empty-state">Nenhuma ordem aberta</div>';
        }
    } catch (error) {
        console.error('Orders error:', error);
        document.getElementById('orders-container').innerHTML =
            `<div class="empty-state">Erro ao carregar ordens: ${error.message}</div>`;
    }
}

document.getElementById('generate-signal-btn').addEventListener('click', generateSignal);
document.getElementById('create-order-btn').addEventListener('click', createOrder);
document.getElementById('refresh-orders-btn').addEventListener('click', loadOrders);

document.getElementById('order-type').addEventListener('change', (e) => {
    const priceGroup = document.getElementById('price-group');
    if (e.target.value === 'Limit') {
        priceGroup.style.display = 'block';
    } else {
        priceGroup.style.display = 'none';
    }
});

async function init() {
    const isOnline = await checkHealth();
    
    if (isOnline) {
        await Promise.all([
            loadBalance(),
            loadPositions(),
            loadPrices(),
            loadOrders()
        ]);
        
        setInterval(() => {
            loadPrices();
            loadPositions();
        }, 10000);
    }
}

init();
