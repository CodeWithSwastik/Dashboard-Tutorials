from quart import Quart, render_template, request, session
from quart_discord import DiscordOAuth2Session

app = Quart(__name__)
app.config["SECRET_KEY"] = "test123"
app.config["DISCORD_CLIENT_ID"] = 1234567890    # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "SHHHH"                # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = ""                 # URL to your callback endpoint.

discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
	return await render_template("index.html",discord_url="login url here")

@app.route("/login")
async def login():
	"""The function that logs the user in.

	It will redirect them to your Discord OAuth2 Flow,
	and they will then be redirected back to your callback
	endpoint, or REDIRECT_URI.
	"""	
	return await discord.create_session()

@app.route("/callback")
async def callback():
	"""Callback.

	This will handle the authentication of
	the user, and create the session and cookies.
	"""
	await discord.callback()
	user = await discord.fetch_user()
	return f"Hello, {user.name}#{user.discriminator}! <img src='{user.avatar_url}'>"

@app.route('/logout')
async def logout():
	"""Logs out the user by REVOKING!!! their token."""
	discord.revoke()

if __name__ == "__main__":
	app.run(debug=True)
