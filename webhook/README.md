# Hook handler for PopperCI

The hook expects:

  * A `WORKSPACE` variable with the path to the workspace folder.
  * A `CREDENTIALS` variable with the path to the credentials folder.
  * A `SQLITEDB` path pointing to a sqlite3 database.

We have a convenience container for this, to run:

```bash
docker run --name webhook-handler \
  -v `pwd`/frontend/gh-webhook:/app/hooks \
  -v /path/to/credentials:/path/to/credentials \
  -v /path/to/workspace:path/to/workspace \
  -v /path/to/db.sqlite:/path/to/db.sqlite \
  -v /usr/bin/docker:/usr/bin/docker \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e WORKSPACE=/path/to/workspace \
  -e CREDENTIALS=/path/to/credentials \
  -e SQLITEDB=/path/to/db.sqlite \
  -p 5000:5000
  ivotron/webhook-handler
```

The above hook container launches other docker containers (as 
explained 
[here](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)), 
so the `docker` binary has to be available inside the 
`webhook-handler` container. To test, create a `payload.json` file 
based on [GitHub's 
schema](https://developer.github.com/v3/activity/events/types/#pushevent) 
and then:

```bash
curl \
  -vX POST http://localhost:5000/webhooks \
  -d @payload.json \
  --header "Content-Type: application/json"
```
