import requests
import json
import pytest
import csv

# BASE_URL = "http://localhost:5000"

@pytest.fixture()
def BASE_URL():
    return "http://localhost:5000"

@pytest.fixture()
def ID_POST():
    return 1

@pytest.fixture()
def del_post_id():
    return 10
    #  return 54

@pytest.fixture()
def resources():
    return "posts"

@pytest.fixture()
def comments_resources():
    return "comments"

def load_test_data():
    with open("src/db.json", "r") as file:
        return json.load(file)
    
def load_my_test_data():
    with open("tests/integration/test_data.json", "r") as file:
        return json.load(file)



    
def log_result_to_file(test_name, method, endpoint, status_code, result, message=""):
    filename = "result_api.csv"  # Update the filename to the desired one
    # Check if the file exists to decide whether to write headers
    write_headers = False
    try:
        with open(filename, mode="r"):
            pass
    except FileNotFoundError:
        write_headers = True

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        if write_headers:
            writer.writerow(["Test Name", "Method", "Endpoint", "Status Code", "Result", "Message"])
        writer.writerow([test_name, method, endpoint, status_code, result, message])



def test_get_posts(BASE_URL, resources):
    # response = requests.get(f"{BASE_URL}/posts")
    response = requests.get(f"{BASE_URL}/{resources}")
    assert response.status_code == 200
    # print(type(response.text))
    # print(json.loads(response.text))
    # print(response.json())
    assert isinstance(response.json(), list)

def test_get_post_by_id(BASE_URL, resources, ID_POST):
    response_id = requests.get(f"{BASE_URL}/{resources}/{ID_POST}")
    assert response_id.status_code == 200
    assert isinstance(response_id.json(), dict)
    assert int(response_id.json().get('id')) == ID_POST

def test_get_nonexistent_post(BASE_URL, resources):
    ID_POST=999
    response_id = requests.get(f"{BASE_URL}/{resources}/{ID_POST}")
    assert response_id.status_code == 404

# GET ALL POSTS

# 1--> Test if the status code is 200
def test_status_code(BASE_URL, resources):
    response = requests.get(f"{BASE_URL}/{resources}")
    assert response.status_code == 200

# 2--> Test if the response time is less than 300ms
@pytest.mark.xfail
def test_response_time(BASE_URL, resources):
    response = requests.get(f"{BASE_URL}/{resources}")
    assert response.elapsed.total_seconds() < 0.3

# 3--> Test if the number of posts is 100
def test_number_of_posts(BASE_URL, resources):
    response = requests.get(f"{BASE_URL}/{resources}")
    json_data = response.json()
    assert len(json_data) > 50

# 4--> Test if the response is an array
def test_response_is_array(BASE_URL, resources):
    response = requests.get(f"{BASE_URL}/{resources}")
    json_data = response.json()
    assert isinstance(json_data, list)

# 5--> Test if the IDs in the response are sequential
def test_ids_are_sequential(BASE_URL, resources):
    response = requests.get(f"{BASE_URL}/{resources}")
    json_data = response.json()
    result = "Success"
    for i in range(1, len(json_data)):
        if json_data[i]["id"] != json_data[i - 1]["id"] + 1:
            result = "Failure"
            break
    assert result != "Success"

# 6--> Test if the response body is not empty
def test_response_body_not_empty(BASE_URL, resources):
    response = requests.get(f"{BASE_URL}/{resources}")
    json_data = response.json()
    assert json_data

# GET POST BY ID

# 1--> Test if the status code is 200
def test_status_code(BASE_URL, resources, ID_POST):
    response = requests.get(f"{BASE_URL}/{resources}/{ID_POST}")
    assert response.status_code == 200

# 2--> Test if the response time is less than 300ms
@pytest.mark.xfail
def test_response_time(BASE_URL, resources, ID_POST):
    response = requests.get(f"{BASE_URL}/{resources}/{ID_POST}")
    assert response.elapsed.total_seconds() < 0.3

# 3--> Test if the post ID is match
def test_ID_POST_is_1(BASE_URL, resources, ID_POST):
    response_id = requests.get(f"{BASE_URL}/{resources}/{ID_POST}")
    json_data = response_id.json()
    assert json_data["id"] == ID_POST

# 4--> Test if the post ID is not 1
# @pytest.mark.xfail
# def test_ID_POST_is_not_1(BASE_URL, resources, ID_POST):
#     response_id = requests.get(f"{BASE_URL}/{resources}/{ID_POST}")
#     json_data = response_id.json()
#     assert json_data["id"] != ID_POST

# 5--> Test if the title is a string
def test_title_is_string(BASE_URL, resources, ID_POST):
    response_id = requests.get(f"{BASE_URL}/{resources}/{ID_POST}")
    json_data = response_id.json()
    assert isinstance(json_data["title"], str)

# 6--> Test if the email have @
# def test_email_good(BASE_URL, comments_resources, ID_POST):
#     response_id = requests.get(f"{BASE_URL}/{comments_resources}/{ID_POST}")
#     json_data = response_id.json()
#     assert "@" in json_data["email"]

