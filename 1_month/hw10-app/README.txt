This homework can start with docker, include readme file and realize next functionality:
 - authorization
 - registration
 - create, delete and read posts with following GUI
 - posts have tags, which can use for filter articles by them

Authorization and registration use JWT system. Fastapi supports JWT, but I did the implementation myself.
Website use cookies for storage token. It's not secured, but, without full js front-end, I can't do that by another way.
All front-end is rendering by jinjaTemplates, but, for some functions, somewhere using js code. Bootstrap was also used.

Main technologies:
  - fastapi
  - gunicorn+uvicorn
  - bootstrap
  - postgress

How it works:
    All endpoints are processed by the backend. Each of them produces a rendered page at the output.
    Pages are stored statically, and all dynamic data is loaded using jinja.
About page:
    Just static text
Home page:
    Displays all articles. Filtering by tags is available (it is processed by the database).
    Any article opens in full screen, where its full version is shown.
    When displaying all articles, their reduced version is used.
Profile page:
    Displays all articles of the selected user. If the user is not authorized, it blocks access.
    It is also possible to add a new article.
    To delete your article, you need to open its full version, where this option is available.
Login page:
    Offers to log in or register. Users are stored in the database, and their passwords are encoded.
    After registration/authorization, a jwt token is issued,
    which is stored in cookies and substituted into the request for each subsequent request.
    After 30 minutes, the token expires and the site requires new authorization.
    The site also has a light and dark theme (this was not specified in the task, but I really wanted to implement it myself).
    The theme type is also stored in cookies.