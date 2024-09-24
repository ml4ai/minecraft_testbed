Messages
========

This section summarizes individual message classes used by `MinecraftBridge`.  As the primary purpose of this package is for interfacing with the DARPA ASIST Minecraft Testbed, message classes primarily reflect the message specifications produced for that project.

For each message listed in this section, a table is provided which describes the properties of the message, aliases for the property, and keyword arguments accetped to assign value to the property during creation.  Additionally, unless otherwise indicated, the behaviors and properties from `BaseMessage` will be inherited for each message class.  For specific messages, additional notes may be provided, as well as descriptions of related classes and use cases, where applicable.


BaseMessage
-----------

.. table:: Properties for `BaseMessage` class
    :name: base_message_properties

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | mission_timer        | tuple of integers; | mission_timer              |
    |                      |                    |                            |
    | missionTimer         | string as argument |                            |
    +----------------------+--------------------+----------------------------+
    | elapsed_milliseconds | integer            | elapsed_milliseconds       |
    +----------------------+--------------------+----------------------------+

* The `BaseMessage` is a common abstract parent class from which all messages are derived.  

* All message subclasses will also have these properties, however, they may be initialized to default values of (-1,-1) for `mission_timer` and -1 for `elapsed_milliseconds` if the properties are not relevant to the specific message class.


Agent Intervention Messages
---------------------------

AgentIntervention
~~~~~~~~~~~~~~~~~

.. table:: Properties for `AgentIntervention` class
    :name: agent_intervention_properties

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | id                   | string             | id                         |
    +----------------------+--------------------+----------------------------+
    | agent                | string             | agent                      |
    +----------------------+--------------------+----------------------------+
    | created              | string             | created                    |
    +----------------------+--------------------+----------------------------+
    | start                | tuple of ints      | start                      |
    +----------------------+--------------------+----------------------------+
    | end                  | string             | end                        |
    +----------------------+--------------------+----------------------------+
    | explanation          | dictionary         | explanation                |
    +----------------------+--------------------+----------------------------+


AgentChatIntervention
~~~~~~~~~~~~~~~~~~~~~

.. table:: Properties for `AgentChatIntervention` class
    :name: agent_chat_intervention_properties

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | content              | string             | content                    |
    +----------------------+--------------------+----------------------------+
    | receiver             | string             | receiver                   |
    +----------------------+--------------------+----------------------------+
    | type                 | string             | type                       |
    +----------------------+--------------------+----------------------------+
    | renderer             | string             | renderer                   |
    +----------------------+--------------------+----------------------------+


Agent Prediction Messages
-------------------------

AgentPredictionBaseMessage
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: Properties for `AgentPredictionBaseMessage` class
    :name: agent_prediction_base_message_properties

    +----------------------+------------------------------+----------------------------+
    | Property             | Expected Datatype            | Accepted Keyword Arguments |
    +======================+==============================+============================+
    | group                | AgentPredictionGroupProperty | group                      |
    +----------------------+------------------------------+----------------------------+
    | created              | string                       | created                    |
    +----------------------+------------------------------+----------------------------+

AgentActionPredictionMessage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: Properties for `AgentActionPredictionMessage` class
    :name: agent_action_prediction_message_properties

    +----------------------+-------------------------------+----------------------------+
    | Property             | Expected Datatype             | Accepted Keyword Arguments |
    +======================+===============================+============================+
    | predictions          | list of AgentActionPrediction | predictions                |
    +----------------------+-------------------------------+----------------------------+

AgentStatePredictionMessage
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: Properties for `AgentStatePredictionMessage` class
    :name: agent_state_prediction_message_properties

    +----------------------+-------------------------------+----------------------------+
    | Property             | Expected Datatype             | Accepted Keyword Arguments |
    +======================+===============================+============================+
    | predictions          | list of AgentStatePrediction  | predictions                |
    +----------------------+-------------------------------+----------------------------+

AgentActionPrediction
~~~~~~~~~~~~~~~~~~~~~

.. table:: Properties for `AgentActionPrediction` class
    :name: agent_action_prediction_properties

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | unique_id            | string             | unique_id                  |
    +----------------------+--------------------+----------------------------+
    | start                | string             | start                      |
    +----------------------+--------------------+----------------------------+
    | duration             | string             | duration                   |
    +----------------------+--------------------+----------------------------+
    | predicted_property   | string             | predicted_property         |
    +----------------------+--------------------+----------------------------+
    | action               | string             | action                     |
    +----------------------+--------------------+----------------------------+
    | using                | string             | using                      |
    +----------------------+--------------------+----------------------------+
    | subject              | string             | subject                    |
    +----------------------+--------------------+----------------------------+
    | object               | string             | object                     |
    +----------------------+--------------------+----------------------------+
    | probability_type     | string             | probability_type           |
    +----------------------+--------------------+----------------------------+
    | probability          | string or float    | probability                |
    +----------------------+--------------------+----------------------------+
    | confidence_type      | string             | confidence_type            |
    +----------------------+--------------------+----------------------------+
    | confidence           | string or float    | confidence                 |
    +----------------------+--------------------+----------------------------+
    | explanation          | dictionary         | explanation                |
    +----------------------+--------------------+----------------------------+

