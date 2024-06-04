FROM node:21.7.1

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

ENV PATH /app/node_modules/.bin:$PATH

EXPOSE 3000

CMD ["npm", "run", "dev"]
