# -*- coding: utf-8 -*-
"""
.. module:: agent_prediction
   :platform: Linux, Windows, OSX
   :synopsis: Message class encapsulating Agent Prediction messages.

.. moduleauthor:: Dana Hughes <danahugh@andrew.cmu.edu>

Definition of a class encapsulating Agent Prediction messages.  Agent
predictions can be either 'state' or 'action' predictions.
"""

import json
import enum
import datetime
import uuid

from ..message_exceptions import (
    MalformedMessageCreationException, 
    MissingMessageArgumentException, 
    ImmutableAttributeException
)
from ..base_message import BaseMessage

class AgentPredictionGroupProperty:
    """
    A simple class encapsulating group properties for predictions.  Properties
    in group apply to all predictions in an AgentPredictionMessage, unless 
    overridden by an individual prediction

    Attributes
    ----------
    start : string
        The time the prediction is effective
    duration : float
        The length of time, in seconds, that the prediction will remain valid.
    explanation : dict (optional, default={})
        Agent custom dictionary describing why the prediction was generated.
    """

    def __init__(self, start, duration, explanation={}):

        self._start = start
        self._duration = duration
        self._explanation = explanation


    @property
    def start(self):
        """
        Get the time the prediction is effective  

        Attempting to set `start` raises an `ImmutableAttributeException`.
        """

        return self._start

    @start.setter
    def start(self, start_time):
        raise ImmutableAttributeException(str(self), "start")


    @property
    def duration(self):
        """
        Get the length of time the prediction remains valid.  

        Attempting to set `duration` raises an `ImmutableAttributeException`.
        """

        return self._duration

    @duration.setter
    def duration(self, duration):
        raise ImmutableAttributeException(str(self), "duration")


    @property
    def explanation(self):
        """
        Get the explanation of why the prediction was generated.  

        Attempting to set `explanation` raises an `ImmutableAttributeException`.
        """

        return self._explanation

    @explanation.setter
    def explanation(self, explanation):
        raise ImmutableAttributeException(str(self), "explanation")


    def toDict(self):
        """
        Generates a dictionary representation of the group properties.

        Returns
        -------
        dict
            A dictionary representation of the group properties.
        """

        jsonDict = { "start_elapsed_time": self.start,
                     "duration": self.duration,
                     "explanation": self.explanation }

        return jsonDict


class AgentPredictionBaseMessage(BaseMessage):
    """
    A class containing common attributes of both state and action prediction
    message types.


    Attributes
    ----------
    group : AgentPredictionGroupProperty
        Set of properties common to all predictions in the list of predictions.
        'Child' properties in the list of predictions override the common group
        properties, if present.
    created : str
        The time the prediction was created (based on trial time).  If not 
        provided, uses the system time when the object was created.
    """


    def __init__(self, **kwargs):

        BaseMessage.__init__(self, **kwargs)

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["group"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        self._group = kwargs["group"]
        self._created = kwargs.get("created", datetime.datetime.now().isoformat()+'Z')


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'AgentPredictionBaseMessage')
        """

        return self.__class__.__name__


    @property
    def group(self):
        """
        Get the group properties.

        Attempting to set `group` raises an `ImmutableAttributeException`.
        """

        return self._group

    @group.setter
    def group(self, group):
        raise ImmutableAttributeException(str(self), "group")


    @property
    def created(self):
        """
        Get the creation time of the prediction.  

        Attempting to set `created` raises an `ImmutableAttributeException`.
        """

        return self._created

    @created.setter
    def created(self, created):
        raise ImmutableAttributeException(str(self), "created")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the AgentPredictionBaseMessage.
        """

        jsonDict = BaseMessage.toDict(self, False)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["group"] = self.group.toDict()
        jsonDict["data"]["created_elapsed_time"] = self.created

        return jsonDict        


    def toJson(self):
        """
        Generates a JSON representation of the message.  Message information is
        contained in a JSON object under the key "data".  Additional named
        headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            AgentPredictionBaseMessage message.
        """

        return json.dumps(self.toDict())