AgentStatePrediction
~~~~~~~~~~~~~~~~~~~~

.. table:: Properties for `AgentStatePrediction` class
    :name: agent_state_prediction_properties

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | unique_id            | string             | unique_id                  |
    +----------------------+--------------------+----------------------------+
    | start                | string             | start                      |
    +----------------------+--------------------+----------------------------+
    | duration             | string             | duration                   |
    +----------------------+--------------------+----------------------------+
    | subject_type         | string             | subject_type               |
    +----------------------+--------------------+----------------------------+
    | subject              | string             | subject                    |
    +----------------------+--------------------+----------------------------+
    | predicted_property   | string             | predicted_property         |
    +----------------------+--------------------+----------------------------+
    | prediction           | string             | prediction                 |
    +----------------------+--------------------+----------------------------+
    | probability_type     | string             | probability_type           |
    +----------------------+--------------------+----------------------------+
    | probability          | string or float    | probability                |
    +----------------------+--------------------+----------------------------+
    | confidence_type      | string             | confidence_type            |
    +----------------------+--------------------+----------------------------+
    | confidence           | string or float    | confidence                 |
    +----------------------+--------------------+----------------------------+
    | explanation          | dictionary         | explanation                |
    +----------------------+--------------------+----------------------------+

AgentPredictionGroupProperty
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: Properties for `AgentPredictionGroupProperty` class
    :name: agent_prediction_group_property_properties

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | start                | string             |                            |
    +----------------------+--------------------+----------------------------+
    | duration             | float              |                            |
    +----------------------+--------------------+----------------------------+
    | explanation          | dictionary         | explanation                |
    +----------------------+--------------------+----------------------------+


AgentVersionInfo
----------------
    
.. table:: Properties for `AgentVersionInfo` class
    :name: agent_version_info_message_properties

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | agent_name           | string             | agent_name                 |
    +----------------------+--------------------+----------------------------+
    | version              | string             | version                    |
    +----------------------+--------------------+----------------------------+
    | owner                | string             | owner                      |
    +----------------------+--------------------+----------------------------+
    | source               | list of strings    | source                     |
    +----------------------+--------------------+----------------------------+
    | dependencies         | list of strings    | dependencies               |
    +----------------------+--------------------+----------------------------+
    | config               | dictionary         | config                     |
    +----------------------+--------------------+----------------------------+
    | publishes            | list of tuples     | publishes                  |
    +----------------------+--------------------+----------------------------+
    | subscribes           | list of tuples     | subscribes                 |
    +----------------------+--------------------+----------------------------+

* `source`, `dependencies`, `config`, `publishes`, and `subscribes` are optional keyword arguments


BeepEvent
---------

.. table:: Properties for `BeepEvent` class
    :name: beep_event_message_properties

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | sourceEntity         | string             | sourceEntity               |
    |                      |                    |                            |
    | source_entity        |                    |                            |
    +----------------------+--------------------+----------------------------+
    | message              | string             | message                    |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of floats    | location                   |
    |                      |                    |                            |
    | beep_x               | float              |                            |
    |                      |                    |                            |
    | beep_y               | float              |                            |
    |                      |                    |                            |
    | beep_z               | float              |                            |
    +----------------------+--------------------+----------------------------+

* `beep_x`, `beep_y`, and `beep_z` correspond to specific elements of `location`, i.e., `location` = (`beep_x`, `beep_y`, `beep_z`).



BlockageList
------------

.. table:: Properties for `BlockageList` class
    :name: blockage_list_message_properties

    +-----------------------+--------------------+----------------------------+
    | Property              | Expected Datatype  | Accepted Keyword Arguments |
    +=======================+====================+============================+
    | mission               | string             | mission                    |
    +-----------------------+--------------------+----------------------------+
    | blockages             | list of `Blockage` | blockages (optional)       |
    |                       |                    |                            |
    | mission_blockage_list |                    |                            |
    +-----------------------+--------------------+----------------------------+

* `blockages` is an optional keyword argument; if not provided, `blockages` will be set to an empty list.

* Adding individual `Blockage` instances can be achieved with the `add(blockage)` method of the class.

