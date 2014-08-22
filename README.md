MauMau
======
[![Deploy Status](http://img.shields.io/badge/cloudControl-deployed-brightgreen.svg)](https://maumau.cloudcontrolapp.com)
[![Build Status](https://travis-ci.org/TooAngel/MauMau.svg?branch=master)](https://travis-ci.org/TooAngel/MauMau)
[![Coverage Status](https://coveralls.io/repos/TooAngel/MauMau/badge.png)](https://coveralls.io/r/TooAngel/MauMau)
[![Dependency Status](https://gemnasium.com/TooAngel/MauMau.svg)](https://gemnasium.com/TooAngel/MauMau)


An implementation of the popular cardgame https://en.wikipedia.org/wiki/Mau_Mau_(card_game)


To the start web application:

  gunicorn -k flask_sockets.worker --config src/gunicorn_config.py --pythonpath src/ --chdir src/ webapp:app
  
To start the game on the command line:

  python src/maumau.py

