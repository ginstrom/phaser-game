FROM node:20-alpine

# Install bash and development tools
RUN apk add --no-cache bash git

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies including dev dependencies
RUN npm install && \
    npm install --save-dev typescript ts-loader webpack webpack-cli webpack-dev-server @types/node

# Copy the rest of the application
COPY . .

EXPOSE 8080

CMD ["npm", "start"] 