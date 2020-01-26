import subprocess

data=[]
for _ in range(100):
    proc=subprocess.Popen(["python3","./python_parser.py",
                           "/home/tsubasa/learnP4/TcpSyn_comment.py"],stdoutsubprocess.PIPE)
    time.sleep(5)
    print(proc.communicate())
    print("slept")
#print("min/avg/max:{}/{}/{}".format(min(data),sum(data)/len(data),max(data)))
