<?php

require_once 'exbitron.php';

$secret_key = '*****';
$api_key = '*****';
$url = '/api/v2/peatio/account/balances';

$api = new Exbitron($api_key, $secret_key);
$response = $api->getRequest($url);

print_r($response);