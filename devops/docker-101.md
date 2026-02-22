## Why Docker?

- Containers bundle all steps and dependencies required to run an application.
- They provide a consistent runtime, simplifying deployment across environments.
- Additional benefits include portability, scalability, and resource efficiency.

## What is a Container?

- A Docker container image is a lightweight standalone, executable package of software that includes everything needed to run an application.
- History?

### Open Container Initiative (OCI)

- The OCI is an open governance structure for the express purpose of creating open industry standards around container formats and runtimes, this is a major player in container space before Docker.
- This helps in
    - Runtime specification
    - Image specification
    - Distribution specification

## Evolution of Virtualization

### Bare Metal

- Tightly coupled dependencies leading to conflicts
- Inefficient memory utilization
- Large blast radius
- Slow boot-up & shut-down speed, could take upto few minutes at minimum.
- Very slow provisioning & decommissioning
- Add image from Excalidraw

### Virtual Machine

- No dependency conflicts
- Better utilization
- Small blast radius
- Faster startup & shut-down speed, could take upto few minutes at max
- Faster provisioning & decommissioning
- Ex. AWS Nitro System, VmWare vSphere, Microsoft Hyper-V, VirtualBox

### Containers

- No dependency conflicts
- Even better utilization
- Smaller blast radius
- Faster startup & shutdown speed, in seconds.
- Faster provisioning & decommissioning
- Lightweight in nature
- Desktop container platforms – Docker, Podman, etc.
- Runtime engines – containerd, CRI‑O, runc, etc.

## Technology Overview

The core of the container involves the following:
1. Namespaces
2. Control Groups - CGroups
3. Union Filesystem

## Namespaces

### What Are Linux Namespaces?

Kernel-level isolation that virtualizes global system resources per process group.

### What Do They Isolate?

- PID Namespace → Separate process IDs
- Network Namespace → Own IP, interfaces, routing
- Mount Namespace → Independent filesystem view
- UTS Namespace → Unique hostname
- IPC Namespace → Isolated shared memory & queues
- User Namespace → UID/GID mapping (root inside ≠ root outside)
- Cgroup Namespace → Resource visibility isolation
- Time Namespace → Independent clock offsets

### How Containers Use Them

When you run a container:

1. A process is created
2. New namespaces are assigned
3. Resource limits applied via cgroups
4. Capabilities are reduced

## Control Groups (CGroups)

Linux cgroups (Control Groups) are a kernel feature that limit and monitor how much CPU, memory, disk I/O, and other resources a group of processes can use. While namespaces provide isolation, cgroups provide resource control. Container platforms like Docker and Kubernetes use cgroups to ensure each container gets defined resource limits, preventing one workload from exhausting the host system.

### What Are Linux Cgroups?

Kernel mechanism to limit, prioritize, account, and isolate resource usage of process groups.

### What Do Cgroups Control?

- CPU → Limit usage, set shares, throttle cores
- Memory → Hard/soft limits, OOM control
- Block I/O → Disk read/write throttling
- Network (via tc integration) → Bandwidth control
- PIDs → Limit number of processes
- Accounting → Track resource consumption

### How Containers Use Cgroups

When you run:

```bash
docker run --memory=512m --cpus=1 nginx
```

Behind the scenes:

- A cgroup is created
- Memory limit = 512 MB
- CPU quota applied
- Kernel enforces limits
- If memory exceeds limit → OOM kill
- If CPU exceeds quota → Throttled

### Namespaces vs Cgroups

| Feature | Namespaces | Cgroups |
|---------|-----------|---------|
| Purpose | Isolation | Resource control |
| View | Virtual view of system | Enforced limits |
| Effect | Hide other processes | Prevent resource abuse |
| Meaning | "Who you see" | "How much you can use" |

### Cgroups v1 vs v2

