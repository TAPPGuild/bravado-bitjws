import bitjws
import httpretty
import json
import os
import pytest
from bravado.swagger_model import load_file
from bravado_bitjws.client import BitJWSSwaggerClient

specurl = "%s/example/swagger.json" % os.path.realpath(os.path.dirname(__file__))
wif = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"

def test_init_WIF():
    client = BitJWSSwaggerClient.from_spec(load_file(specurl),
                                           'https://0.0.0.0:8002', privkey=wif)
    assert 'coin' in client.swagger_spec.definitions
    assert 'user' in client.swagger_spec.definitions
    ckey = client.coin.addCoin.swagger_spec.http_client.authenticator.privkey
    assert isinstance(ckey, bitjws.PrivateKey)
    assert wif == bitjws.privkey_to_wif(ckey.private_key)


def test_init_PrivateKey():
    privkey = bitjws.PrivateKey(bitjws.wif_to_privkey(wif))

    client = BitJWSSwaggerClient.from_spec(load_file(specurl),
                                           'https://0.0.0.0:8002',
                                           privkey=privkey)
    assert 'coin' in client.swagger_spec.definitions
    assert 'user' in client.swagger_spec.definitions
    ckey = client.coin.addCoin.swagger_spec.http_client.authenticator.privkey
    assert isinstance(ckey, bitjws.PrivateKey)
    assert bitjws.privkey_to_wif(privkey.private_key) == \
            bitjws.privkey_to_wif(ckey.private_key)

def test_init():
    client = BitJWSSwaggerClient.from_spec(load_file(specurl),
                                           'https://0.0.0.0:8002')
    assert 'coin' in client.swagger_spec.definitions
    assert 'user' in client.swagger_spec.definitions
    ckey = client.coin.addCoin.swagger_spec.http_client.authenticator.privkey
    assert isinstance(ckey, bitjws.PrivateKey)

def test_init_url_WIF():
    url = "http://spec.com/swagger.json"
    spec = load_file(specurl)
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, url,
                           body=json.dumps(spec))

    client = BitJWSSwaggerClient.from_url(url, privkey=wif)
    assert 'coin' in client.swagger_spec.definitions
    assert 'user' in client.swagger_spec.definitions
    ckey = client.coin.addCoin.swagger_spec.http_client.authenticator.privkey
    assert isinstance(ckey, bitjws.PrivateKey)
    assert wif == bitjws.privkey_to_wif(ckey.private_key)

    httpretty.disable()
    httpretty.reset()

def test_init_url_PrivateKey():
    privkey = bitjws.PrivateKey(bitjws.wif_to_privkey(wif))

    url = "http://spec.com/swagger.json"
    spec = load_file(specurl)
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, url,
                           body=json.dumps(spec))

    client = BitJWSSwaggerClient.from_url(url, privkey=privkey)
    assert 'coin' in client.swagger_spec.definitions
    assert 'user' in client.swagger_spec.definitions
    ckey = client.coin.addCoin.swagger_spec.http_client.authenticator.privkey
    assert isinstance(ckey, bitjws.PrivateKey)
    assert bitjws.privkey_to_wif(privkey.private_key) == bitjws.privkey_to_wif(ckey.private_key)

    httpretty.disable()
    httpretty.reset()

