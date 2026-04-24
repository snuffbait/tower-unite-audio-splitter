import sys, os, subprocess

def go(cmd):
    with open(os.devnull, "wb") as n:
        subprocess.Popen(cmd, stdout=n, stderr=n).wait()

path = sys.argv[1]
name = os.path.splitext(os.path.basename(path))[0]
out = os.path.join(os.path.dirname(os.path.abspath(path)), name)
os.makedirs(out, exist_ok=True)

dur = float(subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", path],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE
).stdout.strip())

bitrate = max(48, min(int((38 * 1024 * 1024 * 8) / dur / 1000), 320))
chunk = dur / 10

for i in range(10):
    print(f"{i+1}/10", flush=True)
    go(["ffmpeg", "-y", "-ss", str(i * chunk), "-t", str(chunk),
        "-i", path, "-c:a", "libvorbis", "-b:a", f"{bitrate}k", f"{out}/{i+1}.ogg"])

input("done")