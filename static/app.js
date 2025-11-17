
// Global state
let autoTradingActive = false;
let autoTradingInterval = null;
let tradeLog = [];
let stats = {
    totalTrades: 0,
    winningTrades: 0,
    totalPnL: 0
};

// Navigation
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupNavigation();
    setupEventListeners();
});

function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('.content-section');

    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetSection = button.getAttribute('data-section');
            
            // Update active button
            navButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Update active section
            sections.forEach(section => section.classList.remove('active'));
            document.getElementById(targetSection).classList.add('active');
        });
    });
}

function initializeApp() {
    checkHealth();
    loadDashboardData();
    
    // Refresh data every 10 seconds
    setInterval(() => {
        if (document.getElementById('dashboard').classList.contains('active')) {
            loadDashboardData();
        }
    }, 10000);
}

function setupEventListeners() {
    // Dashboard listeners
    document.getElementById('refresh-orders-btn')?.addEventListener('click', loadOrders);
    
    // Manual trading listeners
    document.getElementById('generate-signal-btn')?.addEventListener('click', generateSignal);
    document.getElementById('create-order-btn')?.addEventListener('click', createOrder);
    document.getElementById('order-type')?.addEventListener('change', togglePriceField);
    
    // Automated trading listeners
    document.getElementById('start-auto-trading-btn')?.addEventListener('click', startAutoTrading);
    document.getElementById('stop-auto-trading-btn')?.addEventListener('click', stopAutoTrading);
    document.getElementById('test-strategy-btn')?.addEventListener('click', testStrategy);
    document.getElementById('auto-trade-symbol')?.addEventListener('change', updateAutoSymbol);
}

// Health Check
async function checkHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        const indicator = document.getElementById('status-indicator');
        const statusText = document.getElementById('status-text');
        
        if (data.status === 'healthy') {
            indicator.classList.add('online');
            indicator.classList.remove('offline');
            statusText.textContent = 'Conectado';
        } else {
            indicator.classList.add('offline');
            indicator.classList.remove('online');
            statusText.textContent = 'Desconectado';
        }
    } catch (error) {
        console.error('Health check failed:', error);
        const indicator = document.getElementById('status-indicator');
        const statusText = document.getElementById('status-text');
        indicator.classList.add('offline');
        indicator.classList.remove('online');
        statusText.textContent = 'Erro de Conexão';
    }
}

// Dashboard Functions
async function loadDashboardData() {
    await Promise.all([
        loadBalance(),
        loadPositions(),
        loadPrices(),
        loadOrders()
    ]);
}

