FROM node

WORKDIR /ui

COPY package.json .
COPY package-lock.json .
RUN npm i

CMD ["npm", "run", "start"]