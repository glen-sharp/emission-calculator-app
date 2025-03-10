# Contacts Hub UI
User interface using the React framework displaying emissions data for various activities

## Deploying UI locally

```bash
npm install

npm run build

npm start
```

## Deploying UI via Docker Image

```bash
docker build . -t emission-frontend

docker run -p 3000:80 emission-frontend:latest
```