// ASIST
const mqtt = require('mqtt');

const config = require('./ClientMapConfig.json');

isMqttConnected = false;

globalSocket = null;

let globalSocketMap = new Map();

let callSignMap = new Map();

let players = [];

let client = null;

let state = {
    trialStarted: false,
    missionStarted: false,
    microphoneEnabled: false,
    clientInfo: []
};

module.exports = {

    mqttInit:function( ){
        
        if( !isMqttConnected){

            const connectionString = process.env.mqtt_host
                        
            // doesn't store it's own clientId for some reason

            // PROD
            client  = mqtt.connect("mqtt://"+connectionString+":1883", { clientId:"ClientMapBackEnd" } );

            // DEV
            //const client  = mqtt.connect("mqtt://localhost:1883", { clientId:"ClientMapBackEnd" } );
            
            client.clientId = "ClientMapBackEnd";

            client.on("message", (topic,message)=>{
                //console.log("Topic : " + topic);
                //console.log("Message : " + message);
                parseTopic(topic,message);

                //console.log("object.qos : " + object.qos);
                //console.log("object.payload : " + object.payload);
            });
            
            client.on("connect",function(){	
                console.log("mqtt connected : " + client.connected);
                console.log("mqtt clientId : " + client.clientId);
                //console.log( client.constructor.name);
                isMqttConnected=true;
            });

            // client.on("disconnect",function(){	
            //     console.log("mqtt connected : " + client.connected);        
            //     isMqttConnected=false;
            // });

            client.on("close",function(){	
                console.log("mqtt connected : " + client.connected);        
                isMqttConnected=false;
            });
        
            client.subscribe('observations/state');
            client.subscribe('observations/events/mission/perturbation');
            client.subscribe('observations/events/player/role_selected');
            client.subscribe('observations/events/player/marker_placed');
            client.subscribe('observations/events/player/marker_removed');
            client.subscribe('agent/intervention/+/map');
            client.subscribe('trial');
            client.subscribe('observations/events/mission')
            client.subscribe('ground_truth/mission/threatsign_list')
            
            
        }
        else {

            console.log('Page refreshed, mqtt client still connected.');

        }

        return client;
    },

    linkSocketMap:function(socketMap){

        console.log('Passing Socket Map after each User Authentication')

        globalSocketMap = socketMap;        

        for (let key of globalSocketMap.keys()) {
            console.log(key)
        }
    },

    sendName:function(name){
        var d = new Date().toISOString();

        client.publish("status/clientmapsystem/playername", 
        '{ \
            "header": { \
                "timestamp": "' + d + '", \
                "message_type": "status", \
                "version": "1.1" \
            }, \
            "msg": {  \
                "experiment_id":"00000000-0000-0000-0000-000000000000", \
                "trial_id": "00000000-0000-0000-0000-000000000000", \
                "timestamp": "' + d + '", \
                "source": "simulator", \
                "sub_type": "Status:PlayerName", \
                "version": "0.5" \
            }, \
            "data":{ \
                "playername":"' + name + '" \
            } \
        }'
        );
    },
    
    getState:function() {
        return state;
    }
};


const parseTopic = function( topic, message){
    
    splitString = String(topic).split('/')
    
    if (topic === 'observations/state'){ 
        
        processPosition(message);
        
    }
    else if (topic === 'trial'){         
        
        processTrial(message);
        
    }
    else if (topic === 'observations/events/mission') {

        processMission(message);
        
    }
    else if( splitString[0]=='agent' && splitString[1]=='intervention' && splitString[3]=='map' ){
        
        processMapIntervention(message);
    }
    else if (topic === 'observations/events/player/role_selected') {
        
        processRoleSelected(message);

    }
    else if (topic === 'observations/events/player/marker_placed') {
        
        processMarkerPlaced(message);

    }

    else if (topic === 'observations/events/player/marker_removed') {

        console.log('received marker removed in Server2')
        
        processMarkerRemoved(message);

    }

    else if (topic === 'observations/events/mission/perturbation') {
        
        console.log( "Perturbation received from ASISTMOD")
        processPerturbation(message);

    }

    else if (topic === 'ground_truth/mission/threatsign_list'){

        console.log( "Received ThreatList for Engineer ... processing." )

        processThreatList(message)
    }
}

