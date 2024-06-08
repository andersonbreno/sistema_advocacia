function createSearchResultItem(item) {
    const wrapperDiv = document.createElement('div');
    wrapperDiv.className = 'search-result-item';

    const iconDiv = document.createElement('div');
    iconDiv.className = 'search-result-icon';
    // Define um ícone diferente dependendo do tipo
    iconDiv.innerHTML = item.tipo === 'cliente' ? `<i class="fa fa-user"></i>` : `<i class="fa fa-briefcase"></i>`;
    // iconDiv.innerHTML = `<i class="fa fa-user"></i>`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'search-result-content';

    const nameDiv = document.createElement('div');
    nameDiv.className = 'search-result-name';
    // Para processos, exibe 'Processo: ' antes do número
    nameDiv.textContent = item.tipo === 'processo' ? `Processo: ${item.nome}` : item.nome;
    // nameDiv.textContent = item.nome;

    // Se for um cliente e você quiser mostrar mais informações, pode adicionar aqui
    if (item.tipo === 'cliente') {
        // Suponha que você quer mostrar a data em que a pessoa se tornou cliente (se tiver essa informação)
        const infoDiv = document.createElement('div');
        infoDiv.className = 'search-result-info';
        infoDiv.textContent = `Pessoa cadastrada em ${item.data_cadastro}`; // Ajuste isso conforme os seus dados
    }

    const infoDiv = document.createElement('div');
    infoDiv.className = 'search-result-info';
    

    contentDiv.appendChild(nameDiv);
    contentDiv.appendChild(infoDiv);

    wrapperDiv.appendChild(iconDiv);
    wrapperDiv.appendChild(contentDiv);

    // Adiciona ação quando clicar no item do resultado da busca
    wrapperDiv.onclick = () => {
        if (item.tipo === 'cliente') {
            window.location.href = `/clientes/${item.id}/detalhe`;  // Ajuste a URL conforme necessário
        } else if (item.tipo === 'processo') {
            window.location.href = `/processos/${item.id}/detalhe`;  // Ajuste a URL conforme necessário
        }
    };

    return wrapperDiv;
}

// function clearSearch() {
//     const searchInput = document.getElementById('search-input');
//     searchInput.value = ''; // Limpa o campo de busca
//     searchInput.focus(); // Foca no campo de busca
//     const clearButton = document.getElementById('clear-search');
//     clearButton.style.display = 'none'; // Esconde o botão de limpeza
//     hideSearchResultsPanel(); // Chame a função para esconder o painel de resultados
// }

function showSearchResultsPanel() {
    const resultsPanel = document.getElementById('search-results-panel');
    if (resultsPanel) {
        resultsPanel.style.display = 'block'; // Mostra o painel de resultados
    }
}

function hideSearchResultsPanel() {
    const resultsPanel = document.getElementById('search-results-panel');
    if (resultsPanel) {
        resultsPanel.style.display = 'none'; // Esconde o painel de resultados
    }
}

// Função para verificar se o clique foi fora do painel de resultados
function handleClickOutside(event) {
    const resultsPanel = document.getElementById('search-results-panel');
    if (resultsPanel.style.display === 'block' && !resultsPanel.contains(event.target) && event.target !== document.getElementById('search-input')) {
        hideSearchResultsPanel();
    }
}

let timeout = null;

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const clearButton = document.getElementById('clear-search');
    const resultsDiv = document.getElementById('search-results-panel');

    // Adiciona evento para limpar o campo de busca
    clearButton.addEventListener('click', function () {
        searchInput.value = ''; // Limpa o campo
        resultsPanel.style.display = 'none'; // Esconde o painel de resultados
        resultsPanel.innerHTML = ''; // Limpa os resultados existentes
    });

    // Adiciona evento para mostrar/esconder o botão 'X'
    searchInput.addEventListener('input', function () {
        clearButton.style.display = searchInput.value ? 'block' : 'none';
    });

    if (!searchInput || !resultsDiv) {
        console.error('Os elementos do DOM necessários não foram encontrados');
        return;
    }

    const searchUrl = searchInput.getAttribute('data-search-url');

    if (!searchUrl) {
        console.error('A URL de busca não foi encontrada');
        return;
    }

    searchInput.addEventListener('input', function () {
        clearTimeout(timeout);

        const query = this.value;
        if (query.length >= 3) {
            timeout = setTimeout(() => {
                fetch(`${searchUrl}?term=${encodeURIComponent(query)}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        resultsDiv.innerHTML = '';
                        if (data.length > 0) {
                            showSearchResultsPanel(); // Mostra o painel com os resultados
                            data.forEach(item => {
                                const searchResultItem = createSearchResultItem(item);
                                resultsDiv.appendChild(searchResultItem);
                            });
                        } else {
                            // Aqui você pode adicionar uma mensagem indicando que não foram encontrados resultados
                            const noResultsDiv = document.createElement('div');
                            noResultsDiv.className = 'search-result-item';
                            noResultsDiv.textContent = 'Nenhum resultado encontrado.';
                            resultsDiv.appendChild(noResultsDiv);
                            showSearchResultsPanel(); // Ainda queremos mostrar o painel, mas agora ele terá a mensagem de 'sem resultados'
                        }
                    })
                    .catch(error => {
                        console.error('Erro na busca:', error);
                        resultsDiv.innerHTML = '<div class="search-result-item">Não foi possível realizar a busca.</div>';
                        hideSearchResultsPanel(); // Esconde o painel se ocorrer um erro
                    });
            }, 500);
        } else {
            resultsDiv.innerHTML = '';
            hideSearchResultsPanel(); // Esconde o painel se o texto for apagado ou for muito curto
        }
    });

    // Adiciona o ouvinte de eventos para o clique do documento
    document.addEventListener('click', handleClickOutside);

});
