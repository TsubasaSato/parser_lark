import subprocess,time
command="hping3 -I enp1s0f0 -c {0} -s 22222 -a 10.0.1.7 -i u{1} -S -p 11111 10.0.1.5"
data=[]

pps=100
us=int(1000000/pps)
count=pps*5

for _ in range(100):
    out=subprocess.check_output(command.format(count,us),shell=True)
    print(out)


