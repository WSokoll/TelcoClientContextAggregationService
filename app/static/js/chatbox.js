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
		writeMessage(textarea.value)
		setTimeout(autoReply, 1000)
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

function scrollBottom() {
	chatboxMessageWrapper.scrollTo(0, chatboxMessageWrapper.scrollHeight)
}

function isValid(value) {
	let text = value.replace(/\n/g, '')
	text = text.replace(/\s/g, '')

	return text.length > 0
}

// BUTTONS



var devices = ["Cisco Catalyst 9600", "Netgear Nighthawk M5 MR5200", "Cisco ISR4331", "Cisco Catalyst 2960"];





function createDeviceButtons() {
            var buttonContainer = document.getElementById("button-container");

            for (var i = 0; i < devices.length; i++) {
                var deviceButton = document.createElement("button");
                deviceButton.innerHTML = devices[i];
                deviceButton.className = "device-button";
                deviceButton.addEventListener("click", function() {
                    var device = this.innerHTML;
                    buttonContainer.innerHTML = ""; // Clear the button container
                    writeMessage("Reported device: " + device);
                    chatboxForm.classList.toggle('show');
                });

                buttonContainer.appendChild(deviceButton);
            }
        }

function fetchTechnicalData(loggedUser) {
  const url = `http://localhost:5000/api/users/${loggedUser}`;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      	const technicalData = data.technicalData;
      	console.log(technicalData);
      	// Further processing of the technicalData can be done here
		Object.keys(technicalData).forEach((key, index) => {
        // Check if the index is even (to ensure we have pairs)
        if (index % 2 === 0) {
          const pair = [technicalData[key], technicalData[Object.keys(technicalData)[index + 1]]];
          console.log(pair)
          devices.push(pair[0] + " " + pair[1]);
          console.log(devices)
        }
      });
    })
    .catch(error => {
      console.error('Error:', error);
    });
}


fetchTechnicalData(logged_user);
createDeviceButtons();

console.log(devices)
console.log(logged_user)