* Once all blocks have been added, the `finalize()` method should be called to make the message immutable.

Blockage
~~~~~~~~


ChatEvent
---------

.. _chat_event_message_properties:
.. table:: Properties for `ChatEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | sender               | string             | sender                     |
    +----------------------+--------------------+----------------------------+
    | addressees           | list of strings    | addressees                 |
    +----------------------+--------------------+----------------------------+
    | text                 | string             | text                       |
    +----------------------+--------------------+----------------------------+


CompetencyTaskEvent
-------------------

.. _competency_task_event_message_properties:
.. table:: Properties for `CompetencyTaskEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | taskMessage          | string             | taskMessage                |
    |                      |                    |                            |
    | task_message         |                    |                            |
    +----------------------+--------------------+----------------------------+
    | playerName           | string             | playerNAme                 |
    +----------------------+--------------------+----------------------------+
    | callSign             | string             | callSign                   |
    +----------------------+--------------------+----------------------------+


DoorEvent
---------

:numref:`door_event_message_properties` summarizes the properties for the `DoorEvent` class.  Note that `door_x`, `door_y`, and `door_z` correspond to individual elements of `location` / `position`.

.. _door_event_message_properties:
.. table:: Properties for `DoorEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    +----------------------+--------------------+----------------------------+
    | position             | tuple of integers  | position                   |
    |                      |                    |                            |
    | location             |                    |                            |
    |                      |                    |                            |
    | door_x               | integer            |                            |
    |                      |                    |                            |
    | door_y               | integer            |                            |
    |                      |                    |                            |
    | door_z               | integer            |                            |
    +----------------------+--------------------+----------------------------+
    | opened               | boolean            | opened                     |
    |                      |                    |                            |
    | open                 |                    |                            |
    +----------------------+--------------------+----------------------------+

* `door_x`, `door_y`, and `door_z` correspond to individual elements of `location`, i.e., `location` = (`door_x`, `door_y`, `door_z`)

Experiment
----------

.. _experiment_message_properties:
.. table:: Properties for `Experiment` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | name                 | string             | name                       |
    +----------------------+--------------------+----------------------------+
    | date                 | string             | date                       |
    +----------------------+--------------------+----------------------------+
    | author               | string             | author                     |
    +----------------------+--------------------+----------------------------+
    | mission              | string             | mission                    |
    +----------------------+--------------------+----------------------------+


FoVSummary
----------

.. _fov_summary_message_properties:
.. table:: Properties for `FoVSummary` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    +----------------------+--------------------+----------------------------+
    | observationNumber    | integer            | observationNumber          |
    +----------------------+--------------------+----------------------------+
    | blocks               | list of dicts      | blocks (optional)          |
    +----------------------+--------------------+----------------------------+

* Providing the `blocks` keyword argument is optional; by default, the property is set to an empty list.  

* Block summaries can be added to the `blocks` property through the `addBlock(summary)` method.


FoV_VersionInfo
---------------

.. _fov_version_info_message_properties:
.. table:: Properties for `FoV_VersionInfo` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | version              | string             | version                    |
    +----------------------+--------------------+----------------------------+
    | url                  | string             | url                        |
    +----------------------+--------------------+----------------------------+
    | dependencies         | list of            | dependencies (optional)    |
    |                      | FoV_Dependency     |                            |
    +----------------------+--------------------+----------------------------+

* `dependencies` is an optional keyword argument; if not provided, the property will default to an empty list.  

* Dependencies can be added with the `addDependency(dependency)` method.


FoV_Dependency
~~~~~~~~~~~~~~

.. _fov_dependency_message_properties:
.. table:: Properties for `FoV_Dependency` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | package              | string             | package                    |
    +----------------------+--------------------+----------------------------+
    | version              | string             | version                    |
    +----------------------+--------------------+----------------------------+
    | url                  | string             | url                        |
    +----------------------+--------------------+----------------------------+


FoV_MapMetadata
---------------

.. _fov_map_metadata_message_properties:
.. table:: Properties for `FoV_MapMetadata` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | map_name             | string             | map_name                   |
    +----------------------+--------------------+----------------------------+
    | world_name           | string             | world_name                 |
    +----------------------+--------------------+----------------------------+
    | map_url              | string             | map_url                    |
    +----------------------+--------------------+----------------------------+
    | world_url            | string             | world_url                  |
    +----------------------+--------------------+----------------------------+
    | creation_time        | string             | creation_time              |
    +----------------------+--------------------+----------------------------+
    | lower_bound          | tuple of floats    | lower_bound                |
    +----------------------+--------------------+----------------------------+
    | upper_bound          | tuple of floats    | upper_bound                |
    +----------------------+--------------------+----------------------------+
    | ignored_blocks       | list               | ignored_blocks             |
    +----------------------+--------------------+----------------------------+
    | parser_metadata      | dictionary         | parser_metadata            |
    +----------------------+--------------------+----------------------------+


FreezeBlockList
---------------

.. _freezeblock_list_message_properties:
.. table:: Properties for `FreezeBlockList` class

    +--------------------------+--------------------+----------------------------+
    | Property                 | Expected Datatype  | Accepted Keyword Arguments |
    +==========================+====================+============================+
    | mission                  | string             | mission                    |
    +--------------------------+--------------------+----------------------------+
    | freezeblocks             | list of            | freezeblocks (optional)    |
    |                          |                    |                            |
    | mission_freezeblock_list | Freezeblocks       |                            |
    +--------------------------+--------------------+----------------------------+

* `freezeblocks` is an optional argument; if not provided, the attribute will be set to an empty list.


FreezeBlock
~~~~~~~~~~~

.. _freezeblock_properties:
.. table:: Properties for `FreezeBlock` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | location             | tuple of integers  | location                   |
    |                      |                    |                            |
    | x                    | integer            |                            |
    |                      |                    |                            |
    | y                    | integer            |                            |
    |                      |                    |                            |
    | z                    | integer            |                            |
    +----------------------+--------------------+----------------------------+
    | block_type           | string             | block_type                 |
    +----------------------+--------------------+----------------------------+
    | room_name            | string             | room_name                  |
    +----------------------+--------------------+----------------------------+


GasLeakPlacedEvent
------------------

.. _gasleak_placed_event_message_properties:
.. table:: Properties for `GasLeakPlacedEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | location             | tuple of integers  | location                   |
    |                      |                    |                            |
    | gasleak_x            | integer            |                            |
    |                      |                    |                            |
    | gasleak_y            | integer            |                            |
    |                      |                    |                            |
    | gasleak_z            | integer            |                            |
    +----------------------+--------------------+----------------------------+


