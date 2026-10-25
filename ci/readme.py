"""readme.py: README.md = intro + index of results/<wave>-<run>/summary.md (newest first) + the newest summary of each wave."""
import glob
import os

intro = open("ci/README-intro.md").read()
def run_id(p):
    tail = os.path.basename(os.path.dirname(p)).rsplit("-", 1)[-1]
    return int(tail) if tail.isdigit() else 0


runs = sorted(glob.glob("results/*/summary.md"), key=run_id, reverse=True)
lines = [intro, "", "## Results", ""]
seen = set()
for p in runs:
    d = os.path.dirname(p)
    wave = os.path.basename(d).rsplit("-", 1)[0]
    lines.append(f"- [{os.path.basename(d)}]({p})" + ("" if wave in seen else " (latest of its wave)"))
    seen.add(wave)
open("README.md", "w").write("\n".join(lines) + "\n")
