## Project distribution
Install Python, Django and MySQL
```
sudo yum install epel-release
sudo yum update -y && sudo reboot
sudo yum install python-devel python-setuptools python-pip python-dev wget 
sudo pip install --upgrade pip
sudo pip install Django==1.11.20 
sudo yum install mysql-server
```
Install dependencies
```
sudo yum install memcached
pip install python-memcached python-dateutil requests
```
Install nginx and uWSGI
```
sudo yum install nginx 
pip install uwsgi
```
Config nginx, save file in /etc/nginx/conf.d/
```
server {
	listen 80;
	
	charset utf-8;
	client_max_body_size 75M;
	location /static/ {
		alias /path/to/static/dir/static;
	}

	location / {
		proxy_pass http://127.0.0.1:8000;
	}
}
```
Config uWSGI, save as uwsgi_config.ini
```
[uwsgi]
chrdir = /path/to/project/dir
wsgi-file = entry_task/wsgi.py
master = true
processes = 8
threads = 4
http-socket = 127.0.0.1:8000
vaccum = true
```
Start nginx and uWSGI
```
systemtcl start nginx
systemctl start memcached
uwsgi uwsgi_config.ini
```

## API Design
Using JSON format in request and response's body
Each response has "error", "status" and "content"

#### Register

Request POST /api/register
| Field | Type | Description |
|---|---|---|
| username | String required | Username
| password | String required | Password

Reponse: error and status

#### Login

Request POST /api/login
| Field | Type | Description |
|---|---|---|
| username | String required | Username
| password | String required | Password

Reponse
| Field | Type | Description |
|---|---|---|
| token | String | Access token for request |

### These API required token in request header
#### Get events list

Request GET /api/events
| Field | Type | Description |
|---|---|---|
| offset | Number required | start position |
| size | Number required | size |
| category | String optional | require for filtering by category |
| start_date | Date optional | require for filtering by date |
| end_date | Date optional | require for filtering by date |

Response
| Field | Type | Description |
|---|---|---|
| content | Array of Number | List of event ids |

#### Get event's detail

Request GET /api/event
| Field | Type | Description |
|---|---|---|
| event_id | Number required | event id

Response: content
| Field | Type | Description |
|---|---|---|
| id | Number | event's id |
| title | String | Title |
| location | String | Location |
| date | Date | Date |
| description | String | Description |
| photo_url | String | Photo url for display in frontend |
| created_by | Number | Creator's id |

#### Create new event
Request POST /api/event/create
| Field | Type | Description |
|---|---|---|
| title | String required | Title |
| description | String required | Description |
| date | Date required | Date |
| location | String required | Location |
| categories | Array of String required | Categories, can be empty |
| photo_url | String | Photo url in static dir, can be blank |

Response
| Field | Type | Description |
|---|---|---|
| id | Number | New event id |
| created_by | Number | Creator's id |

#### Add comment to event
Request POST /api/event/add_comment
| Field | Type | Description |
|---|---|---|
| event_id | Number required | event id |
| content | String required | comment's content |

Response
| Field | Type | Description |
|---|---|---|
| event_id | Number | event id |
| content | String | comment's content |
| id | Number | comment's id |
| by_user | Number | user's id |

#### Get comments of event
Request GET /api/event/get_comments
| Field | Type | Description |
|---|---|---|
| event_id | Number required | event id

Response: content is an array of comments
| Field | Type | Description |
|---|---|---|
| event_id | Number | event id |
| content | String | content of comment | 
| by_user | Number | which user comment |
| id | Number | comment id |

#### Add participant to event
Request POST /api/event/add_participant
| Field | Type | Description |
|---|---|---|
| event_id | Number required | event id |

Response: error and status

#### Get participants
Request GET /api/event/get_participants
| Field | Type | Description |
|---|---|---|
| event_id | Number required | event id |

Response 
| Field | Type | Description |
|---|---|---|
| content | Array of String | list of username |

#### Add like 
Request POST /api/event/add_like
| Field | Type | Description |
|---|---|---|
| event_id | Number required | event id |

Response: error and status

#### Get likes 
Request GET /api/event/get_likes
| Field | Type | Description |
|---|---|---|
| event_id | Number required | event id |

Reponse:
| Field | Type | Description |
|---|---|---|
| content | Array of String | list of username |

#### Get categories 
Request GET /api/event/get_categories
| Field | Type | Description |
|---|---|---|
| event_id | Number required | event id |

Response
| Field | Type | Description |
|---|---|---|
| content | Array of String | list of categories | 
