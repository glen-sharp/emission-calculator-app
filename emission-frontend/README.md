# Contacts Hub UI
User interface using the React framework displaying emissions data for various activities.
The UI consists of 2 main components:
- Emissions table
- Emission total table

## Deploying UI locally

Requirements:
- Node.js v22.4.1+

To download Node.js instructions can be found [here](https://nodejs.org/en/download)

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