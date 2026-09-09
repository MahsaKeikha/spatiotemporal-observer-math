from pathlib import Path

path = Path("src/observer_math/__init__.py")
text = path.read_text(encoding="utf-8")
start = text.index("__all__ = [\n")
end = text.index("]\n", start)
header = text[: start + len("__all__ = [\n")]
body = text[start + len("__all__ = [\n") : end]
tail = text[end:]
lines = [line for line in body.splitlines() if line.strip()]
if not all(line.startswith('    "') and line.endswith('",') for line in lines):
    raise RuntimeError("unexpected __all__ format")
lines.sort(key=lambda line: line.strip()[1:-2])
path.write_text(header + "\n".join(lines) + "\n" + tail, encoding="utf-8")
