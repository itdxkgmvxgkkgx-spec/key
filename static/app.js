/* ═══ NovaSeek Dashboard — vanilla JS SPA ═══ */
"use strict";
const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);

const I18N = {
  fa: {
    nav_login: "ورود / ثبت‌نام", nav_dash: "داشبورد",
    hero_badge: "موتور جست‌وجوی محلی — نامحدود و بدون محدودیت نرخ",
    hero_t1: "جست‌وجوی وب با یک", hero_t2: "API ساده",
    hero_sub: "NovaSeek روی SearXNG محلی اجرا می‌شود؛ بدون کلید گوگل، بدون سقف درخواست موتور، با سهمیه روزانه هوشمند برای هر کاربر.",
    hero_ph: "مثلاً: هوش مصنوعی چیست؟", hero_go: "جست‌وجو",
    hero_hint: "برای استفاده از API کامل، ثبت‌نام کنید و کلید بسازید — ۱۰۰۰ درخواست رایگان هر روز",
    f1t: "سرعت برق‌آسا", f1d: "کش در حافظه با TTL، SQLite در حالت WAL و GZip — پاسخ تکراری در کسری از میلی‌ثانیه.",
    f2t: "موتور نامحدود", f2d: "SearXNG خودمیزبان روی +۷۰ موتور جست‌وجو؛ بدون کلید، بدون CAPTCHA، بدون سقف. فالبک خودکار به DuckDuckGo.",
    f3t: "کلید API واقعی", f3d: "هر کاربر تا ۱۰ کلید nvsk_ می‌سازد، لغو می‌کند و مصرف هر کلید را جدا می‌بیند.",
    f4t: "سهمیه روزانه", f4d: "۱۰۰۰ درخواست در روز برای هر کاربر که هر روز ساعت ۰۰:۰۰ UTC خودکار تمدید می‌شود.",
    f5t: "پنل ادمین", f5d: "مالک سرویس کاربران را می‌بیند، تعلیق/فعال می‌کند و سهمیه هرکدام را تغییر می‌دهد.",
    f6t: "دو زبانه و دو تم", f6d: "فارسی (راست‌چین) و انگلیسی، دارک/لایت — انتخاب شما در مرورگر ذخیره می‌شود.",
    docs_title: "مستندات API", docs_search_d: "جست‌وجوی وب. احراز هویت با هدر X-API-Key انجام می‌شود.",
    docs_usage_d: "مشاهده سهمیه و مصرف امروز با همان کلید API.",
    th_param: "پارامتر", th_type: "نوع", th_desc: "توضیح",
    p_q: "عبارت جست‌وجو (الزامی)", p_lang: "زبان نتایج: fa, en, all, auto",
    p_site: "محدودسازی به یک سایت، مثل wikipedia.org", p_count: "تعداد نتایج (۱ تا ۵۰، پیش‌فرض ۱۰)",
    copy: "کپی", copied: "کپی شد ✓",
    login: "ورود", register: "ثبت‌نام", username: "نام کاربری", password: "رمز عبور", email: "ایمیل (اختیاری)",
    logout: "خروج", dash_hello: "سلام",
    st_used: "مصرف امروز", st_remain: "باقی‌مانده امروز", st_quota: "سهمیه روزانه", st_total: "کل درخواست‌ها",
    chart_title: "مصرف ۷ روز گذشته", renew_note: "تمدید خودکار: هر روز ۰۰:۰۰ UTC",
    keys_title: "کلیدهای API من", key_name: "نام کلید", key_create: "ساخت کلید",
    th_name: "نام", th_key: "کلید", th_reqs: "درخواست‌ها", th_status: "وضعیت",
    pg_title: "تست زنده API", pg_run: "اجرای درخواست",
    admin_title: "پنل مدیریت", adm_users: "کاربران", adm_keys: "کلیدهای فعال", adm_reqs: "درخواست امروز",
    active: "فعال", suspended: "تعلیق", suspend: "تعلیق", activate: "فعال‌سازی",
    footer: "ساخته‌شده با ❤️ برای جست‌وجوی آزاد",
    err_generic: "خطایی رخ داد", need_key: "اول یک کلید API بسازید",
    quota_msg: "سهمیه جدید", saved: "ذخیره شد", results_for: "نتایج برای",
  },
  en: {
    nav_login: "Sign in / Register", nav_dash: "Dashboard",
    hero_badge: "Local search engine — unlimited, no rate caps",
    hero_t1: "Web search with one", hero_t2: "simple API",
    hero_sub: "NovaSeek runs on a self-hosted SearXNG engine; no Google keys, no engine-side caps, with smart per-user daily quotas.",
    hero_ph: "e.g. what is artificial intelligence?", hero_go: "Search",
    hero_hint: "Register and create a key for full API access — 1,000 free requests every day",
    f1t: "Blazing fast", f1d: "In-memory TTL cache, WAL-mode SQLite and GZip — cached replies in a fraction of a millisecond.",
    f2t: "Unlimited engine", f2d: "Self-hosted SearXNG over 70+ engines; no keys, no CAPTCHA, no ceilings. Automatic DuckDuckGo fallback.",
    f3t: "Real API keys", f3d: "Every user creates up to 10 nvsk_ keys, revokes them, and sees per-key usage.",
    f4t: "Daily quota", f4d: "1,000 requests per user per day, auto-renewed at 00:00 UTC.",
    f5t: "Admin panel", f5d: "The owner sees all users, suspends/activates them, and adjusts each quota.",
    f6t: "Bilingual, dual theme", f6d: "Persian (RTL) and English, dark/light — your choice persists in the browser.",
    docs_title: "API Docs", docs_search_d: "Web search. Authenticate with the X-API-Key header.",
    docs_usage_d: "Check today's quota and usage with the same API key.",
    th_param: "Param", th_type: "Type", th_desc: "Description",
    p_q: "Search query (required)", p_lang: "Result language: fa, en, all, auto",
    p_site: "Restrict to one site, e.g. wikipedia.org", p_count: "Number of results (1–50, default 10)",
    copy: "Copy", copied: "Copied ✓",
    login: "Sign in", register: "Register", username: "Username", password: "Password", email: "Email (optional)",
    logout: "Log out", dash_hello: "Hello",
    st_used: "Used today", st_remain: "Remaining today", st_quota: "Daily quota", st_total: "Total requests",
    chart_title: "Last 7 days usage", renew_note: "Auto-renewal: daily at 00:00 UTC",
    keys_title: "My API keys", key_name: "Key name", key_create: "Create key",
    th_name: "Name", th_key: "Key", th_reqs: "Requests", th_status: "Status",
    pg_title: "Live API playground", pg_run: "Run request",
    admin_title: "Admin panel", adm_users: "Users", adm_keys: "Active keys", adm_reqs: "Requests today",
    active: "Active", suspended: "Suspended", suspend: "Suspend", activate: "Activate",
    footer: "Built with ❤️ for open search",
    err_generic: "Something went wrong", need_key: "Create an API key first",
    quota_msg: "New quota", saved: "Saved", results_for: "Results for",
  },
};