GasLeakRemovedEvent
-------------------

.. _gasleak_removed_event_message_properties:
.. table:: Properties for `GasLeakRemovedEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | `source`             | string             | `source`                   |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of integers  | location                   |
    |                      |                    |                            |
    | gasleak_x            | integer            |                            |
    |                      |                    |                            |
    | gasleak_y            | integer            |                            |
    |                      |                    |                            |
    | gasleak_z            | integer            |                            |
    +----------------------+--------------------+----------------------------+


ItemDropEvent
-------------

.. _item_drop_event_message_properties:
.. table:: Properties for `ItemDropEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    +----------------------+--------------------+----------------------------+
    | itemName             | string             | itemName                   |
    |                      |                    |                            |
    | itemname             |                    |                            |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of floats    | location                   |
    |                      |                    |                            |
    | item_x               | float              |                            |
    |                      |                    |                            |
    | item_y               | float              |                            |
    |                      |                    |                            |
    | item_z               | float              |                            |
    +----------------------+--------------------+----------------------------+


ItemEquippedEvent
-----------------

.. _item_equipped_event_message_properties:
.. table:: Properties for `ItemEquippedEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    +----------------------+--------------------+----------------------------+
    | itemName             | string             | itemName                   |
    |                      |                    |                            |
    | equippeditemname     |                    |                            |
    +----------------------+--------------------+----------------------------+


ItemPickupEvent
---------------

.. _item_picup_event_message_properties:
.. table:: Properties for `ItemPickupEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    +----------------------+--------------------+----------------------------+
    | itemName             | string             | itemName                   |
    |                      |                    |                            |
    | itemname             |                    |                            |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of floats    | location                   |
    |                      |                    |                            |
    | item_x               | float              |                            |
    |                      |                    |                            |
    | item_y               | float              |                            |
    |                      |                    |                            |
    | item_z               | float              |                            |
    +----------------------+--------------------+----------------------------+


LeverEvent
----------

