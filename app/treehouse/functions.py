from app.treehouse.constants import TREEHOUSE_USER

import requests

def get_points():
    try:
        my_request = requests.get(
            "http://teamtreehouse.com/{}.json".format(TREEHOUSE_USER)
        )
        try:
            if my_request.status_code == 200:
                json = my_request.json()  # Get JSON
                subject_points = json["points"]  # Get points
                return subject_points
            else:
                print("Status Code Error: {}".format(my_request.status_code))
        except:
            # Error parsing json
            print("Invalid JSON.")
    except:
        # Error with url
        print("Request error.")


def get_number_of_subjects():
    try:
        my_request = requests.get(
            "http://teamtreehouse.com/{}.json".format(TREEHOUSE_USER)
        )
        try:
            if my_request.status_code == 200:
                json = my_request.json()  # Get JSON
                subject_points = json["points"]  # Get points
                return len(subject_points)
            else:
                print("Status Code Error: {}".format(my_request.status_code))
        except:
            # Error parsing json
            print("Invalid JSON.")
    except:
        # Error with url
        print("Request error.")


def get_courses(number_of_courses):
    try:
        my_request = requests.get(
            "http://teamtreehouse.com/{}.json".format(TREEHOUSE_USER)
        )
        try:
            if my_request.status_code == 200:
                json = my_request.json()  # Get JSON
                badges = json["badges"]  # Get points
                badges = badges[-number_of_courses:]
                badges.reverse()
                return badges
            else:
                print("Status Code Error: {}".format(my_request.status_code))
        except:
            # Error parsing json
            print("Invalid JSON.")
    except:
        # Error with url
        print("Request error.")


def order_points(points):
    return sorted(points.items(), key=lambda x: x[1])[::-1]