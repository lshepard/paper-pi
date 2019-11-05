const { 
    Weather,
    System,
    Notes
} = require('./data-sources/index')
const Draw = require('./ui/Draw')
const fs = require('fs')
const winston = require('winston')
const { zipObj } = require('ramda')
require('dotenv').config()

winston.add(winston.transports.File, { filename: 'error.log' })

const weather = new Weather()

const init = () => new Promise((resolve, reject) => {
  Promise.all([
    weather.getForecast({ latitude: 51.5074, longitude: 0.1278 }).catch(err => { winston.log('error', 'Failed to get weather data %s', err) }),
  ])
  .then(zipObj(['forecast']))
  .then(resolve)
  .catch(reject)
})

function drawImage(data) {
  // if(data.charge < 0.05) {
  //   data.lowPower = true
  // }
  return new Draw({ orientation: 'portrait', ...data }).getImage()
}


module.exports = {
  start: () => new Promise((resolve, reject) => {
    init().then(drawImage).then(image => {
      fs.mkdir('./build', () => {
        fs.writeFile('./build/monocolor.bmp', image,  err => {
          if(err) {
            winston.log('error', 'Failed to write image - %s', err)
          }
          resolve()
        })
      })
    }).catch(err => {
      winston.log('error', 'Failed to initialize - %s', err)
      reject()
    })
  })
}
