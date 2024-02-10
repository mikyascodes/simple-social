const profileImageContainers = document.querySelectorAll('.profile-image-container');
// Add a click event listener to each profile image container
profileImageContainers.forEach(profileImageContainer => {
  profileImageContainer.addEventListener('click', function() {
    // Get the URL from the data-location attribute
    const url = this.dataset.location;

    // Redirect the user to the URL
    window.location.href = url;
  });
});

//END OF THE VIEWPROFILE DIV 

                            const closeButton = document.querySelector('.close-friends-now');
                            // Add an event listener to the close button element for the `click` event
                            closeButton.addEventListener('click', () => {
                            // Redirect to the previous page
                            window.history.back();
                            });
//END OF CLOSE BUTTON on friend_now page


//WEBSOCKET CLIENT
let url = `ws://${window.location.host}/ws/socket-server/`

const chatSocket = new WebSocket(url)

chatSocket.onmessage = function(e){
    let data = JSON.parse(e.data)
    console.log('Data:', data)

    if(data.type === 'chat'){
        let messages = document.getElementById('messages')

        messages.insertAdjacentHTML('beforeend', `<div>
                                <p>${data.message}</p>
                            </div>`)
    }
}

let form = document.getElementById('form')
form.addEventListener('submit', (e)=> {
    e.preventDefault()
    let message = e.target.message.value 
    chatSocket.send(JSON.stringify({
        'message':message
    }))
    form.reset()
})