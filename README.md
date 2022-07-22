# QuTech Quantum Network Explorer MCH2022 Workshop

Welcome to QuTech's [Quantum Network Explorer](https://www.quantum-network.com/) MCH2022 Workshop!

This workshop consists of two parts;

First, a basic introduction to quantum networks. Here, the basic building blocks of a quantum
internet are introduced: quantum bits (qubits), entanglement, and quantum repeaters. This is
presented live, but the [slides are included in this repository](2022-07-23---mch.pptx).

Secondly, to illustrate these concepts, we will go through an implementation of a simple Quantum Key
Distribution (QKD) application whereby Alice and Bob create a quantum-secured secret key which they
can use to encrypt their communication. This will be done in Python using the tools available on the
Quantum Network Explorer. The rest of this README contains the instructions for this part.

You can proceed in two ways:
1. Install the [pre-requisites](#pre-requisites) and then follow further instructions on the screen.
2. Install the [pre-requisites](#pre-requisites) and learn how to [create
   applications](#creating-the-application), [create experiments](#creating-an-experiment), and [run
   experiments](#running-your-experiment) (all documented in this README.md below). Then implement
   the QKD protocol yourself based on the protocol description in the [included
   slides](2022-07-23---mch.pptx). You may still find it helpful to follow the on screen
   instructions for creating applications and running experiments.

## Pre-requisites

Firstly, the recommended OS for this workshop is Linux. If you are using Windows, please install
Linux in a virtual machine or enable [Bash on
Ubuntu](https://docs.microsoft.com/en-us/windows/wsl/). MacOS in principle should work, but it often
causes issues due to `squidasm`'s dependencies. You may try your luck, but you are advised to
install Linux in a virtual machine.

Secondly, you will need Python installed on your machine for this challenge.

**CRITICAL: USE A PYTHON VERSION <= 3.9 --- DO NOT USE PYTHON 3.10**.

The quantum network simulator, NetSquid, has not been updated for Python 3.10 yet.

Before continuing, it is recommended that you set up and work in a Python Virtual Environment. For
more information, please see [this tutorial](https://docs.python.org/3/tutorial/venv.html). In
addition to isolating your environment, it will also allow you to use an older Python version
without having to uninstall Python 3.10 (if you have it). It is assumed from this point, that you
are running in a Python virtual environment. The instructions should still work without a virtual
environment, but they might be more difficult to debug in case something goes wrong.

In order to make use of QuTech's discrete simulator for quantum networks,
[NetSquid](https://netsquid.org/), you will need to first agree to the terms of service by
registering on the community forum. [Please register by following this
link](https://forum.netsquid.org/ucp.php?mode=register). Write down your chosen username and
password, you will need it in a moment.

Next, you need to install SquidASM and the Quantum Network Explorer Application Development Kit
(QNE-ADK). [SquidASM](https://github.com/QuTech-Delft/squidasm) is a
[NetQASM](https://github.com/QuTech-Delft/netqasm) application processor built on top of the
NetSquid quantum network simulator. You will use SquidASM to simulate your quantum network
applications. The QNE-ADK offers a CLI interface for creating and running network experiments.

You can install both easily by running the following commands(you will be prompted for your username
and password that you chose earlier):

Run the following commands:

```sh
pip3 install -e "git+https://github.com/QuTech-Delft/qne-adk.git@a125b2d27f1e5fef2822329cf824b18e22e9d00e#egg=qne-adk"
pip3 install squidasm==0.9.0 --extra-index-url https://pypi.netsquid.org
```

You can verify the QNE ADK installation by running

``` sh
qne --help
```

## Creating the application

First, you need to create the application which contains the source code directory. To create the
application directory, please run

``` sh
qne application create qkd alice bob
```

This will create an application called `qkd` consisting of two programs, `alice` and `bob`, that
will run on separate nodes. You can choose the application name, as well as the node names, to be
whatever you wish.

You will mainly be writing code in `qkd/src/app_alice.py` and `qkd/src/app_bob.py`. For more
information about the directory structure and how to configure the application, please refer to the
[application configuration
guide](https://www.quantum-network.com/knowledge-base/application-configuration/). For more
information on options available through the CLI, please consult `qne application --help`.

## Creating an experiment

An application is not very useful if it does not run on some network as part of some kind of
experiment. To run your application, you first need to create an experiment. To create an
experiment, please run

``` sh
qne experiment create exp qkd randstad
```

This creates an experiment called `exp` running your application called `qkd` on a pre-configured
network called `randstad`. [The Randstad](https://en.wikipedia.org/wiki/Randstad) is an area in the
Netherlands consisting primarily of the four largest Dutch cities (Amsterdam, Rotterdam, The Hague,
and Utrecht) and their surroundings. The details of the available networks, their nodes, and
available channels can be found in the Randstad section on the [network configuration
page](https://www.quantum-network.com/knowledge-base/network-information/).

For more information about the directory structure and how to configure the application, please
refer to the [experiment configuration
guide](https://www.quantum-network.com/knowledge-base/experiment-configuration/). For more
information on options available through the CLI, please consult `qne experiment --help`.

## Running your experiment

Once you have an experiment created you can run it with

``` sh
qne experiment run exp --timeout 30
```

Where you replace `exp` with the experiment name you chose earlier, if it's different from `exp`.

You can view the results of the experiment in `exp/results/processed.json` or by running `qne
experiment results exp --show` (replacing `exp` with your experiment name if necessary). The results
found at the top under `round_result` contain the contents of the dictionaries returns by
`app_alice.py` and `app_bob.py`.

## Iterating on your application

Once created you can rerun the experiment as many times as you wish.

**DO NOT MODIFY the source files in the experiment directory**. They are overwritten with every
experiment run.

If you need to change the application code, make sure you change it in the application directory
`qkd/src`. These files will be copied over to the experiment directory with every run.

To configure your experiment, you can modify the `experiment.json` file in your experiment
directory. You will want to pay particular attention to the `roles` entry which identify the nodes
where your `alice` and `bob` applications are run. By default this will be `amsterdam` and `leiden`
for the `randstad` network. Therefore, the parameters of the relevant quantum channel for your
application are in the entry identified by the `slug` `amsterdam-leiden`.

Please see [experiment
configuration](https://www.quantum-network.com/knowledge-base/experiment-configure/) for more
details on how to use this file.

## Application example

It may be useful to go through an application example to see how to write a quantum network
application. To see such an example, please see [this application
example](https://www.quantum-network.com/knowledge-base/application-example/).

## NetQASM documentation

As you will have seen from the application example, applications are written using the [NetQASM
SDK](https://github.com/QuTech-Delft/netqasm). For detailed documentation about the available
functionality, please see the [documentation page](https://netqasm.readthedocs.io/en/latest/), and
in particular [netqasm.sdk](https://netqasm.readthedocs.io/en/latest/netqasm.sdk.html).

You may also want to read the paper introducing [NetQASM](https://arxiv.org/abs/2111.09823).
