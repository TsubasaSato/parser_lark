import python_parser from program

data=[]
for _ in range(100):
    data.append(program())
    time.sleep(5)
    print("slept")
print("min/avg/max:{}/{}/{}".format(min(data),sum(data)/len(data),max(data)))
