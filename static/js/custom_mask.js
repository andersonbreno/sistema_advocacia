// // static/js/admin_custom_mask.js

// // document.addEventListener('DOMContentLoaded', function() {
// //     console.log("Estou sendo carregado .2");
// //     // Aplica a máscara de entrada aos campos de telefone
// //     jQuery('#id_telefones-0-numero').mask('(00) 0000-00009');
// //     jQuery('#id_telefones-0-numero').blur(function(event) {
// //         if(jQuery(this).val().length == 15){ // Verifica se o telefone tem 9 dígitos após o código de área
// //             jQuery(this).mask('(00) 00000-0009');
// //         } else {
// //             jQuery(this).mask('(00) 0000-00009');
// //         }
// //     });
// // });

// $(document).ready(function () {
// 	alert("Testando importação do jquery!")
	
// });

// const mascara_telefone = function (val) {
// 	return val.replace(/\D/g, "").length === 11
// 		? "(00) 00000-0000"
// 		: "(00) 0000-0000";
// };
// const mascara_telefone_opts = {
// 	onKeyPress: function (val, e, field, options) {
// 		field.mask(mascara_telefone.apply({}, arguments), options);
// 	},
// };

// $(document).ready(function () {
// 	$("#id_data_de_nascimento").mask("00/00/0000");
// 	$(".form-control.cpf-mask").mask("000.000.000-00", { reverse: true });
// 	// $(".mask-cnpj").mask("00.000.000/0000-00", { reverse: true });
// 	$(".mask-cep").mask("00000-000");
// 	$(".mask-telefone").mask(mascara_telefone, mascara_telefone_opts);
// });

$(document).ready(function () {
    
    // $("#id_data_de_nascimento").mask("00/00/0000");
    //$("#id_cpf").mask("000.000.000-00", { reverse: true });
    $("#id_cep").mask("00000-000");

    const mascara_telefone = function (val) {
        return val.replace(/\D/g, "").length === 11 ? "(00) 00000-0000" : "(00) 0000-0000";
    };
    
    const mascara_telefone_opts = {
        onKeyPress: function (val, e, field, options) {
            field.mask(mascara_telefone.apply({}, arguments), options);
        }
    };

    $(".mask-telefone").mask(mascara_telefone, mascara_telefone_opts);
});