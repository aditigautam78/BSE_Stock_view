# BSE-stock view

## About

BSE publishes a "Bhavcopy" file every day here: https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx. This application downloads the Equity bhavcopy zip from the above page- Extracts and parses the CSV file in it- Writes the records into Redis into appropriate data structures(Fields: code, name, open, high, low, close)

## Setting up locally

Make sure you have [Python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/) installed and an active running Redis instance is also present.

```bash
git clone https://github.com/201560543/BSE_Stock_view.git
cd BSE_Stock_view
pip install -r requirements.txt
python app.py
```

The webserver should now be running on http://localhost:5000. Editing app.py will cause cherrypy to reload itself.

## Deploying to Heroku

If you are using paid version of Heroku just configure redis-heroku on the application otherwise use an ngrok tunnel to point to the local redis instance on your server.

Install the [Heroku toolbelt](https://toolbelt.heroku.com/), and make sure you commit your changes to git. Now you can deploy:

```bash
heroku create
git push heroku master
```

If all goes well, you can open your app in the browser:

```bash
heroku open
```
