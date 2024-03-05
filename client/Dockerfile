# Use the officially supported node.js base image
FROM node:16

# Add app source code to image
WORKDIR /client 

COPY package*.json ./

RUN npm install 

COPY . . 

EXPOSE ${CLIENT_PORT}

RUN npm run build

CMD npm start -- --port ${CLIENT_PORT}