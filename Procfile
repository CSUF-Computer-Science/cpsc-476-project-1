articles: env FLASK_APP=services.articles.py flask run -p $PORT
tags: env FLASK_APP=services.tags.py flask run -p $PORT
comments: env FLASK_APP=services.comments.py flask run -p $PORT
users: env FLASK_APP=services.users.py flask run -p $PORT
rss: env FLASK_APP=services.rss.py flask run -p $PORT
init-db: env FLASK_APP=services.users.py flask init-db all
init-data: env FLASK_APP=services.users.py flask init-data all
reset-db: env FLASK_APP=services.users.py flask reset-db all
