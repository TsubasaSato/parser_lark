import subprocess,time
command="hping3 -I enp1s0f0 -c {0} -s 22222 -a 10.0.1.7 -i u{1} -S -p 11111 10.0.1.5"
data=[]

pps=100
us=int(1000000/pps)
count=pps*5

def run_and_capture(cmd):
    '''
    :param cmd: str 実行するコマンド.
    :rtype: str
    :return: 標準出力.
    '''
    # ここでプロセスが (非同期に) 開始する.
    proc = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    buf = []
    a=[b'Calling target program-options parser\n', b'Adding interface enp1s0f0 as port 1\n', b'Adding interface enp1s0f1 as port 2\n']

    while True:
        # バッファから1行読み込む.
        line = proc.stdout.readline()
        buf.append(line)
        print(buf)

        # バッファが空 + プロセス終了.
        if buf==a:
            break
    proc.terminate()

for _ in range(1):
    run_and_capture(command.format(count,us))
    


