# Use the officially supported node.js base image
FROM node:16

# Add app source code to image
WORKDIR /app

# DELETE THIS WHEN YOU MAKE YOUR OWN FRONTEND
RUN npx create-react-app .

COPY package*.json ./

ENV REACT_APP_API_BASE_URL=http://localhost:8080

RUN npm install 

COPY . . 

ENV PORT=3000 

EXPOSE 3000

CMD [ "npm", "start" ]