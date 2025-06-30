import os

# Configurações do servidor
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
workers = int(os.getenv('WEB_CONCURRENCY', '1'))

# Configurações de timeout
timeout = 120
keepalive = 2

# Configurações de logging
loglevel = 'info'
accesslog = '-'
errorlog = '-'

# Configurações de processo
preload_app = True
max_requests = 1000
max_requests_jitter = 50

# Configurações de worker
worker_class = 'sync'
worker_connections = 1000

