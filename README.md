# Flask-Notes
2nd Flask project work for ProductStar

# Usage

* Creating a new event :  ```curl http://127.0.0.1:5000/api/v1/event/ -X POST -d "2023-10-14|First Event|Hello buddy's```

* Getting all events : ```curl http://127.0.0.1:5000/api/v1/event/```

* Getting an event by ID : ```curl http://127.0.0.1:5000/api/v1/event/ id number /```

* Event update by ID : ```curl http://127.0.0.1:5000/api/v1/event/ id number/ -X PUT -d "2023-10-14|First Event|Bye"```

* Deleting an event by ID : ```curl http://127.0.0.1:5000/api/v1/event/ id number / -X DELETE```


# Course Tasks
1. Max header lenght - 30 letters   |   Output >>> Failed: Title length > max: 30
2. Max text lenght - 200 letters | Output >>> Failed: Text length > max: 200
3. Forbidden to add more than one event per day | Output >>> Failed: You may add just one event for a day
