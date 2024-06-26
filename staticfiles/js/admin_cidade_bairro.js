document.addEventListener('DOMContentLoaded', function () {
    const cepField = document.getElementById('id_cep'); // Ajuste para o ID do seu campo de CEP
    const ruaField = document.getElementById('id_rua'); // Ajuste para o ID do seu campo de rua
    const bairroField = document.getElementById('id_bairro'); // Ajuste para o ID do seu campo de bairro
    const cidadeField = document.getElementById('id_cidade'); // Ajuste para o ID do seu campo de cidade
    const estadoField = document.getElementById('id_estado'); // Ajuste para o ID do seu campo de estado
});

document.addEventListener('DOMContentLoaded', function () {
    const cepField = document.getElementById('id_cep'); // Ajuste o ID conforme necessário

    cepField.addEventListener('blur', function() {
        // Remove caracteres não numéricos para obter um CEP "puro"
        let cep = cepField.value.replace(/\D/g, '');
        if (cep.length === 10) { // Verifica se o CEP "puro" tem 8 dígitos
            fetch(`https://viacep.com.br/ws/${cep}/json/`)
                .then(response => response.json())
                .then(data => {
                    if (!("erro" in data)) {
                        // Preenchimento automático dos campos, ajuste os IDs conforme necessário
                        document.getElementById('id_rua').value = data.logradouro;
                        document.getElementById('id_bairro').value = data.bairro;
                        document.getElementById('id_cidade').value = data.localidade;
                        document.getElementById('id_estado').value = data.uf;
                        // O campo CEP já deve estar formatado corretamente pelo usuário
                    } else {
                        console.error("CEP não encontrado.");
                    }
                });
        } else {
            alert("O formato do CEP deve ser 'XX.XXX-XXX'.");
        }
    });
});