async function loadBalance() {
    try {
        const response = await fetch('/api/balance');
        const data = await response.json();
        
        const container = document.getElementById('balance-container');
        
        if (!data.balances || data.balances.length === 0) {
            container.innerHTML = '<div class="empty-state">Nenhum saldo disponível</div>';
            return;
        }
        
        container.innerHTML = data.balances.map(balance => `
            <div class="balance-item">
                <h3>${balance.coin}</h3>
                <div class="info-row">
                    <span class="info-label">Saldo Total:</span>
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
    } catch (error) {
        console.error('Error loading balance:', error);
        document.getElementById('balance-container').innerHTML = 
            '<div class="empty-state">Erro ao carregar saldo</div>';
    }
}

async function loadPositions() {
    try {
        const response = await fetch('/api/positions');
        const data = await response.json();
        
        const container = document.getElementById('positions-container');
        
        if (!data.positions || data.positions.length === 0) {
            container.innerHTML = '<div class="empty-state">Nenhuma posição aberta</div>';
            return;
        }
        
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
                    <span class="info-value">$${pos.entry_price.toFixed(2)}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Preço Atual:</span>
                    <span class="info-value">$${pos.mark_price.toFixed(2)}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">PnL:</span>
                    <span class="info-value ${pos.unrealised_pnl >= 0 ? 'positive' : 'negative'}">
                        $${pos.unrealised_pnl.toFixed(2)}
                    </span>
                </div>
                <div class="info-row">
                    <span class="info-label">Alavancagem:</span>
                    <span class="info-value">${pos.leverage}x</span>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading positions:', error);
        document.getElementById('positions-container').innerHTML = 
            '<div class="empty-state">Erro ao carregar posições</div>';
    }
}

async function loadPrices() {
    try {
        const symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT'];
        const prices = await Promise.all(
            symbols.map(symbol => fetch(`/api/price/${symbol}`).then(r => r.json()))
        );
        
        const container = document.getElementById('prices-container');
        container.innerHTML = prices.map(price => `
            <div class="price-item">
                <h3>${price.symbol}</h3>
                <div class="info-row">
                    <span class="info-label">Preço:</span>
                    <span class="info-value">$${price.price.toFixed(2)}</span>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading prices:', error);
        document.getElementById('prices-container').innerHTML = 
            '<div class="empty-state">Erro ao carregar preços</div>';
    }
}

async function loadOrders() {
    try {
        const response = await fetch('/api/orders');
        const data = await response.json();
        
        const container = document.getElementById('orders-container');
        
        if (!data.orders || data.orders.length === 0) {
            container.innerHTML = '<div class="empty-state">Nenhuma ordem aberta</div>';
            return;
        }
        
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
                    <span class="info-value">$${order.price.toFixed(2)}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Status:</span>
                    <span class="info-value">${order.status}</span>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading orders:', error);
        document.getElementById('orders-container').innerHTML = 
            '<div class="empty-state">Erro ao carregar ordens</div>';
    }
}

// Manual Trading Functions
async function generateSignal() {
    const symbol = document.getElementById('signal-symbol').value;
    const resultDiv = document.getElementById('signal-result');
    const btn = document.getElementById('generate-signal-btn');
    
    btn.disabled = true;
    btn.textContent = 'Gerando...';
    
    try {
        const response = await fetch(`/api/signal/${symbol}`, {
            method: 'POST'
        });
        const data = await response.json();
        
        resultDiv.className = `signal-result show ${data.signal.toLowerCase()}`;
        resultDiv.innerHTML = `
            <div class="signal-badge ${data.signal.toLowerCase()}">${data.signal}</div>
            <div class="info-row">
                <span class="info-label">Símbolo:</span>
                <span class="info-value">${data.symbol}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Preço Atual:</span>
                <span class="info-value">$${data.current_price}</span>
            </div>
            <div class="info-row">
                <span class="info-label">SMA Rápida (9):</span>
                <span class="info-value">$${data.sma_fast}</span>
            </div>
            <div class="info-row">
                <span class="info-label">SMA Lenta (21):</span>
                <span class="info-value">$${data.sma_slow}</span>
            </div>
        `;
    } catch (error) {
        console.error('Error generating signal:', error);
        resultDiv.className = 'signal-result show error';
        resultDiv.innerHTML = `<strong>Erro:</strong> ${error.message}`;
    } finally {
        btn.disabled = false;
        btn.textContent = 'Gerar Sinal SMA';
    }
}

function togglePriceField() {
    const orderType = document.getElementById('order-type').value;
    const priceGroup = document.getElementById('price-group');
    
    if (orderType === 'Limit') {
        priceGroup.style.display = 'block';
    } else {
        priceGroup.style.display = 'none';
    }
}

async function createOrder() {
    const symbol = document.getElementById('order-symbol').value;
    const side = document.getElementById('order-side').value;
    const orderType = document.getElementById('order-type').value;
    const qty = parseFloat(document.getElementById('order-qty').value);
    const price = orderType === 'Limit' ? parseFloat(document.getElementById('order-price').value) : null;
    
    const resultDiv = document.getElementById('order-result');
    const btn = document.getElementById('create-order-btn');
    
    if (!qty || qty <= 0) {
        resultDiv.className = 'order-result show error';
        resultDiv.innerHTML = '<strong>Erro:</strong> Quantidade inválida';
        return;
    }
    
    if (orderType === 'Limit' && (!price || price <= 0)) {
        resultDiv.className = 'order-result show error';
        resultDiv.innerHTML = '<strong>Erro:</strong> Preço inválido para ordem limitada';
        return;
    }
    
    btn.disabled = true;
    btn.textContent = 'Criando...';
    
    try {
        const response = await fetch('/api/order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                symbol,
                side,
                order_type: orderType,
                qty,
                price
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao criar ordem');
        }
        
        const data = await response.json();
        
        resultDiv.className = 'order-result show success';
        resultDiv.innerHTML = `
            <strong>✓ Ordem criada com sucesso!</strong><br>
            ID: ${data.order_id}<br>
            ${data.symbol} - ${data.side} ${data.qty} @ ${data.price || 'Market'}
        `;
        
        // Reload orders
        await loadOrders();
    } catch (error) {
        console.error('Error creating order:', error);
        resultDiv.className = 'order-result show error';
        resultDiv.innerHTML = `<strong>Erro:</strong> ${error.message}`;
    } finally {
        btn.disabled = false;
        btn.textContent = 'Criar Ordem';
    }
}

// Automated Trading Functions
function updateAutoSymbol() {
    const symbol = document.getElementById('auto-trade-symbol').value;
    document.getElementById('auto-symbol').textContent = symbol;
}

async function testStrategy() {
    const symbol = document.getElementById('auto-trade-symbol').value;
    const resultDiv = document.getElementById('strategy-result');
    const btn = document.getElementById('test-strategy-btn');
    
    btn.disabled = true;
    btn.textContent = 'Testing...';
    
    try {
        const response = await fetch(`/api/signal/${symbol}`, {
            method: 'POST'
        });
        const data = await response.json();
        
        resultDiv.className = `signal-result show ${data.signal.toLowerCase()}`;
        resultDiv.innerHTML = `
            <div class="signal-badge ${data.signal.toLowerCase()}">${data.signal}</div>
            <div class="info-row">
                <span class="info-label">Symbol:</span>
                <span class="info-value">${data.symbol}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Current Price:</span>
                <span class="info-value">$${data.current_price}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Fast SMA (9):</span>
                <span class="info-value">$${data.sma_fast}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Slow SMA (21):</span>
                <span class="info-value">$${data.sma_slow}</span>
            </div>
            <p style="margin-top: 10px; color: #94a3b8;">
                This is a test signal. No actual trade will be executed.
            </p>
        `;
        
        addTradeLogEntry('TEST', data.signal, symbol, data.current_price);
    } catch (error) {
        console.error('Error testing strategy:', error);
        resultDiv.className = 'signal-result show error';
        resultDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
    } finally {
        btn.disabled = false;
        btn.textContent = 'Test Strategy';
    }
}

async function startAutoTrading() {
    if (autoTradingActive) return;
    
    const symbol = document.getElementById('auto-trade-symbol').value;
    autoTradingActive = true;
    
    // Update UI
    document.getElementById('strategy-status').textContent = 'ACTIVE';
    document.getElementById('strategy-status').classList.remove('inactive');
    document.getElementById('strategy-status').classList.add('active');
    document.getElementById('start-auto-trading-btn').disabled = true;
    document.getElementById('stop-auto-trading-btn').disabled = false;
    
    addTradeLogEntry('SYSTEM', 'START', symbol, 0, 'Automated trading started');
    
    // Run strategy every 60 seconds
    autoTradingInterval = setInterval(async () => {
        await executeAutoTrade(symbol);
    }, 60000);
    
    // Execute immediately
    await executeAutoTrade(symbol);
}

function stopAutoTrading() {
    if (!autoTradingActive) return;
    
    autoTradingActive = false;
    
    if (autoTradingInterval) {
        clearInterval(autoTradingInterval);
        autoTradingInterval = null;
    }
    
    // Update UI
    document.getElementById('strategy-status').textContent = 'INACTIVE';
    document.getElementById('strategy-status').classList.remove('active');
    document.getElementById('strategy-status').classList.add('inactive');
    document.getElementById('start-auto-trading-btn').disabled = false;
    document.getElementById('stop-auto-trading-btn').disabled = true;
    
    const symbol = document.getElementById('auto-trade-symbol').value;
    addTradeLogEntry('SYSTEM', 'STOP', symbol, 0, 'Automated trading stopped');
}

async function executeAutoTrade(symbol) {
    try {
        const response = await fetch(`/api/signal/${symbol}`, {
            method: 'POST'
        });
        const data = await response.json();
        
        addTradeLogEntry('SIGNAL', data.signal, symbol, data.current_price, 
            `Fast SMA: $${data.sma_fast}, Slow SMA: $${data.sma_slow}`);
        
        // In a real implementation, you would execute trades here based on the signal
        // For now, this is just a placeholder that logs signals
        
        if (data.signal === 'BUY' || data.signal === 'SELL') {
            // Simulate trade execution (in production, you'd call the order API)
            stats.totalTrades++;
            // Simulate random win/loss for demo
            if (Math.random() > 0.5) {
                stats.winningTrades++;
                const profit = Math.random() * 50;
                stats.totalPnL += profit;
            } else {
                const loss = Math.random() * 30;
                stats.totalPnL -= loss;
            }
            updateStats();
        }
    } catch (error) {
        console.error('Error executing auto trade:', error);
        addTradeLogEntry('ERROR', 'FAILED', symbol, 0, error.message);
    }
}

function addTradeLogEntry(type, action, symbol, price, details = '') {
    const logContainer = document.getElementById('trade-log');
    const timestamp = new Date().toLocaleString('pt-BR');
    
    // Remove empty state if present
    if (logContainer.querySelector('.empty-state')) {
        logContainer.innerHTML = '';
    }
    
    const entry = document.createElement('div');
    entry.className = `trade-log-item ${action.toLowerCase()}`;
    entry.innerHTML = `
        <div class="trade-log-header">
            <span class="trade-log-time">${timestamp}</span>
            <span class="trade-log-type ${action.toLowerCase()}">${type}: ${action}</span>
        </div>
        <div class="trade-log-details">
            ${symbol} ${price > 0 ? `@ $${price.toFixed(2)}` : ''}
            ${details ? `<br>${details}` : ''}
        </div>
    `;
    
    // Add to beginning of log
    logContainer.insertBefore(entry, logContainer.firstChild);
    
    // Keep only last 50 entries
    while (logContainer.children.length > 50) {
        logContainer.removeChild(logContainer.lastChild);
    }
}

function updateStats() {
    document.getElementById('total-trades').textContent = stats.totalTrades;
    
    const winRate = stats.totalTrades > 0 
        ? ((stats.winningTrades / stats.totalTrades) * 100).toFixed(1) 
        : 0;
    document.getElementById('win-rate').textContent = `${winRate}%`;
    
    const pnlElement = document.getElementById('total-pnl');
    pnlElement.textContent = `$${stats.totalPnL.toFixed(2)}`;
    pnlElement.className = `stat-value ${stats.totalPnL >= 0 ? 'positive' : 'negative'}`;
}
