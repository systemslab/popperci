# Python-based PopperCI pipeline

Implements the pipeline in python. We package this in a docker image 
(see `docker/` folder). We assume the environment contains all the 
dependencies necessary to run all the PopperCI stages. The script 
creates a `popper_logs` folder and at the end of the experiment, a 
`popper_status` file is written with the CI result of the experiment.

## `popper check` command

The [Popper 
CLI](https://github.com/systemslab/popper/tree/master/popper) makes it 
convenient for users to test an experiment on their local machine, 
before pushing changes and triggering an execution on a PopperCI 
server. This assumes that Docker is available where `popper check` is 
being executed.

An environment is defined with `-e` and `-v` flags, in the similar way 
that these are used when invoking [`docker 
run`](https://docs.docker.com/engine/reference/run/). Sample usage:

```bash
popper check \
  -e CLOUDLAB_USER=ivotron
  -e CLOUDLAB_KEY=/tmp/key
  -v $HOME/mycloudlabkey.pub:/tmp/key
```

The above creates a container and makes the current directory (where 
`popper check` is invoked from) the working working directory inside 
the container. The PopperCI pipeline is then executed inside the 
container, making use of all the environmental variables and paths 
passed with `-e` and `-v`.