.. _lever_event_message_properties:
.. table:: Properties for `LeverEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    +----------------------+--------------------+----------------------------+
    | position             | tuple of integers  | position                   |
    |                      |                    |                            |
    | location             |                    |                            |
    |                      |                    |                            |
    | lever_x              | integer            |                            |
    |                      |                    |                            |
    | lever_y              | integer            |                            |
    |                      |                    |                            |
    | lever_z              | integer            |                            |
    +----------------------+--------------------+----------------------------+
    | powered              | boolean            | powered                    |
    +----------------------+--------------------+----------------------------+


LocationEvent
-------------

.. _location_event_message_properties:
.. table:: Properties for `LocationEvent` class

    +----------------------------------+--------------------+----------------------------------+
    | Property                         | Expected Datatype  | Accepted Keyword Arguments       |
    +==================================+====================+==================================+
    | participant_id                   | string             | participant_id                   |
    +----------------------------------+--------------------+----------------------------------+
    | playername                       | string             | playername                       |
    +----------------------------------+--------------------+----------------------------------+
    | callsign                         | string             | callsign (optional)              |
    +----------------------------------+--------------------+----------------------------------+
    | corresponding_observation_number | integer            | corresponding_observation_number |
    +----------------------------------+--------------------+----------------------------------+
    | locations                        | list               | locations (optional)             |
    +----------------------------------+--------------------+----------------------------------+
    | connections                      | list               | connections (optional)           |
    +----------------------------------+--------------------+----------------------------------+
    | exited_locations                 | list               | exited_locations (optional)      |
    +----------------------------------+--------------------+----------------------------------+
    | exited_connections               | list               | exited_connections (optional)    |
    +----------------------------------+--------------------+----------------------------------+


MarkerDestroyedEvent
--------------------

.. _marker_destroyed_event_message_properties:
.. table:: Properties for `MarkerDestroyedEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | type                 | string             | marker_type                |
    |                      |                    |                            |
    | marker_type          |                    |                            |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of integers  | location                   |
    |                      |                    |                            |
    | marker_x             | integer            |                            |
    |                      |                    |                            |
    | marker_y             | integer            |                            |
    |                      |                    |                            |
    | marker_z             | integer            |                            |
    +----------------------+--------------------+----------------------------+


MarkerPlacedEvent
-----------------

.. _marker_placed_event_message_properties:
.. table:: Properties for `MarkerPlacedEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    |                      |                    |                            |
    | name                 |                    | name                       |
    +----------------------+--------------------+----------------------------+
    | type                 | string             | marker_type                |
    |                      |                    |                            |
    | marker_type          |                    |                            |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of integers  | location                   |
    |                      |                    |                            |
    | marker_x             | integer            |                            |
    |                      |                    |                            |
    | marker_y             | integer            |                            |
    |                      |                    |                            |
    | marker_z             | integer            |                            |
    +----------------------+--------------------+----------------------------+

MarkerRemovedEvent
------------------

.. _marker_removed_event_message_properties:
.. table:: Properties for `MarkerRemovedEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    |                      |                    |                            |
    | name                 |                    | name                       |
    +----------------------+--------------------+----------------------------+
    | type                 | string             | marker_type                |
    |                      |                    |                            |
    | marker_type          |                    |                            |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of integers  | location                   |
    |                      |                    |                            |
    | marker_x             | integer            |                            |
    |                      |                    |                            |
    | marker_y             | integer            |                            |
    |                      |                    |                            |
    | marker_z             | integer            |                            |
    +----------------------+--------------------+----------------------------+


MissionStateEvent
-----------------

.. _mission_state_event_message_properties:
.. table:: Properties for `MissionStateEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | misison              | string             | mission                    |
    +----------------------+--------------------+----------------------------+
    | state                | enum: MissionState | state                      |
    |                      |                    |                            |
    | mission_state        |                    |                            |
    +----------------------+--------------------+----------------------------+

PauseEvent
----------

.. _pause_event_message_properties:
.. table:: Properties for `PauseEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | paused               | boolean            | paused                     |
    +----------------------+--------------------+----------------------------+

PlayerJumpedEvent
-----------------

.. _player_jumped_event_message_properties:
.. table:: Properties for `PlayerJumpedEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of floats    | location                   |
    |                      |                    |                            |
    | item_x               | float              |                            |
    |                      |                    |                            |
    | item_y               | float              |                            |
    |                      |                    |                            |
    | item_z               | float              |                            |
    +----------------------+--------------------+----------------------------+

PlayerSprintingEvent
-------------------

.. _player_sprinting_message_properties:
.. table:: Properties for `PlayerSprintingEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    +----------------------+--------------------+----------------------------+
    | sprinting            | boolean            | sprinting                  |
    +----------------------+--------------------+----------------------------+

PlayerState
-----------

