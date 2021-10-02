# Exbitron.com API 

#### How to generate signature

```ruby
require 'openssl'

nonce = (Time.now.to_f.round(3)*1000).to_i
api_key = '*****'
secret = '*****'
OpenSSL::HMAC.hexdigest("SHA256", secret, nonce + api_key)
```
