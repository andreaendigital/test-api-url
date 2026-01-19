# URL Lookup Service – Technical Exercise

## Context and Note to Reviewers

This repository contains my solution to the URL Lookup Service technical exercise.

I would like to thank you for the opportunity to work on the requested technical assessment.

During the implementation process, I realized that the scope of the exercise went beyond simply creating a GET endpoint or using a simple in-memory structure. Specifically, URL parsing, normalization, URL-encoding, advanced routing, and networking implications (such as proxy architecture and mechanics) require a depth of knowledge that exceeds my current level.

I tried to complete the test using my current resources and knowledge. However, I realized I had knowledge gaps. I relied on AI as a learning guide and identify exactly what I still needed to learn. That being said, I believe it is important to be transparent and admit that I delivered a very scope implementation focused on the core behavior while learning new concepts required to solve it.

I am grateful for this learning experience and I now understand that the role required a standard closer to a Junior-Mid level rather than entry-level. I gained valuable exposure to concepts like URL normalization and canonicalization, encoding/decoding, HTTP routing, automated testing in Python and real-world backend considerations, that were not part of my formal education.

Regardless of the result, I appreciate the opportunity to identify these specific areas for growth. I would welcome any feedback you might have.


## Problem Description

The goal of this exercise is to implement a URL lookup service queried by an HTTP proxy before allowing outbound requests.

The service receives a URL via a GET request of the form:

GET /urlinfo/1/{hostname_and_port}/{original_path_and_query_string}

The service responds with information about the URL and whether it is considered safe to access.


## Scope of This Implementation

This implementation focuses on:

- Receiving and decoding URL components via path parameters
- Parsing and reconstructing the original URL
- Comparing the URL against in-memory allow/deny lists
- Returning a clear verdict (ALLOW / DENY / UNKNOWN)
- Providing automated tests for core behavior

Out of scope for this implementation:

- Persistent storage
- Real proxy integration
- High-scale distributed systems


## Design Decisions

- FastAPI was chosen for simplicity and clarity.
- URLs are reconstructed using standard library parsing instead of manual string manipulation.
- Allow and deny lists are kept in memory to keep the initial design simple.
- Automated tests are used to define expected behavior.
- The design follows an incremental approach, prioritizing correctness over scale.
- This service is intentionally implemented as a read-only lookup service: In a real-world architecture, the responsibility of updating URL lists would belong to a separate ingestion or management service, not to the lookup service itself. For this reason, no POST endpoint is exposed in this implementation.

## How to Run the Project

Create and activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

Install dependencies:

pip install -r requirements.txt

Run the API:

uvicorn main:app --reload

The service will be available at http://localhost:8000

also http://localhost:8000/docs

## How to Test

Run automated tests with:

pytest

Tests validate:
- Allowed URLs return ALLOW
- Blocked URLs return DENY
- Unknown URLs return UNKNOWN

## Example Requests

Allowed URL:

curl "http://localhost:8000/urlinfo/1/example.com/%2Fhome"

Blocked URL:

curl "http://localhost:8000/urlinfo/1/malware.test/%2Fbad%2Fpath"


## Part 2 – Design Considerations (Written Answers)

• The size of the URL list could grow infinitely. How might you scale this beyond the memory capacity of the system? 

In the current implementation, the service uses an in-memory data structure to store and compare URLs. This approach is intentional for an initial version, as it prioritizes simplicity, doing things well and ease of reasoning. But this doesn´t scale when the list grows beyond the memory capacity of the system. 

To scale beyond the memory limits, the URL list would need to be stored in an external persistent system. A coomon approach would be to use a database or a key-value store such as a relational database with proper indexing or a distributed store like Redis or DynamoDB. URLs would be stored in a normalized form to ensure consistent matching. 

This can evolve in a system that also use a layered approach: frequently accessed or recently queried URLs could be cached in memory, while the full dataset resides in persistent storage. This allows fast response times. 

This progresion is an incremental design approach.



• Assume that the number of requests will exceed the capacity of a single system, describe how might you solve this, and how might this change if you have to distribute this workload to an additional region, such as Europe. 

If the request volume exceeds the capacity of a single system, the first step would be to run multiple instances of the service behind a load balancer. Each instance would handle a portion of incoming request, allowing horizontal scaling. If I have to deploy in multiple regions, a regional load balancer or DNS based routing could direct users to the nearest region to minimize latency. 

An additional consideration would be data consistency between regions. For this kind of service strong real-time consistency may not be strictly required. Each region could maintain a local copy of the URL dataset, updated asynchronously.



• What are some strategies you might use to update the service with new URLs? Updates may be as much as 5 thousand URLs a day with updates arriving every 10 minutes.

Updating URLs individually would not be efficient at this scale. Some strategys are: to process updates in batches. Incoming updates can be grouped every few minutes and processed together. To process updates through a message queue or event stream. A producer system would publish URL updates, and one or more consumers would process them asynchronously. 
This decouples the update pipeline from the lookup service and prevents update spikes from impacting user-facing requests.

To ensure safety URL lists can be versioned. Each batch of updates generates a new version of the dataset and the system can switch from the old version to the new one. If a problem is detected, rolling back  means switching back to the previous version.


• You’re woken up at 3am, what are some of the things you’ll look for?

At 3am The first things to check would be monitoring dashboards and alerts to understand whether the issue is related. 

Next, logs would be examined to identify errors, such as failed updates or unexpected input. If the issue matches with a recent URL list update or deployment, the fastest solution may be to roll back to the last known good version of the dataset.


• Does that change anything you’ve done in the app?

This scenario reinforces design decisions like the idea of versioned URL lists to switch between them for fast rollback.  Observability is important even in simple applications. Could integrate monitoring, metrics, and health checks. 


• What are some considerations for the lifecycle of the app?

Throughout the lifecycle of the application, several factors need to be considered: maintainability, scalability, security, and operational stability.

As usage grows, performance optimizations, persistent storage, and caching become more important.

And if the service grows significantly, I would consider backward compatibility as key.


• You need to deploy a new version of this application. What would you do?

I would automate through a CI/CD pipeline. Even in a simpler environment, the principle remains the same: deploy incrementally, validate behavior, testing, and maintain a clear rollback.

Automated tests should run before deployment to catch regressions, and monitoring should be closely observed during and after the release.
