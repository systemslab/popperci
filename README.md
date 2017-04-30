# PopperCI

CI server for Popperized experiments (running at 
<http://ci.falsifiable.us>). This repo contains:

  * `frontend`. The `web2py` frontend.
  * `implementations`. Alternative implementations of the PopperCI 
    workflow.
  * `webhook`. A web service for hooking push events to the CI server.

## Documentation

Available [here](http://popper.readthedocs.com/ci).

## Launching your own instance

We package the server in a Docker image. The service expects the 
following folders in `/var/popperci`:

  * `workspace/` folder storing test output artifacts.
  * `credentials/` folder for storing user credentials.
  * `db/` folder for storing database files.

In addition, the admin password for the frontend can be specified via 
the `WEB2PY_ADMIN` variable (`admin` by default).

To run an instance of the CI server using Docker:

```bash
docker run --name popperci \
  -v /path/to/credentials/:/var/popperci/credentials \
  -v /path/to/workspace/:/var/popperci/workspace \
  -v /path/to/db/:/var/popperci/db \
  -v /usr/bin/docker:/usr/bin/docker \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e WEB2PY_ADMIN=Pa55word! \
  -p 5000:5000 \
  -p 80:80 \
  ivotron/popperci
```

Since the server executes PopperCI pipelines [in 
containers](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/), 
the `docker` binary has to be available to the `popperci` container.
