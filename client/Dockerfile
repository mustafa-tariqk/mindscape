# Use the officially supported node.js base image
FROM node:16

# Add app source code to image
WORKDIR /client 

COPY package*.json ./

RUN npm install 

COPY . . 

ENV PORT=3000 

EXPOSE 3000

CMD [ "npm", "start" ]
