# HTTP Bottom Up 
## Exercises

---

# Day 1

---

## Exercise 1.1

Connect using `nc` to `http00.pipal.in` on port 7, which runs an echo server. It should respond back whatever you type. 

You can press `Ctrl+D` to end the input.

---

## Exercise 1.2

Try sending an email to `<yourname>@mailinator.com` only using netcat and see how that works. What happens if you add additional headers in addition to To, From and Subject.

---
### Exercise 1.3

Write an echo client program that takes host name as argument and sends a message `Hello Socket` to the echo server running on port 7 on that host and prints the response back.

    $ python echo_client.py http00.pipal.in
    Hello Socket

---

### Exercise 1.4


Write a program calc_server.py that provides calculator service. The program should accept the input as a single line as shown in the examples below and respond back with the answer. The program should take the port number as argument and listen on that port.

    ADD 2 3
    5
    SUB 9 3
    6
    MUL 4 5
    20
    DIV 8 2
    4

---
### Exercise 1.5

Write a program to measure the time taken to send one KB (1024 bytes) of data to echo server (port 7) on http00.pipal.in and receive the response.


Hint: Open a connection and send 1KB message and receive response 1000 or 10000 times. Measure the total time and take average.

---

# Day 2

--- 

## Exercise 2.1

Improve the `urlopen` function written earlier to follow redirects.

For example, if you try to open any one of the URLs

    http://thehindu.com/
    http://thehindu.com/cities/bangalore
    http://httpbin.org/redirect-to?url=http://www.thehindu.com/news/cities/bangalore/

the server will respond back with a redirect. Instead of printing the redirect, following the redirect and get the redirected page.

Try: `curl -v -L http://thehindu.com/`

---
## Exercise 2.2

Improve the hello program to take the name of the person to greet from the URL.

    $ curl http://localhost:8000/alice
    Hello alice!

    $ curl http://localhost:8000/bob
    Hello bob!

---

## Exercise 2.3

Improve the hello program further to take an optional query parameter repeats, when specified it repeat the message so many times.

    $ curl http://localhost:8000/alice?repeats=3
    Hello alice!
    Hello alice!
    Hello alice!

---

## Exercise 2.4

Improve the httpserver to serve static files to provide directory listing.

---

## Exercise 2.5

Improve the WSGI hello program to take the name of the person to greet from the URL.

    $ curl http://localhost:8000/alice
    Hello alice!

    $ curl http://localhost:8000/bob
    Hello bob!

---
## Code Examples for this workshop

git clone https://github.com/anandology/httpbottomup
