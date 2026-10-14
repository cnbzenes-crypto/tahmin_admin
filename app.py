from flask import Flask, jsonify, request
from collections import Counter, defaultdict
import json, os, re
from datetime import datetime

VERI = "veri.json"
TAHMIN_DOSYA = "tahminler.json"

VERILER = {
1:[34,36,39,45,53,55],2:[20,21,23,26,32,37],3:[6,9,25,29,45,57],
4:[3,7,12,22,23,55],5:[3,8,10,12,32,42],6:[7,19,23,32,48,55],
7:[1,22,27,41,44,46],8:[9,24,25,33,44,52],9:[6,26,32,43,48,54],
10:[1,2,36,42,49,55],11:[12,20,23,38,49,50],12:[1,7,16,34,38,42],
13:[1,4,7,8,11,41],14:[7,17,21,25,32,52],15:[21,33,43,47,55,59],
16:[14,24,34,42,51,60],17:[8,18,21,29,36,38],18:[9,29,36,46,47,52],
19:[3,5,10,22,23,52],20:[9,16,31,34,40,58],21:[2,14,31,38,47,54],
22:[6,8,43,49,58,60],23:[14,16,30,42,46,55],24:[6,19,31,39,47,51],
25:[3,19,26,37,44,57],26:[3,14,27,32,43,44],27:[17,18,21,27,37,51],
28:[3,11,16,25,37,41],29:[11,41,43,44,51,57],30:[7,9,14,36,52,55],
31:[3,22,38,41,44,50],32:[5,12,21,28,35,42],33:[1,6,7,19,31,44],
34:[18,21,34,43,47,50],35:[8,9,20,30,33,55],36:[7,9,20,22,28,39],
37:[7,14,17,25,42,49],38:[1,17,28,30,32,42],39:[2,16,35,51,52,56],
40:[6,11,22,36,37,53],41:[1,3,14,19,48,56],42:[10,29,36,42,46,52],
43:[6,18,33,40,50,58],44:[11,19,23,27,28,39],45:[13,19,21,30,42,43],
46:[15,20,29,51,56,57],47:[1,11,26,49,55,59],48:[8,31,35,36,49,55],
49:[9,26,30,39,41,45],50:[6,36,38,44,49,53],51:[2,14,22,34,48,59],
52:[25,35,39,41,54,56],53:[1,13,19,27,42,56],54:[14,20,31,35,38,39],
55:[1,11,20,33,35,47],56:[1,8,31,38,40,56],57:[2,19,28,30,31,37],
58:[13,18,35,45,46,50],59:[4,9,11,19,24,26],60:[3,23,27,47,50,53],
61:[7,21,23,25,37,51],62:[19,22,28,30,44,46],63:[9,17,38,47,54,58],
64:[12,21,23,45,49,55],65:[2,4,13,16,48,58],66:[15,18,20,31,43,56],
67:[4,6,7,10,20,28],68:[2,8,21,24,36,47],69:[10,11,35,38,41,57],
70:[15,19,30,38,57,60],71:[3,26,27,32,44,46],72:[8,14,23,32,58,60],
73:[3,27,29,33,34,58],74:[5,6,24,37,43,48],75:[4,29,30,31,37,39],
76:[5,11,31,46,51,56],77:[3,6,12,14,23,47],78:[6,8,15,18,19,29],
79:[6,32,37,38,40,57],80:[40,41,46,52,57,60],81:[4,26,30,38,51,53],
82:[3,16,35,44,50,57],83:[14,15,20,30,36,44],84:[7,8,13,27,37,55],
85:[6,26,30,33,38,46],86:[11,32,33,47,53,59],87:[2,13,30,52,58,60],
88:[2,11,43,47,48,58],89:[6,9,22,27,41,46],90:[3,6,24,50,51,53],
91:[1,25,28,41,55,56],92:[1,4,7,16,30,60],93:[16,23,24,42,46,57],
94:[24,27,38,41,49,50],95:[10,27,31,32,39,54],96:[7,16,22,39,40,60],
97:[18,24,32,34,52,60],98:[8,20,38,45,49,50],99:[16,28,45,49,52,54],
100:[8,21,25,46,48,57],101:[13,25,26,34,35,38],102:[13,19,29,31,34,53],
103:[15,26,27,41,49,52],104:[6,16,25,30,33,46],105:[28,30,40,42,47,59],
106:[3,15,20,23,30,60],107:[27,30,31,41,43,57],108:[2,12,37,52,59,60],
109:[17,28,31,44,48,53],110:[7,23,42,45,47,59],111:[2,23,33,43,44,47],
112:[10,16,30,38,50,59],113:[14,16,43,54,55,56],114:[3,15,43,48,50,52],
115:[3,6,17,18,20,39],116:[16,26,44,46,57,59],117:[2,25,42,45,53,54],
118:[14,15,34,38,50,56],119:[9,17,31,34,51,55],120:[7,14,20,43,46,56],
121:[11,16,21,36,39,58],122:[16,18,22,31,37,55],123:[18,45,54,56,57,60]}


