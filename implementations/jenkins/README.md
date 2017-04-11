# Jenkins implementation of PopperCI

We have an image in the docker hub with a job that implements the 
pipeline. To launch this image:

```bash
docker run --name=jenkins \
  -u root \
  -e JENKINS_HOME=/var/lib/jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /usr/bin/docker:/usr/bin/docker \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp:/tmp \
  ivotron/jenkins-popperci:2.32.3
```

he plugins in the image are the following:

  * Pipeline
  * Credentials
  * Credentials Binding
  * Git
  * SSH agent
  * User env vars

A `test` job with `REPO_URL` and `EXPERIMENT` parameters should be 
able to run Popperized single-node experiments that depend only on 
docker/bash like the one in <https://github.com/ivotron/sample-paper>. 
Username/password is `admin` for both.