class AgentActionPrediction:
    """
    A class encapsulating the contents of a single action prediction.

    Attributes
    ----------
    unique_id : string, optional
        A unique identifier for the prediction, using UUID format.  Will be 
        generated if one is not provided.
    start : string, default=None
        The time the prediction becomes valid.  If `None`, then the prediction
        is assumed to be effective immediately.
    duration : string, default=None
        The duration in seconds that the prediction remains valid.  If `None`,
        then the prediction is valid for the trial run
    action : string
        The type of action being predicted
    using : string
        The tool that is used to perform the action
    subject : string
        The name of the entity taking action
    object : string
        The entity / block being acted upon
    probability_type : string, default="float"
        Data type of the probability ("string" or "float")
    probability : string or float
        Probability of the action occuring
    confidence_type : string, default="float"
        Data type of the confidence ("string" or "float")
    confidence : float or string
        Confidence of the prediction
    explanation : dict, default={}
        Explanation of the prediction
    """

    def __init__(self, **kwargs):

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["action", "using", "object", "subject", "probability",
                         "confidence", "predicted_property"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        # Create a UUID if one wasn't given
        self._unique_id = kwargs.get("unique_id", str(uuid.uuid4()))
        self._start = kwargs.get("start", None)
        self._duration = kwargs.get("duration", None)
        self._predicted_property = kwargs["predicted_property"]        
        self._action = kwargs["action"]
        self._using = kwargs["using"]
        self._subject = kwargs["subject"]
        self._object = kwargs["object"]
        self._probability_type = kwargs.get("probability_type", "float")
        self._probability = kwargs["probability"]
        self._confidence_type = kwargs.get("confidence_type", "float")
        self._confidence = kwargs["confidence"]
        self._explanation = kwargs.get("explanation", {})



    def __str__(self):
        """
        String representation of the prediction.

        Returns
        -------
        string
            Class name of the prediction (i.e., 'AgentActionPrediction')
        """

        return self.__class__.__name__


    @property
    def unique_id(self):
        """
        Get the UUID of the prediciton.

        Attempting to set `unique_id` raises an `ImmutableAttributeException`.
        """

        return self._unique_id

    @unique_id.setter
    def unique_id(self, _id):
        raise ImmutableAttributeException(str(self), "unique_id")


    @property
    def start(self):
        """
        Get the time the prediction becomes valid.

        Attempting to set `start` raises an `ImmutableAttributeException`.
        """

        return self._start

    @start.setter
    def start(self, start_time):
        raise ImmutableAttributeException(str(self), "start")


    @property
    def duration(self):
        """
        Get the duration that the prediction is valid, in seconds.

        Attempting to set `duration` raises an `ImmutableAttributeException`.
        """

        return self._duration

    @duration.setter
    def duration(self, duration):
        raise ImmutableAttributeException(str(self), "duration")


    @property
    def action(self):
        """
        Get the predicted action.

        Attempting to set `action` raises an `ImmutableAttributeException`.
        """

        return self._action

    @action.setter
    def action(self, action):
        raise ImmutableAttributeException(str(self), "action")


    @property
    def using(self):
        """
        Get the tool used in the action.  

        Attempting to set `using` raises an `ImmutableAttributeException`.
        """

        return self._using

    @using.setter
    def using(self, tool):
        raise ImmutableAttributeException(str(self), "using")


    @property
    def subject(self):
        """
        Get the name of the entity performing the action.  

        Attempting to set `subject` raises an `ImmutableAttributeException`.
        """

        return self._subject

    @subject.setter
    def subject(self, entity_name):
        raise ImmutableAttributeException(str(self), "subject")


    @property
    def object(self):
        """
        Get the block / entity being acted upon.  

        Attempting to set `object` raises an `ImmutableAttributeException`.
        """

        return self._object

    @object.setter
    def object(self, object):
        raise ImmutableAttributeException(str(self), "object")


    @property
    def predicted_property(self):
        """
        Get the predicted property.  

        Attempting to set `predicted_property` raises an `ImmutableAttributeException`.
        """

        return self._predicted_property
    
    @predicted_property.setter
    def predicted(self, property):
        raise ImmutableAttributeException(str(self), "object")


    @property
    def probability_type(self):
        """
        Get the probability datatype (`string` or `float`).

        Attempting to set `probability_type` raises an `ImmutableAttributeException`.
        """

        return self._probability_type

    @probability_type.setter
    def probability_type(self, datatype):
        raise ImmutableAttributeException(str(self), "probability_type")


    @property
    def probability(self):
        """
        Get the probability that the action is performed.  

        Attempting to set `probability` raises an `ImmutableAttributeException`.
        """

        return self._probability

    @probability.setter
    def probability(self, probability):
        raise ImmutableAttributeException(str(self), "probability")


    @property
    def confidence_type(self):
        """
        Get the confidence datatype (`string` or `float`).  

        Attempting to set `confidence_type` raises an `ImmutableAttributeException`.
        """

        return self._confidence_type

    @confidence_type.setter
    def confidence_type(self, datatype):
        raise ImmutableAttributeException(str(self), "confidence_type")


    @property
    def confidence(self):
        """
        Get the confidence value of the prediction.  

        Attempting to set `confidence` raises an `ImmutableAttributeException`.
        """

        return self._confidence

    @confidence.setter
    def confidence(self, confidence):
        raise ImmutableAttributeException(str(self), "confidence")


    @property
    def explanation(self):
        """
        Get the explanations for the prediction.  

        Attempting to set `explanation` raises an `ImmutableAttributeException`.
        """

        return self._explanation

    @explanation.setter
    def explanation(self, explanation):
        raise ImmutableAttributeException(str(self), "explanation")
       


    def toDict(self):
        """
        Generates a dictionary representation of the prediction.

        Returns
        -------
        dict
            A dictionary representation of the action prediction.
        """

        jsonDict = { "unique_id": self.unique_id,
                     "start_elapsed_time": self.start,
                     "duration": self.duration,
                     "action": self.action,
                     "using": self.using,
                     "subject": self.subject,
                     "object": self.object,
                     "predicted_property": self.predicted_property,
                     "probability_type": self.probability_type,
                     "probability": self.probability,
                     "confidence_type": self.confidence_type,
                     "confidence": self.confidence,
                     "explanation": self.explanation
                   }

        return jsonDict        


class AgentStatePrediction:
    """
    A class encapsulating the contents of a single state prediction.

    Attributes
    ----------
    unique_id : string, optional
        A unique identifier for the prediction, using UUID format.  Will be 
        generated if one is not provided.
    start : string, default=None
        The time the prediction becomes valid.  If `None`, then the prediction
        is assumed to be effective immediately.
    duration : string, default=None
        The duration in seconds that the prediction remains valid.  If `None`,
        then the prediction is valid for the trial run
    subject : string
        The subject of the prediction (e.g., player, victim, team)
    subject_type : string
        The type of subject (individual or team) being predicted about
    predicted_property : string
        Name of the discrete property being predicted
    prediction : string
        Actual predicted value (e.g., score, player location, etc.)
    probability_type : string, default="float"
        Data type of the probability ("string" or "float")
    probability : string or float
        Value of the prediction as a string for float
    confidence_type : string, default="float"
        Data type of the confidence ("string" or "float")
    confidence : float or string
        Confidence of the prediction
    explanation : dict, default={}
        Explanation of the prediction
    """

    def __init__(self, **kwargs):

        # Check to see if the necessary arguments have been passed, raise an 
        # exception if one is missing
        for arg_name in ["subject", "subject_type", "predicted_property", "prediction", 
                         "probability", "confidence", "subject_type"]:
            if not arg_name in kwargs:
                raise MissingMessageArgumentException(str(self), 
                                                      arg_name) from None

        # Create a UUID if one wasn't given
        self._unique_id = kwargs.get("unique_id", str(uuid.uuid4()))
        self._start = kwargs.get("start", None)
        self._duration = kwargs.get("duration", None)
        self._subject_type = kwargs["subject_type"]
        self._subject = kwargs["subject"]
        self._predicted_property = kwargs["predicted_property"]
        self._prediction = kwargs["prediction"]
        self._probability_type = kwargs.get("probability_type", "float")
        self._probability = kwargs["probability"]
        self._confidence_type = kwargs.get("confidence_type", "float")
        self._confidence = kwargs["confidence"]
        self._explanation = kwargs.get("explanation", {})



    def __str__(self):
        """
        String representation of the prediction.

        Returns
        -------
        string
            Class name of the prediction (i.e., 'AgentStatePrediction')
        """

        return self.__class__.__name__


    @property
    def unique_id(self):
        """
        Get the UUID of the prediciton.

        Attempting to set `unique_id` raises an `ImmutableAttributeException`.
        """

        return self._unique_id

    @unique_id.setter
    def unique_id(self, _id):
        raise ImmutableAttributeException(str(self), "unique_id")


    @property
    def start(self):
        """
        Get the time the prediction becomes valid.

        Attempting to set `start` raises an `ImmutableAttributeException`.
        """

        return self._start

    @start.setter
    def start(self, start_time):
        raise ImmutableAttributeException(str(self), "start")


    @property
    def duration(self):
        """
        Get the duration that the prediction is valid, in seconds.

        Attempting to set `duration` raises an `ImmutableAttributeException`.
        """

        return self._duration

    @duration.setter
    def duration(self, duration):
        raise ImmutableAttributeException(str(self), "duration")


    @property
    def subject(self):
        """
        Get the name of the entity whose state is being predicted.

        Attempting to set `subject` raises an `ImmutableAttributeException`.
        """

        return self._subject

    @subject.setter
    def subject(self, entity_name):
        raise ImmutableAttributeException(str(self), "subject")


    @property
    def subject_type(self):
        """
        Get the type of the entity (individual or team) that predictions are 
        made about.  

        Attempting to set `subject_type` raises an `ImmutableAttributeException`.
        """

        return self._subject_type

    @subject_type.setter
    def subject_type(self, entity_type):
        raise ImmutableAttributeException(str(self), "subject_type")


    @property
    def predicted_property(self):
        """
        Get the predicted property.  

        Attempting to set `predicted_property` raises an `ImmutableAttributeException`.
        """

        return self._predicted_property

    @predicted_property.setter
    def predicted_property(self, property):
        raise ImmutableAttributeException(str(self), "predicted_property")


    @property
    def prediction(self):
        """
        Get the value of the prediction.  

        Attempting to set `prediction` raises an `ImmutableAttributeException`.
        """

        return self._prediction

    @prediction.setter
    def prediciton(self, prediction_value):
        raise ImmutableAttributeException(str(self), "prediction")


    @property
    def probability_type(self):
        """
        Get the probability datatype (`string` or `float`).

        Attempting to set `probability_type` raises an `ImmutableAttributeException`.
        """

        return self._probability_type

    @probability_type.setter
    def probability_type(self, datatype):
        raise ImmutableAttributeException(str(self), "probability_type")


    @property
    def probability(self):
        """
        Get the probability that the action is performed.  

        Attempting to set `probability` raises an `ImmutableAttributeException`.
        """

        return self._probability

    @probability.setter
    def probability(self, probability):
        raise ImmutableAttributeException(str(self), "probability")


    @property
    def confidence_type(self):
        """
        Get the confidence datatype (`string` or `float`).  

        Attempting to set `confidence_type` raises an `ImmutableAttributeException`.
        """

        return self._confidence_type

    @confidence_type.setter
    def confidence_type(self, datatype):
        raise ImmutableAttributeException(str(self), "confidence_type")


    @property
    def confidence(self):
        """
        Get the confidence value of the prediction.  

        Attempting to set `confidence` raises an `ImmutableAttributeException`.
        """

        return self._confidence

    @confidence.setter
    def confidence(self, confidence):
        raise ImmutableAttributeException(str(self), "confidence")


    @property
    def explanation(self):
        """
        Get the explanations for the prediction.  

        Attempting to set `explanation` raises an `ImmutableAttributeException`.
        """

        return self._explanation

    @explanation.setter
    def explanation(self, explanation):
        raise ImmutableAttributeException(str(self), "explanation")
       


    def toDict(self):
        """
        Generates a dictionary representation of the prediction.

        Returns
        -------
        dict
            A dictionary representation of the action prediction.
        """

        jsonDict = { "unique_id": self.unique_id,
                     "start_elapsed_time": self.start,
                     "duration": self.duration,
                     "subject": self.subject,
                     "subject_type": self.subject_type,
                     "predicted_property": self.predicted_property,
                     "prediction": self.prediction,
                     "probability_type": self.probability_type,
                     "probability": self.probability,
                     "confidence_type": self.confidence_type,
                     "confidence": self.confidence,
                     "explanation": self.explanation
                   }

        return jsonDict



class AgentActionPredictionMessage(AgentPredictionBaseMessage):
    """
    A class encapsulating agent action prediction messages.

    Note
    ----
    In addition to the list of attributes below, the message also includes the
    attributes inherited from `AgentPredictionBaseMessage`.


    Attributes
    ----------
    predictions : list of AgentActionPrediction, default=[]
        List of action predictions
    """


    def __init__(self, **kwargs):

        AgentPredictionBaseMessage.__init__(self, **kwargs)

        self._predictions = kwargs.get("predictions", [])

        # _finalized is used to track if predictions can be added
        self._finalized = False


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'AgentActionPredictionMessage')
        """

        return self.__class__.__name__


    def add(self, prediction):
        """
        Add a prediction to the list of predictions.

        Parameters
        ----------
        prediction : AgentActionPrediction
            Prediction to add to the list.
        """

        # Check if the prediction list is finalized. If so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), "predictions (from add)")

        self._predictions.append(prediction)


    def finalize(self):
        """
        Indicate that all predictions have been added to the message.
        """

        self._finalized = True


    @property
    def predictions(self):
        """
        Get the list of predictions.  

        Attempting to set `predictions` raises an `ImmutableAttributeException`.
        """

        return self._predictions

    @predictions.setter
    def predictions(self, predictions):
        raise ImmutableAttributeException(str(self), "predictions")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the AgentActionPredicitonMessage.
        """

        jsonDict = AgentPredictionBaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["predictions"] = [prediction.toDict() for prediction in self.predictions] 

        return jsonDict        


    def toJson(self):
        """
        Generates a JSON representation of the message.  Message information is
        contained in a JSON object under the key "data".  Additional named
        headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            AgentActionPredictionMessage message.
        """

        return json.dumps(self.toDict())



