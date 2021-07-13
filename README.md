# Covid_dashboard

A dashboard of different data regarding covid cases using Django and d3.

## Generate files

The programs reads information from the government and cleans it, once the data is cleaned we can create some json files of the information we want to display, we have 4 different graph displaying some information we wanted to show, to start, type the following command:
```
python .\covid.py
```

***Note: remember to be at the Covid_dashboard\COVID folder when running the command***


## Starting the server

We need to start the server and to do so we need to be at the ***Covid_dashboard\COVID\covid_env\root*** folder once there type the following command:

```
python .\manage.py runserver
```
This should display the following:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
July 12, 2021 - 22:48:34
Django version 3.2.5, using settings 'covid.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
with the server started set http://127.0.0.1:8000/ as the url in your web browser, the page should look like this:

![example](https://github.com/sodes-proxy/Covid_dashboard/blob/main/graph_images/startscreen.png)

to start seeing the graphs we prepare add **covid_app** at the end of the url like this http://127.0.0.1:8000/covid_app:

![example](https://github.com/sodes-proxy/Covid_dashboard/blob/main/graph_images/graph2.png)

To look at the remaining 3 graph we need to add yet again something to the url:

- graph 1: http://127.0.0.1:8000/covid_app/graph1
- ![example](https://github.com/sodes-proxy/Covid_dashboard/blob/main/graph_images/graph1.png)
- graph 3: http://127.0.0.1:8000/covid_app/graph3
- ![example](https://github.com/sodes-proxy/Covid_dashboard/blob/main/graph_images/graph3.png)
- graph 4: http://127.0.0.1:8000/covid_app/graph4
- ![example](https://github.com/sodes-proxy/Covid_dashboard/blob/main/graph_images/graph4.png)


And that should be everything you need to know to view the project, hope you find it worth your while.

Any comment or inconvience you can send me an email, to check what's wrong.

have fun!
