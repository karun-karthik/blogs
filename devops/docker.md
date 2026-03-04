# Docker

### What is Docker?

* Docker is a container technology: A tool for creating and managing containers
* Container is a standardized unit of software.
  - a package of code**and** dependencies to run that code. (ex. Py code + the Py runtime)
  - the same container yields the exact same application and execution behaviour, irrespective of executor or the system of execution.

### Why Containers?

For independent and standardized "application packages"

* because we want the`exact same env` for dev & prod
* we want`reproducibility` of behaviour
* for isolation of dependencies/preventing dependency conflicts

### Virutal Machines vs. Docker Containers

* Simple Virtual Machine structure

- This wastes a lot of space on the hard drive and tends to be slow

```mermaid
flowchart TB
  host["Your Operating System"]

  subgraph A["Environment A"]
    A1["App A"]
    A2["Libraries, Dependencies, Tools"]
    A3["Virtual OS (e.g. Linux)"]
    A1 --> A2 --> A3
  end

  subgraph B["Environment B"]
    B1["App B"]
    B2["Libraries, Dependencies, Tools"]
    B3["Virtual OS (e.g. Linux)"]
    B1 --> B2 --> B3
  end

  subgraph C["Environment C"]
    C1["App C"]
    C2["Libraries, Dependencies, Tools"]
    C3["Virtual OS (e.g. Linux)"]
    C1 --> C2 --> C3
  end

  A3 --> host
  B3 --> host
  C3 --> host
```

| Pros of VM                                     |                      Cons of VM                      |
| ---------------------------------------------- | :--------------------------------------------------: |
| Separated environments                         |              Redundant, Waste of space              |
| Env-specific config                            |        Slow performance and longer boot time        |
| Shareable env-config for reproducing behaviour | reproducing on another server is possible but tricky |

#### Docker Containers

```mermaid
flowchart TB

subgraph C1[Container A]
A1[App A]
L1[Libraries, Dependencies, Tools]
A1 --> L1
end

subgraph C2[Container B]
A2[App B]
L2[Libraries, Dependencies, Tools]
A2 --> L2
end

subgraph C3[Container C]
A3[App C]
L3[Libraries, Dependencies, Tools]
A3 --> L3
end

Docker[Docker Engine]
Support[OS Built-in / Emulated Container Support]
HostOS[Your Operating System]

L1 --> Docker
L2 --> Docker
L3 --> Docker

Docker --> Support
Support --> HostOS
```

| Docker Containers                                  | Virtual Machines                                                     |
| -------------------------------------------------- | -------------------------------------------------------------------- |
| Low impact on OS, very fast and minimal disk usage | High impact on OS, slower and higher disk usage                      |
| Sharing, re-building & distribution is easy        | Sharing, re-building & distribution can be tricky                    |
| Encapsulates the app/environment                   | Encapsulates the whole machine ~ results in bloating the application |
