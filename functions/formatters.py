def _comma(n, fmt):
    s = format(n, fmt)
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s

def fmt_freq(hz: float) -> str:
    if hz >= 1000:
        return _comma(hz, ".1f").rstrip("0").rstrip(",") + " Hz"
    if hz >= 100:
        return _comma(hz, ".0f") + " Hz"
    if hz >= 10:
        return _comma(hz, ".1f").rstrip("0").rstrip(",") + " Hz"
    return _comma(hz, ".2f").rstrip("0").rstrip(",") + " Hz"

def fmt_speed(v: float) -> str:
    return _comma(v, ".2f") + " m/s"

def fmt_len(m: float) -> str:
    if m < 0.01:
        return _comma(m*1000.0, ".1f").rstrip("0").rstrip(",") + " mm"
    if m < 1:
        return _comma(m*100.0, ".1f").rstrip("0").rstrip(",") + " cm"
    if m < 1000:
        return _comma(m, ".2f").rstrip("0").rstrip(",") + " m"
    return _comma(m/1000.0, ".2f").rstrip("0").rstrip(",") + " km"

def fmt_time_s(seconds: float) -> str:
    if seconds < 0.001:
        return _comma(seconds*1_000_000, ".0f") + " µs"
    if seconds < 1:
        return _comma(seconds*1000.0, ".1f").rstrip("0").rstrip(",") + " ms"
    return _comma(seconds, ".3f").rstrip("0").rstrip(",") + " s"

def fmt_ms_per_m(v: float) -> str:
    return _comma(1000.0/v, ".3f").rstrip("0").rstrip(",") + " ms/m"

def fmt_distance(d):
    if d is None:
        return None
    if d < 1:
        return _comma(d*100.0, ".1f").rstrip("0").rstrip(",") + " cm"
    if d < 1000:
        return _comma(d, ".1f").rstrip("0").rstrip(",") + " m"
    return _comma(d/1000.0, ".2f").rstrip("0").rstrip(",") + " km"
