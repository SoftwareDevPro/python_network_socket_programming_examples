
# Python Networking Example to scan a target host for open ports

## To Run

```
python port_scanner.py <mode>
```

where mode is defined to be one of:

* 1: well-known ports (1-1024)
* 2: all non-private ports (1-49152)
* 3: secure application ports (20, 21, 22, 23, 25, 53, 80, 110, 443)
* 4: user-defined ports (entered by user)
