## **Over The Edge**
### Description
<sup>Author: kavigihan</sup><br>
Numbers are fun!! 🔢

`edge.ctf.intigriti.io 1337`<br>
[over_the_edge.py](./over_the_edge.py)

### Solution
```sh
$ nc edge.ctf.intigriti.io 1337
Time to jump over the edge!
1234
Try again.
```
Look at function `process_input()`
```py
def process_input(input_value):
    num1 = np.array([0], dtype=np.uint64)
    num2 = np.array([0], dtype=np.uint64)
    num2[0] = 0
    a = input_value
    if a < 0:
        return "Exiting..."
    num1[0] = (a + 65)
    if (num2[0] - num1[0]) == 1337:
        return 'You won!\n'
    return 'Try again.\n'
```
`num2 - num1` need to equal to `1337`<br>
In Maths format `0 - (input + 65) = 1337` but the input can't be lower than 0 otherwise the program will return `Exiting...` which we don't want that.
If we look a bit up in the function. we will see that the type of `num1` and `num2` is **uint64**

> uint64	Unsigned integer (0 to 18446744073709551615)
{: .prompt-info }

If the input is `18446744073709551550(18446744073709551615 - 65)`<br>
the result: `num1 = 18446744073709551615` | `0(num2) - num1 = 1`

`0 - 18446744073709551551615 = -18446744073709551551615` is out of uint64's range. It return back to `1`<br>
`0 - 18446744073709551551614 = -18446744073709551551614` it return back to `2`<br>
`0 - 18446744073709551551613 = -18446744073709551551613` it return back to `3`

It is **integer overflow**.
Now we know the idea of it. Next let's use some maths.<br> 

So we need `0(num2) - num1 = 1337`. num1 should be `18446744073709550279 (18446744073709551615-1336)`. then the input have to be `18446744073709550214 (18446744073709550279-65)` If the result is 1337, the function will return `You won!` and the program will give us a flag.

```bash
$ nc edge.ctf.intigriti.io 1337
Time to jump over the edge!
18446744073709550214
INTIGRITI{fUn_w1th_1nt3g3r_0v3rfl0w_11}
```
It worked!
> Flag: INTIGRITI{fUn_w1th_1nt3g3r_0v3rfl0w_11}