let state = { lang: localStorage.getItem("nvsk_lang") || "fa",
              theme: localStorage.getItem("nvsk_theme") || "dark",
              token: localStorage.getItem("nvsk_token") || null,
              user: null, authMode: "login", keys: [] };

const t = (k) => I18N[state.lang][k] || k;

function applyLang() {
  document.documentElement.lang = state.lang;
  document.documentElement.dir = state.lang === "fa" ? "rtl" : "ltr";
  $("#langLabel").textContent = state.lang === "fa" ? "EN" : "فا";
  $$("[data-i18n]").forEach((el) => (el.textContent = t(el.dataset.i18n)));
  $$("[data-i18n-ph]").forEach((el) => (el.placeholder = t(el.dataset.i18nPh)));
  localStorage.setItem("nvsk_lang", state.lang);
}

function applyTheme() {
  document.documentElement.dataset.theme = state.theme;
  document.documentElement.classList.toggle("dark", state.theme === "dark");
  $("#themeIcon").textContent = state.theme === "dark" ? "☀️" : "🌙";
  localStorage.setItem("nvsk_theme", state.theme);
}

function toast(msg, kind = "ok") {
  const el = $("#toast");
  el.textContent = msg; el.className = "show " + kind;
  setTimeout(() => el.classList.remove("show"), 2200);
}

