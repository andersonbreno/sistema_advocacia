document.addEventListener('DOMContentLoaded', function () {
    var ctxClientes = document.getElementById('clientesChart').getContext('2d');
    var ctxProcessos = document.getElementById('processosChart').getContext('2d');
    var meses = JSON.parse('{{ meses|escapejs }}');
    var clientes_data = JSON.parse('{{ clientes_data|escapejs }}');
    var processos_data = JSON.parse('{{ processos_data|escapejs }}');

    var clientesChart = new Chart(ctxClientes, {
        type: 'bar',
        data: {
            labels: meses,
            datasets: [{
                label: 'Total de Clientes',
                data: clientes_data,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    var processosChart = new Chart(ctxProcessos, {
        type: 'bar',
        data: {
            labels: meses,
            datasets: [{
                label: 'Total de Processos',
                data: processos_data,
                backgroundColor: 'rgba(255, 99, 132, 0.6)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
});
