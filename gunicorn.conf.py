bind = "0.0.0.0:5000"
workers = 3

# log ke file
accesslog = "/var/log/web3/access.log"
errorlog  = "/var/log/web3/error.log"

# format: IP asli dari header X-Forwarded-For
access_log_format = '%({x-forwarded-for}i)s - - [%(t)s] "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
