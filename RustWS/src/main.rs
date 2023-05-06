use std::error::Error;
use tokio::net::TcpListener;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use reqwest;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;
    println!("Listening on: {}", "127.0.0.1:8080");

    loop {
        let (mut socket, _) = listener.accept().await?;

        tokio::spawn(async move {
            let mut buffer = [0; 1024];
            socket.read(&mut buffer).await.unwrap();

            let response = if buffer.starts_with(b"GET /randomcard") {
                // Make a request to Scryfall API
                let response = reqwest::get("https://api.scryfall.com/cards/random").await.unwrap();
                let card_json = response.text().await.unwrap();

                // Extract the name of the card from the JSON response
                let card_name = serde_json::from_str::<serde_json::Value>(&card_json)
                    .unwrap()
                    .get("name")
                    .unwrap()
                    .as_str()
                    .unwrap()
                    .to_owned();
                println!("The card name is: {}", card_name);

                format!(
                    "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {}\r\n\r\n",
                    card_json.len()
                ).to_owned() + &card_json
            } else if buffer.starts_with(b"GET / ") {
                // Greet the user when they visit the root URL
                println!("Hello, world!");
                "HTTP/1.1 200 OK\r\n\r\nHello, world!".to_owned()
            } else {
                // Return a 404 page for all other URL paths
                "HTTP/1.1 404 NOT FOUND\r\n\r\n404 Page Not Found".to_owned()
            };
            socket.write_all(response.as_bytes()).await.unwrap();
        }).await.unwrap(); // add this line to wait for the task to complete before continuing
    }
}
