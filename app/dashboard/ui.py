from fastapi import APIRouter
from fastapi.responses import HTMLResponse

ui_router = APIRouter()

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="ARPI">
<meta name="theme-color" content="#0A0E1A">
<title>ARPI — دستیار هوشمند بازار</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#0A0E1A;
    --surface:#121729;
    --surface-2:#1A2036;
    --border:#232A44;
    --gold:#E8B54D;
    --gold-dim:#8A6B2E;
    --text:#F2F0EA;
    --muted:#8B93A7;
    --buy:#4ADE80;
    --sell:#F16565;
    --hold:#8B93A7;
    --risk-low:#4ADE80;
    --risk-medium:#E8B54D;
    --risk-high:#F0954A;
    --risk-critical:#F16565;
  }

  *{box-sizing:border-box; margin:0; padding:0;}

  body{
    background:
      radial-gradient(ellipse 800px 500px at 50% -10%, rgba(232,181,77,0.08), transparent),
      var(--bg);
    color:var(--text);
    font-family:'Vazirmatn', sans-serif;
    min-height:100vh;
    padding-bottom:48px;
    -webkit-font-smoothing:antialiased;
  }

  .mono{ font-family:'JetBrains Mono', monospace; direction:ltr; unicode-bidi:isolate; }

  header{
    position:sticky; top:0; z-index:20;
    backdrop-filter:blur(14px);
    background:rgba(10,14,26,0.85);
    border-bottom:1px solid var(--border);
    padding:14px 20px;
    display:flex; align-items:center; justify-content:space-between;
  }

  .brand{ display:flex; align-items:center; gap:10px; }
  .brand-mark{
    width:30px; height:30px; border-radius:8px;
    background:linear-gradient(135deg, var(--gold), #B8863A);
    display:flex; align-items:center; justify-content:center;
    font-weight:800; color:#0A0E1A; font-size:15px;
  }
  .brand-name{ font-weight:700; font-size:16px; letter-spacing:0.3px; }
  .brand-sub{ font-size:10.5px; color:var(--muted); margin-top:1px; }

  .live-dot{
    width:7px; height:7px; border-radius:50%; background:var(--buy);
    box-shadow:0 0 0 0 rgba(74,222,128,0.6);
    animation:pulse 2s infinite;
  }
  @keyframes pulse{
    0%{ box-shadow:0 0 0 0 rgba(74,222,128,0.55); }
    70%{ box-shadow:0 0 0 8px rgba(74,222,128,0); }
    100%{ box-shadow:0 0 0 0 rgba(74,222,128,0); }
  }
  .status-chip{
    display:flex; align-items:center; gap:6px;
    font-size:11px; color:var(--muted);
    padding:6px 10px; border:1px solid var(--border); border-radius:100px;
    cursor:pointer; background:var(--surface);
  }

  main{ max-width:720px; margin:0 auto; padding:20px 16px 0; }

  /* ---- Setup panel ---- */
  #setup{
    background:var(--surface); border:1px solid var(--border); border-radius:16px;
    padding:18px; margin-bottom:20px;
  }
  #setup label{ font-size:12px; color:var(--muted); display:block; margin-bottom:8px; }
  #setup .row{ display:flex; gap:8px; }
  #setup input{
    flex:1; background:var(--surface-2); border:1px solid var(--border); color:var(--text);
    border-radius:10px; padding:11px 12px; font-size:13px; font-family:'JetBrains Mono',monospace;
    direction:ltr; text-align:left;
  }
  #setup input::placeholder{ color:#555c73; }
  #setup button, .refresh-btn{
    background:var(--gold); color:#171208; border:none; border-radius:10px;
    padding:0 18px; font-weight:700; font-size:13px; cursor:pointer;
    font-family:'Vazirmatn',sans-serif;
  }
  #setup .hint{ font-size:11px; color:var(--muted); margin-top:10px; line-height:1.9; }

  /* ---- Hero score ---- */
  #hero{
    background:linear-gradient(160deg, var(--surface), var(--surface-2));
    border:1px solid var(--border); border-radius:20px;
    padding:26px 22px; margin-bottom:20px;
    display:flex; align-items:center; justify-content:space-between; gap:16px;
    position:relative; overflow:hidden;
  }
  #hero::before{
    content:''; position:absolute; inset:0;
    background:radial-gradient(circle at 100% 0%, rgba(232,181,77,0.10), transparent 55%);
  }
  #hero .info{ position:relative; z-index:1; }
  #hero .eyebrow{ font-size:11px; color:var(--gold); letter-spacing:1px; font-weight:600; margin-bottom:8px;}
  #hero .rec{ font-size:22px; font-weight:800; margin-bottom:4px; }
  #hero .sub{ font-size:12px; color:var(--muted); }
  .gauge-wrap{ position:relative; width:104px; height:104px; flex-shrink:0; z-index:1; }
  .gauge-wrap svg{ transform:rotate(-90deg); }
  .gauge-bg{ fill:none; stroke:var(--border); stroke-width:8; }
  .gauge-fg{ fill:none; stroke:var(--gold); stroke-width:8; stroke-linecap:round; transition:stroke-dashoffset 1s ease; }
  .gauge-label{
    position:absolute; inset:0; display:flex; flex-direction:column;
    align-items:center; justify-content:center;
  }
  .gauge-label .val{ font-size:22px; font-weight:700; font-family:'JetBrains Mono',monospace; }
  .gauge-label .pct{ font-size:10px; color:var(--muted); margin-top:-2px; }

  /* ---- Risk summary strip ---- */
  #risk-strip{
    display:flex; gap:8px; margin-bottom:22px; overflow-x:auto;
  }
  .risk-pill{
    flex:1; min-width:74px; text-align:center; padding:10px 6px;
    background:var(--surface); border:1px solid var(--border); border-radius:12px;
  }
  .risk-pill .n{ font-size:18px; font-weight:800; font-family:'JetBrains Mono',monospace; }
  .risk-pill .l{ font-size:10px; color:var(--muted); margin-top:2px; }

  /* ---- Asset cards ---- */
  #assets{ display:flex; flex-direction:column; gap:12px; }
  .card{
    background:var(--surface); border:1px solid var(--border); border-radius:16px;
    padding:16px; cursor:pointer; transition:border-color .15s;
  }
  .card:active{ border-color:var(--gold-dim); }
  .card-top{ display:flex; align-items:center; justify-content:space-between; }
  .asset-name{ font-weight:700; font-size:15px; text-transform:capitalize; }
  .asset-badges{ display:flex; align-items:center; gap:8px; }

  .signal-badge{
    font-size:11px; font-weight:800; padding:5px 12px; border-radius:100px;
    font-family:'JetBrains Mono',monospace; letter-spacing:0.5px;
  }
  .signal-BUY{ background:rgba(74,222,128,0.14); color:var(--buy); }
  .signal-SELL{ background:rgba(241,101,101,0.14); color:var(--sell); }
  .signal-HOLD, .signal-WAIT{ background:rgba(139,147,167,0.14); color:var(--hold); }
  .signal-NO_DATA{ background:rgba(139,147,167,0.1); color:var(--muted); }

  .card-mid{ display:flex; align-items:center; gap:10px; margin-top:12px; }
  .conf-track{
    flex:1; height:6px; background:var(--surface-2); border-radius:100px; overflow:hidden;
  }
  .conf-fill{ height:100%; background:linear-gradient(90deg, var(--gold-dim), var(--gold)); border-radius:100px; transition:width .8s ease; }
  .conf-num{ font-size:12px; font-family:'JetBrains Mono',monospace; color:var(--muted); min-width:34px; text-align:left; }

  .risk-tag{
    font-size:10px; font-weight:700; padding:3px 9px; border-radius:6px; margin-top:10px; display:inline-block;
  }
  .risk-LOW{ background:rgba(74,222,128,0.12); color:var(--risk-low); }
  .risk-MEDIUM{ background:rgba(232,181,77,0.14); color:var(--risk-medium); }
  .risk-HIGH{ background:rgba(240,149,74,0.14); color:var(--risk-high); }
  .risk-CRITICAL{ background:rgba(241,101,101,0.16); color:var(--risk-critical); }

  .reasons{
    margin-top:12px; padding-top:12px; border-top:1px solid var(--border);
    display:none; flex-direction:column; gap:6px;
  }
  .card.open .reasons{ display:flex; }
  .reasons li{
    list-style:none; font-size:12.5px; color:var(--muted); line-height:1.7;
    display:flex; gap:7px; align-items:flex-start;
  }
  .reasons li::before{ content:'—'; color:var(--gold-dim); flex-shrink:0; }
  .no-reason{ font-size:12px; color:var(--muted); font-style:italic; }

  #empty, #err{
    text-align:center; padding:60px 20px; color:var(--muted); font-size:13px; line-height:2;
  }
  #err{ color:var(--sell); display:none; }
  #loading{ text-align:center; padding:60px 20px; color:var(--muted); font-size:13px; display:none; }

  .footer-note{
    text-align:center; font-size:10.5px; color:#4B5268; margin-top:28px; line-height:1.9;
  }

  @media (min-width:640px){
    #assets{ display:grid; grid-template-columns:1fr 1fr; }
  }
