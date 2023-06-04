# Overview

This is a pretty simple P2P bridge between two addresses written in Golang. The idea is to
be able to communicate with someone with just their IP

[Software Demo Video](https://youtu.be/dDOIa8qKoeQ)

# Development Environment
* IntelliJ Ultimate IDEA
* git / Github
* Golang 1.20.4
* Net
* buffio

This was written in Golang because it has quite good networking abilities. I used the net module because it can handle
connections between two IP addresses such as listening for a connection. I used buffio to stream the data to each client.

# Useful Websites

* [Golang Docs](https://go.dev/doc/)
* [Golang Net Docs](https://pkg.go.dev/net)
* [Golang buffio Docs](https://pkg.go.dev/bufio)
* [What is P2P](https://www.blockchain-council.org/blockchain/peer-to-peer-network/)

# Future Work
- Create a UI
- add a layer of protection
- create a middle man server to mask IPs

How to run:
Run this on both instances:
```
go run main.go
```