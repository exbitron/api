# Exbitron.com API 

#### Install

```
curl -sL https://github.com/exbitron/api/raw/main/php/exbitron.php > exbitron.php
```

#### Usage

```php
<?php
require_once 'exbitron.php';

$secret_key = '*****';
$api_key = '*****';
$url = '/api/v2/peatio/account/balances';

$api = new Exbitron($api_key, $secret_key);
$response = $api->getRequest($url);

print_r($response);
```

#### How to get OTP code 

You will need `MFA code` from your 2FA account:

![imgotpmfa](https://user-images.githubusercontent.com/6382002/137104288-dbe63284-49cb-4664-b800-a64bff5fb6c4.png)

```php
require_once 'exbitron.php';

$mfa_codey = 'MFACODE****EXAMPLE';
$api = new Exbitron();
$otp = $api->get2FACode($mfa_code);

print_r($otp);
```
