#!/usr/bin/env python3
"""
Onchain palette generator — deterministic, no dependencies, no API.

Takes ONE brand anchor hex and emits the full 3-layer token set:
  Primitive (50..950 ramp)  ->  Theme (brand + tinted neutrals + status + chart)
                            ->  Semantic (Dark + Light)

The anchor hex is PRESERVED EXACTLY as the 500 step; the rest of the ramp is
built around it. Colour math is done in OKLCH (perceptually uniform) so the ramp
has even visual steps regardless of hue, and out-of-gamut steps have their
chroma reduced until they fit sRGB (never hard-clipped to a muddy value).
All conversions are implemented inline (sRGB <-> linear <-> OKLab <-> OKLCH).

Usage:
    python3 generate-palette.py "#7C5CFF"            # full token set
    python3 generate-palette.py "#14F195" --name emerald
    python3 generate-palette.py "#7C5CFF" --css      # emit CSS custom properties
"""
import sys, math, argparse

# ---------- sRGB <-> OKLCH ----------
def normalize_hex(h):
    """'#abc' / 'abc' / '#AABBCC' -> '#AABBCC'. Raises on anything else."""
    s = h.lstrip('#')
    if len(s) == 3:
        s = ''.join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f'not a hex colour: #{s}')
    int(s, 16)                      # raises ValueError on non-hex digits
    return f'#{s.upper()}'

