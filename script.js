function sayHello() {
    // Chama a função Python que foi exposta ao JavaScript
    window.pywebview.api.say_hello().then(function(response) {
        document.getElementById('response').innerText = response;
    });
}
