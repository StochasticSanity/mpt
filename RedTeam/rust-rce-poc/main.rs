// Adapted from Bryan's Python
// Author: Joseph Erdosy
//
// This script sends a GET request to a specified URL with the
// hostname and username as URL parameters.

use std::env;
use attohttpc;

fn main() {
    // Customize IP and port here
    let ip = "localhost";
    let port = 8080;

    // Get the hostname and username
    let hostname = hostname::get().unwrap();
    let username = env::var("USER").unwrap();

    // Build the URL
    let url = format!(
        "http://{}:{}/?hostname={}&username={}",
        ip, port, hostname.to_string_lossy(), username
    );

    // Send the GET request to the Go server
    let response = attohttpc::get(&url).send().unwrap().text().unwrap();
    println!("{}", response)
}




