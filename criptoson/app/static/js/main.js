document.addEventListener('DOMContentLoaded', function() {
    
    // --- LÓGICA DE TEMA (CLARO/ESCURO) ---
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

    // Verifica o tema salvo no localStorage ou a preferência do sistema
    if (localStorage.getItem('color-theme') === 'dark' || 
       (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
        themeToggleLightIcon.classList.remove('hidden');
    } else {
        document.documentElement.classList.remove('dark');
        themeToggleDarkIcon.classList.remove('hidden');
    }

    themeToggleBtn.addEventListener('click', function() {
        // Alterna os ícones
        themeToggleDarkIcon.classList.toggle('hidden');
        themeToggleLightIcon.classList.toggle('hidden');

        // Se o tema estiver salvo, alterna e atualiza
        if (localStorage.getItem('color-theme')) {
            if (localStorage.getItem('color-theme') === 'light') {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            } else {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            }
        } else { // Se não, baseia-se na classe atual do HTML
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('color-theme', 'light');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('color-theme', 'dark');
            }
        }
    });

    // --- LÓGICA DO SELETOR DE MOEDA ---
    const currencySelector = document.getElementById('currencySelector');
    if (currencySelector) {
        currencySelector.addEventListener('change', function() {
            const selectedCurrency = this.value;
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('currency', selectedCurrency);
            window.location.href = currentUrl.toString();
        });
    }

    // --- LÓGICA DA PÁGINA INICIAL ---
    const coinTable = document.getElementById('coinTable');
    if (coinTable) {
        // Redireciona para a página de detalhes ao clicar na linha
        coinTable.addEventListener('click', function(e) {
            const row = e.target.closest('.coin-row');
            if (row) {
                const coinId = row.dataset.id;
                const currency = new URLSearchParams(window.location.search).get('currency') || 'brl';
                window.location.href = `/coin/${coinId}?currency=${currency}`;
            }
        });

        // Lógica de busca
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('keyup', function() {
            const filter = searchInput.value.toLowerCase();
            const rows = coinTable.getElementsByTagName('tr');
            for (let i = 1; i < rows.length; i++) { // Começa em 1 para pular o cabeçalho
                const coinName = rows[i].cells[1].textContent.toLowerCase();
                if (coinName.includes(filter)) {
                    rows[i].style.display = '';
                } else {
                    rows[i].style.display = 'none';
                }
            }
        });

        // Atualização de preços via AJAX (Polling)
        setInterval(updatePrices, 60000); // 60 segundos
    }

    function updatePrices() {
        console.log('Atualizando preços...');
        const currency = new URLSearchParams(window.location.search).get('currency') || 'brl';
        fetch(`/api/tickers?currency=${currency}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(coin => {
                    const priceCell = document.querySelector(`.price-cell[data-coin-id="${coin.id}"]`);
                    const changeCell = document.querySelector(`.change-cell[data-coin-id="${coin.id}"]`);
                    
                    if (priceCell && changeCell) {
                        const oldPrice = parseFloat(priceCell.textContent.replace(/[^0-9,-]+/g,"").replace(",", "."));
                        const newPrice = coin.current_price;

                        priceCell.textContent = newPrice.toLocaleString('pt-BR', { style: 'currency', currency: currency.toUpperCase() }).replace(currency.toUpperCase(), '').trim();
                        changeCell.textContent = `${coin.price_change_percentage_24h.toFixed(2)}%`;

                        // Remove classes de cor e adiciona a nova
                        changeCell.classList.remove('price-up', 'price-down');
                        if (coin.price_change_percentage_24h > 0) {
                            changeCell.classList.add('price-up');
                        } else {
                            changeCell.classList.add('price-down');
                        }

                        // Efeito visual de atualização
                        if (newPrice > oldPrice) {
                            flashCell(priceCell, 'green');
                        } else if (newPrice < oldPrice) {
                            flashCell(priceCell, 'red');
                        }
                    }
                });
            })
            .catch(error => console.error('Erro ao atualizar preços:', error));
    }

    function flashCell(cell, color) {
        const originalColor = cell.style.backgroundColor;
        cell.style.transition = 'background-color 0.2s ease-in-out';
        cell.style.backgroundColor = color === 'green' ? 'rgba(34, 197, 94, 0.2)' : 'rgba(239, 68, 68, 0.2)';
        setTimeout(() => {
            cell.style.backgroundColor = originalColor;
        }, 1000);
    }

    // --- LÓGICA DA PÁGINA DE DETALHES (GRÁFICO) ---
    const priceChartCanvas = document.getElementById('priceChart');
    if (priceChartCanvas && typeof COIN_ID !== 'undefined') {
        const ctx = priceChartCanvas.getContext('2d');
        let priceChart;

        const chartLoading = document.getElementById('chart-loading');
        const chartContainer = document.getElementById('chart-container');
        
        async function fetchAndRenderChart(days) {
            chartContainer.classList.add('hidden');
            chartLoading.classList.remove('hidden');

            try {
                const response = await fetch(`/api/historical/${COIN_ID}?currency=${CURRENT_CURRENCY}&days=${days}`);
                const data = await response.json();
                
                const labels = data.prices.map(price => new Date(price[0]).toLocaleDateString('pt-BR'));
                const prices = data.prices.map(price => price[1]);

                if (priceChart) {
                    priceChart.destroy();
                }

                priceChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: `Preço (${CURRENT_CURRENCY.toUpperCase()})`,
                            data: prices,
                            borderColor: '#4f46e5',
                            backgroundColor: 'rgba(79, 70, 229, 0.1)',
                            fill: true,
                            tension: 0.1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: {
                                grid: { color: document.documentElement.classList.contains('dark') ? '#374151' : '#e5e7eb' },
                                ticks: { color: document.documentElement.classList.contains('dark') ? '#d1d5db' : '#6b7280' }
                            },
                            y: {
                                grid: { color: document.documentElement.classList.contains('dark') ? '#374151' : '#e5e7eb' },
                                ticks: { 
                                    color: document.documentElement.classList.contains('dark') ? '#d1d5db' : '#6b7280',
                                    callback: function(value, index, values) {
                                        return value.toLocaleString('pt-BR', { style: 'currency', currency: CURRENT_CURRENCY.toUpperCase(), minimumFractionDigits: 2 });
                                    }
                                }
                            }
                        },
                        plugins: {
                            legend: {
                                display: false
                            }
                        }
                    }
                });

            } catch (error) {
                console.error('Erro ao buscar dados do gráfico:', error);
                chartLoading.textContent = 'Falha ao carregar dados do gráfico.';
            } finally {
                chartContainer.classList.remove('hidden');
                chartLoading.classList.add('hidden');
            }
        }
        
        // Botões de período do gráfico
        const timeRangeButtons = document.querySelectorAll('.time-range-btn');
        timeRangeButtons.forEach(button => {
            button.addEventListener('click', () => {
                fetchAndRenderChart(button.dataset.days);
            });
        });

        // Carrega o gráfico inicial com 30 dias
        fetchAndRenderChart(30);
    }

});
