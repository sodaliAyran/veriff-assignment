### How to Run the Service

1. Pull and run the **veriff** `face-encoding-test-task` with:

```docker run --name face-encoding-app -p 8000:8000 veriffdocker/face-encoding-test-task```

2. Clone this repo and build the docker image:

```docker build -t veriff-assignment .```

3. Run the docker image:

```docker run -p 8001:8001 --link face-encoding-app:face-encoding-app veriff-assignment```

4. You can go to `localhost:8001/docs` and try the service manually or

5. Send `curl localhost:8001/session` to get your session key. Example response:

```{"key":"33a13f14-c6f3-4311-ad33-f8ccbe052ae5"}```

6. Send `curl -X -H "key: 'your-api-key'" -F "file=@/path/to/your/file" localhost:8001/encode`.

Depending on the image you send you can get the following responses:
- HTTP 200 -> Encoding Successful.
- HTTP 500 -> There was a problem with the service.
- HTTP 400 -> The image you sent does not have any faces or more than 6 faces.

7. Send `curl -i -H "key='your-api-key'" localhost:8001/summary`

You will get a response like below:
```{"image_encodings":[{"faces":[{"encoding":[-0.09708715230226517]}]}]}```

8. Send `curl -X DELETE -H "key='your-api-key'" localhost:8001/session`

To delete your session encodings.

### How to Run the Tests

1. Run the dependency service:
```docker run --name face-encoding-app -p 8000:8000 veriffdocker/face-encoding-test-task```

2. Set the environment variable ```export ENCODER_URL="http://localhost:8000/v1/selfie"```
3. Run ```python3 -m pytest```


# Veriff Face Encoder Design