def hex_to_rgb(h):
    s = normalize_hex(h).lstrip('#')
    return tuple(int(s[i:i+2], 16) / 255 for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    f = lambda x: format(max(0, min(255, round(x * 255))), '02X')
    return f'#{f(r)}{f(g)}{f(b)}'

def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def linear_to_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055

def linear_to_oklab(r, g, b):
    l = 0.4122214708*r + 0.5363325363*g + 0.0514459929*b
    m = 0.2119034982*r + 0.6806995451*g + 0.1073969566*b
    s = 0.0883024619*r + 0.2817188376*g + 0.6299787005*b
    l_, m_, s_ = l**(1/3), m**(1/3), s**(1/3)
    return (
        0.2104542553*l_ + 0.7936177850*m_ - 0.0040720468*s_,
        1.9779984951*l_ - 2.4285922050*m_ + 0.4505937099*s_,
        0.0259040371*l_ + 0.7827717662*m_ - 0.8086757660*s_,
    )

def oklab_to_linear(L, a, b):
    l_ = L + 0.3963377774*a + 0.2158037573*b
    m_ = L - 0.1055613458*a - 0.0638541728*b
    s_ = L - 0.0894841775*a - 1.2914855480*b
    l, m, s = l_**3, m_**3, s_**3
    return (
        +4.0767416621*l - 3.3077115913*m + 0.2309699292*s,
        -1.2684380046*l + 2.6097574011*m - 0.3413193965*s,
        -0.0041960863*l - 0.7034186147*m + 1.7076147010*s,
    )

def hex_to_oklch(h):
    r, g, b = (srgb_to_linear(c) for c in hex_to_rgb(h))
    L, a, bb = linear_to_oklab(r, g, b)
    C = math.hypot(a, bb)
    H = math.degrees(math.atan2(bb, a)) % 360
    return L, C, H

def _linear_rgb(L, C, H):
    a = C * math.cos(math.radians(H))
    b = C * math.sin(math.radians(H))
    return oklab_to_linear(L, a, b)

def in_gamut(L, C, H, eps=1e-4):
    return all(-eps <= c <= 1 + eps for c in _linear_rgb(L, C, H))

def oklch_to_hex(L, C, H):
    """Convert to hex, reducing chroma (binary search) until the colour fits sRGB."""
    if not in_gamut(L, C, H):
        lo, hi = 0.0, C
        for _ in range(24):
            mid = (lo + hi) / 2
            if in_gamut(L, mid, H):
                lo = mid
            else:
                hi = mid
        C = lo
    return rgb_to_hex(*(linear_to_srgb(c) for c in _linear_rgb(L, C, H)))

# ---------- brand ramp ----------
# Reference lightness curve (OKLCH L). The curve's SHAPE is what's tuned here;
# it is re-anchored below so the anchor hex lands exactly on 500.
STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
TARGET_L = {
    50: 0.971, 100: 0.936, 200: 0.885, 300: 0.808, 400: 0.723,
    500: 0.637, 600: 0.575, 700: 0.505, 800: 0.432, 900: 0.360, 950: 0.265,
}
# Chroma is scaled relative to the anchor's own chroma, peaking mid-ramp,
# tapering at the extremes so 50/950 don't look muddy or neon.
CHROMA_SCALE = {
    50: 0.30, 100: 0.45, 200: 0.65, 300: 0.85, 400: 0.97, 500: 1.00,
    600: 1.00, 700: 0.92, 800: 0.80, 900: 0.65, 950: 0.45,
}
L_LIGHTEST, L_DARKEST = TARGET_L[50], TARGET_L[950]
L_PIVOT = TARGET_L[500]

def _rescale_L(step, L_anchor):
    """Map the reference curve onto the anchor: 500 -> L_anchor, ends held.

    The light half is compressed/stretched between L_anchor and the lightest
    step, the dark half between L_anchor and the darkest, so the ramp stays
    monotonic whatever the anchor's own lightness is.
    """
    L_ref = TARGET_L[step]
    if L_ref == L_PIVOT:
        return L_anchor
    if L_ref > L_PIVOT:                                  # lighter than 500
        top = max(L_LIGHTEST, L_anchor + 0.03)           # keep headroom
        t = (L_ref - L_PIVOT) / (L_LIGHTEST - L_PIVOT)
        return L_anchor + t * (top - L_anchor)
    bottom = min(L_DARKEST, L_anchor - 0.03)             # keep footroom
    t = (L_PIVOT - L_ref) / (L_PIVOT - L_DARKEST)
    return L_anchor - t * (L_anchor - bottom)

def build_ramp(anchor_hex):
    """500 is the anchor, byte-for-byte; every other step derives from it."""
    L0, C0, H = hex_to_oklch(anchor_hex)
    if L0 > 0.93 or L0 < 0.22:
        print(f'warning: anchor lightness {L0:.2f} is near-{"white" if L0 > 0.5 else "black"} — '
              'one half of the ramp will be compressed. A mid-lightness anchor '
              '(L 0.45-0.80) gives a usable 50-950 ramp.', file=sys.stderr)
    ramp = {}
    for step in STEPS:
        if step == 500:
            ramp[step] = normalize_hex(anchor_hex)
            continue
        ramp[step] = oklch_to_hex(_rescale_L(step, L0), C0 * CHROMA_SCALE[step], H)
    return ramp, H

# ---------- neutrals ----------
# A whisper of the brand hue at every step — the anti-generic device. The chroma
# is a fixed small absolute value, NOT a percentage of the anchor's chroma, so a
# muted brand and a neon one get the same restrained tint.
NEUTRAL_TINT_C = 0.006
NEUTRAL_L = {0: 0.995, 25: 0.975, 50: 0.962, 100: 0.930, 200: 0.885, 300: 0.820,
             400: 0.700, 500: 0.630, 600: 0.500, 700: 0.430, 800: 0.330,
             850: 0.280, 900: 0.230, 925: 0.205, 950: 0.180, 1000: 0.130}

def tinted_neutrals(brand_hue):
    return {k: oklch_to_hex(L, NEUTRAL_TINT_C, brand_hue) for k, L in NEUTRAL_L.items()}

# ---------- contrast (WCAG 2.x) ----------
DARK_INK, LIGHT_INK = '#0A0B0D', '#FFFFFF'
AA_NORMAL = 4.5

def relative_luminance(hex_c):
    def f(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(c) for c in hex_to_rgb(hex_c))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(a, b):
    hi, lo = sorted((relative_luminance(a), relative_luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)

def on_color(hex_bg, label=''):
    """The legible ink for text on a filled step — chosen by MEASURED contrast.

    Picking by lightness alone gets mid-tone fills wrong (it hands white to a
    colour that black clears more comfortably). Both candidates are measured and
    the better one wins; if even the better one misses AA, that shade is not a
    usable text-bearing fill and we say so (design-system.md, SKILL.md §5).
    """
    ranked = sorted((DARK_INK, LIGHT_INK), key=lambda ink: -contrast_ratio(ink, hex_bg))
    best = ranked[0]
    r = contrast_ratio(best, hex_bg)
    if r < AA_NORMAL:
        print(f'warning: {label or hex_bg} ({hex_bg}) has no AA-legible on-colour '
              f'(best is {best} at {r:.2f}:1, AA needs {AA_NORMAL}). Neither black nor '
              'white passes on this shade — use a lighter or darker ramp step for any '
              'fill that carries text, or keep this one as a non-text surface.',
              file=sys.stderr)
    return best

# ---------- status ----------
# Fixed hues, independent of the brand: status must stay recognisable as
# green/amber/red/blue whatever the brand hue is. Dark-mode values run lighter
# (they sit on dark surfaces), light-mode values run deeper.
STATUS_HUES = {'success': 152, 'warning': 85, 'error': 27, 'info': 250}
STATUS_RECIPE = {                    # (L, C) for dark mode, then light mode
    'base':   ((0.74, 0.16), (0.56, 0.17)),
    'subtle': ((0.29, 0.055), (0.94, 0.045)),
}

def status_tokens():
    out = {}
    for name, H in STATUS_HUES.items():
        for level, ((Ld, Cd), (Ll, Cl)) in STATUS_RECIPE.items():
            out[f'{name}/{level}'] = (oklch_to_hex(Ld, Cd, H), oklch_to_hex(Ll, Cl, H))
    return out

# ---------- chart ----------
# Categorical series rotate around the wheel from the brand hue, so the data
# palette rhymes with the brand without reusing UI or status colours. Direction
# tokens are deliberately NOT the same hexes as success/error: a red candle and
# a green success toast can share a screen without collision.
CHART_SERIES = 6
CHART_LC = ((0.73, 0.13), (0.58, 0.15))          # (L, C) dark, light
CHART_DIRECTION = {'positive': (150, (0.70, 0.15), (0.52, 0.16)),
                   'negative': (24,  (0.68, 0.16), (0.53, 0.18))}

def chart_tokens(brand_hue):
    out = {}
    (Ld, Cd), (Ll, Cl) = CHART_LC
    for i in range(CHART_SERIES):
        H = (brand_hue + i * (360 / CHART_SERIES)) % 360
        out[f'chart/{i + 1}'] = (oklch_to_hex(Ld, Cd, H), oklch_to_hex(Ll, Cl, H))
    for name, (H, (dL, dC), (lL, lC)) in CHART_DIRECTION.items():
        out[f'chart/{name}'] = (oklch_to_hex(dL, dC, H), oklch_to_hex(lL, lC, H))
    return out

# ---------- semantic mapping ----------
def semantic_tokens(name):
    return {
        'color/brand/primary':  (f'{name}/500', f'{name}/600'),
        'color/brand/hover':    (f'{name}/600', f'{name}/700'),
        'color/brand/pressed':  (f'{name}/700', f'{name}/800'),
        'color/brand/subtle':   (f'{name}/950', f'{name}/100'),
        'color/brand/text':     (f'{name}/300', f'{name}/800'),
        'color/brand/on':       ('on-500', 'on-600'),
        'color/bg/base':        ('neutral/1000', 'neutral/0'),
        'color/bg/surface':     ('neutral/950', 'neutral/25'),
        'color/bg/raised':      ('neutral/925', 'neutral/0'),
        'color/bg/muted':       ('neutral/850', 'neutral/100'),
        'color/bg/overlay':     ('neutral/1000 @ 70%', 'neutral/1000 @ 45%'),
        'color/text/primary':   ('neutral/50', 'neutral/900'),
        'color/text/secondary': ('neutral/400', 'neutral/700'),
        # tertiary sits one step in from secondary but must still clear AA on
        # base/surface/raised — a step further out reads nicer and fails 4.5:1.
        'color/text/tertiary':  ('neutral/500', 'neutral/600'),
        'color/text/inverse':   ('neutral/1000', 'neutral/0'),
        'color/border/subtle':  ('neutral/900', 'neutral/100'),
        'color/border/default': ('neutral/850', 'neutral/200'),
        'color/border/strong':  ('neutral/800', 'neutral/300'),
        'color/chart/grid':     ('neutral/900', 'neutral/100'),
        'color/chart/axis':     ('neutral/700', 'neutral/300'),
    }

# ---------- output ----------
def _css_var(token):
    return '--' + token.replace('color/', '').replace('/', '-')

def _resolve(ref, name, ramp, neutrals, on500, on600):
    """Semantic value -> the primitive var it points at (or an rgb() recipe)."""
    if ' @ ' in ref:                                    # bg/overlay: 'neutral/1000 @ 70%'
        base, alpha = ref.split(' @ ')
        hexv = neutrals[int(base.split('/')[1])]
        r, g, b = (int(hexv[i:i + 2], 16) for i in (1, 3, 5))
        return f'rgb({r} {g} {b} / {alpha})'
    if ref == 'on-500':
        return on500
    if ref == 'on-600':
        return on600
    family, step = ref.split('/')
    return f'var(--neutral-{step})' if family == 'neutral' else f'var(--{name}-{step})'

def emit_css(name, ramp, neutrals, on500, on600, status, chart):
    print('/* Primitives — the raw ramp. Components should NOT consume these */')
    print(':root {')
    for k, v in ramp.items():
        print(f'  --{name}-{k}: {v};')
    print(f'  --{name}-on-500: {on500};')
    print(f'  --{name}-on-600: {on600};')
    for k, v in neutrals.items():
        print(f'  --neutral-{k}: {v};')
    print('}\n')
    print('/* Semantic layer per mode — this is what components use. */')
    print('/* Swap the selector for `.dark` / `.light` if that is the project strategy. */')
    semantics = semantic_tokens(name)
    for mode, idx in (('dark', 0), ('light', 1)):
        print(f':root[data-theme="{mode}"] {{')
        for tok, refs in semantics.items():
            print(f'  {_css_var(tok)}: {_resolve(refs[idx], name, ramp, neutrals, on500, on600)};')
        for k, v in status.items():
            print(f'  --{k.replace("/", "-")}: {v[idx]};')
        for k, v in chart.items():
            print(f'  --{k.replace("/", "-")}: {v[idx]};')
        print('}')

def emit_text(name, anchor, hue, ramp, neutrals, on500, on600, status, chart):
    print(f'\nBRAND RAMP  (anchor {normalize_hex(anchor)} preserved at /500 — hue {hue:.1f}deg)')
    for k, v in ramp.items():
        mark = '  <- anchor' if k == 500 else ''
        print(f'  {name}/{k:<4} {v}{mark}')
    print(f'  on-500 {on500}   on-600 {on600}')
    print('\nTINTED NEUTRALS')
    for k, v in neutrals.items():
        print(f'  neutral/{k:<5} {v}')
    print('\nSTATUS               Dark      Light')
    for k, (d, l) in status.items():
        print(f'  {k:<18} {d}   {l}')
    print('\nCHART                Dark      Light')
    for k, (d, l) in chart.items():
        print(f'  {k:<18} {d}   {l}')
    print('\nSEMANTIC (Dark / Light)')
    for tok, (d, l) in semantic_tokens(name).items():
        print(f'  {tok:<24} {d:<18} {l}')

def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('anchor', help='brand anchor hex, e.g. "#7C5CFF" — preserved as the 500 step')
    ap.add_argument('--name', default='brand', help='token prefix for the brand ramp')
    ap.add_argument('--css', action='store_true', help='emit CSS custom properties')
    args = ap.parse_args()

    try:
        ramp, hue = build_ramp(args.anchor)
    except ValueError:
        sys.exit(f'error: "{args.anchor}" is not a hex colour — expected #RGB or #RRGGBB')

    neutrals = tinted_neutrals(hue)
    on500, on600 = on_color(ramp[500], f'{args.name}/500'), on_color(ramp[600], f'{args.name}/600')
    status, chart = status_tokens(), chart_tokens(hue)

    if args.css:
        emit_css(args.name, ramp, neutrals, on500, on600, status, chart)
    else:
        emit_text(args.name, args.anchor, hue, ramp, neutrals, on500, on600, status, chart)

if __name__ == '__main__':
    main()
