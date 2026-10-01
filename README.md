<div align="center">

# 🔭 NovaSeek — Self-Hosted Search API

**Blazing-fast · Unlimited local engine · API keys · Bilingual dashboard**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![SearXNG](https://img.shields.io/badge/Engine-SearXNG%20local-3050FF)
![SQLite](https://img.shields.io/badge/DB-SQLite%20WAL-003B57?logo=sqlite&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/Deploy-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Tunnel-Cloudflare%20Quick-F38020?logo=cloudflare&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

[فارسی](#-راهنمای-فارسی) · [English](#-english-guide)

</div>

---

## 🇫🇷 راهنمای فارسی

### NovaSeek چیه؟

NovaSeek یه **سرویس Search API** کامل و آماده‌ی دیپلویه که روی **GitHub Actions** رایگان اجرا میشه:

- 🔍 **موتور جست‌وجوی محلی SearXNG** — بدون کلید گوگل، بدون CAPTCHA، بدون سقف درخواست (متاهان‌جست‌وجو روی +۷۰ موتور). اگر SearXNG بالا نیومد، خودکار به **DuckDuckGo** فالبک می‌کنه.
- 🔑 **سیستم کلید API واقعی** — هر کاربر تا ۱۰ کلید `nvsk_...` می‌سازه، کپی می‌کنه، لغو می‌کنه.
- 📊 **سهمیه روزانه** — ۱۰۰۰ درخواست برای هر کاربر که هر روز ساعت ۰۰:۰۰ UTC خودکار تمدید میشه.
- 👑 **پنل اونر** — دیدن همه کاربران، مصرف امروز/کل هرکدوم، تعلیق/فعال‌سازی، تغییر سهمیه.
- 🌗 **UI دو زبانه (فارسی RTL / English)** با **تم دارک/لایت** — انتخابت تو مرورگر ذخیره میشه.
- 🔁 **لوپ ۶ ساعته** — قبل از تایم‌اوت گیت‌هاب، دیتابیس بکاپ میشه و با توکن `GH_PAT` ران بعدی خودکار استارت میخوره؛ **همه اطلاعات (کاربران، کلیدها، مصرف) دست نخورده برمی‌گرده**.
- 🌐 **تانل موقت Cloudflare** (`trycloudflare.com`) — بدون نیاز به اکانت کلادفلر، آدرس عمومی تو خلاصه‌ی ران چاپ میشه.
- 💾 **دیتابیس لوکال SQLite با WAL** — سبک، سریع و برای هزاران کاربر هم‌زمان مناسب؛ با کش TTL حافظه‌ای و GZip برای سرعت مضاعف.

---

### 🚀 راه‌اندازی قدم‌به‌قدم (۵ دقیقه)

#### ۱) ریپو رو بساز و کد رو پوش کن

```bash
git init && git add . && git commit -m "NovaSeek v1.0"
git remote add origin https://github.com/<YOU>/novaseek.git
git push -u origin main
```

#### ۲) سکرت‌ها رو ست کن

برو به: **Settings → Secrets and variables → Actions → New repository secret**

| سکرت | توضیح | مثال |
|---|---|---|
| `APP_SECRET_KEY` | کلید امضای JWT (رشته طولانی رندوم) | `openssl rand -hex 32` |
| `OWNER_USERNAME` | یوزرنیم اکانت اونر | `admin` |
| `OWNER_PASSWORD` | پسورد اکانت اونر (قوی انتخاب کن!) | `S3cure!Pass` |
| `GH_PAT` | توکن گیت‌هاب برای لوپ ۶ ساعته — [ایجاد](https://github.com/settings/tokens) با اسکوپ `repo` و `workflow` | `ghp_...` |

> ⚠️ هیچ‌کدوم از این مقادیر تو کد هاردکد نشدن — فقط از سکرت‌ها خونده میشن.

#### ۳) ورک‌فلو رو ران کن

**Actions → NovaSeek Deploy & Keepalive → Run workflow**

بعد از ~۱ دقیقه، تو صفحه‌ی ران باکس **«🚀 NovaSeek is LIVE»** رو می‌بینی با آدرس عمومی مثل:
`https://random-words-123.trycloudflare.com`

#### ۴) لوپ خودکار

- جاب حدود **۵ ساعت و ۵۰ دقیقه** زنده می‌مونه (هر ۵ دقیقه heartbeat می‌زنه).
- بعدش: بکاپ دیتابیس تو **Releases** ذخیره میشه → ران جدید خودکار تریگر میشه → دیتابیس ری‌استور میشه → سرویس با **همون کاربران و کلیدها** بالا میاد.
- آدرس تانل تو هر ران عوض میشه (ماهیت تانل موقته)؛ آدرس جدید همیشه تو Summary آخرین ران هست.

---

### 📡 استفاده از API

```bash
# جست‌وجو
curl -H "X-API-Key: nvsk_YOUR_KEY" \
  "https://YOUR-URL.trycloudflare.com/api/v1/search?q=هوش+مصنوعی&lang=fa&count=10"

# محدود به یه سایت خاص
curl -H "X-API-Key: nvsk_YOUR_KEY" \
  "https://YOUR-URL/api/v1/search?q=python&site=wikipedia.org"

# چک کردن سهمیه
curl -H "X-API-Key: nvsk_YOUR_KEY" "https://YOUR-URL/api/v1/usage"
```

```python
import httpx
r = httpx.get("https://YOUR-URL/api/v1/search",
              params={"q": "AI", "lang": "fa"},
              headers={"X-API-Key": "nvsk_YOUR_KEY"})
print(r.json()["results"])
```

| پارامتر | نوع | توضیح |
|---|---|---|
| `q` | string * | عبارت جست‌وجو (الزامی) |
| `lang` | string | زبان نتایج: `fa`، `en`، `all`، `auto` |
| `site` | string | محدود به یک دامنه |
| `count` | int | تعداد نتایج (۱ تا ۵۰) |

**پاسخ:** `results[]` با `title`، `url`، `snippet`، `engine` + آبجکت `usage` (مصرف امروز/باقی‌مانده).

مستندات تعاملی Swagger هم همیشه روشنه: **`/docs`**

### 👑 پنل اونر

با `OWNER_USERNAME` / `OWNER_PASSWORD` لاگین کن → پنل مدیریت باز میشه: لیست کاربران با مصرف امروز و کل، دکمه تعلیق/فعال‌سازی، تغییر سهمیه هر کاربر، آمار کلی سرویس.

### 💻 اجرای لوکال (بدون گیت‌هاب)

```bash
pip install -r requirements.txt
docker run -d -p 8888:8080 -v $PWD/searxng:/etc/searxng:ro searxng/searxng:latest
cp .env.example .env   # مقدارها رو پر کن
python run.py          # http://localhost:8000
```

### 🗂️ ساختار پروژه

```
novaseek/
├── .github/workflows/deploy.yml   # دیپلوی + لوپ ۶ ساعته + بکاپ
├── app/
│   ├── main.py                    # FastAPI app + ساخت خودکار اکانت اونر
│   ├── config.py                  # تنظیمات از env/secrets
│   ├── database.py                # SQLite async + WAL
│   ├── models.py                  # User / APIKey / DailyUsage / UsageLog
│   ├── security.py                # PBKDF2 + JWT + تولید کلید nvsk_
│   ├── deps.py                    # احراز هویت JWT و API Key
│   ├── routers/                   # auth, keys, search, dashboard, admin
│   └── services/                  # موتور جست‌وجو + سهمیه روزانه
├── searxng/settings.yml           # کانفیگ SearXNG (JSON فعال، limiter خاموش)
├── static/                        # UI دوزبانه دارک/لایت (SPA)
├── run.py · requirements.txt · LICENSE (MIT)
```

### ⚡ نکات پرفورمنس (ساپورت ۱۰۰۰+ کاربر)

- SQLite با **WAL + busy_timeout** → خواندن/نوشتن هم‌زمان امن
- **TTLCache** حافظه‌ای → کوئری تکراری بدون هزینه موتور
- **GZip** روی پاسخ‌ها، اتصال HTTP keep-alive به موتور
- حسابداری سهمیه با **یک رکورد per user/day** → کوئری O(1)
- محدودیت ۱۰ کلید per کاربر → جلوگیری از سوءاستفاده

---

## 🇬🇧 English Guide

### What is NovaSeek?

NovaSeek is a **production-ready Search API service** that deploys for **free on GitHub Actions**:

- 🔍 **Local SearXNG metasearch engine** — no Google keys, no CAPTCHAs, no engine-side rate limits (70+ engines). Automatic **DuckDuckGo fallback** if SearXNG is still warming up.
- 🔑 **Real API-key system** — each user creates up to 10 `nvsk_...` keys, copies and revokes them, with per-key usage stats.
- 📊 **Daily quota** — 1,000 requests/user/day, auto-renewed at 00:00 UTC.
- 👑 **Owner panel** — list all users, see today's/total usage, suspend/activate, edit quotas.
- 🌗 **Bilingual UI (Persian RTL / English)** with **dark/light themes**, persisted in localStorage.
- 🔁 **6-hour keepalive loop** — before GitHub's job timeout, the SQLite DB is backed up to a Release and the next run is triggered via `GH_PAT`; **all users, keys and usage survive restarts**.
- 🌐 **Cloudflare quick tunnel** (`trycloudflare.com`) — no Cloudflare account needed; the public URL is printed in the run Summary.
- 💾 **Local SQLite (WAL mode)** + in-memory TTL cache + GZip — built to serve 1,000+ concurrent users.

### 🚀 Setup (5 minutes)

1. **Push this repo** to GitHub.
2. **Set secrets** (Settings → Secrets → Actions):

   | Secret | Purpose |
   |---|---|
   | `APP_SECRET_KEY` | JWT signing key (`openssl rand -hex 32`) |
   | `OWNER_USERNAME` | Owner account username |
   | `OWNER_PASSWORD` | Owner account password |
   | `GH_PAT` | PAT with `repo` + `workflow` scope for the 6h loop |

3. **Run the workflow**: Actions → *NovaSeek Deploy & Keepalive* → Run workflow.
4. The run Summary shows **🚀 NovaSeek is LIVE** with your public URL. Every ~5h50m the DB is backed up to Releases and a fresh run starts automatically with all data intact.

### 📡 API quick start

```bash
curl -H "X-API-Key: nvsk_YOUR_KEY" \
  "https://YOUR-URL/api/v1/search?q=openai&lang=en&count=10"
```

Params: `q` (required), `lang` (`fa`/`en`/`all`/`auto`), `site` (restrict to a domain), `count` (1–50).
Interactive docs at **`/docs`**. Quota check: `GET /api/v1/usage` with the same key.

### 💻 Run locally

```bash
pip install -r requirements.txt
docker run -d -p 8888:8080 -v $PWD/searxng:/etc/searxng:ro searxng/searxng:latest
cp .env.example .env
python run.py   # http://localhost:8000
```

### 📄 License

MIT — see [LICENSE](LICENSE) for the full third-party attribution list (SearXNG is AGPL-3.0, Vazirmatn font OFL-1.1, cloudflared Apache-2.0, the rest MIT/BSD).