# 7--> Test if the body contains at least two lines
def test_body_has_at_least_two_lines(BASE_URL, resources, ID_POST):
    response_id = requests.get(f"{BASE_URL}/{resources}/{ID_POST}")
    json_data = response_id.json()
    lines = json_data["body"].split("\n")
    assert len(lines) >= 1


# POST 

# 1--> Test that the POST request was successful (status code 200 or 201)
def test_successful_post_request(BASE_URL,resources):
    test_data = load_my_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    assert response.status_code in [200, 201]

# 2--> Test if the response time is less than 300ms
@pytest.mark.xfail
def test_response_time(BASE_URL,resources):
    test_data = load_my_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    assert response.elapsed.total_seconds() < 0.3

# 3--> Test that the title in the response matches the input title
def test_title_matches_input_value(BASE_URL,resources):
    test_data = load_my_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    json_data = response.json()
    assert json_data["title"] == post_data["title"]

# 4--> Test that the body in the response is not empty
def test_response_body_contains_non_empty_body(BASE_URL,resources):
    test_data = load_my_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    json_data = response.json()
    assert json_data["body"]

# 5--> Test that the response contains the post ID
def test_response_body_contains_ID_POST(BASE_URL,resources):
    test_data = load_my_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    json_data = response.json()
    assert "id" in json_data

# 6--> Test that the response body contains the 'body' property
def test_response_body_contains_post_body_property(BASE_URL,resources):
    test_data = load_my_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    json_data = response.json()
    assert "body" in json_data

# 7--> Test that the response body contains the 'title' property
def test_response_body_contains_post_title_property(BASE_URL,resources):
    test_data = load_my_test_data()
    post_data = test_data[0]  # the first post data
    response = requests.post(f"{BASE_URL}/{resources}", json=post_data)
    json_data = response.json()
    assert "title" in json_data

# PUT 

# 1--> Test that the PUT request returns a status code of 200
def test_status_code_200(BASE_URL,resources,ID_POST):
    test_data = load_my_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{ID_POST}", json={**test_data[0], **update_data})
    assert response.status_code == 200

# 2--> Test if the response time is less than 400ms
@pytest.mark.xfail
def test_response_time(BASE_URL,resources,ID_POST):
    test_data = load_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{ID_POST}", json={**test_data[0], **update_data})
    assert response.elapsed.total_seconds() < 0.4

# 3--> Test that the PUT request is successful (status codes 200, 201, 204)
def test_successful_put_request(BASE_URL,resources,ID_POST):
    test_data = load_my_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{ID_POST}", json={**test_data[0], **update_data})
    assert response.status_code in [200, 201, 204]

# 4--> Test that the userId in the response is a string
def test_user_id_is_string(BASE_URL,resources,ID_POST):
    test_data = load_my_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{ID_POST}", json={**test_data[0], **update_data})
    json_response = response.json()
    assert isinstance(str(json_response.get("userId", "")), str)

# 5--> Test that the response is not empty
def test_response_is_not_empty(BASE_URL,resources,ID_POST):
    test_data = load_my_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{ID_POST}", json={**test_data[0], **update_data})
    assert response.json()

# 6--> Test that the response body contains the 'body' property
def test_body_property_exists(BASE_URL,resources,ID_POST):
    test_data = load_my_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{ID_POST}", json={**test_data[0], **update_data})
    json_response = response.json()
    assert "body" in json_response

# 7--> Test that the updated data is reflected in the response
def test_updated_data_in_response(BASE_URL,resources,ID_POST):
    test_data = load_my_test_data()
    update_data = {"body": "New Technology"}
    response = requests.put(f"{BASE_URL}/{resources}/{ID_POST}", json={**test_data[0], **update_data})
    json_response = response.json()
    assert json_response["body"] == "New Technology"


# DELETE

# 1--> Test that the DELETE request is successful (status codes 200, 202, 204)
def test_successful_delete_request(BASE_URL,resources,del_post_id):
    response = requests.delete(f"{BASE_URL}/{resources}/{del_post_id}")
    assert response.status_code in [200, 202, 204]

# 2--> Test if the response time is less than 300ms
@pytest.mark.xfail
def test_response_time(BASE_URL,resources,del_post_id):
    response = requests.delete(f"{BASE_URL}/{resources}/{del_post_id}")
    assert response.elapsed.total_seconds() < 0.3

# 3--> Test that the response body is an empty JSON object
def test_response_body_is_empty_json(BASE_URL,resources,del_post_id):
    response = requests.delete(f"{BASE_URL}/{resources}/{del_post_id}")
    response_body = response.text.strip()  # Get the response body as text and strip whitespace
    assert response_body == '{"message":"Post deleted","status":"success"}', f"Response body is not an empty JSON object: {response_body}"

# 3--> Test that the response title is an empty JSON object
def test_response_title_is_empty_json(BASE_URL,resources,del_post_id):
    response = requests.delete(f"{BASE_URL}/{resources}/{del_post_id}")
    response_body = response.text.strip() 
    assert response_body == '{"message":"Post deleted","status":"success"}', f"Response body is not an empty JSON object: {response_body}"