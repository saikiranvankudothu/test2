// static/js/mindmap.js

let scale = 1;
let panX = 0;
let panY = 0;
let isPanning = false;
let startX, startY;

function applyTransform() {
  const canvas = document.querySelector(".mindmap-canvas");
  if (!canvas) return;

  canvas.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`;
}

window.generateMindmap = async function () {
  const text = document.getElementById("doc_text").textContent;
  const preview = document.getElementById("mindmap_preview");
  const loader = document.getElementById("mindmap_loading");

  // Reset state
  scale = 1;
  panX = 0;
  panY = 0;

  preview.innerHTML = "";
  loader.style.display = "block";

  const form = new URLSearchParams();
  form.append("text", text);

  try {
    const res = await fetch("/mindmap", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form,
    });

    const data = await res.json();
    loader.style.display = "none";

    preview.innerHTML = `
      <div class="mindmap-canvas mermaid">
        ${data.mindmap}
      </div>
    `;

    mermaid.initialize({ startOnLoad: false });
    mermaid.run();

    setTimeout(applyTransform, 50);
  } catch {
    loader.style.display = "none";
    preview.innerHTML = "<p>Failed to generate mind map.</p>";
  }
};

/* ---------------- ZOOM (MOUSE WHEEL) ---------------- */

document.addEventListener(
  "wheel",
  function (e) {
    const preview = document.getElementById("mindmap_preview");
    if (!preview.contains(e.target)) return;

    e.preventDefault();

    const delta = e.deltaY > 0 ? -0.1 : 0.1;
    scale = Math.min(Math.max(0.3, scale + delta), 3);

    applyTransform();
  },
  { passive: false }
);

/* ---------------- PAN (CLICK + DRAG) ---------------- */

document.addEventListener("mousedown", function (e) {
  const preview = document.getElementById("mindmap_preview");
  if (!preview.contains(e.target)) return;

  isPanning = true;
  startX = e.clientX - panX;
  startY = e.clientY - panY;
});

document.addEventListener("mousemove", function (e) {
  if (!isPanning) return;

  panX = e.clientX - startX;
  panY = e.clientY - startY;
  applyTransform();
});

document.addEventListener("mouseup", function () {
  isPanning = false;
});
