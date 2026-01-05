// static/js/pdf_viewer.js

let pdfDoc = null;
let currentPage = 1;
let totalPages = 0;
let currentScale = 1.5;

document.addEventListener("DOMContentLoaded", () => {
  pdfjsLib.GlobalWorkerOptions.workerSrc =
    "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

  const pdfURL = window.PDF_URL;

  pdfjsLib.getDocument(pdfURL).promise.then((pdf) => {
    pdfDoc = pdf;
    totalPages = pdf.numPages;
    renderPage(currentPage);
  });
});

function renderPage(pageNum) {
  pdfDoc.getPage(pageNum).then((page) => {
    const canvas = document.getElementById("pdfCanvas");
    const ctx = canvas.getContext("2d");
    const viewport = page.getViewport({ scale: currentScale });

    canvas.height = viewport.height;
    canvas.width = viewport.width;

    page.render({ canvasContext: ctx, viewport });

    document.getElementById(
      "pageInfo"
    ).textContent = `Page ${currentPage} of ${totalPages}`;
  });
}

function nextPage() {
  if (currentPage < totalPages) {
    currentPage++;
    renderPage(currentPage);
  }
}

function prevPage() {
  if (currentPage > 1) {
    currentPage--;
    renderPage(currentPage);
  }
}

// expose for onclick
window.nextPage = nextPage;
window.prevPage = prevPage;