def yukle():
    if os.path.exists(VERI):
        try:
            return {int(k): v for k, v in json.load(open(VERI, encoding="utf-8")).items()}
        except Exception:
            pass
    json.dump({str(k): v for k, v in VERILER.items()}, open(VERI, "w", encoding="utf-8"))
    return dict(VERILER)


def kaydet():
    json.dump({str(k): veri[k] for k in sorted(veri)}, open(VERI, "w", encoding="utf-8"))


def th_yukle():
    if os.path.exists(TAHMIN_DOSYA):
        try:
            return json.load(open(TAHMIN_DOSYA, encoding="utf-8"))
        except Exception:
            pass
    return {"kayitli": [], "karsilastirma": []}


def th_kaydet():
    json.dump(tahminler, open(TAHMIN_DOSYA, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


veri = yukle()
tahminler = th_yukle()


def frekans(v, bas=None, son=None):
    c = Counter()
    for k in sorted(v):
        if (bas is None or k >= bas) and (son is None or k <= son):
            c.update(v[k])
    return c


def siniflandir(f):
    ort = sum(f.values()) / 60 if f else 1
    sicak = sorted([s for s in range(1, 61) if f.get(s, 0) >= ort * 1.15], key=lambda x: -f.get(x, 0))
    soguk = sorted([s for s in range(1, 61) if f.get(s, 0) <= ort * 0.85], key=lambda x: f.get(x, 0))
    ilimli = [s for s in range(1, 61) if s not in sicak and s not in soguk]
    return sicak, ilimli, soguk


def skor_hesapla(v):
    if not v:
        return {s: 0 for s in range(1, 61)}, Counter(), Counter(), {s: 0 for s in range(1, 61)}, [], []
    keys = sorted(v)
    f = frekans(v)
    son10 = frekans(v, son=keys[-10] if len(keys) >= 10 else keys[0])
    son30 = frekans(v, son=keys[-30] if len(keys) >= 30 else keys[0])
    son = v[keys[-1]]
    onceki = v[keys[-2]] if len(keys) >= 2 else []
    ort = sum(f.values()) / 60 if f else 1
    trend = {s: son30.get(s, 0) - ort * (30 / max(len(v), 1)) for s in range(1, 61)}
    mf = max(f.values()) if f else 1
    mf10 = max(son10.values()) if son10 else 1
    skor = {}
    for s in range(1, 61):
        a = f.get(s, 0) / mf
        b = son10.get(s, 0) / mf10
        c = max(0, min(1, (trend[s] + 3) / 6))
        ceza = (0.15 if s in son else 0) + (0.10 if s in onceki else 0)
        skor[s] = max(0, 0.4 * a + 0.3 * b + 0.3 * c - ceza)
    return skor, f, son10, trend, son, onceki


def markov_skor(v):
    cift = Counter()
    for sayilar in v.values():
        for a in sayilar:
            for b in sayilar:
                if a != b:
                    cift[(a, b)] += 1
    return cift


def kolon_uret():
    sk6or, f, son:
10, trend, son           , onceki = skor_hesapla(veri)
    sicak, ilimli, soguk = siniflandir(f)
    siral = sorted(skor, key=skor.get, reverse=True)
    tr = sorted(trend, key=lambda x: -trend[x])
    s10 = sorted(son10, key=lambda x: -son10[x])

    kolonlar = []
    kolonlar.append(("En yuksek skor", siral[:6]))
    kolonlar.append(("Sicak + trend", list(dict.fromkeys(sicak[:4] + tr[:4]))[:6]))
    kolonlar.append(("Soguk-denge", list(dict.fromkeys(soguk[:3] + sicak[:3]))[:6]))
    kolonlar.append(("Ilimli-orta", list(dict.fromkeys(ilimli[:4] + sicak[:2]))[:6]))
    kolonlar.append(("Son 10 formu", s10[:6]))

    # Markov - son cekilis sayilari SIRALI okunur (deterministik)
    cift = markov_skor(veri)
    mskor = Counter()
    for a in sorted(son):  # <-- sorted() eklendi
        for b in range(1, 61):
            if a != b:
                mskor[b] += cift.get((a, b), 0)
    markov_siral = sorted(mskor, key=lambda x: (-mskor[x], x))  # skor, sonra sayi
    kolonlar.append(("Markov gecis", markov_siral[:6]))

    # K7 (rastgele) KALDIRILDI

    sonuc = []
    for et, k in kolonlar:
        k = list(k)
        while len(k) k.append(next(s for s in siral if s not in k))
        k = sorted(list(set(k))[:6])
        tek = sum(1 for x in k if x % 2 == 1)
        cls = ["sicak" if x in sicak else ("soguk" if x in soguk else "ilimli") for x in k]
        sonuc.append({"e": et, "s": k, "t": sum(k), "tk": tek, "cf": 6 - tek, "c": cls})
    return sonuc


def backtest(n=50):
    keys = sorted(veri.keys())
    test = keys[-n:] if len(keys) >= n else keys
    detay = []
    toplam = 0
    sayi = 0
    for tn in test:
        gecmis = {k: veri[k] for k in keys if k < tn}
        if len(gecmis) < 10:
            continue
        skor, _, _, _, _, _ = skor_hesapla(gecmis)
        siral = sorted(skor, key=skor.get, reverse=True)
        tah = set(siral[:6])
        ger = set(veri[tn])
        tut = len(tah & ger)
        toplam += tut
        sayi += 1
        detay.append({"no": tn, "tahmin": sorted(tah), "gercek": sorted(ger), "tutan": tut})
    return {
        "detay": detay[-20:],
        "ortalama": round(toplam / sayi, 2) if sayi else 0,
        "test": sayi,
        "toplam_tutulan": toplam
    }


HTML = r"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="UTF-8"><title>Loto v5</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Segoe UI,Arial,sans-serif;background:#1e1e2e;color:#eee;padding:16px}
.c{max-width:1100px;margin:auto}
h1{color:#f5c542;text-align:center;margin-bottom:12px;font-size:22px}
.hdr{text-align:center;margin-bottom:16px}
.b{background:#2a2a3e;padding:6px 14px;border-radius:20px;display:inline-block;margin:3px;font-size:12px}
.tabs{display:flex;gap:4px;flex-wrap:wrap;justify-content:center;margin-bottom:16px}
.tab{padding:8px 16px;background:#2a2a3e;border:none;color:#eee;border-radius:8px;cursor:pointer;font-size:13px;font-weight:600}
.tab.on{background:#f5c542;color:#1e1e2e}
.pnl{display:none;background:#2a2a3e;padding:18px;border-radius:12px;margin-bottom:14px}
.pnl.on{display:block}
.card{background:#2a2a3e;padding:14px;border-radius:10px;margin:8px 0;display:flex;align-items:center;gap:10px;flex-wrap:wrap;border-left:4px solid #f5c542}
.top{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;color:#1e1e2e}
.sicak{background:#f5c542}.soguk{background:#5dade2;color:#fff}.ilimli{background:#95a5a6}
.meta{margin-left:auto;font-size:11px;color:#a0a0c0;text-align:right}
button.bp{background:#f5c542;color:#1e1e2e;padding:10px 18px;border:none;border-radius:8px;font-weight:700;cursor:pointer;margin:3px;font-size:13px}
button.bg{background:#2ecc71;color:#fff;padding:10px 18px;border:none;border-radius:8px;font-weight:700;cursor:pointer;margin:3px;font-size:13px}
button.bi{background:#3498db;color:#fff;padding:10px 18px;border:none;border-radius:8px;font-weight:700;cursor:pointer;margin:3px;font-size:13px}
button.bu{background:#9b59b6;color:#fff;padding:10px 18px;border:none;border-radius:8px;font-weight:700;cursor:pointer;margin:3px;font-size:13px}
input,textarea{width:100%;padding:10px;background:#1e1e2e;color:#eee;border:1px solid #3a3a4e;border-radius:8px;font-family:Consolas,monospace;margin-bottom:8px;font-size:13px}
h3{color:#f5c542;margin-bottom:10px;font-size:15px}
table{width:100%;border-collapse:collapse;font-size:12px}
th,td{padding:6px;border-bottom:1px solid #3a3a4e;text-align:left}
th{color:#f5c542}
.stat{display:inline-block;background:#1e1e2e;padding:10px 16px;border-radius:8px;margin:4px;font-size:13px}
.stat b{color:#f5c542;font-size:18px;display:block}
.chart-box{background:#1e1e2e;padding:12px;border-radius:10px;height:340px}
</style></head><body><div class="c">
<h1>🎯 Loto Tahmin v5</h1>
<div class="hdr"><span class="b" id="st">...</span></div>
<div class="tabs">
<button class="tab on" onclick="go('t')">Tahmin</button>
<button class="tab" onclick="go('g')">Grafik</button>
<button class="tab" onclick="go('s')">Simulasyon</button>
<button class="tab" onclick="go('k')">Kayitli</button>
<button class="tab" onclick="go('e')">Ekle</button>
<button class="tab" onclick="go('tp')">Toplu</button>
<button class="tab" onclick="go('y')">Yonet</button>
</div>

<div id="p-t" class="pnl on">
<h3>Tahmin Kolonlari</h3>
<button class="bp" onclick="tahmin()">🎲 6 STRATEJI URET</button>
<button class="bi" onclick="window.print()">📄 PDF</button>
<div id="kl"></div>
</div>

<div id="p-g" class="pnl">
<h3>Sayi Frekans Grafigi</h3>
<div class="chart-box"><canvas id="grf"></canvas></div>
<h3 style="margin-top:16px">Trend (Son 30 vs Genel)</h3>
<div class="chart-box"><canvas id="trf"></canvas></div>
</div>

<div id="p-s" class="pnl">
<h3>Simulasyon (Backtest)</h3>
<p style="color:#a0a0c0;font-size:12px;margin-bottom:10px">Model gecmise gore test edilir - son N cekiliste dogruluk olculur.</p>
<button class="bp" onclick="backtest(30)">Son 30</button>
<button class="bp" onclick="backtest(50)">Son 50</button>
<button class="bp" onclick="backtest(100)">Son 100</button>
<div id="bt-sonuc"></div>
</div>

<div id="p-k" class="pnl">
<h3>Kayitli Tahminler ve Karsilastirma</h3>
<button class="bi" onclick="kayitlariGoster()">🔄 Yenile</button>
<button class="bg" onclick="tahminiKaydet()">💾 Su An Tahmin Et ve Kaydet</button>
<div id="kayit-list"></div>
</div>

<div id="p-e" class="pnl">
<h3>Yeni Cekilis Ekle</h3>
<input id="en" type="number" placeholder="124">
<input id="es" placeholder="5 12 24 29 48 55">
<button class="bg" onclick="ekle()">KAYDET</button>
</div>

<div id="p-tp" class="pnl">
<h3>Toplu Ekle - Yapistir</h3>
<p style="color:#a0a0c0;font-size:12px;margin-bottom:8px">Her satir: &lt;no&gt; &lt;s1&gt;...&lt;s6&gt; (no bos ise otomatik) - Millipiyango sitesinden kopyalayip yapistirin, otomatik ayristirilir.</p>
<textarea id="tm" rows="8" placeholder="124 5 12 24 29 48 55&#10;125 3 18 27 33 41 57"></textarea>
<button class="bg" onclick="toplu()">KAYDET</button>
</div>

<div id="p-y" class="pnl">
<h3>Yonet - Tum Cekilisler</h3>
<input id="ya" placeholder="Ara (no)..." oninput="yliste()">
<div id="yliste"></div>
</div>

</div>
<script>
let grf=null, trf=null;
async function dst(){let r=await fetch('/api/d'),d=await r.json();
document.getElementById('st').textContent=d.t+' cekilis, Son #'+d.s;
document.getElementById('en').placeholder=d.s+1;}
function go(id){document.querySelectorAll('.pnl').forEach(p=>p.classList.remove('on'));
document.querySelectorAll('.tab').forEach(t=>t.classList.remove('on'));
document.getElementById('p-'+id).classList.add('on');
event.target.classList.add('on');
if(id==='g')grafik();if(id==='k')kayitlariGoster();if(id==='y')yliste();if(id==='e')dst();}
async function tahmin(){let r=await fetch('/api/t'),ks=await r.json();
let d=document.getElementById('kl');d.innerHTML='';
let c=['#e74c3c','#f39c12','#3498db','#2ecc71','#9b59b6','#e67e22','#1abc9c'];
ks.forEach((k,i)=>{let e=document.createElement('div');e.className='card';
e.style.borderLeftColor=c[i];
let t='';k.s.forEach((s,j)=>{t+='<div class="top '+k.c[j]+'">'+String(s).padStart(2,'0')+'</div>';});
e.innerHTML='<b style="color:'+c[i]+'">K'+(i+1)+'</b><div style="display:flex;gap:5px;flex-wrap:wrap">'+t+'</div>'+
'<div class="meta">Top:'+k.t+' | '+k.tk+'T-'+k.cf+'C<br><i>'+k.e+'</i></div>';
d.appendChild(e);});}
async function grafik(){
let r=await fetch('/api/grafik'),d=await r.json();
if(grf)grf.destroy();
let ctx=document.getElementById('grf').getContext('2d');
let renk=d.sayilar.map(s=>s.sinif==='sicak'?'#f5c542':(s.sinif==='soguk'?'#5dade2':'#95a5a6'));
grf=new Chart(ctx,{type:'bar',data:{labels:d.sayilar.map(x=>x.s),
datasets:[{label:'Cikis sayisi',data:d.sayilar.map(x=>x.f),backgroundColor:renk}]},
options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#eee'}}},
scales:{x:{ticks:{color:'#a0a0c0'}},y:{ticks:{color:'#a0a0c0'}}}}});
if(trf)trf.destroy();
let ctx2=document.getElementById('trf').getContext('2d');
let renk2=d.trend.map(x=>x.t>0?'#2ecc71':'#e74c3c');
trf=new Chart(ctx2,{type:'bar',data:{labels:d.trend.map(x=>x.s),
datasets:[{label:'Trend',data:d.trend.map(x=>x.t.toFixed(2)),backgroundColor:renk2}]},
options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#eee'}}},
scales:{x:{ticks:{color:'#a0a0c0'}},y:{ticks:{color:'#a0a0c0'}}}}});
}
async function backtest(n){let r=await fetch('/api/backtest?n='+n),d=await r.json();
let h='<div style="margin:12px 0"><div class="stat"><b>'+d.ortalama+'</b>Ortalama tutan</div>'+
'<div class="stat"><b>'+d.test+'</b>Test sayisi</div>'+
'<div class="stat"><b>'+d.toplam_tutulan+'</b>Toplam tutan</div></div>';
h+='<table><tr><th>No</th><th>Tahmin</th><th>Gercek</th><th>Tutan</th></tr>';
d.detay.forEach(x=>{h+='<tr><td>#'+x.no+'</td><td style="color:#f5c542">'+x.tahmin.join(', ')+'</td>'+
'<td>'+x.gercek.join(', ')+'</td><td><b>'+x.tutan+'</b></td></tr>';});
h+='</table>';
document.getElementById('bt-sonuc').innerHTML=h;}
async function tahminiKaydet(){
let r=await fetch('/api/tahmin_kaydet',{method:'POST'});
let d=await r.json();
if(d.ok){bildirim('Tahmin kaydedildi!');kayitlariGoster();}
else alert(d.hata);}
async function kayitlariGoster(){let r=await fetch('/api/kayitli'),d=await r.json();
let h='<h4 style="color:#f5c542;margin:10px 0">Aktif tahminler (henuz sonuclanmamis)</h4>';
if(d.kayitli.length===0)h+='<p style="color:#a0a0c0">Yok</p>';
d.kayitli.forEach(x=>{h+='<div class="card"><b>'+x.tarih+'</b> → '+x.sayilar.join(', ')+'</div>';});
h+='<h4 style="color:#f5c542;margin:10px 0">Karsilastirmalar</h4>';
if(d.karsilastirma.length===0)h+='<p style="color:#a0a0c0">Henuz sonuclanmis tahmin yok</p>';
d.karsilastirma.slice().reverse().forEach(x=>{
h+='<div class="card"><b>'+x.tarih+'</b><br>Tahmin: '+x.tahmin.join(', ')+
'<br>Gercek: '+x.gercek.join(', ')+
'<br><span style="color:'+(x.tutan>=3?'#2ecc71':'#e74c3c')+'">Tutan: '+x.tutan+' sayi ('+(x.tutulan.length?x.tutulan.join(', '):'-')+')</span></div>';});
document.getElementById('kayit-list').innerHTML=h;}
async function ekle(){let n=+document.getElementById('en').value,s=document.getElementById('es').value;
let r=await fetch('/api/e',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({no:n,sayilar:s})});
let d=await r.json();
if(d.ok){bildirim('Cekilis #'+n+' eklendi');document.getElementById('es').value='';dst();kayitlariGoster();}
else alert(d.hata||d.mesaj);}
async function toplu(){let m=document.getElementById('tm').value;
let r=await fetch('/api/top',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({metin:m})});
let d=await r.json();alert(d.mesaj||d.hata);if(d.ok){document.getElementById('tm').value='';dst();}}
async function yliste(){let r=await fetch('/api/l'),d=await r.json();
let q=document.getElementById('ya').value.trim();
let div=document.getElementById('yliste');div.innerHTML='<table><tr><th>No</th><th>Sayilar</th><th>#</th></tr>';
d.liste.forEach(x=>{if(q&&!String(x.no).includes(q))return;
div.innerHTML+='<tr><td>#'+x.no+'</td><td>'+x.sayilar.join(', ')+'</td>'+
'<td><button class="bi" style="padding:3px 8px;font-size:11px" onclick="sil('+x.no+')">Sil</button></td></tr>';});
div.innerHTML+='</table>';}
async function sil(n){if(!confirm('Sil?'))return;await fetch('/api/s/'+n,{method:'DELETE'});yliste();dst();}
function bildirim(msg){if(Notification.permission==='granted'){new Notification('Loto',{body:msg});}}
if(Notification.permission==='default')Notification.requestPermission();
dst();
</script></body></html>"""


app = Flask(__name__)


@app.route("/")
def idx():
    return HTML


@app.route("/api/d")
def api_d():
    return jsonify({"t": len(veri), "s": max(veri.keys()) if veri else 0})


@app.route("/api/t")
def api_t():
    return jsonify(kolon_uret())


@app.route("/api/grafik")
def api_grafik():
    f = frekans(veri)
    sicak, ilimli, soguk = siniflandir(f)
    sayilar = []
    for s in range(1, 61):
        if s in sicak:
            sn = "sicak"
        elif s in soguk:
            sn = "soguk"
        else:
            sn = "ilimli"
        sayilar.append({"s": s, "f": f.get(s, 0), "sinif": sn})
    son30 = frekans(veri, son=max(veri.keys()) - 29) if veri else Counter()
    ort = sum(f.values()) / 60 if f else 1
    trend = [{"s": s, "t": son30.get(s, 0) - ort * (30 / max(len(veri), 1))} for s in range(1, 61)]
    return jsonify({"sayilar": sayilar, "trend": trend})


@app.route("/api/backtest")
def api_bt():
    n = int(request.args.get("n", 50))
    return jsonify(backtest(n))


@app.route("/api/tahmin_kaydet", methods=["POST"])
def api_th_kaydet():
    ks = kolon_uret()
    en_iyi = ks[0]["s"]
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M")
    tahminler["kayitli"].append({"tarih": tarih, "sayilar": en_iyi})
    th_kaydet()
    return jsonify({"ok": True})


@app.route("/api/kayitli")
def api_kayitli():
    return jsonify(tahminler)


@app.route("/api/e", methods=["POST"])
def api_e():
    try:
        d = request.get_json()
        n = int(d["no"])
        s = [int(x) for x in re.findall(r"\d+", str(d["sayilar"]))]
        if len(s) != 6 or len(set(s)) != 6:
            return jsonify({"ok": False, "hata": "6 farkli sayi"})
        if not all(1 <= x <= 60 for x in s):
            return jsonify({"ok": False, "hata": "1-60 arasi"})
        if n in veri:
            return jsonify({"ok": False, "hata": "Zaten var"})
        veri[n] = sorted(s)
        kaydet()
        # Karsilastirma: eski tahminlerle otomatik karsilastir
        yeni_kars = []
        for t in tahminler["kayitli"]:
            tut = set(t["sayilar"]) & set(s)
            if len(tut) > 0:
                tahminler["karsilastirma"].append({
                    "tarih": t["tarih"], "tahmin": t["sayilar"],
                    "gercek": sorted(s), "tutan": len(tut), "tutulan": sorted(list(tut)),
                    "cekilis_no": n
                })
        tahminler["kayitli"] = []
        th_kaydet()
        return jsonify({"ok": True})
    except Exception as ex:
        return jsonify({"ok": False, "hata": str(ex)})


@app.route("/api/top", methods=["POST"])
def api_top():
    try:
        d = request.get_json()
        lines = [x.strip() for x in d["metin"].splitlines() if x.strip()]
        bas = 0
        ns = max(veri.keys()) + 1 if veri else 1
        for ln in lines:
            try:
                p = re.findall(r"\d+", ln)
                if len(p) == 6:
                    while ns in veri:
                        ns += 1
                    n = ns
                    s = [int(x) for x in p]
                    ns += 1
                elif len(p) == 7:
                    n = int(p[0])
                    s = [int(x) for x in p[1:]]
                else:
                    continue
                if n not in veri and len(set(s)) == 6 and all(1 <= x <= 60 for x in s):
                    veri[n] = sorted(s)
                    bas += 1
            except Exception:
                pass
        kaydet()
        return jsonify({"ok": True, "mesaj": str(bas) + " eklendi"})
    except Exception as ex:
        return jsonify({"ok": False, "hata": str(ex)})


@app.route("/api/l")
def api_l():
    return jsonify({"liste": [{"no": n, "sayilar": veri[n]} for n in sorted(veri)]})


@app.route("/api/s/<int:n>", methods=["DELETE"])
def api_s(n):
    if n in veri:
        del veri[n]
        kaydet()
        return jsonify({"ok": True})
    return jsonify({"ok": False})


if __name__ == "__main__":
    print("=" * 45)
    print("  LOTO v5 - TAM OZELLIKLI")
    print("=" * 45)
    print("  Hafiza: " + str(len(veri)) + " cekilis")
    print("  http://127.0.0.1:5000")
    print("=" * 45)
    app.run(host="0.0.0.0", port=5000)