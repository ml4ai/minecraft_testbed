# Measures
run **measures.py** with metadata file as input
````
> python measures.py -f [metadata file]
````
## Notes
- Time elapsed in milliseconds begins at Zero and in incremented over the duration of the trial

Required message sub_types:
- SemanticMap:Initialized
- Event:location
- Event:Scoreboard
- state
- Event:MissionState
- Event:ProximityBlockInteraction
- Event:RoleSelected
#### M2:
- Current N value 2 seconds
- observations/state message is published every ~102 ms due to this checking the player state(location) after n seconds has a margin of error of up to +20ms per second
- For a location (x, y, z) where positive x corresponds to East on the Client Map, y is the elevation (not needed) and negative z corresponds to the North of the Client Map.
- Angle is the calculation of ````atan2(-z, x)```` which returns the angle to the point relative to the positive x axis, z is flipped since -z is north
    - E = 0&deg; + 22.5&deg; , 360 - 22.5&deg; (includes end points)
    - NE = 45&deg; +/- 22.5&deg;    
    - N = 90&deg; +/- 22.5&deg; (includes end points)
    - NW = 135&deg; +/- 22.5&deg;
    - W = 180&deg; +/- 22.5&deg; (includes end points)
    - SW = 225&deg; +/- 22.5&deg;
    - S = 270&deg; +/- 22.5&deg; (includes end points)
    - SE = 315&deg; +/- 22.5&deg;
#### M3:
- Player map messages TBD
#### M5:
- Visitors are listed in order
- Staging area visits are ignored in the tally
## Example Output:

Output **ground_truth.json** is generated which contains the trial ground truth

````
{
    "M1": {
        "gt_final_score": 160
    },
    "M2": {
        "n_value": 2,
        "post_room_exit_locations": [
            {
                "time_elapsed_milliseconds": 744031,
                "player_name": "ShriTata",
                "room_name": "Buffet",
                "angle": 166.65,
                "direction": "W"
            },
            {
                "time_elapsed_milliseconds": 746900,
                "player_name": "ShriTata",
                "room_name": "The Limping Lamb Chophouse",
                "angle": 59.9,
                "direction": "NE"
            },
            {
                "time_elapsed_milliseconds": 759910,
                "player_name": "ASIST4",
                "room_name": "The Limping Lamb Chophouse",
                "angle": 20.85,
                "direction": "E"
            },
            {
                "time_elapsed_milliseconds": 761242,
                "player_name": "WoodenHorse9773",
                "room_name": "The Limping Lamb Chophouse",
                "angle": 24.7,
                "direction": "NE"
            },
            {
                "time_elapsed_milliseconds": 761346,
                "player_name": "ShriTata",
                "room_name": "Room 103",
                "angle": 207.66,
                "direction": "SW"
            },
        ]
    },
    "M3": [
        {
            "player_name": "N/A",
            "map_name": "N/A"
        }
    ],
    "M4": {
        "hvt_victims": [
            {
                "victim_location": {
                    "x": -2197,
                    "z": 39
                },
                "loiter_time": 6.0,
                "player_arrivals": {
                    "Bulbousonions13": 220096,
                    "Aptiminer1": 224096,
                    "Scouter_B": 226096
                }
            },
            {
                "victim_location": {
                    "x": -2095,
                    "z": 9
                },
                "loiter_time": 0.002,
                "player_arrivals": {
                    "Aptiminer1": 600097,
                    "Scouter_B": 600098,
                    "Bulbousonions13": 600099
                }
            },
            {
                "victim_location": {
                    "x": -2131,
                    "z": 41
                },
                "loiter_time": 20.001,
                "player_arrivals": {
                    "Scouter_B": 648096,
                    "Aptiminer1": 665096,
                    "Bulbousonions13": 668097
                }
            }
        ],
        "trial_loiter_stats": {
            "max": 20.001,
            "min": 0.002,
            "avg": 8.6677
        }
    },
   "M5": {
        "rooms_visited": {
            "r101": {
                "room_name": "Room 101",
                "Medical_Specialist": 1,
                "Search_Specialist": 0,
                "Hazardous_Material_Specialist": 2,
                "visitors": [
                    {
                        "player": {
                            "name": "intermonk",
                            "role": "Hazardous_Material_Specialist"
                        },
                        "time_elapsed_milliseconds": 474133
                    },
                    {
                        "player": {
                            "name": "ASIST4",
                            "role": "Hazardous_Material_Specialist"
                        },
                        "time_elapsed_milliseconds": 614757
                    },
                    {
                        "player": {
                            "name": "WoodenHorse9773",
                            "role": "Medical_Specialist"
                        },
                        "time_elapsed_milliseconds": 869024
                    }
                ]
            },
            "kit": {
                "room_name": "Kitchen",
                "Medical_Specialist": 0,
                "Search_Specialist": 0,
                "Hazardous_Material_Specialist": 1,
                "visitors": [
                    {
                        "player": {
                            "name": "intermonk",
                            "role": "Hazardous_Material_Specialist"
                        },
                        "time_elapsed_milliseconds": 851231
                    }
                ]
            }
        },
        "total_revisits": {
            "medical_revisits": 0,
            "search_revisits": 0,
            "hazard_revisits": 1,
            "total_revisits": 1
        }
    },
    "study_number": "2",
    "trial_number": "T000***",
    "experiment_name": "TM0000**"
}
