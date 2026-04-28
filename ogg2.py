import sys,os,subprocess
go=lambda cmd:subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).wait()
p=sys.argv[1];n=os.path.splitext(os.path.basename(p))[0];b=os.path.dirname(os.path.abspath(p))
o1=os.path.join(b,n+"_part1");o2=os.path.join(b,n+"_part2")
os.makedirs(o1,exist_ok=True);os.makedirs(o2,exist_ok=True)
dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",p],stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.strip())
C=900;chunks=int(dur/C)+(1 if dur%C else 0);half=chunks//2
for i in range(chunks):
 s=i*C;l=min(C,dur-s)
 if l<1:break
 o=o1 if i<half else o2;idx=(i+1)if i<half else(i-half+1)
 print(f"{i+1}/{chunks}",flush=True)
 go(["ffmpeg","-y","-ss",str(s),"-t",str(l),"-i",p,"-c:a","libvorbis","-b:a","48k","-ac","1","-ar","44100",f"{o}/{idx}.ogg"])
input("done")
