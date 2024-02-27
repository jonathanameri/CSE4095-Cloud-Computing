'''
Tests for the hw06 API
'''
from http_utils import get, post, delete, \
    create_post_data_for_post_object, create_data_for_del_object

BASE_API_URL = "https://06zdgzxbea.execute-api.us-east-1.amazonaws.com/dev"

def test_list_buckets():
    '''
    test_list_buckets. make a call to the API to list the buckets
    '''
    url = BASE_API_URL + '/list'
    response = get(url)
    assert response['statusCode'] == 200
    assert response['body'] is not None
    assert 'hw05-jonathan-ameri' in response['body']

def test_list_objects():
    '''
    test_list_objects. make a call to the API to list the objects in a bucket
    '''
    url = BASE_API_URL + '/hw05-jonathan-ameri'
    response = get(url)
    assert response['statusCode'] == 200
    assert response['body'] is not None
    # may have to update the file, unsure what's in the bucket
    assert 'test.txt' in response['body']

def test_post_object():
    '''
    test_post_object. make a call to the API to post an object to a bucket
    '''
    url = BASE_API_URL + '/hw05-jonathan-ameri'
    post_data = create_post_data_for_post_object('hw05-jonathan-ameri',
                                                 'test_file.txt', 'hello world')
    response = post(url, post_data)
    assert response['statusCode'] == 200
    assert response['body'] is not None
    assert 'test_file.txt' in response['body']

def test_delete_object():
    '''
    test_delete_object. make a call to the API to delete an object from a bucket
    '''
    url = BASE_API_URL + '/hw05-jonathan-ameri/test_file.txt'
    data = create_data_for_del_object('hw05-jonathan-ameri', 'test_file.txt')
    response = delete(url, data)
    assert response['statusCode'] == 200
    assert response['body'] is not None
    assert 'test_file.txt' not in response['body']