.. _player_state_message_properties:
.. table:: Properties for `PlayerState` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername, name           |
    |                      |                    |                            |
    | name                 |                    |                            |
    +----------------------+--------------------+----------------------------+
    | id                   | string             | entity_id                  |
    |                      |                    |                            |
    | entity_id            |                    |                            |
    +----------------------+--------------------+----------------------------+
    | entity_type          | string             | entity_type                |
    +----------------------+--------------------+----------------------------+
    | observation_number   | integer            | observation_number         |
    +----------------------+--------------------+----------------------------+
    | timestamp            | string             | timestamp                  |
    +----------------------+--------------------+----------------------------+
    | world_time           | integer            | world_time                 |
    +----------------------+--------------------+----------------------------+
    | total_time           | integer            | total_time                 |
    +----------------------+--------------------+----------------------------+
    | position             | tuple of floats    | position                   |
    |                      |                    |                            |
    | x                    | float              |                            |
    |                      |                    |                            |
    | y                    | float              |                            |
    |                      |                    |                            |
    | z                    | float              |                            |
    +----------------------+--------------------+----------------------------+
    | orientation          | tuple of floats    | orientation                |
    |                      |                    |                            |
    | pitch                | float              |                            |
    |                      |                    |                            |
    | yaw                  | float              |                            |
    +----------------------+--------------------+----------------------------+
    | velocity             | tuple of floats    | velocity                   |
    |                      |                    |                            |
    | motion_x             | float              |                            |
    |                      |                    |                            |
    | motion_y             | float              |                            |
    |                      |                    |                            |
    | motion_z             | float              |                            |
    +----------------------+--------------------+----------------------------+
    | life                 | float              | life                       |
    +----------------------+--------------------+----------------------------+

PlayerSwingingEvent
-------------------

.. _player_sprinted_message_properties:
.. table:: Properties for `PlayerSwingingEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    +----------------------+--------------------+----------------------------+
    | swinging             | boolean            | swinging                   |
    +----------------------+--------------------+----------------------------+

RoleSelectedEvent
-----------------

.. _role_selected_message_properties:
.. table:: Properties for `RoleSelectedEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    +----------------------+--------------------+----------------------------+
    | new_role             | string             | new_role                   |
    |                      |                    |                            |
    | newRole              |                    |                            |
    +----------------------+--------------------+----------------------------+
    | prev_role            | string             | prev_role                  |
    |                      |                    |                            |
    | previousRole         |                    |                            |
    +----------------------+--------------------+----------------------------+


RubbleDestroyedEvent
--------------------

.. _rubble_destroyed_message_properties:
.. table:: Properties for `RubbleDestroyedEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | name, playername           |
    |                      |                    |                            |
    | name                 |                    |                            |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of integers  | location                   |
    |                      |                    |                            |
    | rubble_x             |                    |                            |
    |                      |                    |                            |
    | rubble_y             |                    |                            |
    |                      |                    |                            |
    | rubble_z             |                    |                            |
    +----------------------+--------------------+----------------------------+


RubblePlacedEvent
-----------------

.. _rubble_placed_message_properties:
.. table:: Properties for `RubblePlacedEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | from_location        | tuple of integers  | from_location              |
    |                      |                    |                            |
    | from_x               | integer            |                            |
    |                      |                    |                            |
    | from_y               | integer            |                            |
    |                      |                    |                            |
    | from_z               | integer            |                            |
    +----------------------+--------------------+----------------------------+
    | to_location          | tuple of integers  | to_location                |
    |                      |                    |                            |
    | to_x                 | integer            |                            |
    |                      |                    |                            |
    | to_y                 | integer            |                            |
    |                      |                    |                            |
    | to_z                 | integer            |                            |
    +----------------------+--------------------+----------------------------+


ScoreboardEvent
---------------

.. _scoreboard_event_message_properties:
.. table:: Properties for `ScoreboardEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | scoreboard           | dictionary         | scoreboard (optional)      |
    +----------------------+--------------------+----------------------------+

StaticMapInitialized
--------------------

.. _static_map_initialized_message_properties:
.. table:: Properties for `StaticMapInitialized` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | semantic_map_name    | string             | semantic_map_name          |
    +----------------------+--------------------+----------------------------+
    | semantic_map         | dictionary         | semantic_map               |
    +----------------------+--------------------+----------------------------+


ThreatSignList
--------------

.. _threat_sign_list_message_properties:
.. table:: Properties for `ThreatSignList` class

    +-------------------------+--------------------+----------------------------+
    | Property                | Expected Datatype  | Accepted Keyword Arguments |
    +=========================+====================+============================+
    | mission                 | string             | mission                    |
    +-------------------------+--------------------+----------------------------+
    | threat_signs            | string             | threat_sign_list           |
    |                         |                    |                            |
    | mission_threatsign_list |                    |                            |
    +-------------------------+--------------------+----------------------------+


ThreatSign
~~~~~~~~~~

.. _threat_sign_message_properties:
.. table:: Properties for `ThreatSign` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | location             | tuple of integers  | location                   |
    |                      |                    |                            |
    | x                    | integer            |                            |
    |                      |                    |                            |
    | y                    | integer            |                            |
    |                      |                    |                            |
    | z                    | integer            |                            |
    +----------------------+--------------------+----------------------------+
    | block_type           | string             | block_type                 |
    +----------------------+--------------------+----------------------------+
    | room_name            | string             | room_name                  |
    +----------------------+--------------------+----------------------------+
    | feature_type         | string             | feature_type (optional)    |
    +----------------------+--------------------+----------------------------+


ToolDepletedEvent
-----------------

.. _tool_depleted_event_message_properties:
.. table:: Properties for `ToolDepletedEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    +----------------------+--------------------+----------------------------+
    | tool_type            | string             | tool_type                  |
    +----------------------+--------------------+----------------------------+


