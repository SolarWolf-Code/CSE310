# Overview

RustWS is a simple example of a webserver written in Rust. The purpose of this project is to demonstrate the use of Rust as a programming language and the performance we can expect from it.

[Demo of RustWS](https://youtu.be/Jb9dUYCJBVc)

# Development Environment
* Intellij IDEA
* Rust
* Cargo
* Git
* GitHub
* Tokio
* Reqwest
* Serde

As shown above I used the Rust programming language and I used several popular libraries to write the webserver. Tokio is a library that allows for asynchronous programming in Rust. Reqwest is a library that allows for HTTP requests to be made. Serde is a library that allows for serialization and deserialization of data.

# Useful Websites
- [Tokio Docs](https://docs.rs/tokio/latest/tokio/)
- [Reqwest Docs](https://docs.rs/reqwest/latest/reqwest/)
- [Rust Beginner's Guide](https://blog.jetbrains.com/rust/2023/02/21/learn-rust-with-jetbrains-ides/)

# Future Work
- Add more functionality to the webserver
- Add more error handling
- Add CSS and HTML to the webserver
- Provide better testing for the ideal performance range of the webserver


How to run:
`cargo run --release --bin RustWS` This is for the main webserver
`cargo run --release --bin benchmark` This we need to be ran after the webserver is started