| Feature | v1 | v2 |
|---------|----|----|
| Controllers | Separate hierarchies | Unified hierarchy |
| Complexity | Higher | Simpler |
| Modern distros | Legacy | Default |

Most modern Linux distributions use cgroup v2.



## Union Mount Filesystems

A Union Mount Filesystem merges multiple directories (layers) into a single unified view. **OverlayFS** is the most widely used implementation and is the foundation of container image layering.

### How It Works

```
Lowerdir (read-only image layers)
         +
Upperdir (writable container layer)
         =
Merged (unified view)
```

When a container modifies a file from the lower layer, it's copied to the upper layer first (Copy-on-Write), keeping original layers untouched.

### Why It Matters

- **Disk efficiency**: Layers shared across containers and images
- **Fast startup**: No need to copy entire image
- **Layer caching**: Reuse unchanged layers in builds
- **Image distribution**: Smaller, more efficient transfers

### Example

```dockerfile
FROM ubuntu
RUN apt install nginx
COPY . /app
```

Each instruction creates a new read-only layer. OverlayFS stacks them, and Docker adds a writable layer on top for container changes.

### OverlayFS vs Traditional Filesystem

| Feature | Traditional | OverlayFS |
|---------|-----------|-----------|
| Structure | Single directory | Layered directories |
| Writes | Direct | Copy-on-write |
| Reusability | No layer sharing | Shared read-only layers |
| Efficiency | Lower | Higher |

### OverlayFS Core Components

A convenient reference to the four directories that OverlayFS uses internally. understanding these is helpful when reasoning about how layers are stacked and where changes actually live.

- 📦 **Lowerdir** → read-only layers (base image layers) that make up the immutable portion of an image.
- ✏️ **Upperdir** → the writable overlay where all container modifications are recorded; new files are created here and modified files are copied up into it.
- 🔀 **Workdir** → an internal workspace used by the kernel for bookkeeping during operations such as copy-on-write, not visible to container processes.
- 👀 **Merged** → the final unified view that container processes interact with; it presents the combination of lower and upper directories according to overlay rules.

OverlayFS stacks the immutable lower layers, applies any modifications in the upper layer, keeps temporary state in the workdir, and exposes the combined filesystem at the merged mount point.

### Docker Components & Flow

#### Core stack (Linux native)

- **Docker CLI** → user‑facing client
- **dockerd** (daemon / manager) → controls API, lifecycle, networking
- **containerd** (runtime manager) → supervises containers
- **runc** (OCI runtime) → spawns containers using kernel syscalls
- **Linux kernel** → enforces isolation & limits via namespaces, cgroups, overlayFS, capabilities

#### Responsibilities

| Component    | Role                                     | Mnemonic        |
|--------------|------------------------------------------|-----------------|
| Docker CLI   | Sends commands to the daemon            | Client          |
| dockerd      | Manages high‑level features & API        | Manager         |
| containerd   | Handles container lifecycle             | Runtime Manager |
| runc         | Executes containers via kernel           | Executor        |
| Linux kernel | Provides the actual isolation & control  | Infrastructure  |

#### Execution flow (`docker run nginx`)

1. CLI sends a REST request to dockerd.
2. dockerd validates the request and coordinates with containerd.
3. containerd prepares the container bundle.
4. `runc`:
   - creates the necessary namespaces,
   - sets up cgroups,
   - mounts the overlay filesystem,
   - starts the container process.
5. The kernel then executes and isolates the process.

#### Docker Desktop vs native engine

On **Linux hosts** the engine runs directly:

```
Linux host → Docker Engine → Containers
```

On **macOS/Windows**, a lightweight Linux VM is introduced:

```
Host OS → Linux VM → Docker Engine → Containers
```

Docker Desktop packages the engine inside that VM (WSL2 or Apple framework).

| Feature         | Docker Engine       | Docker Desktop           |
|-----------------|---------------------|--------------------------|
| Runtime         | Native on Linux     | Inside a VM              |
| Typical use     | Production servers  | Developer machines       |
| Hypervisor      | None                | Required (WSL2/Hyperkit) |

