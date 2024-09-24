# MinecraftBridge

MinecraftBridge is a package designed to interact with Minecraft through a 
variety of backends, using a common interface.  Currently, this package allows
for interfacing through the following backends:

* ASIST Testbed through MQTT broker.

Clients interact with the MinecraftBridge through a set of pre-defined Message
classes, which encapsulate interactions with specific backends.  As each 
backend provides different capabilities for interaction, it's possible that
certain backends do not generate / support specific message classes.

## Installation

The MinecraftBridge package can be installed via `pip`.  A basic install can be done from the root folder of the package with the following command:

    pip install --user -e .

To install with all extras:

    pip install --user -e .[all]

## ASIST Requirements

This package depends on the following repository:
* [`MinecraftElements`](https://gitlab.com/cmu_asist/MinecraftElements) (version >= 0.4.3)

This can be pip-installed as an extra. From the root MinecraftBridge folder, run:

    pip install --user -e .[MinecraftElements]

If you already have `MinecraftElements` installed locally and want to avoid overriding it with remote versions, simply omit it from the extras on installation.

## Backends

The following backends are supported through the provided import statements:

* Asist Testbed through MQTT broker

    from MinecraftBridge.mqtt import Bridge


## Messages

The defined message classes are in the `messages` submodule, and consist of

* `BusHeader` - Header for MQTT bus, used as subcomponent of other messages

* `MessageHeader` - Header for MQTT bus, used as subcomponent of other messages

* `TriageCount` - Message summarizing Triage Count summaries

* `TriageEvent` - Message encapsulating a triage attempts, successes, and failures

* `PlayerState` - Message encapsulating player position, orientation, health, etc.

* `LeverEvent` - Message encapsulating change of lever states

* `DoorEvent` - Message encapsulating change of door states

* `FoVSummary` - Messages encapsulating a summary of blocks in the player's FoV

* `MissionStateEvent` - Messages encapsulating information regarding the start and stop of missions

* `VictimList` - Messages encapsulating lists of victims

* `BlockageList` - MEssages encapsulating generated blockages
