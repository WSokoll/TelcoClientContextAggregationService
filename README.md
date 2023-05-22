# TelcoClientContextAggregationService

## Project setup

### Installing dependencies

```
pip install -r .\app\requirements.txt
```

### Configuration
In the **.\local** folder, create a file called `config.local.py`. 
Then copy the contents of the **.\app\config.default.py** file and change the values if needed.

### Databases
The project requires two databases:  
1. Context database - MongoDB
2. App database (used for storing configuration and auth data) - MySQL database, which can be initiated with the script from the *db/init.sql* file.