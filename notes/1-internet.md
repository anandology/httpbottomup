# The Internet

## Finding IP address of a host

The host command can be used to resolve any host name.

    $ host google.com
    google.com has address 216.58.197.46
    google.com has IPv6 address 2404:6800:4007:807::200e
    google.com mail is handled by 30 alt2.aspmx.l.google.com.
    google.com mail is handled by 50 alt4.aspmx.l.google.com.
    google.com mail is handled by 10 aspmx.l.google.com.
    google.com mail is handled by 40 alt3.aspmx.l.google.com.
    google.com mail is handled by 20 alt1.aspmx.l.google.com.

It can also be used to do a reverse lookup.

    $ host 216.58.197.46
    46.197.58.216.in-addr.arpa domain name pointer maa03s20-in-f46.1e100.net.
    46.197.58.216.in-addr.arpa domain name pointer maa03s20-in-f14.1e100.net.

We can also specify which nameserver to use as optional second argument to host command.

    $ host pipal.in ns1.digitalocean.com
    Using domain server:
    Name: ns1.digitalocean.com
    Address: 173.245.58.51#53
    Aliases:

    pipal.in has address 139.59.9.235
    pipal.in mail is handled by 10 mail.pipal.in.

The ns1.digitalocean.com is a private DNS server that contains only the domains it manages. If we try some other domain, it will fail.

    $ host google.com
    Using domain server:
    Name: ns1.digitalocean.com
    Address: 173.245.58.51#53
    Aliases:

There are some public DNS servers, if you wish to try them out. 

* 8.8.8.8 - Google Public DNS
* 8.8.4.4 - Google Public DNS
* resolver1.opendns.com - Open DNS
* resolver2.opendns.com - Open DNS

The `dig` command is another interesting tool that can be used for resolving domain names.

    $ dig pipal.in
    ; <<>> DiG 9.8.3-P1 <<>> pipal.in
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 8547
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

    ;; QUESTION SECTION:
    ;pipal.in.              IN      A

    ;; ANSWER SECTION:
    pipal.in.           1799    IN      A       139.59.9.235

    ;; Query time: 318 msec
    ;; SERVER: 8.8.8.8#53(8.8.8.8)
    ;; WHEN: Thu Sep 15 23:13:45 2016
    ;; MSG SIZE  rcvd: 42

Another example:

    $ dig pipal.in mx
    ...
    ;; QUESTION SECTION:
    ;pipal.in.              IN      MX

    ;; ANSWER SECTION:
    pipal.in.           1799    IN      MX      10 mail.pipal.in.
    ...

## Network Servers and Clients

The `telnet` and `nc` (netcat) are some nice unix utilities that'll allow us to connect to any remote server and communicate.

Lets try to connect to daytime server using telnet and nc.

    $ telnet http00.pipal.in 13
    Trying 139.59.25.206...
    Connected to http00.pipal.in.
    Escape character is '^]'.
    13 SEP 2016 06:50:48 UTC
    Connection closed by foreign host.

    $ nc http00.pipal.in 13
    13 SEP 2016 06:51:37 UTC

**Exercise:** Connect to `http00.pipal.in` on port 7, which runs an echo server. It'll respond back whatever you type. 

### Running a network server

The `nc` program can also work like a server. It'll respond back whatever we type in there. 

Lets start a server using `-l` option.

    $ nc -l localhost 12345

and start a client connected to the same port.

    $ nc localhost 12345

Now whatever you type at the client prompt will reach the server and whatever you type at the server prompt will reach the client. 

We'll use this later to explore HTTP servers as well.

## Example: Sending Email

Out of the many popular internet applications, applications SMTP and HTTP use textual protocols, making it easier to understand and experiment with them. The other applications like DNS, FTP etc. use transmit data in binary, which requires packing and unpacking it, often requires understanding of the protocol to inspect the data.

Lets play with SMTP protocol. We'll now send an email with hand.

    $ nc -c mail.mailinator.com 25 <<EOF
    HELO mail.mailinator.com
    MAIL FROM: <test@example.com>
    RCPT TO: <httpbottomup@mailinator.com>
    DATA
    To: HTTP Bottom Up <httpbottomup@mailinator.com>
    From: Test <test@example.com>
    Subject: Test mail

    Body of email.
    .
    QUIT
    EOF

The `-c` flag sends makes `nc` send carriage-return (`'\r'`) and line-feed (`'\n'`) characters for every new line, as expected by the SMTP protocol.

The mailinator.com is an interesting open email service, which allows anyone access any mailbox. You just need to go to the website and provide the mailbox name. After doing the above exercise, you'll be able to see that email in the "httpbottomup" mailbox.

**Exercise:** Try sending an email to `<yourname>@mailinator.com` and see how that works. What happens if you add additional headers in addition to To, From and Subject.

