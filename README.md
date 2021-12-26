#Simporter Test Task (Junior PyDev)

Let’s suppose we have a number of events that are distributed in time. Each event has several
attributes. And we have a service (webpage) which purpose is to visualize this distribution (i.e.
show a timeline) using different filters. Visualisation can be shown in either cumulative or usual
way (see below).

Your task is to create an API providing data for visualization.

##Details

Source data is csv file containing following data:

* Event id (column id )
* Event timestamp (column timestamp )
* Several event attributes (columns asin, brand, etc )

Link: https://1drv.ms/u/s!AvTeEdxQwFAJqliTn-n6Yxk353vF?e=llePiD

You are expected to create two API methods:

###GET /api/info
Example:

http://localhost:5000/api/info

This method doesn’t require any parameters
Returns: Information about possible filtering (list of attributes and list of values for each attribute)

GET /api/timeline

Example:

http://localhost:5000/api/timeline?startDate=2019-01-01&endDate=2020-01-01&Type=cumulative&Grouping=weekly&attr1=value1&attr2=value2

####Parameters:
* startDate
* endDate
* Type (cumulative or usual)
* Grouping (weekly, bi-weekly or monthly)
* Filters (attributes and values)
* 
####Grouping types:
#####You need to aggregate data during the period (from startDate to endDate):
* weekly (data for each week)
* bi - weekly (data for each 2 weeks)
* monthly (data for each month)

Returns: JSON with timeline information according to input parameters:

Each point on the graph will be in a format:
* data type - dict:
** keys data type - str
** values data type - int (number of events during this period)

The response should have “timeline”(str) as a key, value - list of dicts with timeline data.

Example of response:

```json
{"timeline": [{"date": "2019-01-01", "value": 10} ] }
```

Technical requirements
* Python 3.7+
* Flask
* Other details are up to you

Good luck and have fun.

###Example query:

```sql
SELECT strftime('%W', timestamp) AS  WeekNumber,
       COUNT(id) AS Events,
       SUM(COUNT(id)) OVER (order by timestamp) as Sum,
       timestamp
FROM event_model
WHERE timestamp BETWEEN '2019-01-01' AND
datetime('2019-01-01', '+9 months')
GROUP BY WeekNumber
ORDER BY WeekNumber
```
