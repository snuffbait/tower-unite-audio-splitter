import sys, os, subprocess

def go(cmd):
    with open(os.devnull, "wb") as n:
        subprocess.Popen(cmd, stdout=n, stderr=n).wait()

path = sys.argv[1]
name = os.path.splitext(os.path.basename(path))[0]
base = os.path.dirname(os.path.abspath(path))
out1 = os.path.join(base, name + "_part1")
out2 = os.path.join(base, name + "_part2")
os.makedirs(out1, exist_ok=True)
os.makedirs(out2, exist_ok=True)

dur = float(subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", path],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE
).stdout.strip())

chunk = 900
chunks = int(dur / chunk) + (1 if dur % chunk else 0)
half = chunks // 2

for i in range(chunks):
    start = i * chunk
    length = min(chunk, dur - start)
    if length < 1:
        break
    out = out1 if i < half else out2
    idx = (i + 1) if i < half else (i - half + 1)
    print(f"{i+1}/{chunks}", flush=True)
    go(["ffmpeg", "-y", "-ss", str(start), "-t", str(length),
        "-i", path, "-c:a", "libvorbis", "-b:a", "48k",
        "-ac", "1", "-ar", "44100", f"{out}/{idx}.ogg"])

input("done")