</style>
</head>
<body>

<header>
  <div class="brand">
    <div class="brand-mark">A</div>
    <div>
      <div class="brand-name">ARPI</div>
      <div class="brand-sub">دستیار هوشمند بازار</div>
    </div>
  </div>
  <div class="status-chip" id="statusChip" onclick="toggleSetup()">
    <span class="live-dot" id="liveDot"></span>
    <span id="statusText">تنظیمات</span>
  </div>
</header>

<main>

  <div id="setup" style="display:none">
    <label>آدرس API (فقط اگر داشبورد را جدا از سرور باز کرده‌اید)</label>
    <div class="row">
      <input id="apiUrl" type="text" placeholder="https://xxxx-8000.app.github.dev" />
      <button onclick="saveAndLoad()">اتصال</button>
    </div>
    <div class="hint">
      چون این صفحه از همان سرور ARPI سرو می‌شود، معمولاً نیازی به این تنظیم نیست.
    </div>
  </div>

  <div id="hero" style="display:none">
    <div class="info">
      <div class="eyebrow">وضعیت کلی بازار</div>
      <div class="rec" id="heroRec">—</div>
      <div class="sub" id="heroSub">در حال بارگذاری…</div>
    </div>
    <div class="gauge-wrap">
      <svg width="104" height="104">
        <circle class="gauge-bg" cx="52" cy="52" r="44"></circle>
        <circle class="gauge-fg" id="heroGaugeFg" cx="52" cy="52" r="44" stroke-dasharray="276" stroke-dashoffset="276"></circle>
      </svg>
      <div class="gauge-label">
        <div class="val mono" id="heroScoreVal">—</div>
        <div class="pct">اطمینان</div>
      </div>
    </div>
  </div>

  <div id="risk-strip" style="display:none"></div>

  <div id="loading">در حال دریافت اطلاعات بازار…</div>
  <div id="err"></div>
  <div id="empty">آدرس API را وارد کن و «اتصال» را بزن تا تحلیل زنده‌ی بازار نمایش داده شود.</div>

  <div id="assets"></div>

  <div class="footer-note">ARPI Enterprise · تحلیل خودکار — نه توصیه‌ی قطعی سرمایه‌گذاری</div>
