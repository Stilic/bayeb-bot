const { io } = require("socket.io-client");
const axios = require("axios").default;
const socket = io("https://devel.windows96.net:4096");

const prefix = "b!";
const session = {
    username: `BayebBot[${prefix}]`,
    user_id: null,
    onlineUsers: [],
};

socket.on("connect", () => {
    console.log("connected to the server");
});
socket.on("auth-complete", (userId) => {
    console.log("authentificated");
    session.user_id = userId;
});

socket.on("auth-error", function (errorObject) {
    throw Error(errorObject.reason);
});
socket.on("werror", function (reason) {
    console.log("server announcement: " + reason);
});

function sendMessage(text) {
    socket.emit("message", {
        type: "text",
        content: text,
    });
}

socket.on("message", (message) => {
    if (message.id != session.user_id) {
        if (message.content.startsWith(prefix)) {
            const cmd = message.content.split(" ")[0].slice(prefix.length);
            var options = [];
            if (message.content.length > prefix.length + cmd.length) {
                options = message.content.split(" ").slice(1);
            }
            if (cmd == "ping") {
                sendMessage("Pong!");
            } else if (cmd == "http") {
                axios.get(options[0]).then((rep) => {
                    sendMessage(rep.data);
                });
            } else if (cmd == "rename") {
                var username = "";
                for (const sec in options) {
                    username += options[sec];
                    if (sec != options.length) {
                        username += " ";
                    }
                }
                if (username.length > 16) {
                    sendMessage("This username is too long!");
                } else {
                    session.username = username;
                    socket.emit("change-user", username);
                }
            }
        }
    }
});

if (session.username.length > 16) {
    throw Error("The username is too long.");
} else {
    socket.emit("auth", { user: session.username });
}
