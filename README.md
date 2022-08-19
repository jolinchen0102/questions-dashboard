# questions-dashboard

### MVP

Product implemented with django framwork, deployed on Heroku

- Index page of the dashboard (with minimal UI): https://dashboard-cb.herokuapp.com/dashboard/base

- Geolocation distribution map: https://dashboard-cb.herokuapp.com/dashboard/geolocations
- Question category treemap: https://dashboard-cb.herokuapp.com/dashboard/categoryMap
- Display all questions (filter is not implemented): https://dashboard-cb.herokuapp.com/dashboard/questions

### Improvements

- URI resources could be designed better
- Base index page could be managed better or consider putting all graphs in the same page
- Filters not implemented
- Communications are through API calls, involving network layer communication. One potential implementation considers directly accessing database