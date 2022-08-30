# sproutai
Technical task for Sprout AI Interview

### Overview
The Project contains a Fast API app to serve the moderation API which is used to simulate an external ML API.
And a Django project consisting of `Posts` app. The Posts app handles all the implementation related to:
* Creating and storing the Post
* Integration with Moderation service


### The Fast API Moderation Service
It's a simple one API app which uses below worlds to check if a given sentence contains fould language:
```json
[
    "foul1",
    "foul2",
    "foul3",
    "foul4",
    "foul5",
    "foul6",
]
```

### The Posts App
#### APIs
###### POST: `/api/posts/`
This API allows the user to create a Post in the system, below is a sample request data:
```json
{
    "title": "First Blog",
    "paragraphs": [
        "This is the first paragraph. It contains two sentences.",
        "This is the second paragraph. It contains two more sentences",
        "Third paragraph here."
    ]
}
```
While storing the Post data into the database, the moderation service is used to check if the Post contains any foul language.
In case the Moderation service is unavailable, a celery task is queued with 60 seconds delay to try the API again.
The `Post.has_foul_language` is used to store the result and also represents the status of the moderation check which can be used to show appropriate message to the end user, refer below:
```
Value: None, Status: In Progress
Value: True/False, Status: Complete
```
<br>

###### GET `/api/posts/{id}/check`
This API allows the user to check the moderation status of a Post, also call the Moderation service if needed. Please find a sample response below:
```json
{
    "id": 1,
    "title": "First Blog",
    "paragraphs": [
        [
            "This is the first paragraph. It contains two sentences foul1",
            "This is the second paragraph. It contains two more sentences",
            "Third paragraph here"
        ]
    ],
    "has_foul_language": true,
    "moderation_check_status": "Complete"
}
```


## Features:
* Near real-time moderation check using multiple threads
* Celery tasks to run the failed API calls again and update the status in the DB
* Unit tests with >90% coverage
* Scalable DB modelling
* Thin Views Fat Serializers/Models design
* Dedicated API to trigger the moderation check on a Post.


### Docker Set up
Pre-requisites: Docker service must be up and running
* Run command: `make dc-start`

## Steps to use the service
Pre-requisites: Docker set up must be successful
* Refer Postman collection for API details[here](https://documenter.getpostman.com/view/4969182/VUxNQ7BL)

### Run Unit Tests
Pre-requisites: Docker service must be up and running
* Run command: `make tests`, coverage report will be printed at the end

### Possible Improvements
* Add integration tests
* Separate DEV and PROD requirements
* Add MAX_ATTEMPTS restriction to stop trying the Moderation API call for same sentence.