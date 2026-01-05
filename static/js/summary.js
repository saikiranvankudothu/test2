// static/js/summary.js

window.generateSummary = async function () {
  const textEl = document.getElementById("doc_text");
  const outputBox = document.getElementById("summaryBox");
  const loader = document.getElementById("summaryOutput");

  if (!textEl || !outputBox || !loader) {
    console.error("Summary elements not found in DOM");
    return;
  }

  const text = textEl.textContent.trim();
  if (!text) {
    outputBox.textContent = "No document text available.";
    return;
  }

  // Clear old content
  outputBox.textContent = "";
  loader.style.display = "block";

  const form = new URLSearchParams();
  form.append("text", text);

  try {
    const res = await fetch("/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: form,
    });

    const data = await res.json();

    loader.style.display = "none";

    // 🔴 THIS IS THE IMPORTANT LINE
    outputBox.textContent = data.summary || "No summary returned.";
  } catch (err) {
    loader.style.display = "none";
    outputBox.textContent = "Failed to generate summary.";
    console.error(err);
  }
};

// // static/js/summary.js

// window.generateSummary = async function () {
//   const text = document.getElementById("doc_text").textContent;

//   document.getElementById("summaryOutput").style.display = "block";
//   document.getElementById("summaryBox").textContent = "";

//   const form = new URLSearchParams();
//   form.append("text", text);
//   try {
//     const res = await fetch("/summarize", {
//       method: "POST",
//       headers: { "Content-Type": "application/x-www-form-urlencoded" },
//       body: form,
//     });

//     const data = await res.json();
//     document.getElementById("summaryOutput").style.display = "none";
//     document.getElementById("summaryBox").textContent = data.summary;
//   } catch {
//     document.getElementById("summaryOutput").style.display = "none";
//     document.getElementById("summaryBox").textContent = "Summary failed.";
//   }
// };
