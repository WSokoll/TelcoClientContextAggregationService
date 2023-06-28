// MESSAGE INPUT
const textarea = document.querySelector('.chatbox-message-input')
const chatboxForm = document.querySelector('.chatbox-message-form')

textarea.addEventListener('input', function () {
	let line = textarea.value.split('\n').length

	if(textarea.rows < 6 || line < 6) {
		textarea.rows = line
	}

	if(textarea.rows > 1) {
		chatboxForm.style.alignItems = 'flex-end'
	} else {
		chatboxForm.style.alignItems = 'center'
	}
})



// TOGGLE CHATBOX
const chatboxToggle = document.querySelector('.chatbox-toggle')
const chatboxMessage = document.querySelector('.chatbox-message-wrapper')

chatboxToggle.addEventListener('click', function () {
	chatboxMessage.classList.toggle('show')
})



// CHATBOX MESSAGE
const chatboxMessageWrapper = document.querySelector('.chatbox-message-content')
const chatboxNoMessage = document.querySelector('.chatbox-message-no-message')

chatboxForm.addEventListener('submit', function (e) {
	e.preventDefault()

	if(isValid(textarea.value)) {
		const messageToSend = textarea.value
		writeMessage(messageToSend)
		handleSendMessage(messageToSend, "IN_PROGRESS")
		// setTimeout(autoReply, 1000)
	}
})



function addZero(num) {
	return num < 10 ? '0'+num : num
}

function writeMessage(messagetext) {
	const today = new Date()
	let message = `
		<div class="chatbox-message-item sent">
			<span class="chatbox-message-item-text">
				${messagetext.trim().replace(/\n/g, '<br>\n')}
			</span>
			<span class="chatbox-message-item-time">${addZero(today.getHours())}:${addZero(today.getMinutes())}</span>
		</div>
	`
	chatboxMessageWrapper.insertAdjacentHTML('beforeend', message)
	chatboxForm.style.alignItems = 'center'
	textarea.rows = 1
	textarea.focus()
	textarea.value = ''
	chatboxNoMessage.style.display = 'none'
	scrollBottom()
}

function autoReply() {
	const today = new Date()
	let message = `
		<div class="chatbox-message-item received">
			<span class="chatbox-message-item-text">
				Thank you for testing :)
			</span>
			<span class="chatbox-message-item-time">${addZero(today.getHours())}:${addZero(today.getMinutes())}</span>
		</div>
	`
	chatboxMessageWrapper.insertAdjacentHTML('beforeend', message)
	scrollBottom()
}

function readMessage(receivedText) {
	const today = new Date()
	let message = `
		<div class="chatbox-message-item received">
			<span class="chatbox-message-item-text">
				${receivedText}
			</span>
			<span class="chatbox-message-item-time">${addZero(today.getHours())}:${addZero(today.getMinutes())}</span>
		</div>
	`
	chatboxMessageWrapper.insertAdjacentHTML('beforeend', message)
	scrollBottom()
}


function scrollBottom() {
	chatboxMessageWrapper.scrollTo(0, chatboxMessageWrapper.scrollHeight)
}

function isValid(value) {
	let text = value.replace(/\n/g, '')
	text = text.replace(/\s/g, '')

	return text.length > 0
}

// BUTTONS



// var devices = ["Cisco Catalyst 9600", "Netgear Nighthawk M5 MR5200", "Cisco ISR4331", "Cisco Catalyst 2960"];

var devices = [];
let userName;
let userAge;



function createDeviceButtons(devices_list) {
	var buttonContainer = document.getElementById("button-container");

	for (var i = 0; i < devices_list.length; i++) {
		var deviceButton = document.createElement("button");
		deviceButton.innerHTML = devices_list[i];
		deviceButton.className = "device-button";
		deviceButton.addEventListener("click", function() {
			chosenDevice = this.innerHTML;
			buttonContainer.innerHTML = ""; // Clear the button container
			writeMessage("Reported device: " + chosenDevice);
			chatboxForm.classList.toggle('show');
			handleClick(chosenDevice);
		});

		buttonContainer.appendChild(deviceButton);
	}
}

