document.addEventListener('DOMContentLoaded', function() {
    console.log("Estou sendo carregado")
    // Função para mostrar/esconder a justificativa
    function toggleJustificativa() {
        const cadastradoPlanilha = document.getElementById('id_cadastrado_planilha').checked;
        const justificativaField = document.querySelector('.field-justificativa');
        justificativaField.style.display = cadastradoPlanilha ? 'none' : 'block';
    }

    // Adicione um ouvinte de evento ao campo 'cadastrado_planilha'
    document.getElementById('id_cadastrado_planilha').addEventListener('change', toggleJustificativa);

    // Chame a função no carregamento para definir o estado inicial
    toggleJustificativa();
});