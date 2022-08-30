# How to run Macproxy in Docker
## Building
A simple ```docker build -t macproxy:latest .``` should work

## Running
### Regular run

```docker run macproxy```
### With arguments
This container supports both user agents and other options
For user agent support:
* add ```-e USER_AGENT=usedagent``` to the docker run command, replacing the ```usedagent``` with the user-agent string
For other arguments: 
just add it to the normal docker run command