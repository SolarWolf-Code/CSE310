use std::error::Error;
use std::time::Instant;
use tokio::sync::mpsc;
use tokio::time::{sleep, Duration};
use tokio::task;
use reqwest::Client;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // Number of concurrent users to simulate
    let num_users = 200;

    // Number of requests to send per user
    let num_requests = 10;

    // Base URL of the webserver
    let base_url = "http://localhost:8080";

    // Create a channel to communicate between the sender and receiver tasks
    let (mut sender, mut receiver) = mpsc::channel(num_users);

    // Spawn the sender tasks
    for _ in 0..num_users {
        let sender = sender.clone();
        task::spawn(async move {
            let client = Client::new();
            for _ in 0..num_requests {
                let start = Instant::now();
                let response = client.get(base_url).send().await;
                let duration = start.elapsed().as_millis();
                sender.send(duration).await.unwrap();
            }
        });
    }

    // Wait for all the sender tasks to complete
    drop(sender);

    // Collect the response times from the receiver task
    let mut response_times = Vec::new();
    while let Some(duration) = receiver.recv().await {
        response_times.push(duration);
    }

    // Calculate and print the statistics
    let num_requests = num_users * num_requests;
    let total_duration: u128 = response_times.iter().sum();
    let mean_duration = total_duration as f64 / num_requests as f64;
    let mut sorted_durations = response_times.clone();
    sorted_durations.sort();
    let p90_duration = sorted_durations[(num_requests * 9 / 10) as usize];
    let p99_duration = sorted_durations[(num_requests * 99 / 100) as usize];
    println!("Number of requests: {}", num_requests);
    println!("Mean duration: {:.2} ms", mean_duration);
    println!("90th percentile duration: {} ms", p90_duration);
    println!("99th percentile duration: {} ms", p99_duration);

    Ok(())
}