const processThreatList=function(message){
    
    try{

        const jsonMessage = JSON.parse(message);

        const list = jsonMessage['data']['mission_threatsign_list'];

        console.log('Converting threatlist to simple array')
    
        const xzlist = [];
        list.forEach( item =>{
            xzlist.push( [item['x'],item['z']]);
        })
    
        globalSocketMap.forEach((value, key) =>{
    
            // type is 'removed'
            value.emit('threatlist', xzlist);
    
        }) 

    }
   catch(e){
       console.log("Something went wrong processing the threat list.")
   }
}

const processMarkerPlaced=function(message){

    const jsonMessage = JSON.parse(message);

    const x = Math.floor(jsonMessage['data']['marker_x']);
    const y = Math.floor(jsonMessage['data']['marker_y']);
    const z = Math.floor(jsonMessage['data']['marker_z']);
    
    const playername = jsonMessage['data']['playername']
    const type = jsonMessage['data']['type']

    globalSocketMap.forEach((value, key) =>{

        value.emit('markerUpdate_global', [x, y, z, playername, type]);

    })     

}

const processMarkerRemoved=function(message){

    const jsonMessage = JSON.parse(message);

    const x = Math.floor(jsonMessage['data']['marker_x']);
    const y = Math.floor(jsonMessage['data']['marker_y']);
    const z = Math.floor(jsonMessage['data']['marker_z']);
    
    const playername = jsonMessage['data']['playername']
    const type = jsonMessage['data']['type']

    globalSocketMap.forEach((value, key) =>{

        // type is 'removed'
        value.emit('markerUpdate_global', [x, y, z, playername, 'removed']);

    })
}


const processPosition=function( message ){

    // process observation
    try {
        const jsonMessage = JSON.parse(message);

        const x = Math.floor(jsonMessage['data']['x']);
        const y = Math.floor(jsonMessage['data']['y']);
        const z = Math.floor(jsonMessage['data']['z']);
        
        const playername = jsonMessage['data']['playername']

        const mission_timer = jsonMessage['data']['mission_timer']

        // console.log(playername + ' : Position : ' + [x,y,z] );

        // SEND UPDATED POSITIONS TO ALL CONNECTED CLIENTS
        if(config['showGlobalPositions']){

            globalSocketMap.forEach((value, key) =>{

                value.emit('positionUpdate_global', [x, y, z, mission_timer, playername]);

            })     

        }
        else {

            socket = globalSocketMap.get(playername);       
        
            if (socket !== undefined && socket !== null ){

                socket.emit('positionUpdate_'+playername,[x,y,z,mission_timer, playername]);

            }

            socket = globalSocketMap.get("asist_advisor");

            if (socket !== undefined && socket !== null) {

                // console.log("Emitting positon for " + playername + " to advisor page : " + [x,y,z]);

                socket.emit('positionUpdate_global', [x, y, z, mission_timer, playername]);

            }
        }        
            
    } catch (error) {
        console.log(error)
    }
}

const processMapIntervention=function(message){

    try {

        console.log('We received an agent map intervention');

        const jsonMessage = JSON.parse(message);

        const intervention = jsonMessage['data'];

        const msg = jsonMessage['msg'];

        const callsign = intervention['receiver'];

        const name = callSignMap.get(callsign);

        if (msg['sub_type'] === 'Intervention:Text') {
            
            callSignMap.forEach((value, key) => {
                
                console.log("Sending to :" + key + " - " + value);

                const socket = globalSocketMap.get(value)
    
                if (socket !== undefined) {

                    const startTime = intervention['start'];
                    const endTime = intervention['end'];

                    console.log('We received a text clientmap intervention');
                    const content = intervention['content'];
                    socket.emit('textIntervention_' + value, [content, startTime, endTime, name]);
                }
            });
        }

        else if (msg['sub_type'] === 'Intervention:HeatMap') {
            
            console.log('We received a heatmap clientmap intervention');

            const socket = globalSocketMap.get(name);
            
            if (socket !== undefined) {

                const startTime = intervention['start'];
                const endTime = intervention['end'];

                const topleft = intervention['top_left'];
                const bottomright = intervention['bottom_right'];
                socket.emit('heatmapIntervention_' + name, [startTime, endTime, topleft, bottomright])
            }
        }
        
    } catch (error) {

        console.log(error)

    }

    // KEEP THIS IN CASE WE GO BACK TO INTERVENTION ARRAYS///////////////////////

    // for(let i=0; i<interventions.length; i++){
    //     if(interventions[i]['renderer'] === 'Client_Map'){
    //         console.log('We received a client map intervention');
    //         const name = interventions[i]['receiver'];
    //         socket = globalSocketMap.get(name);
    //         if (socket !== undefined ){
    //             const content = interventions[i]['content'];
    //             socket.emit('mapIntervention_'+name,content);
    //         }    
    //     }
    // }
    ///////////////////////////////////////////////////////////////
    
}

