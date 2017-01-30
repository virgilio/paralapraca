
/*
 * Sistema que garante o download de certificados/comprovantes
 */

// Desativa o sistema de criação de PDFs via javascript no Internet Explorer
if (navigator.appName == 'Microsoft Internet Explorer' ||  !!(navigator.userAgent.match(/Trident/) || navigator.userAgent.match(/rv 11/)) || (typeof $.browser !== "undefined" && $.browser.msie == 1)){
      var download_button = document.getElementById("download-certificate");
      download_button.textContent="Imprimir";
      download_button.setAttribute("href","print");
      download_button.setAttribute("target","_blank");
      download_button.setAttribute("onclick","");
}

// Prepara a versão em PDF do certificado/comprovante sendo exibido no momento
var pdf = new jsPDF({
  orientation: 'landscape',
  unit: 'mm',
  format: [225, 131]
});

pdf.addHTML(document.getElementsByClassName('certificate-container'), function () {});

// Apenas quando o usuário clicar no botão de download, o arquivo PDF será enviado para download
// Vale lembrar que esse recurso não está disponível para Internet Explorer
function printToPDF() {
    pdf.save('certificado.pdf');
}
