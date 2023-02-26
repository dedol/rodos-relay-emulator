# RODOS Relay Emulator

RODOS Relay API Emulator with GUI and virtual traffic light.

## Docker build

```
docker build -t rodos-relay-emulator:1.0.0 .
```

```
docker run -d --name rodos-relay-emulator -p 8003:80 --restart always rodos-relay-emulator:1.0.0
```