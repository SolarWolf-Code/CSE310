package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"time"
)

func main() {
	fmt.Println("=== Peer-to-Peer Communication ===")
	fmt.Print("Enter your address: ")
	reader := bufio.NewReader(os.Stdin)
	address, _ := reader.ReadString('\n')
	address = strings.TrimSpace(address)

	fmt.Print("Enter the other computer's address: ")
	otherAddress, _ := reader.ReadString('\n')
	otherAddress = strings.TrimSpace(otherAddress)

	go startListening(address)
	sendMessage(otherAddress)
}

func startListening(address string) {
	listener, err := net.Listen("tcp", address)
	if err != nil {
		log.Fatal("Error listening:", err)
	}

	defer listener.Close()
	fmt.Println("Listening for incoming connections on", address)

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Fatal("Error accepting connection:", err)
		}

		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	fmt.Println("Connected to", conn.RemoteAddr().String())

	reader := bufio.NewReader(conn)

	for {
		message, err := reader.ReadString('\n')
		if err != nil {
			log.Println("Connection closed by", conn.RemoteAddr().String())
			break
		}
		fmt.Println("Received message:", message)
	}
}

func sendMessage(address string) {
	for {
		fmt.Println(fmt.Sprintf("Attempting to connect to %s, please make sure it is discoverable and searching as well...", address))

		conn, err := net.Dial("tcp", address)
		if err != nil {
			time.Sleep(time.Second * 2) // Retry after 2 seconds
			continue
		}

		fmt.Println(fmt.Sprintf("Connected to %s", address))
		defer conn.Close()

		reader := bufio.NewReader(os.Stdin)
		writer := bufio.NewWriter(conn)

		for {
			fmt.Println("Enter message to send (or 'quit' to exit):")
			message, _ := reader.ReadString('\n')
			message = strings.TrimSpace(message)

			if message == "quit" {
				break
			}

			_, err = writer.WriteString(message + "\n")
			if err != nil {
				log.Fatal("Error sending message:", err)
			}
			err = writer.Flush()
			if err != nil {
				log.Fatal("Error sending message:", err)
			}
		}

		break
	}
}
