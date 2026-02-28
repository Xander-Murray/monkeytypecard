if (localStorage.getItem("ui-theme") === "light") {
  document.body.classList.add("light");
}

const usernameEl = document.getElementById("username");
const themeEl = document.getElementById("theme");
const wordValueEl = document.getElementById("wordValue");
const timeValueEl = document.getElementById("timeValue");
const previewImg = document.getElementById("cardPreview");
const previewCard = document.querySelector(".preview-card");
const output = document.getElementById("output");
const themeGrid = document.getElementById("themeGrid");
const themeSearch = document.getElementById("themeSearch");
const randBtn = document.getElementById("randomTheme");

let themes = [];

function buildUrl() {
  const params = new URLSearchParams({
    username: usernameEl.value.trim(),
    theme: themeEl.value,
    wordValue: wordValueEl.value,
    timeValue: timeValueEl.value,
  });
  return `${window.location.origin}/monkeytype.svg?${params.toString()}`;
}

// Show loading state while the SVG fetches, error state if it fails
function preview() {
  const url = buildUrl();

  previewCard.classList.add("loading");
  previewCard.classList.remove("error");
  previewCard.removeAttribute("data-error");

  previewImg.src = url;
  output.value = url;
}

// Clear loading state once the image loads successfully
previewImg.addEventListener("load", () => {
  previewCard.classList.remove("loading");
});

// Show error message inside the preview area if the image fails
previewImg.addEventListener("error", () => {
  previewCard.classList.remove("loading");
  previewCard.classList.add("error");
  previewCard.setAttribute("data-error", "could not load card");
});

function showToast(msg) {
  let toast = document.querySelector(".toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.className = "toast";
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 1800);
}

// Clipboard fallback for non-HTTPS environments
async function copyToClipboard(text) {
  if (navigator.clipboard) {
    await navigator.clipboard.writeText(text);
  } else {
    // Fallback: create a temporary textarea and use execCommand
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
  }
}

function renderThemes(filter = "") {
  themeGrid.innerHTML = "";
  const q = filter.toLowerCase();
  const filtered = themes.filter((t) => t.name.toLowerCase().includes(q));

  for (const t of filtered) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "theme-btn" + (t.name === themeEl.value ? " active" : "");
    // Store theme name as data attr for random-theme lookup
    btn.dataset.theme = t.name;

    btn.innerHTML = `
      <span class="theme-name">${t.name.replace(/_/g, " ")}</span>
      <div class="theme-colors">
        <span style="background:${t.bgColor}"></span>
        <span style="background:${t.subAltColor}"></span>
        <span style="background:${t.subColor}"></span>
        <span style="background:${t.mainColor}"></span>
        <span style="background:${t.textColor}"></span>
      </div>
    `;

    btn.addEventListener("click", () => {
      themeEl.value = t.name;
      themeGrid
        .querySelectorAll(".theme-btn")
        .forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      preview();
    });

    themeGrid.appendChild(btn);
  }
}

async function loadThemes() {
  const res = await fetch("/api/themes");
  themes = await res.json();
  renderThemes();
}

themeSearch.addEventListener("input", () => {
  renderThemes(themeSearch.value);
});

document.getElementById("previewBtn").addEventListener("click", preview);

document.getElementById("copyUrlBtn").addEventListener("click", async () => {
  const url = buildUrl();
  await copyToClipboard(url);
  output.value = url;
  showToast("URL copied!");
});

document.getElementById("copyMdBtn").addEventListener("click", async () => {
  const url = buildUrl();
  const md = `![Monkeytype Stats](${url})`;
  await copyToClipboard(md);
  output.value = md;
  showToast("Markdown copied!");
});

// Random theme picks a theme and scrolls it into view
randBtn.addEventListener("click", () => {
  if (themes.length === 0) return;
  const randTheme = themes[Math.floor(Math.random() * themes.length)];
  themeEl.value = randTheme.name;

  // Clear search so the full list is visible for scrolling
  themeSearch.value = "";
  renderThemes();

  // Find the button by data-theme and highlight + scroll to it
  const activeBtn = themeGrid.querySelector(`[data-theme="${randTheme.name}"]`);
  if (activeBtn) {
    activeBtn.classList.add("active");
    activeBtn.scrollIntoView({ behavior: "smooth", block: "center" });
  }
  preview();
});

// Auto-preview on control change
[usernameEl, wordValueEl, timeValueEl].forEach((el) => {
  el.addEventListener("change", preview);
});

let debounce;
usernameEl.addEventListener("input", () => {
  clearTimeout(debounce);
  debounce = setTimeout(preview, 400);
});

document.getElementById("themeToggle").addEventListener("click", () => {
  document.body.classList.toggle("light");
  const mode = document.body.classList.contains("light") ? "light" : "dark";
  localStorage.setItem("ui-theme", mode);
});

// Init
loadThemes().then(preview);