#### Five key points to remember

1. The **Linux kernel** provides isolation, not Docker itself.
2. `runc` interacts directly with the kernel.
3. `containerd` manages container lifecycle.
4. `dockerd` adds orchestration, networking, and API features.
5. Docker Desktop simply adds a Linux VM layer to the stack.

## Using third-party libraries (containers/tools)

Need a database, a one‑off shell or a utility without touching your host?
Grab a public image and run it with Docker. Keep any state you care about on a
volume or bind‑mount, and supply options via `-e` or config files. 

Common targets are databases (Postgres, Mongo, etc.), disposable language
runtimes (`ubuntu`, `python`, `node`), or CLI helpers (`jq`, `aws-cli`).

Switching versions is as easy as changing the image tag; unless you mount a
path, containers throw away their filesystem when removed.


### I. Understanding data persistence

When we create a container from a container image, everything in the image is treated as read-only, and there is a new layer overlayed on top that is read/write.

![](./readme-assets/container-filesystem.jpg)

#### A. Installing Dependencies:

Let's experiment with how installing something into a container at runtime behaves!

***Note:** Modifying the contents of a container at runtime is not something you would normally do. We are doing it here for instructional purposes only!*


```bash
# Create a container from the ubuntu image
docker run --interactive --tty --rm ubuntu:22.04

# Try to ping google.com
ping google.com -c 1 # This results in `bash: ping: command not found`

# Install ping
apt update
apt install iputils-ping --yes

ping google.com -c 1 # This time it succeeds!
exit
```

Let's try that again:
```bash
docker run -it --rm ubuntu:22.04
ping google.com -c 1 # It fails! 🤔
```

It fails the second time because we installed it into that read/write layer specific to the first container, and when we tried again it was a **separate** container with a **separate** read/write layer!

We can give the container a name so that we can tell docker to reuse it:
```bash
# Create a container from the ubuntu image (with a name and WITHOUT the --rm flag)
docker run -it --name my-ubuntu-container ubuntu:22.04

# Install & use ping
apt update
apt install iputils-ping --yes
ping google.com -c 1
exit

# List all containers
docker container ps -a | grep my-ubuntu-container
docker container inspect my-ubuntu-container

# Restart the container and attach to running shell
docker start my-ubuntu-container
docker attach my-ubuntu-container

# Test ping
ping google.com -c 1 # It should now succeed! 🎉
exit
```

We generally never want to rely on a container to persist the data, so for a dependency like this, we would want to include it in the image:

```bash
# Build a container image with ubuntu image as base and ping installed
docker build --tag my-ubuntu-image -<<EOF
FROM ubuntu:22.04
RUN apt update && apt install iputils-ping --yes
EOF

# Run a container based on that image
docker run -it --rm my-ubuntu-image

# Confirm that ping was pre-installed
ping google.com -c 1 # Success! 🥳
```

The `FROM... RUN...` stuff is part of what is called a `Dockerfile` that is used to specify how to build a container image. We will go much deeper into building containers later in the course, but for now just understand that for anything we need in the container at runtime we should build it into the image! 