## Table of Contents
1. [Goal](#goal)
    1. [Functional Requirements](#functional-requirements)
    2. [Non-Functional Requirements](#non-functional-requirements)
2. [Design Decisions](#design-decisions)
3. [Endpoints](#endpoints)
    1. [/ping](#ping)
    2. [/session](#session)
    3. [/encode](#encode)
    4. [/summary](#summary)
4. [Post Implementation Decision](#post-implementation-decisions)

## Goal

The goal of this project is to create a readable, performant, easily extendable and throughly tested web service that can create user session summaries for the images they uploaded. 
This service will exclusively be an API and will not have a user interface.

### Functional Requirements
- Customers will be able to start sessions.
- Customers will be able to upload images to the sessions.
- Each session can hold up to 5 files.
- Each image will be encoded using a dependency call.
- Customers will be able to see their session summary.

### Non Functional Requirements
- The service needs to be documented.
- The code needs to be readable.
- Design of the service and its architecture should be easily extendable.
- The service should be through tested.
- The service needs to be highly available and should have low latency.

## Design Decisions

### Customers will be able to start sessions
Here the "session" wording is a a bit vague. Depending on the context a "session" can mean anything from a time interval to an authentication system. Therefore I'm going to define my "session" terminology. 

In my application a session will refer to an API Key. Through an endpoint I will provide users their own API keys. The users will need to pass these API keys access any other functionality of the service. These API keys will not have an expiration dates and will live indefinitely. (Until the service is killed.) I won't have any restrictions on API Key generation, meaning that any user will be able to create as many API Keys as they want.

I won't implement an integration with a third party authorization tool(OAuth etc.) and will create these API Keys with UUID format. Meaning that there will be a very minor possibility that some users can have the same API Key but I will accept this risk since high traffic/scalability is not within the requirements and even if they were, the possibility is so small that refunding a customer for this mistake would be cheaper than implementing this feature.


### Customers will be able to upload images to sessions.
I will provide this functionality through an endpoint. By using their API Keys, customers will be able to send media requests to the service. I thought between having batch image calls or accepting a single image each request and decided to go with accepting a single image with each request since I believe that will be simpler to implement.

Normally for storing images and object storage(Like AWS S3.) would be used but I will assume that the customers do not consent for my service storing their images(Also storing images is not within the requirements), therefore I will not store their images exactly but I will try to store a hash of their images for caching purposes. (I'm assuming I will be able to hash consistently.)

### Each session can hold up to 5 files
This looks like a simple requirement, but it raises a few questions:
- What happens when the customer reach their file limit? -> I will return an error response.
- Should the customers be able to reset their sessions, and if so should they be able to reset all of the session or can they remove a single image? -> I will provide a functionality reset all the session but won't provide a functionality remove a single image.

### Each image will be encoded using a dependency call
This will require implementing a dependency client. Normally dependency services have their own client SDKs but sadly this is not the case for this task. Therefore I will implement a simple client with simple configurations.(I'm thinking only a timeout configuration.)

Here I thought about two approaches:

#### Store the images first and only call the dependency when the user wants to access their summary.
**Pros:**
- If the service is write heavy, there will be fewer calls to the dependency.
- Nothing will be encoded unless it is used.
- If there were to be a batch API functionality of the dependency we would save some network usage.
- Faster image storing(write) functionality response time.
  
**Cons:**
- Requires object storage.
- Long response time for session summary(read) functionality.

#### Immediately encode images. (SELECTED)
**Pros:**
- If the service is read heavy, the response time will be faster.
- No object storage is needed.
- Simpler to implement.
- Faster read functionality response time.
  
**Cons:**
- More dependency calls. (Can be mitigated by caching at the cost of staleness.)
- Long response time for write functionality.
- More network usage.
- Creating and storing encodings that may never be queried.

Here I decided to pick the latter approach because of the following reasons:
- It is already established that the customers do not consent for us storing their images.
- I believe this service will be read heavy than write heavy.
- Shortcomings of second approach can be mitigated by caching. Since consistency is not a requirement and the encodings will rarely change the trade-off is in favour of us.

### Customers will be able to see their session summary.
Simple enough functionality. I will provide this through an endpoint. When the customer sends a request to this endpoint with their API Key I will return their session summary.

### The service needs to be documented.
This will be done in two parts:
- This README is the first part.
- I will also create the service using the python framework FastAPI and leverage Swagger for API documentation.

### Code Readability
Well there is no magic cure for this. We can only see the end result and judge.

### Service Architecture

To make the design easily extendable I will follow an Object-Oriented Structure.
Every functionality of my service will have its own class.
Interactions with the dependency will be done through a client class.
And although I will not use any external databases or cache systems(since this is a code challenge and usually in code challenges it is looked down upon using databases unless it is requested.) 
I will still write the necessary clients and write the code as if they are external services. (I may not do this since I feel like I'm over-engineering *a bit*.)
I may also implement a simple LRU cache with no TTL. (I know it is unnecessary.)

As per design this service will be stateful and there won't be any data persistence meaning all the data will be gone when the service goes down.
Normally this would cause scalability issues since scaling stateful applications is very hard but scalability and persistence is not within our requirements.

The design will look like something below:
![Image](https://i.ibb.co/LnY2NMf/Screenshot-2024-05-17-at-19-18-00.png)

### Testing
For coding challenges I manage the expectations and don't go for 100% coverage, but I will still write some tests.
My testing strategy will be twofold.
- Unit testing the functionality
- Dependency functionality testing. (These will act kind of like integration tests.)

For the functionalities I write I will write unit tests. (More like I will make ChatGPT write unit tests.)
And for the dependency integration I will create some exploratory tests to understand dependency behaviour and make sure it does not behave unexpectedly.

### Availability and Latency

For this kind of services availability is usually provided through vertical scaling. But since my service stateful this is not as easy.
For this service vertical scaling can be done through sticky connections between load balancer and the service. By using sticky connections the client will always call the service their data resides in.
So I will assume the availability is handled through the load balancer and scaling through sticky connections.

For latency, since I decided to keep everything within memory and do operations within the service our only bottleneck is the dependency call.
We can reduce the latency here by caching.

To reduce the calls to the dependency I will implement a twofold caching strategy.
Once the customer uploads a file to the service I will hash this file and check whether I have already encoded this hash before by going through my database.
If I see that I have encoded this value before I won't send a call to the dependency and just update the database.

While requesting the summary I will look through my LRU cache first for any cached data and if I can not find the data I will query my database to get the data and cache it.

The cache key I will use here will be the image hashes. Because using customer API key as hash key may cause some problematic behaviours for the following scenario.
1. Customer uploads a file.
2. File is encoded and uploaded to the database.
3. Customer asks for summary.
4. Data not found in cache. Database is queried.
5. Data is returned from the database and cached.
6. Valid result is returned.
7. Customer uploads another file.
8. Customer asks for summary.
9. Data is found in the cache.
10. Customer gets stale summary.

Another way to mitigate this problem would be caching during the encoding process but as established previously our service will be read heavy than write heavy therefore caching the most frequently used images will have better performance.

All this will cost data staleness, but I don't think the encodings will change frequently therefore it is safe to cache here.

## Endpoints

### ping
**Accepts:** GET

**Returns:** 200

A health check endpoint validate the service is up and running.

### session
**Accepts:** GET, DELETE

**Returns:** 200, 204

The endpoint to create and clear user sessions. 
Keep in mind that session clear will not delete the API key but the resources related to the session.
A regular session creation workflow will be like below:

1. Request hits the endpoint.
2. SessionService is called to generate an API key.
3. API key is saved to the database.
4. API Key is returned to the user.

### encode
**Accepts:** POST

**Returns:** 200, 400, 403, 500

The endpoint for user to encode images.
Although known to be problematic, as established previously the encoding will be done asynchronously and the user will not be aware of any issues related to encoding.

A regular encoding workflow will be like below:

1. Request hits endpoint.
2. Request body is parsed and validated.
3. API Key gets validated through Session Service.
4. Image hash is created through ImageHasherService.
5. Through DBClient EncoderService checks if there exists an encoding for this Image Hash.
6. If there is, Skip to #10 
7. If there isn't, a request is sent to the encoder service through FaceEncoderClient.
8. Response from Encoder Service is parsed and validated.
9. The encoding is saved to the database.
10. An entry in the database is created linking the session to the Image Encoding. 
11. Operation is successful.

### summary
**Accepts:** GET

**Returns:** 200, 400, 403

The endpoint for user to get their face encoding summary.

A regular summary workflow will be like below:

1. Request hits endpoint.
2. API Key gets validated through Session Service.
3. Database is queried to check which image encodings user has access to.
4. Cache is queried to check if any of the image encodings user has access is cached.
5. Database is queried to return encodings that are not in the cache
6. The results are cached.
7. Service returns the result to the user.

## Post Implementation Decisions

- During implementation, I realized I was using API Keys raw. Saving them to database as they are. 
This is a huge security issue therefore I decided to change `ImageHasher` class to `DataHasher`. 
I did not update the design for this though.
- I think I over-engineered this solution to the point where a simpler implementation would be fast. 
In theory my implementation is the ideal scenario but in practically, 
everything is already in the memory and there are no database table joins therefore I'm checking the memory twice for no reason.
The reason I decided to do this is that I wanted to approach this challenge as system design challenge rather than a co challenge.
- Tests do not cover 100%. I think O wrote enough tests to show that I do write tests.
- For testing the dependency client I decided not to use mocking. 
The reason for that is I kind of wanted to make them function kind of like integration tests, testing the whole functionality.
- I did not choose to user docker-compose because NO.
- I did not dive deep into input sanitization. I think just checking file type and size is enough for this.
- I'm not emitting any metrics because I think that would have been an overkill but I decided to log some metrics.(latency)