async function api(path, opts = {}) {
  const headers = { "Content-Type": "application/json", ...(opts.headers || {}) };
  if (state.token) headers["Authorization"] = "Bearer " + state.token;
  const res = await fetch(path, { ...opts, headers });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) { const e = new Error(typeof data.detail === "string" ? data.detail : "error"); e.status = res.status; e.data = data; throw e; }
  return data;
}

function copyText(txt) {
  navigator.clipboard.writeText(txt).then(() => toast(t("copied"))).catch(() => {
    const ta = document.createElement("textarea"); ta.value = txt; document.body.appendChild(ta);
    ta.select(); document.execCommand("copy"); ta.remove(); toast(t("copied"));
  });
}

/* ── views ── */
function show(view) {
  ["landing", "features", "authSection", "dashSection"].forEach((id) => {
    const el = document.getElementById(id); if (el) el.classList.add("hidden");
  });
  if (view === "landing") { $("#landing").classList.remove("hidden"); $("#features").classList.remove("hidden"); }
  if (view === "auth") $("#authSection").classList.remove("hidden");
  if (view === "dash") $("#dashSection").classList.remove("hidden");
  $("#navAuthBtn").classList.toggle("hidden", !!state.user);
  $("#navDashBtn").classList.toggle("hidden", !state.user);
}

/* ── auth ── */
function setAuthMode(mode) {
  state.authMode = mode;
  $("#tabLogin").className = "flex-1 py-2.5 font-bold " + (mode === "login" ? "bg-brand-600 text-white" : "opacity-60");
  $("#tabRegister").className = "flex-1 py-2.5 font-bold " + (mode === "register" ? "bg-brand-600 text-white" : "opacity-60");
  $("#authEmail").classList.toggle("hidden", mode === "login");
  $("#authSubmit").textContent = t(mode);
  $("#authMsg").textContent = "";
}

async function submitAuth() {
  const body = { username: $("#authUser").value.trim(), password: $("#authPass").value };
  if (state.authMode === "register") body.email = $("#authEmail").value.trim() || null;
  try {
    const data = await api("/api/auth/" + state.authMode, { method: "POST", body: JSON.stringify(body) });
    state.token = data.token; state.user = data.user;
    localStorage.setItem("nvsk_token", state.token);
    await loadDashboard();
  } catch (e) { $("#authMsg").textContent = e.data?.detail || t("err_generic"); }
}

/* ── dashboard ── */
async function loadDashboard() {
  try { state.user = await api("/api/auth/me"); }
  catch { state.token = null; state.user = null; localStorage.removeItem("nvsk_token"); show("landing"); return; }
  show("dash");
  $("#dashUsername").textContent = state.user.username;
  const stats = await api("/api/me/stats");
  $("#stUsed").textContent = stats.used_today.toLocaleString();
  $("#stRemain").textContent = stats.remaining_today.toLocaleString();
  $("#stQuota").textContent = stats.daily_quota.toLocaleString();
  $("#stTotal").textContent = stats.total_requests.toLocaleString();
  drawChart(stats.history_7d);
  await loadKeys();
  if (state.user.is_admin) { $("#adminPanel").classList.remove("hidden"); loadAdmin(); }
}