ToolUsedEvent
-------------

.. _tool_used_event_message_properties:
.. table:: Properties for `ToolUsedEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    +----------------------+--------------------+----------------------------+
    | tool_type            | string             | tool_type                  |
    +----------------------+--------------------+----------------------------+
    | durability           | integer            | durability                 |
    +----------------------+--------------------+----------------------------+
    | count                | integer            | count                      |
    +----------------------+--------------------+----------------------------+
    | block_location       | tuple of integers  | block_location             |
    |                      |                    |                            |
    | target_block_x       | integer            |                            |
    |                      |                    |                            |
    | target_block_y       | integer            |                            |
    |                      |                    |                            |
    | target_block_z       | integer            |                            |
    +----------------------+--------------------+----------------------------+
    | block_type           | string             | block_type                 |
    |                      |                    |                            |
    | target_block_type    |                    |                            |
    +----------------------+--------------------+----------------------------+


TriageCount
-----------

.. _triage_count_message_properties:
.. table:: Properties for `TriageCount` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | player_name          | string             | player_name                |
    +----------------------+--------------------+----------------------------+
    | triage_counts        | dictionary         | triage_counts              |
    +----------------------+--------------------+----------------------------+


TriageEvent
-----------

.. _triage_event_message_properties:
.. table:: Properties for `TriageEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | player_name          | string             | player_name                |
    |                      |                    |                            |
    | playername           |                    |                            |
    +----------------------+--------------------+----------------------------+
    | victim_location      | tuple of integers  | victim_location            |
    |                      |                    |                            |
    | victim_x             | integer            |                            |
    |                      |                    |                            |
    | victim_y             | integer            |                            |
    |                      |                    |                            |
    | victim_z             | integer            |                            |
    +----------------------+--------------------+----------------------------+
    | color                | string             | color                      |
    |                      |                    |                            |
    | type                 |                    |                            |
    +----------------------+--------------------+----------------------------+
    | victim_id            | integer            |                            |
    +----------------------+--------------------+----------------------------+


TriageState
~~~~~~~~~~~

`TriageState` is an enumeration of possible triage states:

* IN_PROGRESS
* UNSUCCESSFUL
* SUCCESSFUL


Trial
-----

.. _trial_message_properties:
.. table:: Properties for `Trial` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | name                 | string             | name                       |
    +----------------------+--------------------+----------------------------+
    | date                 | string             | date                       |
    +----------------------+--------------------+----------------------------+
    | experimenter         | string             | experimenter               |
    +----------------------+--------------------+----------------------------+
    | subjects             | list of strings    | subjects                   |
    +----------------------+--------------------+----------------------------+
    | trial_number         | string             | trial_number               |
    +----------------------+--------------------+----------------------------+
    | group_number         | string             | group_number               |
    +----------------------+--------------------+----------------------------+
    | study_number         | string             | study_number               |
    +----------------------+--------------------+----------------------------+
    | condition            | string             | condition                  |
    +----------------------+--------------------+----------------------------+
    | notes                | list of strings    | notes                      |
    +----------------------+--------------------+----------------------------+
    | testbed_version      | string             | testbed_version            |
    +----------------------+--------------------+----------------------------+
    | experiment_name      | string             | experiment_name            |
    +----------------------+--------------------+----------------------------+
    | experiment_date      | string             | experiment_date            |
    +----------------------+--------------------+----------------------------+
    | experiment_author    | string             | experiment_author          |
    +----------------------+--------------------+----------------------------+
    | experiment_mission   | string             | experiment_mission         |
    +----------------------+--------------------+----------------------------+
    | map_name             | string             | map_name                   |
    +----------------------+--------------------+----------------------------+
    | map_block_filename   | string             | map_block_filename         |
    +----------------------+--------------------+----------------------------+
    | client_info          | list of ClientInfo | client_info                |
    +----------------------+--------------------+----------------------------+


ClientInfo
~~~~~~~~~~

