from pathlib import Path

path = Path("README.md")
text = path.read_text(encoding="utf-8")
old = "The physics pipeline is an explanatory diagram and is not included in the 27 scientific-result figure count."
new = "The physics pipeline is an explanatory diagram and is not included in the 28 scientific-result figure count."
if text.count(old) != 1:
    raise RuntimeError(f"expected one stale figure-count sentence, found {text.count(old)}")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
