from flask import Flask, request, render_template
from functions import speed_of_sound_celsius, fmt_freq, fmt_speed, fmt_len, fmt_time_s, fmt_ms_per_m, fmt_distance, parse_number, parse_freq, parse_len, parse_dist

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    results = None
    is_post = request.method == "POST"
    has_get_values = any((request.args.get("frequency", "").strip(), request.args.get("wavelength", "").strip()))
    do_compute = is_post or has_get_values
    incoming = request.form if is_post else request.args
    form = {
        "input_type": incoming.get("input_type", "frequency"),
        "temperature": incoming.get("temperature", "15"),
        "distance": incoming.get("distance", ""),
        "frequency": incoming.get("frequency", ""),
        "wavelength": incoming.get("wavelength", ""),
    }
    if do_compute:
        try:
            input_type = incoming.get("input_type", "frequency")
            temperature = parse_number(incoming.get("temperature", "15"), 15.0, field="Temperatura")
            distance = parse_dist(incoming.get("distance", ""), None)
            v = speed_of_sound_celsius(temperature)
            if input_type == "frequency":
                f = parse_freq(incoming.get("frequency", ""), None)
                if f is None or f <= 0:
                    raise ValueError("Frequência deve ser maior que zero.")
                lam = v / f
            else:
                lam = parse_len(incoming.get("wavelength", ""), None)
                if lam is None or lam <= 0:
                    raise ValueError("Comprimento de onda deve ser maior que zero.")
                f = v / lam
            T = 1.0 / f
            delay_str = None
            if distance is not None:
                if distance < 0:
                    raise ValueError("Distância não pode ser negativa.")
                delay_str = fmt_time_s(distance / v)
            results = {
                "v_str": fmt_speed(v),
                "f_str": fmt_freq(f),
                "T_str": fmt_time_s(T),
                "lambda_str": fmt_len(lam),
                "ms_per_m_str": fmt_ms_per_m(v),
                "delay_str": delay_str,
                "distance_str": fmt_distance(distance) if distance is not None else None,
                "v_raw": f"{v:.6f}",
                "lambda_quarter": fmt_distance(lam/4.0),
                "lambda_half": fmt_distance(lam/2.0),
                "lambda_full_fmt": fmt_distance(lam),
                "lambda_m": f"{lam:.6f}",
            }
        except ValueError as e:
            error = str(e)
    return render_template("index.html", results=results, error=error, form=form)

vercel_app = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