</main>

<script>
const RISK_FA = {LOW:'کم', MEDIUM:'متوسط', HIGH:'بالا', CRITICAL:'بحرانی'};
const SIGNAL_FA = {BUY:'خرید', SELL:'فروش', HOLD:'نگه‌داری', WAIT:'صبر', NO_DATA:'بدون داده'};

function toggleSetup(){
  const el = document.getElementById('setup');
  el.style.display = el.style.display === 'none' ? 'block' : 'none';
}

function saveAndLoad(){
  const url = document.getElementById('apiUrl').value.trim().replace(/\/$/, '');
  if(!url) return;
  localStorage.setItem('arpi_api_url', url);
  document.getElementById('setup').style.display = 'none';
  load();
}

function circleOffset(pct, r=44){
  const c = 2 * Math.PI * r;
  return c - (pct/100) * c;
}

async function load(){
  // اگر آدرس دستی ذخیره نشده باشد، از همین سرور (مسیر نسبی) استفاده می‌شود
  const base = localStorage.getItem('arpi_api_url') || '';

  const loading = document.getElementById('loading');
  const err = document.getElementById('err');
  const empty = document.getElementById('empty');
  const hero = document.getElementById('hero');
  const riskStrip = document.getElementById('risk-strip');

  empty.style.display = 'none';
  err.style.display = 'none';
  loading.style.display = 'block';

  try{
    const res = await fetch(base + '/dashboard/summary');
    if(!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();

    loading.style.display = 'none';
    hero.style.display = 'flex';
    riskStrip.style.display = 'flex';
    document.getElementById('statusText').textContent = 'متصل';

    const score = data?.arpi_score?.value ?? 0;
    document.getElementById('heroScoreVal').textContent = score;
    document.getElementById('heroGaugeFg').style.strokeDashoffset = circleOffset(score);

    const rec = data?.decision_summary?.recommendation ?? 'HOLD';
    document.getElementById('heroRec').textContent = SIGNAL_FA[rec] || rec;
    document.getElementById('heroSub').textContent =
      (data?.assets?.total ?? 0) + ' دارایی تحلیل شد · آخرین به‌روزرسانی همین الان';

    const rs = data?.risk_intelligence?.risk_summary || {};
    riskStrip.innerHTML = ['LOW','MEDIUM','HIGH','CRITICAL'].map(k =>
      `<div class="risk-pill">
         <div class="n" style="color:var(--risk-${k.toLowerCase()})">${rs[k] ?? 0}</div>
         <div class="l">${RISK_FA[k]}</div>
       </div>`
    ).join('');

    const assets = data?.assets?.analyzed || [];
    const assetsEl = document.getElementById('assets');

    if(assets.length === 0){
      assetsEl.innerHTML = '';
      empty.style.display = 'block';
      empty.textContent = 'داده‌ای برای نمایش موجود نیست.';
    } else {
      assetsEl.innerHTML = assets.map((a, i) => {
        const conf = Math.round(a.confidence ?? 0);
        const signal = a.signal || 'NO_DATA';
        const risk = a.risk_level || a.risk || 'MEDIUM';
        const reasons = a.reasoning || [];
        return `
        <div class="card" onclick="this.classList.toggle('open')">
          <div class="card-top">
            <div class="asset-name">${a.asset}</div>
            <div class="asset-badges">
              <span class="signal-badge signal-${signal}">${SIGNAL_FA[signal] || signal}</span>
            </div>
          </div>
          <div class="card-mid">
            <div class="conf-track"><div class="conf-fill" style="width:${conf}%"></div></div>
            <div class="conf-num mono">${conf}%</div>
          </div>
          <span class="risk-tag risk-${risk}">ریسک: ${RISK_FA[risk] || risk}</span>
          <ul class="reasons">
            ${reasons.length ? reasons.map(r => `<li>${r}</li>`).join('') : '<li class="no-reason">دلیل خاصی ثبت نشده</li>'}
          </ul>
        </div>`;
      }).join('');
    }

  } catch(e){
    loading.style.display = 'none';
    hero.style.display = 'none';
    riskStrip.style.display = 'none';
    err.style.display = 'block';
    err.textContent = 'اتصال به API برقرار نشد. آدرس را چک کن، یا مطمئن شو سرور (run_local.py) روشن است. جزئیات خطا: ' + e.message;
    document.getElementById('statusText').textContent = 'قطع';
  }
}

window.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('arpi_api_url');
  if(saved){ document.getElementById('apiUrl').value = saved; }
  load();
});
</script>
</body>
</html>
"""


@ui_router.get("/ui", response_class=HTMLResponse)
def dashboard_ui():
    return DASHBOARD_HTML