function drawChart(history) {
  const cv = $("#usageChart"), ctx = cv.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = 90;
  cv.width = W * dpr; cv.height = H * dpr; ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, W, H);
  const max = Math.max(1, ...history.map((h) => h.count));
  const bw = W / Math.max(1, history.length);
  history.forEach((h, i) => {
    const bh = Math.max(3, (h.count / max) * (H - 24));
    const g = ctx.createLinearGradient(0, H - bh, 0, H);
    g.addColorStop(0, "#818cf8"); g.addColorStop(1, "#a855f7");
    ctx.fillStyle = g;
    const x = i * bw + bw * 0.2, w = bw * 0.6;
    ctx.beginPath(); ctx.roundRect(x, H - bh - 14, w, bh, 5); ctx.fill();
    ctx.fillStyle = "rgba(128,128,140,.8)"; ctx.font = "9px Vazirmatn";
    ctx.textAlign = "center";
    ctx.fillText(h.date.slice(5), x + w / 2, H - 2);
    if (h.count) ctx.fillText(h.count, x + w / 2, H - bh - 18);
  });
}

async function loadKeys() {
  const data = await api("/api/keys");
  state.keys = data.keys;
  const tb = $("#keysTable"); tb.innerHTML = "";
  data.keys.forEach((k) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="font-bold">${esc(k.name)}</td>
      <td><code class="text-xs text-brand-400" dir="ltr">${esc(k.key.slice(0, 18))}…</code>
        <button class="copy-btn ms-1" data-k="${esc(k.key)}">📋</button></td>
      <td>${k.total_requests.toLocaleString()}</td>
      <td>${k.is_active ? `<span class="pill-on">${t("active")}</span>` : `<span class="pill-off">${t("suspended")}</span>`}</td>
      <td>${k.is_active ? `<button class="copy-btn !text-rose-400 revoke" data-id="${k.id}">✕</button>` : ""}</td>`;
    tb.appendChild(tr);
  });
  tb.querySelectorAll("[data-k]").forEach((b) => (b.onclick = () => copyText(b.dataset.k)));
  tb.querySelectorAll(".revoke").forEach((b) => (b.onclick = async () => {
    await api("/api/keys/" + b.dataset.id, { method: "DELETE" }); toast(t("saved")); loadKeys();
  }));
  const sel = $("#pgKey"); sel.innerHTML = "";
  data.keys.filter((k) => k.is_active).forEach((k) => {
    const o = document.createElement("option"); o.value = k.key; o.textContent = k.name; sel.appendChild(o);
  });
}

async function runPlayground() {
  const key = $("#pgKey").value;
  if (!key) return toast(t("need_key"), "err");
  const params = new URLSearchParams({ q: $("#pgQuery").value || "novaseek", lang: $("#pgLang").value, count: "5" });
  if ($("#pgSite").value.trim()) params.set("site", $("#pgSite").value.trim());
  $("#pgOutput").textContent = "…";
  try {
    const res = await fetch("/api/v1/search?" + params, { headers: { "X-API-Key": key } });
    $("#pgOutput").textContent = JSON.stringify(await res.json(), null, 2);
    loadDashboard();
  } catch { $("#pgOutput").textContent = t("err_generic"); }
}

/* ── admin ── */
async function loadAdmin() {
  const ov = await api("/api/admin/overview");
  $("#admUsers").textContent = ov.users.toLocaleString();
  $("#admKeys").textContent = ov.active_api_keys.toLocaleString();
  $("#admReqs").textContent = ov.requests_today.toLocaleString();
  const { users } = await api("/api/admin/users");
  const tb = $("#adminTable"); tb.innerHTML = "";
  users.forEach((u) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${u.id}</td><td class="font-bold">${esc(u.username)}${u.is_admin ? " 👑" : ""}</td>
      <td>${u.used_today.toLocaleString()}</td>
      <td><input class="input !w-24 !py-1 !px-2 text-xs quota-in" data-id="${u.id}" type="number" value="${u.daily_quota}"></td>
      <td>${u.total_requests.toLocaleString()}</td>
      <td>${u.is_active ? `<span class="pill-on">${t("active")}</span>` : `<span class="pill-off">${t("suspended")}</span>`}</td>
      <td class="whitespace-nowrap">
        ${u.is_admin ? "" : `<button class="copy-btn toggle-u" data-id="${u.id}" data-act="${u.is_active ? "off" : "on"}">${u.is_active ? t("suspend") : t("activate")}</button>`}
        <button class="copy-btn save-q" data-id="${u.id}">💾</button>
      </td>`;
    tb.appendChild(tr);
  });
  tb.querySelectorAll(".toggle-u").forEach((b) => (b.onclick = async () => {
    await api("/api/admin/users/" + b.dataset.id, { method: "PATCH", body: JSON.stringify({ is_active: b.dataset.act === "on" }) });
    toast(t("saved")); loadAdmin();
  }));
  tb.querySelectorAll(".save-q").forEach((b) => (b.onclick = async () => {
    const v = parseInt(tb.querySelector(`.quota-in[data-id="${b.dataset.id}"]`).value) || 0;
    await api("/api/admin/users/" + b.dataset.id, { method: "PATCH", body: JSON.stringify({ daily_quota: v }) });
    toast(t("quota_msg") + ": " + v.toLocaleString()); loadAdmin();
  }));
}

