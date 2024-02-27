import requests
import base64
from http_utils import *

BASE_API_URL = "https://06zdgzxbea.execute-api.us-east-1.amazonaws.com/dev"

def test_list_buckets():
    url = BASE_API_URL + '/list'
    response = get(url)
    assert response['statusCode'] == 200
    assert response['body'] != None
    assert 'hw05-jonathan-ameri' in response['body']

def test_list_objects():
    url = BASE_API_URL + '/hw05-jonathan-ameri'
    response = get(url)
    assert response['statusCode'] == 200
    assert response['body'] != None
    # may have to update the file, unsure what's in the bucket
    assert 'test.txt' in response['body']

def test_post_object():
    url = BASE_API_URL + '/hw05-jonathan-ameri'
    post_data = create_post_data_for_post_object('hw05-jonathan-ameri', 'test_file.txt', 'hello world')
    response = post(url, post_data)
    assert response['statusCode'] == 200
    assert response['body'] != None
    assert 'test_file.txt' in response['body']

def test_delete_object():
    url = BASE_API_URL + '/hw05-jonathan-ameri/test_file.txt'
    data = create_data_for_del_object('hw05-jonathan-ameri', 'test_file.txt')
    response = delete(url, data)
    assert response['statusCode'] == 200
    assert response['body'] != None
    assert 'test_file.txt' not in response['body']

 