The one exception to this rule is environment specific configuration (environment variables, config files, etc...) which can be provided at runtime as a part of the environment (see: https://12factor.net/config).

#### B. Persisting Data Produced by the Application:

Often, our applications produce data that we need to safely persist (e.g. database data, user uploaded data, etc...) even if the containers are destroyed and recreated. Luckily, Docker (and containers more generally) have a feature to handle this use case called `Volumes` and `mounts`!

![](./readme-assets/volumes.jpg)

`Volumes` and `mounts` allow us to specify a location where data should persist beyond the lifecycle of a single container. The data can live in a location managed by Docker (`volume mount`), a location in your host filesystem (`bind mount`), or in memory (`tmpfs mount`, not pictured). 

***NOTE:** This third option (`tmpfs mount`) does not persist the data after the container exits, and is instead used as a temporary store for data you specifically DON'T want to persist (for example credential files). It is included here for completeness but should not be used for application data you want to persist.*

Let's experiment with how creating some data within a container at runtime behaves!

```bash
# Create a container from the ubuntu image
docker run -it --rm ubuntu:22.04

# Make a directory and store a file in it
mkdir my-data
echo "Hello from the container!" > /my-data/hello.txt

# Confirm the file exists
cat my-data/hello.txt
exit
```

If we then create a new container, (as expected) the file does not exist!

```bash
# Create a container from the ubuntu image
docker run -it --rm ubuntu:22.04

# Check if the file exists
cat my-data/hello.txt # Produces error: `cat: my-data/hello.txt: No such file or directory`
```

##### i. Volume Mounts
We can use volumes and mounts to safely persist the data.

```bash
# create a named volume
docker volume create my-volume

# Create a container and mount the volume into the container filesystem
docker run  -it --rm --mount source=my-volume,destination=/my-data/ ubuntu:22.04
# There is a similar (but shorter) syntax using -v which accomplishes the same
docker run  -it --rm -v my-volume:/my-data ubuntu:22.04

# Now we can create and store the file into the location we mounted the volume
echo "Hello from the container!" > /my-data/hello.txt
cat my-data/hello.txt
exit
```

We can now create a new container and mount the existing volume to confirm the file persisted:

```bash
# Create a new container and mount the volume into the container filesystem
docker run  -it --rm --mount source=my-volume,destination=/my-data/ ubuntu:22.04
cat my-data/hello.txt # This time it succeeds! 
exit
```

Where is this data located? On linux it would be at `/var/lib/docker/volumes`... but remember, on docker desktop, Docker runs a linux virtual machine.

One way we can view the filesystem of that VM is to use a [container image](https://hub.docker.com/r/justincormack/nsenter1) created by `justincormack` that allows us to create a container within the namespace of PID 1. This effectively gives us a container with root access in that VM. 

***NOTE:** Generally you should be careful running containers in privileged mode with access to the host system in this way. Only do it if you have a specific reason to do so and you trust the container image.*

```bash
# Create a container that can access the Docker Linux VM
# Pinning to the image hash ensures it is this SPECIFIC image and not an updated one helps minimize the potential of a supply chain attack
docker run -it --rm --privileged --pid=host justincormack/nsenter1@sha256:5af0be5e42ebd55eea2c593e4622f810065c3f45bb805eaacf43f08f3d06ffd8

# Navigate to the volume inside the VM at:
ls /var/lib/docker/volumes/my-volume/_data
cat /var/lib/docker/volumes/my-volume/_data/hello.txt # Woohoo! we found our data!
```

This approach can then be used to mount a volume at the known path where a program persists its data:
```bash
# Create a container from the postgres container image and mount its known storage path into a volume named pgdata
docker run -it --rm -v pgdata:/var/lib/postgresql/data -e POSTGRES_PASSWORD=foobarbaz postgres:15.1-alpine
```

##### ii. Bind Mounts

Alternatively, we can mount a directory from the host system using a bind mount:

```bash
# Create a container that mounts a directory from the host filesystem into the container
docker run  -it --rm --mount type=bind,source="${PWD}"/my-data,destination=/my-data ubuntu:22.04
# Again, there is a similar (but shorter) syntax using -v which accomplishes the same
docker run  -it --rm -v ${PWD}/my-data:/my-data ubuntu:22.04

echo "Hello from the container!" > /my-data/hello.txt

# You should also be able to see the hello.txt file on your host system
cat my-data/hello.txt
exit
```

Bind mounts can be nice if you want easy visibility into the data being stored, but there are a number of reasons outlined at https://docs.docker.com/storage/volumes/ (including speed if you are running Docker Desktop on windows/mac) for why volumes are preferred. 

### II. Use Cases

Now that we have an understanding of how data storage works with containers we can start to explore various use cases for running 3rd party containers.

For me, the main categories are databases, interactive test environments, and CLI utilities.

#### A. Databases

Databases are notoriously fickle to install and configure. The instructions are often complex and vary across different versions and operating systems. For development, where you might need to run multiple versions of a single database or create a fresh database for testing purposes running in a container can be a massive improvement.

The setup/installation is handled by the container image, and all you need to provide is some configuration values. Switching between versions of the database is as easy as specifying a different image tag (e.g. `postgres:14.6` vs `postgres:15.1` ).

A few key considerations when running databases in containers:
- **Use volume(s) to persist data:** The entire reason for section above was to give you an understanding of how to avoid data loss. Generally databases will store its data at one or more known paths. You should identify those and mount volumes to those locations in the containers to ensure data persists beyond the container.
- **Use bind mount(s) for additional config:** Often databases use configuration files to influence runtime behavior. You can create these files on your host system, and then use a bind mount to place them in the correct location within the container to be read upon startup.
- **Set environment variables:** In addition to configuration files many databases use environment variables to influence runtime behavior (for example setting the admin password). Identify these variables and set the accordingly.

Here are a some useful databases container images and sample commands that attempt to mount the necessary data directories into volumes and set key environment variables.

🚨🚨🚨 ***WARNING:** While I have made a best effort to set up the volume mounts properly, please confirm the volume mounts match the location data is persisted within the container independently to ensure your data safety.* 🚨🚨🚨

#### Postgres 
https://hub.docker.com/_/postgres
```bash
docker run -d --rm \
  -v pgdata:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=foobarbaz \
  -p 5432:5432 \
  postgres:15.1-alpine

# With custom postresql.conf file
docker run -d --rm \
  -v pgdata:/var/lib/postgresql/data \
  -v ${PWD}/postgres.conf:/etc/postgresql/postgresql.conf \
  -e POSTGRES_PASSWORD=foobarbaz \
  -p 5432:5432 \
  postgres:15.1-alpine -c 'config_file=/etc/postgresql/postgresql.conf'
```

#### Mongo
https://hub.docker.com/_/mongo
```bash
docker run -d --rm \
  -v mongodata:/data/db \
  -e MONGO_INITDB_ROOT_USERNAME=root \
  -e MONGO_INITDB_ROOT_PASSWORD=foobarbaz \
  -p 27017:27017 \
  mongo:6.0.4

# With custom mongod.conf file
docker run -d --rm \
  -v mongodata:/data/db \
  -v ${PWD}/mongod.conf:/etc/mongod.conf \
  -e MONGO_INITDB_ROOT_USERNAME=root \
  -e MONGO_INITDB_ROOT_PASSWORD=foobarbaz \
  -p 27017:27017 \
  mongo:6.0.4 --config /etc/mongod.conf
```

#### Redis
https://hub.docker.com/_/redis

Depending how you are using redis within your application, you may or may not care if the data is persisted.

```bash
docker run -d --rm \
  -v redisdata:/data \
  redis:7.0.8-alpine

# With custom redis.conf file
docker run -d --rm \
  -v redisdata:/data \
  -v ${PWD}/redis.conf:/usr/local/etc/redis/redis.conf \
  redis:7.0.8-alpine redis-server /usr/local/etc/redis/redis.conf
```

#### MySQL
https://hub.docker.com/_/mysql
```bash
docker run -d --rm \
  -v mysqldata:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=foobarbaz \
  -p 3306:3306 \
  mysql:8.0.32

# With custom conf.d
docker run -d --rm \
  -v mysqldata:/var/lib/mysql \
  -v ${PWD}/conf.d:/etc/mysql/conf.d \
  -e MYSQL_ROOT_PASSWORD=foobarbaz \
  -p 3306:3306 \
  mysql:8.0.32
```

#### Elasticsearch
https://hub.docker.com/_/elasticsearch
```bash
docker run -d --rm \
  -v elasticsearchdata:/usr/share/elasticsearch/data
  -e ELASTIC_PASSWORD=foobarbaz \
  -e "discovery.type=single-node" \
  -p 9200:9200 \
  -p 9300:9300 \
  elasticsearch:8.6.0
```

#### Neo4j
https://hub.docker.com/_/neo4j

```bash
docker run -d --rm \
    -v=neo4jdata:/data \
    -e NEO4J_AUTH=neo4j/foobarbaz \
    -p 7474:7474 \
    -p 7687:7687 \
    neo4j:5.4.0-community
```

#### B. Interactive Test Environments

#### i. Operating systems

```bash
# https://hub.docker.com/_/ubuntu
docker run -it --rm ubuntu:22.04

# https://hub.docker.com/_/debian
docker run -it --rm debian:bullseye-slim

# https://hub.docker.com/_/alpine
docker run -it --rm alpine:3.17.1

# https://hub.docker.com/_/busybox
docker run -it --rm busybox:1.36.0 # small image with lots of useful utilities
```


#### ii. Programming runtimes:
```bash
# https://hub.docker.com/_/python
docker run -it --rm python:3.11.1

# https://hub.docker.com/_/node
docker run -it --rm node:18.13.0

# https://hub.docker.com/_/php
docker run -it --rm php:8.1

# https://hub.docker.com/_/ruby
docker run -it --rm ruby:alpine3.17
```

#### C. CLI Utilities

Sometimes you don't have a particular utility installed on your current system, or breaking changes between versions make it handy to be able to run a specific version of a utility inside of a container without having to install anything on the host!

**jq (json command line utility)**

https://hub.docker.com/r/stedolan/jq
```bash
docker run -i stedolan/jq <sample-data/test.json '.key_1 + .key_2'
```

**yq (yaml command line utility)**

https://hub.docker.com/r/mikefarah/yq
```bash
docker run -i mikefarah/yq <sample-data/test.yaml '.key_1 + .key_2'
```

**sed**

GNU `sed` behaves differently from the default MacOS version for certain edge cases.
```bash
docker run -i --rm busybox:1.36.0 sed 's/file./file!/g' <sample-data/test.txt
```

**base64**

GNU `base64` behaves differently from the default MacOS version for certain edge cases.
```bash
# Pipe input from previous command
echo "This string is just long enough to trigger a line break in GNU base64." | docker run -i --rm busybox:1.36.0 base64

# Read input from file
docker run -i --rm busybox:1.36.0 base64 </sample-data/test.txt
```

**Amazon Web Services CLI**

https://hub.docker.com/r/amazon/aws-cli
```bash
# Bind mount the credentials into the container
docker run --rm -v ~/.aws:/root/.aws amazon/aws-cli:2.9.18 s3 ls
```

**Google Cloud Platform CLI**

```bash
# Bind mount the credentials into the container
docker run --rm -v ~/.config/gcloud:/root/.config/gcloud gcr.io/google.com/cloudsdktool/google-cloud-cli:415.0.0 gsutil ls
# Why is the container image so big 😭?! 2.8GB
```

#### D. Improving the Ergonomics

If you plan to use one of these utilities inside of a container frequently, it can be useful to use a shell function or alias to make the ergonomics feel like the program is installed on the host. Here are examples of this for `yq`:

```bash
# Shell function
yq-shell-function() {
  docker run --rm -i -v ${PWD}:/workdir mikefarah/yq "$@"
}
yq-shell-function <sample-data/test.yaml '.key_1 + .key_2'
```

---

#### Alias
alias 'yq-alias=docker run --rm -i -v ${PWD}:/workdir mikefarah/yq'
yq-alias <sample-data/test.yaml '.key_1 + .key_2'
```
