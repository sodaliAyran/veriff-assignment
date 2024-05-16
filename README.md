# Veriff Face Encoder Design

## Goal

The goal of this project is to create a readable, performant, easily extendable and throughly tested web service that can create user session summaries for the images they uploaded. This service will exclusively be an API and will not have a user interface.

## Functional Requirements
- Customers will be able to start sessions.
- Customers will be able to upload images to the sessions.
- Each session can hold up to 5 files.
- Each image will be encoded using a dependency call.
- Customers will be able to see their session summary.

## Non Functional Requirements
- The service needs to be documented.
- The code needs to be readable.
- Design of the service and its architecture should be easily extendable.
- The service should be throughly tested.
- The service needs to be highly available and should have low latency.

## Design Decisions to Reach Requirements

## How am I going to fulfill Functional Requirements?

### Customers will be able to start sessions
Here the "session" wording is a a bit vague. Depending on the context a "session" can mean anything from a time interval to an authentication system. Therefore I'm going to define my "session" terminology. 

In my application a session will refer to an API Key. Through an endpoint I will provide users their own API keys. The users will need to pass these API keys access any other functionality of the service. These API keys will not have an expiration dates and will live indefinitely. (Until the service is killed.) I won't have any restrictions on API Key generation, meaning that any user will be able to create as many API Keys as they want.

I won't implement an integration with a third party autharization tool(OAuth etc.) and will create these API Keys with UUID format. Meaning that there will be a very minor possibility that some users can have the same API Key but I will accept this risk since high traffic/scalability is not within the requirements and even if they were, the possibility is so small that refunding a customer for this mistake would be cheaper than implementing this feature.


### Customers will be able to upload images to sessions.
I will provide this functionality through an endpoint. By using their API Keys, customers will be able to send media requests to the service. I thought between having batch image calls or accepting a single image each request and decided to go with accepting a single image with each request since I believe that will be simpler to implement.

Normally for storing images and object storage(Like AWS S3.) would be used but I will assume that the customers do not consent for my service storing their images(Also storing images is not within the requirements), therefore I will not store their images exactly but I will try to store a hash of their images for caching purposes. (I'm assuming I will be able to hash consistently.)

### Each session can hold up to 5 files
This looks like a simple requirement but it raises a few questions:
- What happens when the customer reach their file limit? -> I will return an error message.
- Should the customers be able to reset their sessions, and if so should they be able to reset all of the session or can they remove a single image? -> I will provide a functionality reset all the session but won't provide a functionality remove a single image.(Unless it is the whole session.)

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
- Faster read fucntionality response time.
  
**Cons:**
- More dependency calls. (Can be mitigated by caching at the cost of staleness.)
- Long response time for write functionality. (Can be mitigated by async calls sacrificing consistency.)
- More network usage.
- Creating and storing encodings that may never be queried.

Here I decided to pick the latter approach because of the following reasons:
- It is already established that the customers do not consent for us storing their images.
- I believe this service will be read heavy than write heavy.
- Shortcomings of second approach can be mitigated by caching and async calls. Since consistency is not a requirement and the encodings will rarely change the trade off is in favour of us.

### Customers will be able to see their session summary.
Simple enough functionality. I will provide this through an endpoint. When the customer sends a request to this endpoint with their API Key I will return their session summary.

## How am I going to fulfill Non Functional Requirements?




