# Exbitron.com API 

#### How to generate signature

```js
const crypto = require("crypto");
const util = require("util");
const request = require("request");

var impl = {
    // settings
    base_url : "https://www.exbitron.com",
    base_path: "/api/v2",
    access_key: '*****',
    secret: '*****',

    // internal methods
    signature: signature,
    payload: payload,
    params_string: params_string,
    url: url,

    get_private: get_private,
    exec_req: exec_req,
    exec_private: exec_private,

    // dependencies
    request: request,
    crypto: crypto
};

function exec_req(method, path, params, query_params_str) {
    var p = new Promise(function(resolve, reject) {
      var req_url = impl.url(path, params, query_params_str);
      impl.request({uri: req_url, method: method}, function(error, response, body) {
        if (error) {
            reject(error)
        } else {
            resolve(body)
        }
      });
    });

    return p.then(function(data){
      return JSON.parse(data)
    })
}

function params_string(params) {
    var str = "";
    var sorted_keys = Object.keys(params);
    sorted_keys.sort();
    for(var key of sorted_keys) {
      str += util.format("%s=%s&", key, params[key])
    }
    return str
}

function url(path, params, query_params_str) {
    var params_str = query_params_str; // passed qp string has prio over hash
    if (params_str == null)
      params_str = impl.params_string(params);
    return util.format("%s%s/%s?%s", impl.base_url, impl.base_path, path, params_str)
}

function payload(method, path, params) {
    var temp_str = impl.params_string(params);
    var params_str = temp_str.substring(0, temp_str.length - 1);
    return util.format("%s|%s/%s|%s", method, impl.base_path, path, params_str)
}

function signature(payload, secret) {
    return impl.crypto.createHmac('sha256', secret).update(payload).digest("hex");
}

function exec_private(method, path, query_params, tonce) {
    var params = query_params || {};

    params["tonce"] = tonce || Date.now();
    params["access_key"] = impl.access_key;

    var payload_ = impl.payload(method, path, params);
    var signature_ = impl.signature(payload_, impl.secret);
    var qp_str = impl.params_string(params) + util.format("signature=%s", signature_);

    return impl.exec_req(method, path, params, qp_str)
}

function get_private(path, query_params, tonce) {
    return impl.exec_private("GET", path, query_params, tonce)
}

function post(path, params, query_params_str) {
    return impl.exec_req("POST", path, params, query_params_str)
}

function get(path, params, query_params_str) {
    return impl.exec_req("GET", path, params, query_params_str)
}
```


Usage

```js
const pair = 'rvlrvn';
api.get("depth", {market: pair}).then(function(data){
    console.log(data);
});
```