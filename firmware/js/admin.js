function loadConfig() {
    fetch('/get_config')
        .then(response => response.json())
        .then(config => {
            document.getElementById('startupColor').value = config.startupColor;
            document.getElementById('apPassword').value = config.apPassword;
            document.getElementById('bootTime').value = config.bootTime;
            document.getElementById('version').value = config.version;
        })
        .catch(error => console.error('Error loading config:', error));
}

function saveConfig() {
    const config = {
        startupColor: document.getElementById('startupColor').value,
        apPassword: document.getElementById('apPassword').value,
        bootTime: document.getElementById('bootTime').value,
        version: document.getElementById('version').value,
    };

    fetch('/set_config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(config)
    })
    .then(response => response.json())
    .then(data => {
        alert('Configuration saved successfully!');
    })
    .catch(error => {
        console.error('Error saving config:', error);
        alert('Failed to save configuration.');
    });
}