function fetchTechnicalData(loggedUser) {
  const url = `http://localhost:5000/api/users/${loggedUser}`;

  return fetch(url)
    .then(response => response.json())
    .then(data => {
      const technicalData = data.technicalData;
      console.log(technicalData);
      userAge = data.personalData.age;
      userName = data.personalData.name;
      const devicesList = [];

      // Iterate over the keys of the technicalData object
      Object.keys(technicalData).forEach((key, index) => {
        // Check if the index is even (to ensure we have pairs)
        if (index % 2 === 0) {
          const pair = [technicalData[key], technicalData[Object.keys(technicalData)[index + 1]]];
          devicesList.push(pair[0] + " " + pair[1]);
        }
      });

      console.log(devicesList);
      return devicesList;
    })
    .catch(error => {
      console.error('Error:', error);
      return [];
    });
}


fetchTechnicalData(logged_user)
.then(updatedDevices => {
	devices = updatedDevices;
    console.log(devices);
    createDeviceButtons(devices); // Call createDeviceButtons after fetchTechnicalData
  });


console.log(devices)
console.log(logged_user)

let socket; // Declare a variable to hold the socket object
let chat_id;
let chosenDevice;

// Function to start Socket.IO client connection
function startSocketIOClient(url) {
	socket = io(url);

	// Event listener for 'connect' event
	socket.on('connect', () => {
	  	console.log('Connected to the server');
	});

	// Event listener for custom events
	socket.on('response', (data) => {
		const jsonResponse = JSON.parse(data);
		console.log("Received response (RAW):\n" + data);
		const service = jsonResponse.service;
		const metadata = jsonResponse.metadata;

	  switch (service) {
		case "IN_PROGRESS":
			readMessage(jsonResponse.message)
			console.log("Service is in progress");
			break;
		case "UNKNOWN_ERROR":
			console.log("Unknown error occurred");
			break;
		case "NEEDS_HELP":
			console.log("Help is needed");
			break;
		default:
			console.log("Unknown service");
	  }
		//readMessage(jsonResponse.message);
	  	// console.log('Received customEvent:', data);
	});

	socket.on('startChat', (data) => {
		//readMessage(data);
	  	console.log('Received customEvent:', data);
	});

	// Event listener for built-in 'disconnect' event
	socket.on('disconnect', () => {
	  	console.log('Disconnected from the server');
	});
}

// Function to emit a message
function emitMessage(eventType, message) {
	if (socket) {
	  	socket.emit(eventType, message);
	} else {
	  	console.log('Socket is not connected');
	}
}

// Function to initialize socket and send starting message
function initializeSocketAndSendMessage(url, startingMessage) {
	if (!chat_id){
		chat_id = Math.floor(Math.random() * (10000 - 1) + 1);
	}
	startingMessage.service = "START";
	startSocketIOClient(url);
	sendSocketMessage('request', startingMessage,"IN_PROGRESS")
	//emitMessage('startChat', startingMessage);
}


function sendSocketMessage(event, message, serviceType) {
	// const chatId = chat_id;
	const service = serviceType;// ["IN_PROGRESS", "COMPLETED", "UNKNOWN_ERROR", "START"];
	const messageText = message;
	const conversationStarter = {
	  client_id: logged_user,
	  name: userName,
	  age: userAge,
	  behavior: "nice",
	  device_model: chosenDevice
	};
	const metadata = "TBD";


	const jsonObject = {
	  chat_id: chat_id,
	  service: service,
	  message: messageText,
	  "conversation starter": conversationStarter,
	  metadata: metadata
	};
	console.log(jsonObject)
	emitMessage('request', JSON.stringify(jsonObject));
}

let chatServerUrl = 'http://10.144.59.161:7000' //'https://10.144.76.174:7000' ////'http://10.144.239.226:7000' //'http://localhost:3000'

// Example usage
function handleClick(message) {
	//startSocketIOClient(chatServerUrl);
	//sendSocketMessage("request", message, "START")
	initializeSocketAndSendMessage(chatServerUrl, message);
}

function handleSendMessage(message, serviceType) {
	sendSocketMessage("request", message, serviceType);
}