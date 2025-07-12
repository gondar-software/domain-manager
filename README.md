# Domain Manager
This is a simple react/vite + fastapi project to manage certificates and nginx config for several domain servicing in a instance.

## How to run

### Prepare the env
path: `./backend/env`
```
GODADDY_API_KEY=
GODADDY_API_SECRET=
DOMAIN=
EMAIL_ADDRESS=
JWT_SECRET=
JWT_ALGORITHM=
TOKEN_EXPIRE_TIMEOUT=
PASSWORD=
SERVER_PORT=
PROJECT_NAME=
SECRET_KEY=
```

### Install dependencies
```
cd backend
pip3 install -r requirements
```

```
cd frontend
npm install
```

### Run the backend and frontend
```
cd backend
python3 -m server
```
```
cd frontend
npm run build
cd dist
http-server-spa ./ ./index.html -p 8000
```

## Live link
https://portfolio-app.online