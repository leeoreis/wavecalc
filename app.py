from flask import Flask, request, render_template_string

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang="pt-br">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Conversor de Áudio — Freq • Onda • Delay</title>
<style>
  :root { --bg:#0b0f13; --card:#121821; --ink:#eaf2ff; --muted:#9fb2cc; --pri:#3aa0ff; --ok:#00d08a; --err:#ff5a5a; --br:20px; }
  * { box-sizing: border-box; }
  html, body { margin:0; padding:0; background:var(--bg); color:var(--ink); font:16px/1.4 system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Arial, sans-serif; }
  .wrap { max-width:520px; margin:0 auto; padding:24px 16px 40px; }
  h1 { font-size:1.25rem; margin:0 0 8px; }
  p.lead { margin:0 0 16px; color:var(--muted); }
  form { background:var(--card); padding:16px; border-radius:var(--br); box-shadow:0 8px 20px rgba(0,0,0,.25); }
  .row { display:flex; gap:10px; }
  .col { flex:1; }
  .field { margin-bottom:12px; }
  .label { display:block; font-size:.9rem; color:var(--muted); margin-bottom:6px; }
  .input { width:100%; padding:14px 14px; border-radius:14px; border:1px solid #1f2a38; background:#0e141c; color:var(--ink); outline:none; }
  .input:focus { border-color:var(--pri); box-shadow:0 0 0 3px rgba(58,160,255,.2); }
  .units { font-size:.85rem; color:var(--muted); margin-left:6px; }
  .radios { display:flex; gap:8px; background:#0e141c; padding:6px; border-radius:12px; border:1px solid #1f2a38; }
  .radio { flex:1; }
  .radio input { display:none; }
  .radio label { display:block; text-align:center; padding:10px 8px; border-radius:8px; border:1px solid transparent; color:var(--muted); }
  .radio input:checked + label { background:#132030; color:var(--ink); border-color:#213246; }
  .hint { font-size:.8rem; color:var(--muted); margin-top:4px; }
  .btn { appearance:none; border:0; width:100%; padding:14px; border-radius:14px; font-weight:700; background:linear-gradient(180deg, #40a7ff, #2b93f0); color:white; margin-top:8px; }
  .btn:active { transform: translateY(1px); }
  .results { margin-top:16px; display:grid; grid-template-columns:1fr 1fr; gap:10px; }
  .card { background:var(--card); border:1px solid #1f2a38; border-radius:var(--br); padding:14px; }
  .k { color:var(--muted); font-size:.85rem; }
  .v { font-size:1.25rem; font-weight:700; margin-top:4px; line-height:1.2; }
  .sub { font-size:.9rem; color:var(--muted); margin-top:2px; }
  .foot { text-align:center; color:var(--muted); font-size:.8rem; margin-top:14px; }
  .err { background:#2a0e12; border:1px solid #44151b; color:#ffd6d6; padding:12px; border-radius:12px; margin-bottom:12px; }
  .chips { display:flex; gap:8px; margin-top:6px; }
  .chip { background:#0e141c; border:1px solid #1f2a38; color:var(--ink); border-radius:999px; padding:8px 12px; font-size:.9rem; }
  .chip:active { transform: translateY(1px); }
  .calc { grid-column:1 / -1; background:#0e141c; border:1px dashed #243044; border-radius:16px; padding:12px; }
  .calc h3 { margin:0 0 8px; font-size:1rem; }
  .calc .row { align-items:center; }
  .calc .out { font-weight:800; font-size:1.2rem; text-align:right; }
</style>
</head>
<body>
  <div class="wrap">
    <h1>Conversor de Áudio</h1>
    <p class="lead">Informe frequência <b>ou</b> comprimento de onda e a temperatura. Opcionalmente, uma distância para calcular o atraso.</p>

    {% if error %}<div class="err">{{ error }}</div>{% endif %}

    <form method="post">
      <div class="field">
        <div class="label">Tipo de entrada</div>
        <div class="radios">
          <div class="radio">
            <input id="r-f" type="radio" name="input_type" value="frequency" {% if form.input_type != 'wavelength' %}checked{% endif %}>
            <label for="r-f">Frequência (Hz)</label>
          </div>
          <div class="radio">
            <input id="r-l" type="radio" name="input_type" value="wavelength" {% if form.input_type == 'wavelength' %}checked{% endif %}>
            <label for="r-l">Compr. de onda (m)</label>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="field col" id="freq-field">
          <label class="label">Frequência<span class="units">Hz</span></label>
          <input class="input" type="text" inputmode="decimal" name="frequency" value="{{ form.frequency or '' }}" placeholder="ex.: 20" {% if form.input_type == 'wavelength' %}disabled{% endif %}>
          <div class="hint">Use esta opção para obter λ, período e delays.</div>
        </div>
        <div class="field col" id="wave-field">
          <label class="label">Comprimento de onda<span class="units">m</span></label>
          <input class="input" type="text" inputmode="decimal" name="wavelength" value="{{ form.wavelength or '' }}" placeholder="ex.: 3,4" {% if form.input_type != 'wavelength' %}disabled{% endif %}>
          <div class="hint">Use esta opção para obter f, período e delays.</div>
        </div>
      </div>

      <div class="row">
        <div class="field col">
          <label class="label">Temperatura do ar<span class="units">°C</span></label>
          <input class="input" type="text" inputmode="decimal" name="temperature" id="temp" value="{{ form.temperature or '15' }}" placeholder="ex.: 15">
        </div>
        <div class="field col">
          <label class="label">Distância (opcional)<span class="units">m</span></label>
          <input class="input" type="text" inputmode="decimal" name="distance" value="{{ form.distance or '' }}" placeholder="ex.: 10" id="distance-input">
          <div class="chips">
            <button class="chip" type="button" data-d="1">1 m</button>
            <button class="chip" type="button" data-d="5">5 m</button>
            <button class="chip" type="button" data-d="10">10 m</button>
          </div>
          <div class="hint">Toque em um atalho para preencher rápido.</div>
        </div>
      </div>

      <button class="btn" type="submit">Calcular</button>

      {% if results %}
      <div class="results" data-v="{{ results.v_raw }}">
        <div class="card"><div class="k">Velocidade do som</div><div class="v">{{ results.v_str }}</div></div>
        <div class="card"><div class="k">Frequência</div><div class="v">{{ results.f_str }}</div></div>
        <div class="card"><div class="k">Período</div><div class="v">{{ results.T_str }}</div></div>
        <div class="card"><div class="k">Comprimento de onda</div><div class="v">{{ results.lambda_str }}</div></div>
        <div class="card"><div class="k">Atraso por metro</div><div class="v">{{ results.ms_per_m_str }}</div><div class="sub">Tempo que o som leva para percorrer 1 metro.</div></div>
        {% if results.delay_str %}
        <div class="card"><div class="k">Atraso para {{ results.distance_str }}</div><div class="v">{{ results.delay_str }}</div></div>
        {% endif %}

        <div class="calc card">
          <h3>Calculadora rápida de delay</h3>
          <div class="row">
            <div class="col">
              <label class="label">Distância<span class="units">m</span></label>
              <input class="input" type="text" inputmode="decimal" id="qd-distance" placeholder="ex.: 17,30">
              <div class="hint">Usa a temperatura atual para calcular a velocidade do som.</div>
            </div>
            <div class="col">
              <div class="label">Delay estimado</div>
              <div class="out" id="qd-out">—</div>
            </div>
          </div>
        </div>
      </div>
      <div class="foot">Fórmula de v(T): v ≈ 331,3 + 0,606·T (°C)</div>
      {% endif %}
    </form>
  </div>
<script>
  const rf = document.getElementById('r-f');
  const rl = document.getElementById('r-l');
  const freqInput = document.querySelector('input[name="frequency"]');
  const waveInput = document.querySelector('input[name="wavelength"]');
  function sync() {
    if (rf.checked) { freqInput.disabled = false; waveInput.disabled = true; }
    else { freqInput.disabled = true; waveInput.disabled = false; }
  }
  rf.addEventListener('change', sync);
  rl.addEventListener('change', sync);
  sync();

  const dist = document.getElementById('distance-input');
  document.querySelectorAll('.chip').forEach(b=>{
    b.addEventListener('click',()=>{
      dist.value = b.dataset.d;
      dist.dispatchEvent(new Event('input',{bubbles:true}));
    });
  });

  function parseNum(s){ if(!s) return NaN; return Number(String(s).replace(",", ".")); }
  function fmtDelay(ms){
    if(!isFinite(ms)) return "—";
    if(ms >= 1000) { const s = (ms/1000).toFixed(2).replace(".", ","); return s+" s"; }
    return (Math.round(ms*10)/10).toString().replace(".", ",")+" ms";
  }
  function vFromTemp(){
    const t = parseNum(document.getElementById('temp')?.value || "15");
    return 331.3 + 0.606 * (isFinite(t)? t : 15);
  }
  const qdIn = document.getElementById('qd-distance');
  const qdOut = document.getElementById('qd-out');
  function recalcQD(){
    const d = parseNum(qdIn?.value);
    const v = vFromTemp();
    if(isFinite(d) && d>=0) { const ms = (d / v) * 1000; qdOut.textContent = fmtDelay(ms); }
    else { qdOut.textContent = "—"; }
  }
  ['input','change'].forEach(evt=>{
    qdIn?.addEventListener(evt, recalcQD);
    document.getElementById('temp')?.addEventListener(evt, recalcQD);
  });
</script>
</body>
</html>
"""

def speed_of_sound_celsius(T):
    return 331.3 + 0.606 * T

def parse_num(s, default=None):
    if s is None: return default
    s = s.strip().replace(",", ".")
    if s == "": return default
    return float(s)

def _comma(n, fmt):
    s = format(n, fmt)
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s

def fmt_freq(hz):
    if hz >= 1000: return _comma(hz, ".1f").rstrip("0").rstrip(",") + " Hz"
    if hz >= 100: return _comma(hz, ".0f") + " Hz"
    if hz >= 10: return _comma(hz, ".1f").rstrip("0").rstrip(",") + " Hz"
    return _comma(hz, ".2f").rstrip("0").rstrip(",") + " Hz"

def fmt_speed(v):
    return _comma(v, ".2f") + " m/s"

def fmt_len(m):
    if m < 0.01: return _comma(m*1000.0, ".1f").rstrip("0").rstrip(",") + " mm"
    if m < 1: return _comma(m*100.0, ".1f").rstrip("0").rstrip(",") + " cm"
    if m < 1000: return _comma(m, ".2f").rstrip("0").rstrip(",") + " m"
    return _comma(m/1000.0, ".2f").rstrip("0").rstrip(",") + " km"

def fmt_time_s(seconds):
    if seconds < 0.001: return _comma(seconds*1_000_000, ".0f") + " µs"
    if seconds < 1: return _comma(seconds*1000.0, ".1f").rstrip("0").rstrip(",") + " ms"
    return _comma(seconds, ".3f").rstrip("0").rstrip(",") + " s"

def fmt_ms_per_m(v):
    return _comma(1000.0/v, ".3f").rstrip("0").rstrip(",") + " ms/m"

def fmt_distance(d):
    if d is None: return None
    if d < 1: return _comma(d*100.0, ".1f").rstrip("0").rstrip(",") + " cm"
    if d < 1000: return _comma(d, ".1f").rstrip("0").rstrip(",") + " m"
    return _comma(d/1000.0, ".2f").rstrip("0").rstrip(",") + " km"

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    results = None
    form = {"input_type": request.form.get("input_type", "frequency")}
    if request.method == "POST":
        try:
            input_type = request.form.get("input_type", "frequency")
            temperature = parse_num(request.form.get("temperature", "15"), 15.0)
            distance = parse_num(request.form.get("distance", ""), None)
            v = speed_of_sound_celsius(temperature)
            if input_type == "frequency":
                f = parse_num(request.form.get("frequency", ""))
                if f is None or f <= 0: raise ValueError("Frequência deve ser maior que zero.")
                lam = v / f
            else:
                lam = parse_num(request.form.get("wavelength", ""))
                if lam is None or lam <= 0: raise ValueError("Comprimento de onda deve ser maior que zero.")
                f = v / lam
            T = 1.0 / f
            delay_str = None
            if distance is not None:
                if distance < 0: raise ValueError("Distância não pode ser negativa.")
                delay_str = fmt_time_s(distance / v)
            results = {
                "v_str": fmt_speed(v),
                "f_str": fmt_freq(f),
                "T_str": fmt_time_s(T),
                "lambda_str": fmt_len(lam),
                "ms_per_m_str": fmt_ms_per_m(v),
                "delay_str": delay_str,
                "distance_str": fmt_distance(distance) if distance is not None else None,
                "v_raw": f"{v:.6f}"
            }
            form.update({
                "temperature": request.form.get("temperature", "15"),
                "distance": request.form.get("distance", ""),
                "frequency": request.form.get("frequency", ""),
                "wavelength": request.form.get("wavelength", ""),
                "input_type": input_type
            })
        except ValueError as e:
            error = str(e)
            form.update({
                "temperature": request.form.get("temperature", "15"),
                "distance": request.form.get("distance", ""),
                "frequency": request.form.get("frequency", ""),
                "wavelength": request.form.get("wavelength", ""),
            })
    return render_template_string(TEMPLATE, results=results, error=error, form=form)

vercel_app = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
