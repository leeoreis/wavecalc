def _clean(s: str) -> str:
    return s.strip().lower().replace(" ", "")

def parse_number(s, default, *, field: str):
    if s is None:
        return default
    s2 = s.strip().replace(",", ".")
    if s2 == "":
        return default
    try:
        return float(s2)
    except ValueError:
        raise ValueError(f"{field} inválido.")

def parse_freq(s, default):
    if s is None:
        return default
    raw = _clean(s).replace(",", ".")
    if raw == "":
        return default
    mult = 1.0
    if raw.endswith("khz"):
        raw = raw[:-3]
        mult = 1000.0
    elif raw.endswith("k"):
        raw = raw[:-1]
        mult = 1000.0
    elif raw.endswith("hz"):
        raw = raw[:-2]
    try:
        return float(raw) * mult
    except ValueError:
        raise ValueError("Frequência inválida.")

def parse_len(s, default):
    if s is None:
        return default
    raw = _clean(s).replace(",", ".")
    if raw == "":
        return default
    mult = 1.0
    if raw.endswith("cm"):
        raw = raw[:-2]
        mult = 0.01
    elif raw.endswith("mm"):
        raw = raw[:-2]
        mult = 0.001
    elif raw.endswith("m"):
        raw = raw[:-1]
    try:
        return float(raw) * mult
    except ValueError:
        raise ValueError("Comprimento de onda inválido.")

def parse_dist(s, default):
    if s is None:
        return default
    raw = _clean(s).replace(",", ".")
    if raw == "":
        return default
    mult = 1.0
    if raw.endswith("cm"):
        raw = raw[:-2]
        mult = 0.01
    elif raw.endswith("mm"):
        raw = raw[:-2]
        mult = 0.001
    elif raw.endswith("m"):
        raw = raw[:-1]
    try:
        return float(raw) * mult
    except ValueError:
        raise ValueError("Distância inválida.")
