import os

bind = "0.0.0.0:{}".format(os.getenv("PORT", 5000))
workers = 4
timeout = 120
