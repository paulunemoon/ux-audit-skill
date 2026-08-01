#!/usr/bin/env python3
"""
WCAG 2.x contrast checker — deterministic, no dependencies, no API.

Turns "that looks low contrast" into "3.21:1, AA needs 4.5:1" — which is the
difference between a finding a team can act on and one they can argue with.

Usage:
    # one pair
    contrast-check.py "#8A8F98" "#F5F5F7"

    # one foreground against several backgrounds
    contrast-check.py "#8A8F98" "#FFFFFF" "#F5F5F7" "#E5E7EB"

    # a whole palette: every colour as text on every other colour
    contrast-check.py --matrix "#111827" "#6B7280" "#9CA3AF" "#FFFFFF"

    # semi-transparent foreground, composited over the background first
    contrast-check.py "#000000" "#FFFFFF" --alpha 0.6

    # pick the legible ink (black or white) for a fill
    contrast-check.py --on "#F0A500"

    # suggest the nearest passing shade of a failing foreground
    contrast-check.py "#8A8F98" "#F5F5F7" --suggest

Thresholds (WCAG 2.1):
    normal text  >= 4.5 (AA)   >= 7.0 (AAA)
    large text   >= 3.0 (AA)   >= 4.5 (AAA)   [>=18.66px bold / >=24px regular]
    non-text     >= 3.0 (AA)   -- UI boundaries, control states, focus rings,
                                  and meaningful graphics (1.4.11)

Caveats worth stating in a finding (see references/accessibility.md):
  * Opacity is not colour. Use --alpha so the composited value is measured.
  * Text over an image or gradient must pass at its WORST point, not the mean.
  * WCAG 2.x contrast is imperfect for some hue pairs. It is nonetheless the
    AA standard a conformance claim is measured against — report against it,
    and note perceptual concerns separately rather than substituting a
    different threshold.
"""
import sys
import argparse

AA_NORMAL, AAA_NORMAL = 4.5, 7.0
AA_LARGE, AAA_LARGE = 3.0, 4.5
AA_NONTEXT = 3.0

DARK_INK, LIGHT_INK = '#000000', '#FFFFFF'


# ---------- colour ----------
def normalize_hex(h):
    """'#abc' / 'abc' / '#AABBCC' -> '#AABBCC'. Raises on anything else."""
    s = str(h).strip().lstrip('#')
    if len(s) == 3:
        s = ''.join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f'not a hex colour: {h}')
    int(s, 16)                      # raises ValueError on non-hex digits
    return f'#{s.upper()}'


