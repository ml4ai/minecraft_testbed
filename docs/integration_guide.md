# ASIST Testbed Integration and Extension Guide

## Introduction
The ASIST testbed provides a variety of mechanisms to extend the capabilities of the testbed to meet the
needs of the ASIST program.  These mechanisms break down into two main categories.
First is the ability to support additional data and the second is to support additional functions.  

This document provides some guidence on how to extend the ASIST testbed.  It is organized by first describing
several use case scenarios of the types of extensions that can created and then a more detailed description of
the extension mechanisms themselves.

## Extension Use Case Scenarios

1. Add a tool to the testbed
One way to add new capability to the testbed is to develop a new tool and integrate it into the testbed. 
The purpose of the tool could be to take raw data and generate some derived values, or to take some collection of 
data from the testbed and generate some results.  
The output values can then be shared with other components of the testbed  as well as captured and stored.
The testbed architecture is designed to support the inclusion of new containerized tools.
These tools can be depolyed with the testbed and can subscribe and publish data to the testbed message bus.

2. Define a message
Some testbed users may want to share new data with other components of the testbed.
This can be done by defining new messages.
The testbed architecture is designed to allow new messages to be defined and handled by the testbed. 
Messages that are published on the message bus can be verified and recorded by the data collection component of
the testbed (Elastic and Logstash).  Messages published on the message bus can be subscribed to by any of the other 
components on the message bus within the testbed system.

3. Enhancements to code or documentation
Some testbed users might have new ideas for testbed features and/or find issues with the testbed that they can fix.
This could be a simple as an additionl to the documentation to make it more clear or a utility function that could 
be useful to other message bus tool developers.  

## Extension Mechanisms

### Message Bus Tools
Message bus tools can be developed in just about any language and incorporated into the testbed at runtime.
The testbed disbribution contains at least one reference agent that gives an example of how an agent can be build.
Message bus tols are Docker containerized components that connect to the testbed via the MQTT message bus.
The testbed publishes control messages that message bus tools can use as indicators of when 
to start and stop.  The control messages also provide experiment/trial metadata.

### Message Formats
The testbed supports json format message for communication between components.  All messages must have a markdown
file that documents the fields of the message and a json schema file which is a machine readable schema of the message.
The message documents (.md) and schema (.json) files are stored in the testbed distribution in the MessageSpecs directory.  
The testbed includes a message validator which can be turned on and off and which can validate the messages on the message bus 
against the json schema for that message type and report errors to the control GUI.
New message formats should be discussed with the testbed working group before implemented and 
reviewed by the testbed working group before they can be proposed for incorporation into the testbed release.

### Code Contributions
Some enhancements to the testbed might involve base testbed components or more fundamental aspects of the testbed. 
This type of testbed enhancement must be carefully vetted for compatibilty with the testbed architecture and future direction.
To support this type of testbed enhancement, the testbed source repository will allow branching which can facilitate
the development of more complex enhancements to the testbed.  This type of code changes should be first discussed with
the Testbed Working Group and then proposed to the testbed development group.
The testbed development will make the final decision as to if, when and how to incorporate the code enhancement 
via a merge request in the source repository.