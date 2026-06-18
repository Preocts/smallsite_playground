#### Can I make a docker image with a Python app in under 20MB?

This doesn't work but it's a fun exercise. The resulting binary from `nuitka` does not run even in the builder image.

```
IMAGE         ID             DISK USAGE   CONTENT SIZE   EXTRA
test:latest   1dc7b22bcda0       24.4MB         12.1MB
```

-egg
