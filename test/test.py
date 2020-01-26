import subprocess,time

data=[]
for _ in range(100):
    t1=time.time()
    subprocess.call(["python3","./python_parser.py",
                           "/home/tsubasa/learnP4/TcpSyn_comment.py"])
    t2=time.time()
    time.sleep(5)
    print(t2-t1)
    data.append(t2-t1)
print("min/avg/max:{}/{}/{}".format(min(data),sum(data)/len(data),max(data)))
