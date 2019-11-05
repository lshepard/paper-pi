const http = require('http')
const fs = require('fs')
const path = require('path')
const generate = require('./generate')
const port = process.env.PORT || 8080

const requestHandler = async (req, response) => {
    response.writeHead(200, {'Content-Type':'text/html'})
    response.end("Hello world!")
    
  }).catch(() => {
    response.end('Error')
  })
}

const server = http.createServer(requestHandler)

server.listen(port, err => {
  if (err) {
    return console.log('Something went wrong', err)
  }
})
