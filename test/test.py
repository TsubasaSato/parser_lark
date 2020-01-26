import subprocess,time

data=[]
for _ in range(100):
    t1=time.time()
    proc=subprocess.Popen(["python3","./python_parser.py",
                           "/home/tsubasa/learnP4/TcpSyn_comment.py"],stdout=subprocess.PIPE)
    time.sleep(5)
    t2=time.time()
    print(t2-t1)
    data.append(t2-t1)
print("min/avg/max:{}/{}/{}".format(min(data),sum(data)/len(data),max(data)))
