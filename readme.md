# Sample Log Generator
Simple script to constantly spam simple logs

## Installation
```
$ mkvirtualenv log_generator_env
(log_generator_env) $ pip install -r requirements.txt
(log_generator_env) $ python log_generator.py
```

## Configuration
Just edit `defaults.cfg` to set up host, port and optional delay

## Debugging
`debug_listener.py` is included to listen for all spam log entries
