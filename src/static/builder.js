const usernameEl = document.getElementById("username");
const themeEl = document.getElementById("theme");
const wordValueEl = document.getElementById("wordValue");
const timeValueEl = document.getElementById("timeValue");
const previewImg = document.getElementById("cardPreview");
const output = document.getElementById("output");
const themeGrid = document.getElementById("themeGrid");
const themeSearch = document.getElementById("themeSearch");

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

function preview() {
  const url = buildUrl();
  previewImg.src = url;
  output.value = url;
}

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

function renderThemes(filter = "") {
  themeGrid.innerHTML = "";
  const q = filter.toLowerCase();
  const filtered = themes.filter((t) => t.name.toLowerCase().includes(q));

  for (const t of filtered) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "theme-btn" + (t.name === themeEl.value ? " active" : "");

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
  await navigator.clipboard.writeText(url);
  output.value = url;
  showToast("URL copied!");
});

document.getElementById("copyMdBtn").addEventListener("click", async () => {
  const url = buildUrl();
  const md = `![Monkeytype Stats](${url})`;
  await navigator.clipboard.writeText(md);
  output.value = md;
  showToast("Markdown copied!");
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

// Init
loadThemes().then(preview);
