const Url = "http://127.0.0.1:5000"

async function getMessage() {
    const localUrl = `${Url}/messages/get`;
    let response = await fetch(localUrl);

    if (!response.ok) {
        const data = await response.json();

        if (data.error === "No messages found in the database.") {
            const renewUrl = `${Url}/messages/renew`;
            const renewResponse = await fetch(renewUrl, {
                method: "POST"
            });

            if (!renewResponse.ok) {
                console.log("Failed to renew messages.");
                return null;
            }

            return getMessage(); // Try fetching messages again after renewal
        }

        console.log(data.error || "Failed to fetch messages.");
        return null;
    }

    const data = await response.json();

    console.log(data.content);
    return data.content;
}

async function getMusic() {
    const localUrl = `${Url}/musics/get`;
    let response = await fetch(localUrl);

    if (!response.ok) {
        const data = await response.json();

        if (data.error === "No music found in the database.") {
            const renewUrl = `${Url}/musics/renew`;
            const renewResponse = await fetch(renewUrl, {
                method: "POST"
            });

            if (!renewResponse.ok) {
                console.log("Failed to renew musics.");
                return null;
            }

            return getMusic(); // Try fetching musics again after renewal
        }

        console.log(data.error || "Failed to fetch musics.");
        return null;
    }

    const data = await response.json();
    console.log(data.url);
    return data.url;
}

async function getPhoto() {
    const localUrl = `${Url}/photos/get_random`; 
    const response = await fetch(localUrl);
    const result = await response.json();
    return result.content;
}

async function showMessage() {
    const message = await getMessage();
    const music = await getMusic();

    const container = document.getElementById("input-container");
    if (!container) {
        console.log({ message, music });
        return;
    }

    container.innerHTML = `
        <div id="message-container">
            <div>
                <img src="http://127.0.0.1:5000/photos/get_random" alt="Random Photo" id="random-photo" style="max-width: 50%; height: auto;">
            </div>
        <p class="message">${message}</p>
        <br> <br>
        <p class="music">A musica de hoje vai ser: </p>
        <a href="${music}" id="music-link" target="_blanket">Essa aqui</a>
        </div>

        <div id="seen-container">
            <ul id="seen-list">
                <li><button class="seen" onclick="showSeenMessages()">Ver mensagens vistas anteriormente</button></li>
                <li><button class="seen" onclick="showSeenMusics()">Ver Músicas vistas anteriormente</button></li>
            </ul>
        </div>
        <br> <br> <br>
        <div>
            <button class="return" onclick="returnMain()">Retornar ao início</button>
        </div>        

    `;

}


async function showSeenMessages() {
    let localUrl = `${Url}/messages/get_seen`;
    let response = await fetch(localUrl);

    if (!response.ok) {
        let data = await response.json();
        if (data.error === "No seen messages found in the database.")
            return "No seen messages found in the database.";
    } else {
        let lista = await response.json();
        console.log(lista);
        for (const file of lista.messages) {
            console.log(file.content);
        }
        return lista;
    }
}

async function showSeenMusics() {
    let localUrl = `${Url}/musics/get_seen`;
    let response = await fetch(localUrl);

    if (!response.ok) {
        let data = await response.json();
        if (data.error === "No seen music found.") {
            return "No seen musics in the database.";
        }
    } else {
        
        let lista = await response.json();
        console.log(lista);
        for (const file of lista.musics) {
            console.log(file.url);
        }
        return lista;
    }
}


async function returnMain() {
    window.location.href = "http://127.0.0.1:5000"
}