/* ── hero demo (public, no key — uses /api/health ping + playful preview) ── */
async function heroSearch() {
  const q = $("#heroQuery").value.trim();
  if (!q) return;
  const box = $("#heroResults");
  box.classList.remove("hidden");
  box.innerHTML = `<div class="card result-card text-center opacity-70">${"⏳"}</div>`;
  // The demo prompts signup; real search needs a key.
  box.innerHTML = `<div class="card result-card text-center">
    <p class="font-bold mb-2">${t("results_for")} «${esc(q)}»</p>
    <p class="text-sm opacity-70 mb-4">${t("hero_hint")}</p>
    <button class="btn-primary text-sm" onclick="show('auth')">${t("nav_login")}</button></div>`;
}

function esc(s) { return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }

/* ── wire up ── */
$("#langToggle").onclick = () => { state.lang = state.lang === "fa" ? "en" : "fa"; applyLang(); setAuthMode(state.authMode); if (state.user) loadDashboard(); };
$("#themeToggle").onclick = () => { state.theme = state.theme === "dark" ? "light" : "dark"; applyTheme(); };
$("#navAuthBtn").onclick = () => { show("auth"); window.scrollTo({ top: 0, behavior: "smooth" }); };
$("#navDashBtn").onclick = () => loadDashboard();
$("#tabLogin").onclick = () => setAuthMode("login");
$("#tabRegister").onclick = () => setAuthMode("register");
$("#authSubmit").onclick = submitAuth;
$("#authPass").addEventListener("keydown", (e) => e.key === "Enter" && submitAuth());
$("#logoutBtn").onclick = () => { state.token = null; state.user = null; localStorage.removeItem("nvsk_token"); show("landing"); };
$("#createKeyBtn").onclick = async () => {
  try { const k = await api("/api/keys", { method: "POST", body: JSON.stringify({ name: $("#newKeyName").value || "default" }) });
    toast(t("copied")); copyText(k.key); loadKeys(); } catch (e) { toast(e.data?.detail || t("err_generic"), "err"); }
};
$("#pgRun").onclick = runPlayground;
$("#heroSearchBtn").onclick = heroSearch;
$("#heroQuery").addEventListener("keydown", (e) => e.key === "Enter" && heroSearch());
$$("[data-copy]").forEach((b) => (b.onclick = () => copyText(b.dataset.copy)));

applyTheme(); applyLang(); setAuthMode("login");
if (state.token) loadDashboard(); else show("landing");
