import subprocess,time
command="hping3 -I enp1s0f0 -q -c {0} -s 22222 -a 10.0.1.7 -i u{1} -S -p 11111 10.0.1.5"
data=[]

pps=100
us=int(1000000/pps)
count=pps*5
"""
def run_and_capture(cmd):
    '''
    :param cmd: str 実行するコマンド.
    :rtype: str
    :return: 標準出力.
    '''
    # ここでプロセスが (非同期に) 開始する.
    proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    buf = []
    a=b'--- 10.0.1.5 hping statistic ---\n'

    while True:
        # バッファから1行読み込む.
        line = proc.stdout.readline()
        print(line)
        # バッファが空 + プロセス終了.
        if a == line:
            
    proc.terminate()
    return buf[-2]"""
for _ in range(1):
    proc = subprocess.run(command.format(count,us),shell=True,stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(proc.stdout.decode("utf8"))
    #print(run_and_capture(command.format(count,us)))
    


