import subprocess,time
command="hping3 -I enp1s0f0 -q -c {0} -s 22222 -a 10.0.1.7 -i u{1} -S -p 11111 10.0.1.5"
data=[]


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
        buf.append(line)
        # バッファが空 + プロセス終了.
        if len(buf) >3:
            break
    proc.terminate()
    return buf

for x in range(35):
    pps=200*(int(x)+1)
    us=int(1000000/pps)
    count=pps*50

    data.append(run_and_capture(command.format(count,us)))

print(data)
with open(r"./zikken.txt","w") as f:
    f.write(str(data))


