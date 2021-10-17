import asyncio
import socketio
import commands

sio = socketio.AsyncClient()

bot_prefix = "b/"
session = {
    "username": "BayebBot [b/]",
    "userId": None,
    "userObj": None,
    "onlineUsers": [],
}

if len(session["username"]) > 17:
    raise Exception("The username is too long!")


@sio.event
async def connect():
    print("Connected to server")
    print("Authentication in progress...")
    await sio.emit("auth", {"user": session["username"]})


@sio.on("auth-error")
async def authError(error):
    raise Exception("Authentification failed: " + error["reason"])


@sio.on("auth-complete")
async def authComplete(id):
    print("Authentication completed!")
    session["userId"] = id


# sync to server's users list
@sio.event
async def online(users):
    session["onlineUsers"] = users


@sio.on("user-join")
async def userJoin(user):
    if user["user"] == session["username"]:
        session["userObj"] = user
    else:
        session["onlineUsers"] += user


@sio.on("user-leave")
async def userLeave(user):
    if user in session["onlineUsers"]:
        session["onlineUsers"].remove(user)


@sio.on("message")
async def handleCmd(data):
    if str(data["content"]).startswith(bot_prefix):
        rendered = commands.handle(str(data["content"]).removeprefix(bot_prefix), data)
        if rendered != "":
            await sio.emit("message", rendered)


@sio.event
async def werror(reason):
    print(reason)


@sio.event
async def disconnect():
    print("Disconnected from server")


async def main():
    await sio.connect("https://devel.windows96.net:4096")
    await sio.wait()


if __name__ == "__main__":
    asyncio.run(main())
