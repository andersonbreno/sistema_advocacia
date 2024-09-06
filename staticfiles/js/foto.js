// // Corrigido para esperar pelo evento DOMContentLoaded
// document.addEventListener('DOMContentLoaded', function() {
//     const video = document.getElementById('webcam');
//     const canvas = document.getElementById('canvas');
//     const snap = document.getElementById("capture");
//     const errorMsgElement = document.querySelector('span#errorMsg');

//     const constraints = {
//         audio: false,
//         video: {
//             width: 640, height: 480
//         }
//     };

//     // Acessar a webcam
//     async function init() {
//         try {
//             const stream = await navigator.mediaDevices.getUserMedia(constraints);
//             handleSuccess(stream);
//         } catch (e) {
//             errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
//         }
//     }

//     // Sucesso
//     function handleSuccess(stream) {
//         window.stream = stream;
//         video.srcObject = stream;
//     }

//     // Carregar webcam
//     init();

//     // Capturar a foto
//     snap.addEventListener("click", function() {
        
//         canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
//         let image_data_url = canvas.toDataURL('image/jpeg');

//         console.log("Chegou até aqui.")
//         // Colocar a foto no input para ser enviada pelo formulário
//         document.getElementById('foto').value = image_data_url;
//         console.log("Chegou até aqui 2 ...");
//     });
// });

    

	// (function () {
	// 	const camera = document.getElementById("camera");
	// 	camera.style.display = "none";
	// 	let fator = 0;
	// 	const height = 240;
	// 	let width = 0;

	// 	let streaming = false;

	// 	let video = null;
	// 	let video_src = null;
	// 	let canvas = null;
	// 	let canvas_src = null;
	// 	let foto = null;
	// 	let foto_src = null;
	// 	let foto_bt = null;
	// 	let capturar_bt = null;
	// 	let reverter_bt = null;

	// 	const imagem_cadastrada = "{{ widget.value.url }}" ? true : false;
	// 	let imagem_capturada = false;

	// 	function carregar_data_uri(blob) {
	// 		let fileName = "foto_perfil.jpeg";
	// 		let file = new File(
	// 			[blob],
	// 			fileName,
	// 			{ type: "image/jpeg", lastModified: new Date().getTime() },
	// 			"utf-8",
	// 		);
	// 		let container = new DataTransfer();
	// 		container.items.add(file);
	// 		foto_src.files = container.files;
	// 	}

	// 	function inicializacao() {
	// 		video = document.getElementById("video");
	// 		video_src = document.getElementById("video_src");
	// 		canvas = document.getElementById("canvas");
	// 		canvas_src = document.getElementById("canvas_src");
	// 		foto = document.getElementById("foto");
	// 		foto_src = document.getElementById("{{ widget.attrs.id }}");
	// 		foto_bt = document.getElementById("{{ widget.name }}_bt");
    //         console.log("Estou chegando até aqui? ... ")
	// 		capturar_bt = document.getElementById("capturar_{{ widget.name }}_bt");
	// 		console.log("Elemento capturar_bt:", capturar_bt);
	// 		capturar_bt.style.display = "none";
	// 		reverter_bt = document.getElementById("reverter_{{ widget.name }}_bt");
	// 		reverter_bt.style.display = "none";

	// 		if (!imagem_cadastrada) {
	// 			foto.style.display = "none";
	// 		}

	// 		navigator.mediaDevices
	// 			.getUserMedia({ video: true, audio: false })
	// 			.then(function (stream) {
	// 				const h = stream.getVideoTracks()[0].getSettings().height;
	// 				const w = stream.getVideoTracks()[0].getSettings().width;
	// 				fator = w / h;
	// 				video.srcObject = stream;
	// 				video.play();
	// 				video_src.srcObject = stream;
	// 				video_src.play();
	// 			})
	// 			.catch(function (erro) {
	// 				console.log("Ocorreu um erro: " + erro);
	// 			});

	// 		video.addEventListener(
	// 			"canplay",
	// 			function (ev) {
	// 				if (!streaming) {
	// 					width = height * video.videoWidth / video.videoHeight;
	// 					video.setAttribute("width", width);
	// 					video.setAttribute("height", height);
	// 					video_src.setAttribute("width", fator * width);
	// 					video_src.setAttribute("height", fator * height);
	// 					canvas.setAttribute("width", width);
	// 					canvas.setAttribute("height", height);
	// 					canvas_src.setAttribute("width", fator * width);
	// 					canvas_src.setAttribute("height", fator * height);
	// 					streaming = true;
	// 				}
	// 			},
	// 			false,
	// 		);


	// 		capturar_bt.addEventListener(
	// 			"click",
	// 			function (ev) {
	// 				ev.preventDefault();
	// 				limpar_foto();
	// 				capturar_foto();
	// 				camera.style.display = "none";
	// 				foto.style.display = "";
	// 				this.disabled = true;
	// 				this.style.display = "none";
	// 				reverter_bt.disabled = false;
	// 				reverter_bt.style.display = "";
	// 			},
	// 			false,
	// 		);

	// 		foto_bt.addEventListener(
	// 			"click",
	// 			function (ev) {
	// 				ev.preventDefault();
	// 				if (!imagem_cadastrada) {
	// 					let pfp_placeholder = document.querySelector(".pfp-placeholder");
	// 					pfp_placeholder.style.display = "none";
	// 				}
	// 				foto.style.display = "none";
	// 				camera.style.display = "";
	// 				this.disabled = true;
	// 				this.style.display = "none";
	// 				capturar_bt.disabled = false;
	// 				capturar_bt.style.display = "";
	// 				reverter_bt.disabled = true;
	// 				reverter_bt.style.display = "none";
	// 			},
	// 			false,
	// 		);

	// 		reverter_bt.addEventListener(
	// 			"click",
	// 			function (ev) {
	// 				ev.preventDefault();
	// 				limpar_foto();
	// 				this.disabled = true;
	// 				this.style.display = "none";
	// 				if (imagem_cadastrada) {
	// 					foto_bt.disabled = false;
	// 					foto_bt.style.display = "";
	// 					camera.style.display = "none";
	// 					foto.setAttribute("src", "{{ widget.value.url }}");
	// 					foto.style.display = "";
	// 				} else {
	// 					capturar_bt.disabled = false;
	// 					capturar_bt.style.display = "";
	// 					camera.style.display = "";
	// 					foto.style.display = "none";
	// 				}
	// 			},
	// 			false,
	// 		);

	// 	}

	// 	function limpar_foto() {
	// 		let context = canvas.getContext("2d");
	// 		context.fillStyle = "#DDD";
	// 		context.fillRect(0, 0, canvas.width, canvas.height);

	// 		let data = canvas.toDataURL("image/jpeg", 1.0);
	// 		foto.setAttribute("src", data);
	// 		foto_src.value = null;
	// 	}

	// 	function capturar_foto() {
	// 		let context = canvas.getContext("2d");
	// 		let context_src = canvas_src.getContext("2d");
	// 		if (width && height) {
	// 			context.drawImage(video, 0, 0, canvas.width, canvas.height);
	// 			context_src.drawImage(video_src, 0, 0, canvas_src.width, canvas_src.height);

	// 			let data = canvas.toDataURL("image/jpeg", 1.0);
	// 			foto.setAttribute("src", data);
	// 			canvas_src.toBlob(carregar_data_uri, "image/jpeg", 1.0);
	// 		} else {
	// 			limpar_foto();
	// 		}
	// 	}

	// 	window.addEventListener("load", inicializacao, false);
	// })();