class AgentStatePredictionMessage(AgentPredictionBaseMessage):
    """
    A class encapsulating agent state prediction messages.

    Note
    ----
    In addition to the list of attributes below, the message also includes the
    attributes inherited from `AgentPredictionBaseMessage`.


    Attributes
    ----------
    predictions : list of AgentStatePrediction, default=[]
        List of state predictions
    """


    def __init__(self, **kwargs):

        AgentPredictionBaseMessage.__init__(self, **kwargs)

        self._predictions = kwargs.get("predictions", [])

        # _finalized is used to track if predictions can be added
        self._finalized = False


    def __str__(self):
        """
        String representation of the message.

        Returns
        -------
        string
            Class name of the message (i.e., 'AgentStatePredictionMessage')
        """

        return self.__class__.__name__


    def add(self, prediction):
        """
        Add a prediction to the list of predictions.

        Parameters
        ----------
        prediction : AgentStatePrediction
            Prediction to add to the list.
        """

        # Check if the prediction list is finalized. If so, raise an exception
        if self._finalized:
            raise ImmutableAttributeException(str(self), "predictions (from add)")

        self._predictions.append(prediction)


    def finalize(self):
        """
        Indicate that all predictions have been added to the message.
        """

        self._finalized = True


    @property
    def predictions(self):
        """
        Get the list of predictions.  

        Attempting to set `predictions` raises an `ImmutableAttributeException`.
        """

        return self._predictions

    @predictions.setter
    def predictions(self, predictions):
        raise ImmutableAttributeException(str(self), "predictions")


    def toDict(self):
        """
        Generates a dictionary representation of the message.  Message
        information is contained in a dictionary under the key "data".
        Additional named headers may also be present.

        Returns
        -------
        dict
            A dictionary representation of the AgentStatePredicitonMessage.
        """

        jsonDict = AgentPredictionBaseMessage.toDict(self)

        # Check to see if a "data" is in the dictionary, and add if not
        # Note that headers should have been added in jsonDict, as well as
        # common message data.
        if not "data" in jsonDict:
            jsonDict["data"] = {}

        # Add the message data
        jsonDict["data"]["predictions"] = [prediction.toDict() for prediction in self.predictions] 

        return jsonDict        


    def toJson(self):
        """
        Generates a JSON representation of the message.  Message information is
        contained in a JSON object under the key "data".  Additional named
        headers may also be present.

        Returns
        -------
        string
            A JSON string mapping header names to a JSON representation of the
            AgentStatePredictionMessage message.
        """

        return json.dumps(self.toDict())