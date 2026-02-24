const usernameEl = document.getElementById("username");
const themeEl = document.getElementById("theme");
const testTypeEl = document.getElementById("testType");
const wordValueEl = document.getElementById("wordValue");
const timeValueEl = document.getElementById("timeValue");
const previewImg = document.getElementById("cardPreview");
const output = document.getElementById("output");

function buildUrl() {
  const params = new URLSearchParams({
    username: usernameEl.value.trim(),
    theme: themeEl.value,
    wordValue: wordValueEl.value,
    timeValue: timeValueEl.value,
  });
  return `${window.location.origin}/api/monkeytype.svg?${params.toString()}`;
}

function preview() {
  const url = buildUrl();
  previewImg.src = url;
  output.value = url;
}

document.getElementById("previewBtn").addEventListener("click", preview);

document.getElementById("copyUrlBtn").addEventListener("click", async () => {
  const url = buildUrl();
  await navigator.clipboard.writeText(url);
  output.value = url;
});

document.getElementById("copyMdBtn").addEventListener("click", async () => {
  const url = buildUrl();
  const md = `![Monkeytype Stats](${url})`;
  await navigator.clipboard.writeText(md);
  output.value = md;
});

[usernameEl, themeEl, wordValueEl, timeValueEl].forEach((el) => {
  el.addEventListener("change", preview);
});

preview();
