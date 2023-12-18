#use the offically supported node.js base image
FROM node:16

#add app source code to image
WORKDIR /app

COPY package*.json ./

ENV REACT_APP_API_BASE_URL: http://localhost:8080

RUN npm install 

COPY . . 

ENV PORT = 3000 

EXPOSE 3000

CMD [ "npm", "start" ]