def hex_to_rgb(h):
    s = normalize_hex(h).lstrip('#')
    return tuple(int(s[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    f = lambda x: format(max(0, min(255, round(x * 255))), '02X')
    return f'#{f(r)}{f(g)}{f(b)}'


def composite(fg_hex, bg_hex, alpha):
    """Flatten a semi-transparent foreground onto its background (sRGB space,
    which is what a browser does for `opacity` and rgba fills)."""
    fr, fg_, fb = hex_to_rgb(fg_hex)
    br, bg_, bb = hex_to_rgb(bg_hex)
    return rgb_to_hex(fr * alpha + br * (1 - alpha),
                      fg_ * alpha + bg_ * (1 - alpha),
                      fb * alpha + bb * (1 - alpha))


# ---------- WCAG 2.x contrast ----------
def relative_luminance(hex_c):
    def f(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(c) for c in hex_to_rgb(hex_c))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b):
    hi, lo = sorted((relative_luminance(a), relative_luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def verdicts(ratio):
    """(normal-text, large-text, non-text) verdicts for a ratio."""
    normal = 'AAA' if ratio >= AAA_NORMAL else 'AA' if ratio >= AA_NORMAL else 'FAIL'
    large = 'AAA' if ratio >= AAA_LARGE else 'AA' if ratio >= AA_LARGE else 'FAIL'
    nontext = 'pass' if ratio >= AA_NONTEXT else 'FAIL'
    return normal, large, nontext


# ---------- suggestion ----------
def _scale(hex_c, factor):
    """Lighten (factor > 1) or darken (factor < 1) toward white/black."""
    r, g, b = hex_to_rgb(hex_c)
    if factor >= 1:
        t = 1 - 1 / factor
        return rgb_to_hex(r + (1 - r) * t, g + (1 - g) * t, b + (1 - b) * t)
    t = 1 - factor
    return rgb_to_hex(r * (1 - t), g * (1 - t), b * (1 - t))


def suggest(fg, bg, target):
    """Nearest shade of fg (moved toward black or white) that clears `target`.

    Returns (hex, ratio) or None. Keeps the hue: it only walks lightness, so
    the suggestion still reads as the same colour rather than a new one.
    """
    best = None
    for direction in (0.995, 1.005):                 # darker, then lighter
        cur = fg
        for _ in range(400):
            cur = _scale(cur, direction)
            r = contrast_ratio(cur, bg)
            if r >= target:
                if best is None or r < best[1]:      # prefer the nearest pass
                    best = (cur, r)
                break
    return best


# ---------- output ----------
def _row(label, ratio, width=34):
    normal, large, nontext = verdicts(ratio)
    flag = '  <- FAIL' if normal == 'FAIL' else ''
    return (f'  {label:<{width}} {ratio:6.2f}:1   '
            f'normal {normal:<4} large {large:<4} non-text {nontext}{flag}')


def report_pairs(fg, backgrounds, target, do_suggest):
    print(f'\nFOREGROUND  {fg}')
    print('BACKGROUNDS')
    any_fail = False
    for bg in backgrounds:
        ratio = contrast_ratio(fg, bg)
        print(_row(bg, ratio))
        if ratio < target:
            any_fail = True
            if do_suggest:
                s = suggest(fg, bg, target)
                if s:
                    print(f'      -> {s[0]} clears {target} on {bg} '
                          f'at {s[1]:.2f}:1 (same hue, lightness shifted)')
                else:
                    print(f'      -> no shade of this hue clears {target} on {bg}; '
                          'change the background instead')
    return any_fail


def report_matrix(colors):
    width = max(len(c) for c in colors) + 2
    print('\nCONTRAST MATRIX  (rows = text, columns = background)')
    print(' ' * width + ''.join(f'{c:>10}' for c in colors))
    for fg in colors:
        cells = []
        for bg in colors:
            if fg == bg:
                cells.append(f'{"-":>10}')
                continue
            r = contrast_ratio(fg, bg)
            mark = '' if r >= AA_NORMAL else '*'
            cells.append(f'{r:>9.2f}{mark}')
        print(f'{fg:<{width}}' + ''.join(cells))
    print('\n  * below 4.5:1 — fails AA for normal text')


def report_on_color(fill):
    """The legible ink for text on a fill — chosen by MEASURED contrast.

    Picking by lightness alone gets mid-tone fills wrong: it hands white ink to
    a colour that black clears more comfortably. Both candidates are measured
    and the better one wins.
    """
    ranked = sorted((DARK_INK, LIGHT_INK),
                    key=lambda ink: -contrast_ratio(ink, fill))
    best, other = ranked
    rb, ro = contrast_ratio(best, fill), contrast_ratio(other, fill)
    print(f'\nFILL  {fill}')
    print(_row(f'{best}  (best)', rb))
    print(_row(f'{other}', ro))
    if rb < AA_NORMAL:
        print(f'\n  WARNING: no AA-legible on-colour. Best is {best} at {rb:.2f}:1, '
              f'AA needs {AA_NORMAL}.\n'
              '  Neither black nor white passes on this shade, so it is not a usable\n'
              '  text-bearing fill. Shift the fill lighter or darker until one ink\n'
              '  clears AA, or keep this shade as a non-text surface only.')
        return True
    print(f'\n  Use {best} for text on this fill ({rb:.2f}:1).')
    if rb < AAA_NORMAL:
        print(f'  Clears AA, not AAA (needs {AAA_NORMAL}).')
    return False


def main():
    ap = argparse.ArgumentParser(
        description='WCAG 2.x contrast ratios for a pair, a set, or a palette.',
        epilog='Thresholds: normal 4.5 (AA) / 7.0 (AAA) · large 3.0 / 4.5 · non-text 3.0',
    )
    ap.add_argument('colors', nargs='*',
                    help='foreground then one or more backgrounds; '
                         'with --matrix, the palette; with --on, the fill')
    ap.add_argument('--matrix', action='store_true',
                    help='every colour as text on every other colour')
    ap.add_argument('--on', metavar='FILL',
                    help='pick the legible ink (black or white) for a fill')
    ap.add_argument('--alpha', type=float, metavar='A',
                    help='foreground opacity 0-1; composited over each background '
                         'before measuring (opacity is not colour)')
    ap.add_argument('--large', action='store_true',
                    help='judge against the large-text threshold (3.0) instead of 4.5')
    ap.add_argument('--suggest', action='store_true',
                    help='for each failing pair, propose the nearest passing shade')
    args = ap.parse_args()

    try:
        if args.on:
            failed = report_on_color(normalize_hex(args.on))
            sys.exit(1 if failed else 0)

        colors = [normalize_hex(c) for c in args.colors]

        if args.matrix:
            if len(colors) < 2:
                sys.exit('error: --matrix needs at least two colours')
            report_matrix(colors)
            sys.exit(0)

        if len(colors) < 2:
            ap.print_usage()
            sys.exit('error: give a foreground and at least one background '
                     '(or use --matrix / --on)')

        fg, backgrounds = colors[0], colors[1:]
        target = AA_LARGE if args.large else AA_NORMAL

        if args.alpha is not None:
            if not 0.0 <= args.alpha <= 1.0:
                sys.exit('error: --alpha must be between 0 and 1')
            print(f'\nCompositing {fg} at {args.alpha:g} opacity over each background:')
            for bg in backgrounds:
                flat = composite(fg, bg, args.alpha)
                ratio = contrast_ratio(flat, bg)
                print(f'  on {bg} -> {flat}')
                print(_row(f'{flat} on {bg}', ratio))
            sys.exit(0)

        any_fail = report_pairs(fg, backgrounds, target, args.suggest)
        print()
        sys.exit(1 if any_fail else 0)

    except ValueError as e:
        sys.exit(f'error: {e} — expected #RGB or #RRGGBB')


if __name__ == '__main__':
    main()
