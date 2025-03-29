[sib-coder@fedora osint]$ sudo docker run -p 4444:4444 -p 30555:30555 --name osint osint
Warning: _curses.error: setupterm: could not find terminfo database

Terminal features will not be available.  Consider setting TERM variable to your current terminal name (or xterm).
[x] Trying to bind to :: on port 4444
[x] Trying to bind to :: on port 4444: Trying ::
[+] Trying to bind to :: on port 4444: Done
[x] Waiting for connections on :::4444
[+] Waiting for connections on :::4444: Got connection from ::ffff:172.17.0.1 on port 33866
[x] Waiting for connections on :::4444
[*] Closed connection to ::ffff:172.17.0.1 port 33866
Traceback (most recent call last):
  File "/app/lenin.py", line 50, in work_once
    workline= server_conn.recvline().decode('utf-8')
  File "/usr/local/lib/python3.10/dist-packages/pwnlib/tubes/tube.py", line 497, in recvline
    return self.recvuntil(self.newline, drop = not keepends, timeout = timeout)
  File "/usr/local/lib/python3.10/dist-packages/pwnlib/tubes/tube.py", line 340, in recvuntil
    res = self.recv(timeout=self.timeout)
  File "/usr/local/lib/python3.10/dist-packages/pwnlib/tubes/tube.py", line 105, in recv
    return self._recv(numb, timeout) or b''
  File "/usr/local/lib/python3.10/dist-packages/pwnlib/tubes/tube.py", line 175, in _recv
    if not self.buffer and not self._fillbuffer(timeout):
  File "/usr/local/lib/python3.10/dist-packages/pwnlib/tubes/tube.py", line 154, in _fillbuffer
    data = self.recv_raw(self.buffer.get_fill_size())
  File "/usr/local/lib/python3.10/dist-packages/pwnlib/tubes/sock.py", line 35, in recv_raw
    raise EOFError
EOFError

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.10/dist-packages/pwnlib/tubes/sock.py", line 65, in send_raw
    self.sock.sendall(data)
BrokenPipeError: [Errno 32] Broken pipe

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/app/lenin.py", line 135, in <module>
    main()
  File "/app/lenin.py", line 129, in main
    work_once(jury, cmd.team_id)
  File "/app/lenin.py", line 102, in work_once
    server_conn.sendline(b'\nEOFError occurred')
  File "/usr/local/lib/python3.10/dist-packages/pwnlib/tubes/tube.py", line 816, in sendline
    self.send(line + self.newline)
  File "/usr/local/lib/python3.10/dist-packages/pwnlib/tubes/tube.py", line 795, in send
    self.send_raw(data)
  File "/usr/local/lib/python3.10/dist-packages/pwnlib/tubes/sock.py", line 70, in send_raw
    raise EOFError
EOFError
^CException ignored in: <module 'threading' from '/usr/lib/python3.10/threading.py'>
Traceback (most recent call last):
  File "/usr/lib/python3.10/threading.py", line 1567, in _shutdown
    lock.acquire()
KeyboardInterrupt: 