const processPerturbation = function (message) {
    try {
        const data = JSON.parse(message)["data"];

        console.log(data);

        globalSocketMap.forEach( (value, key) =>{           
            
            if(data["type"] === "blackout") {
                console.log("Emitting perturbation for : " + key)
                value.emit('commBlackout', data["mission_state"])
            }
            
        })
    }
    catch (error) {
        console.log(error)
    }
}

const processRoleSelected = function (message) {
    
    try {

        const data = JSON.parse(message)["data"];

        const socket = globalSocketMap.get(data['playername']);
    
        const content = data['new_role']
        if (socket !== undefined) {
            socket.emit('roleChange', content)
        }
        
    } catch (error) {
        console.log(error)
    }
   
}


// Ingests the MissionState message
const publishRoleTextMessages = function (message){

    const d = new Date().toISOString();
    let topic = 'ground_truth/mission/role_text'
    const missionName = message['data']['mission']
    
    let medicText;
    let engText;
    let tranText;

    let medicTextSummary;
    let engTextSummary;
    let tranTextSummary;

    if(missionName.includes('Saturn_A',0)){
        medicText = config['Saturn_A_Text']['Medic']       
        engText = config['Saturn_A_Text']['Engineer']        
        tranText = config['Saturn_A_Text']['Transporter']

        medicTextSummary = config['Saturn_A_Text_Summary']['Medic']
        engTextSummary = config['Saturn_A_Text_Summary']['Engineer']
        tranTextSummary = config['Saturn_A_Text_Summary']['Transporter']
    }
    else if(missionName.includes('Saturn_B',0)){
        medicText = config['Saturn_B_Text']['Medic']
        engText = config['Saturn_B_Text']['Engineer']
        tranText = config['Saturn_B_Text']['Transporter']

        medicTextSummary = config['Saturn_B_Text_Summary']['Medic']
        engTextSummary = config['Saturn_B_Text_Summary']['Engineer']
        tranTextSummary = config['Saturn_B_Text_Summary']['Transporter']
    }
    else if(missionName.includes('Saturn_C',0)){
        medicText = config['Saturn_C_Text']['Medic']
        engText = config['Saturn_C_Text']['Engineer']
        tranText = config['Saturn_C_Text']['Transporter']

        medicTextSummary = config['Saturn_C_Text_Summary']['Medic']
        engTextSummary = config['Saturn_C_Text_Summary']['Engineer']
        tranTextSummary = config['Saturn_C_Text_Summary']['Transporter']
    }
    else if(missionName.includes('Saturn_D',0)){
        medicText = config['Saturn_D_Text']['Medic']
        engText = config['Saturn_D_Text']['Engineer']
        tranText = config['Saturn_D_Text']['Transporter']

        medicTextSummary = config['Saturn_D_Text_Summary']['Medic']
        engTextSummary = config['Saturn_D_Text_Summary']['Engineer']
        tranTextSummary = config['Saturn_D_Text_Summary']['Transporter']
    }
    else if(missionName.includes('Training')){
        medicText = config['Training_Text']['Medic']
        engText = config['Training_Text']['Engineer']
        tranText = config['Training_Text']['Transporter']

        medicTextSummary = config['Training_Text_Summary']['Medic']
        engTextSummary = config['Training_Text_Summary']['Engineer']
        tranTextSummary = config['Training_Text_Summary']['Transporter']
    }

    const header = {
        "timestamp": d,
        "message_type": "groundtruth",
        "version": "2.0"
    }
    const msg = {
        "experiment_id":message['msg']['experiment_id'],
        "trial_id":message['msg']['trial_id'],
        "timestamp": d,
        "source":"simulator",
        "sub_type": "Mission:RoleText",
        "version":"2.1"
    }
    let data = {
        "missionName":missionName,
        "medical_specialist_text":medicText,
        "engineering_specialist_text":engText,
        "transport_specialist_text":tranText
    }

    const jsonObject = {
        "header":header,
        "msg":msg,
        "data":data
    }    
    
    client.publish( topic, JSON.stringify(jsonObject) );

    jsonObject.header.message_type = "event";
    jsonObject.msg.sub_type = "Event:PuzzleTextSummary";
    jsonObject.msg.version = "2.0";
    jsonObject.data =    {
        "missionName":missionName,
        "medical_specialist_puzzle_summary":medicTextSummary,
        "engineering_specialist_puzzle_summary":engTextSummary,
        "transport_specialist_puzzle_summary":tranTextSummary
    }

    topic = "observations/events/mission/puzzle_summary"
    client.publish( topic, JSON.stringify(jsonObject) );
    
    
}

