// static/js/admin_custom_mask.js

$(document).ready(function () {
    $('.mask-telefone').mask('(00) 00000-0000');  // Permite 15 dígitos (9º dígito) 
    $(".cpf-mask").mask("000.000.000-00", { reverse: true });
    $(".mask-cnpj").mask("00.000.000/0000-00", { reverse: true });
    $(".mask-cep").mask("00000-000");
});