.. _client_info_properties:
.. table:: Properties for `ClientInfo` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    +----------------------+--------------------+----------------------------+
    | callsign             | string             | callsign                   |
    +----------------------+--------------------+----------------------------+
    | participantid        | string             | participantid              |
    +----------------------+--------------------+----------------------------+
    | staticmapversion     | string             | staticmapversion           |
    +----------------------+--------------------+----------------------------+
    | markerblocklegend    | string             | markerblocklegend          |
    +----------------------+--------------------+----------------------------+
    | uniqueid             | string             | uniqueid                   |
    +----------------------+--------------------+----------------------------+                
    

VictimList
----------

.. _victim_list_message_properties:
.. table:: Properties for `VictimList` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | mission              | string             | mission                    |
    +----------------------+--------------------+----------------------------+
    | victims              | list of Victim     | victims (optional)         |
    |                      |                    |                            |
    | mission_victim_list  |                    |                            |
    +----------------------+--------------------+----------------------------+

Victim
~~~~~~

.. _victim_properties:
.. table:: Properties for `Victim` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | block_type           | string             | block_type                 |
    +----------------------+--------------------+----------------------------+
    | room_name            | string             | room_name                  |
    +----------------------+--------------------+----------------------------+
    | unique_id            | integer            | unique_id                  |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of integers  | location                   |
    |                      |                    |                            |
    | x                    | integer            |                            |
    |                      |                    |                            |
    | y                    | integer            |                            |
    |                      |                    |                            |
    | z                    | integer            |                            |
    +----------------------+--------------------+----------------------------+


VictimNoLongerSafe
------------------

.. _victim_no_longer_safe_message_properties:
.. table:: Properties for `VictimNoLongerSafe` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | type                 |                    | type                       |
    |                      |                    |                            |
    | color                |                    | color                      |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of integers  | location                   |
    |                      |                    |                            |
    | victim_x             | integer            |                            |
    |                      |                    |                            |
    | victim_y             | integer            |                            |
    |                      |                    |                            |
    | victim_z             | integer            |                            |
    +----------------------+--------------------+----------------------------+


VictimPickedUp
--------------

.. _victim_picked_up_message_properties:
.. table:: Properties for `VictimPickedUpVictimNoLongerSafe` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    |                      |                    |                            |
    | name                 |                    |                            |
    +----------------------+--------------------+----------------------------+
    | victim_id            |                    | victim_id                  |
    +----------------------+--------------------+----------------------------+
    | type                 |                    | type                       |
    |                      |                    |                            |
    | color                |                    | color                      |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of integers  | location                   |
    |                      |                    |                            |
    | victim_x             | integer            |                            |
    |                      |                    |                            |
    | victim_y             | integer            |                            |
    |                      |                    |                            |
    | victim_z             | integer            |                            |
    +----------------------+--------------------+----------------------------+

VictimPlaced
------------

.. _victim_placed_message_properties:
.. table:: Properties for `VictimPlaced` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | playername           | string             | playername                 |
    |                      |                    |                            |
    | name                 |                    |                            |
    +----------------------+--------------------+----------------------------+
    | victim_id            |                    | victim_id                  |
    +----------------------+--------------------+----------------------------+
    | type                 |                    | type                       |
    |                      |                    |                            |
    | color                |                    | color                      |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of integers  | location                   |
    |                      |                    |                            |
    | victim_x             | integer            |                            |
    |                      |                    |                            |
    | victim_y             | integer            |                            |
    |                      |                    |                            |
    | victim_z             | integer            |                            |
    +----------------------+--------------------+----------------------------+


VictimsExpired
--------------

.. _victims_expired_message_properties:
.. table:: Properties for `VictimsExpired` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | message              | string             | message                    |
    |                      |                    |                            |
    | expired_message      |                    |                            |
    +----------------------+--------------------+----------------------------+


VictimsRescued
--------------

.. _victims_rescued_message_properties:
.. table:: Properties for `VictimsRescued` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | message              | string             | message                    |
    |                      |                    |                            |
    | rescued_message      |                    |                            |
    +----------------------+--------------------+----------------------------+

WoofEvent
---------

.. _woof_event_message_properties:
.. table:: Properties for `WoofEvent` class

    +----------------------+--------------------+----------------------------+
    | Property             | Expected Datatype  | Accepted Keyword Arguments |
    +======================+====================+============================+
    | sourceEntity         | string             | sourceEntity               |
    |                      |                    |                            |
    | source_entity        |                    |                            |
    +----------------------+--------------------+----------------------------+
    | message              | string             | message                    |
    +----------------------+--------------------+----------------------------+
    | location             | tuple of floats    | location                   |
    |                      |                    |                            |
    | woof_x               | float              |                            |
    |                      |                    |                            |
    | woof_y               | float              |                            |
    |                      |                    |                            |
    | woof_z               | float              |                            |
    +----------------------+--------------------+----------------------------+