const processTrial=function( message ){

    

    // process observation
    try {
        
        const jsonMessage = JSON.parse(message);
        
        const sub_type = jsonMessage['msg']['sub_type']

        

        if (sub_type == "start") { 
            
            
        
            console.log("Received trial start message!");
            
            const client_info = jsonMessage['data']['client_info']

            if (client_info != null) {

                // CALLSIGN ROUTING

                const advisor_socket = globalSocketMap.get('asist_advisor');

                // SEND THE CLIENT INFO TO THE ADVISOR
                if (advisor_socket) {
                    message = { name:'asist_advisor', info: client_info }
                    advisor_socket.emit('assignCallsign', message);
                }
                // SEND THE CLIENT INFO TO EACH PLAYER
                for (let i = 0; i < client_info.length; i++) {

                    const playername = client_info[i].playername;
                    const callsign = client_info[i].callsign;

                    if(playername && callsign){
                        console.log([playername, callsign])
                        callSignMap.set(callsign,playername);
                    }
                    // console.log("ClientInfo: playername = " + playername);
                    socket = globalSocketMap.get(playername);
                    //send all the information to each player so it can be displayed on the interaction panel
                    if (socket !== undefined && callsign !== null) {                    
                        message = { name: playername, info: client_info }                    
                        socket.emit('assignCallsign', message);
                    }
                }
                // END CALLSIGN ROUTING

                // STATE
                state.clientInfo = client_info;
                state.trialStarted = true;
                state.microphoneEnabled = true;

                console.log( "Setting State.trialStarted in mqtt manager : " + state.trialStarted )

                for(let i=0; i<client_info.length; i++){
                    const playername = client_info[i].playername;
                    players.push(playername)                
                    socket = globalSocketMap.get(playername);
                    if (socket !== undefined){
                        socket.emit('trial', jsonMessage);
                    }
                    // why are we sending these 2 below one by one when the above does it?
                    if (socket !== undefined && client_info[i].unique_id != null){
                        console.log("ClientInfo: Updating " + playername + " to unique ID: " + client_info[i].unique_id);
                        socket.emit('unique_idUpdate_'+playername, client_info[i].unique_id);
                    }
                    if (socket !== undefined && client_info[i].participant_id != null){
                        console.log("ClientInfo: Updating " + playername + " to participant ID: " + client_info[i].participant_id);
                        socket.emit('participant_idUpdate_'+playername, client_info[i].participant_id);
                    }
                }
            }
        }
        else if (sub_type == "end" || sub_type == "stop") {
            
            console.log("Received trial end message!");
            const client_info = jsonMessage['data']['client_info']
            if (client_info != null) {
                
                // STATE
                state.trialStarted = false;
                state.missionStarted = false;
                state.microphoneEnabled = false;

                for(let i=0; i<client_info.length; i++){
                    
                    const playername = client_info[i].playername;
                    // console.log("ClientInfo: playername = " + playername);
                    socket = globalSocketMap.get(playername);

                    if (socket !== undefined){
                        socket.emit('trial', jsonMessage);
                    }
                }
            }
        }
    }
    catch(error) {
        console.log(error)        
    }    
}

const processMission = function(message) {
    
    const jsonMessage = JSON.parse(message);
    const missionState = jsonMessage['data']['mission_state'];

    console.log("Received MissionState Message.")   
        
    try{
        if (missionState === 'Start') {
            publishRoleTextMessages(jsonMessage)
        }
        globalSocketMap.forEach( (value, key) =>{           
        
            console.log(" Sending Mission State message to " + key )                
                
            if (missionState === 'Start') {

                state.missionStarted = true;

                console.log('Received mission start message!');

                value.emit('missionState','Start');                

            } else if (missionState === 'Stop') {

                state.missionStarted = false;

                console.log('Received mission stop message!');

                value.emit('missionState','Stop');
            } else {
                console.log(`Received invalid mission_state value of ${missionState}`)
            }               
        });
    }
    catch(sally){
        console.log(sally)
    }        
        
}

