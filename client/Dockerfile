# Use the officially supported node.js base image
FROM node:16

# Add app source code to image
WORKDIR /client 

COPY package*.json ./

RUN npm install 

COPY . . 

EXPOSE ${CLIENT_PORT}

CMD if [ "$TESTING" = "0" ]; then \
    npm run start:https -- --port ${CLIENT_PORT}; \
else \
    npm start -- --port ${CLIENT_PORT}; \
fi