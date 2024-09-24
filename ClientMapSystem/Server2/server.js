// ASIST
const mqtt = require('./mqtt_manager');

const express = require('express');

const app = express();

const bodyParser = require("body-parser");

const port = 3080;

const cors = require('cors');

var corsOptions = {
  origin: 'http://localhost:4200',
  optionsSuccessStatus: 200 // some legacy browsers (IE11, various SmartTVs) choke on 204
}

const socketIO = require('socket.io');

// read in config

const config = require('./ClientMapConfig.json');

console.log(config);
console.log(config['showGlobalPositions'])


// username : socket
const users = new Map();

const players = [];

app.use(bodyParser.json());

app.use(express.static(process.cwd()+"/frontend/"));

app.use(cors());

// ROUTING

// this '/' maybe what's causing that weird redirect
app.get('', (req,res) => {
  res.sendFile(process.cwd()+"/frontend/index.html")
});

app.get('/map', (req,res) => {
  res.redirect('/ClientMap/')
});

app.get('/login', (req,res) => {
  res.redirect('/ClientMap/')
});

app.get('/state', function(req, res){
  res.send(mqtt.getState());
 });

app.get('/advisor', (req, res) => {
  res.redirect('/ClientMap/')
})

// END ROUTING

// Initiate server object
server = app.listen(port, () => {
    
    console.log(`Server listening on the port::${port}`);     

});

options = {
  transport:['websocket'],
  allowUpgrades:true
}

console.log('Attempting to start mqtt connection ...')

const client = mqtt.mqttInit(users);

const map = process.env.map

// Initiate Websocket service
const io = socketIO(server, options);

io.on('connection', (socket) => {

  // this one socket is associated with one client ... so you have to pass the socket to the mqttparse thingy
    
  console.log('websocket user connected : ' + socket.client.id);
  
  socket.emit('hello','Connected to the ClientMapBackend');  

  // mqtt publish message to advisor
  client.emit('advisor', 'message');
  // send config to the client
  socket.emit('config',config);

  socket.on('authenticate', (payload) => {

    console.log( payload );

    const name = payload['name']

    const settings = config;

    if(name !== undefined && name !== null ){

      if( ( name.length>0 ) && (payload['password']==='admin') ) {
        
        if (!users.get(name)){
          players.push(name);
        }

        console.log('Authentication successful for : ' + name);
        
        users.set( name, socket );

        mqtt.sendName(name);

        mqtt.linkSocketMap(users);
  
        // add user to mqtt filtering process
  
        socket.emit('authenticationResponse', {response:true, token:'aUniqueToken', map:map, name: name, config: settings })       
  
      }
      else {

        console.log('Authentication failure for : ' + name);
  
        socket.emit('authenticationResponse', {response:false})
  
      }

    }
    else {

      console.log("Player Name was undefined or null. Please resubmit this conneciton attempt.");

    }      
    });    

    // HANDLES INTERVENTION COMING FROM THE HUMAN ADVISOR AND ROUTES THEM TO CLIENTS
    socket.on('intervention', (payload) => {

      var d = new Date().toISOString();

      // we want to update this message with agent info and trial info and stuff

      client.emit('message', 'agent/intervention/advisor/map', 
      '{ \
        "header": { \
          "timestamp": "' + d + '",\
          "message_type": "agent",\
          "version": "0.1"\
        }, \
        "msg": {  \
            "experiment_id":"00000000-0000-0000-0000-000000000000", \
            "trial_id": "00000000-0000-0000-0000-000000000000", \
            "timestamp": "' + d + '", \
          "replay_id": "00000000-0000-0000-0000-000000000000", \
          "replay_root_id": "00000000-0000-0000-0000-000000000000", \
          "source": "Agent_1.0_ADAPT",\
          "sub_type": "Intervention:Text",\
          "version": "0.1"\
        },\
        "data": {\
            "id": "00000000-0000-0000-0000-000000000000", \
            "created":"' + d + '", \
            "start": "' + payload["start"] + '", \
            "end": "' + payload["end"] + '", \
            "content": "' + payload["text"] + '", \
            "receiver": "' + payload["receiver"] + '", \
            "type": "Intervention:Text", \
            "renderer": ["Minecraft_Chat"], \
            "explanation": "{<agent custom json object>}" \
          }\
        }'
      );
/*
    players.forEach(player => {
      if (player.toLowerCase() !== 'adapt_advisor') {
        const message = [];
        message.push(payload['text']);
        message.push(payload['start']);
        message.push(payload['end']);
        message.push(payload['receiver'])

        let playerSocket = users.get(player);
        if (playerSocket) {
          playerSocket.emit('textIntervention_' + player, message);
        }
      }
    })
    */
  });     
});















