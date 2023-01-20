# General-Discord-Bot
A discord bot with general, administrative and moderation commands. This also includes customized help command that uses a embed and the ability to blacklist words from the server. 

Purpose <br/>
The General Discord Bot was made in mind to provide utility to administrive and moderation members of a Discord server. The some of the commands are features found within Discord however, the commands shorten the process of having to manually execute Discord features. Other commands were designed outside of what the Discord GUI application is able to provide to general users.

Highlighted features <br/>
- Recording member information within a JSON file that the server uses for commands.<br/>
  - Keeps track of the number of times a user has been warned.<br/>
  - Keeps track of the number times a user used a blacklisted word.<br/>
- The ability for members to gain points that are used to buy roles within the server.<br/>
  - Roles can be recorded within a JSON file with their purchase price.<br/>
  - Users are able to view what roles are purchasable with their price from an embed. <br/>
- Adding words to a blacklist that are forbidden within the server.<br/>
- Detects messages with blacklisted words.<br/> 
  - Deletes messages that contain the blacklisted words.<br/> 
  - Warns members of their message that contains forbidden words.<br/>
- Ban or unban multiple members within a single command.<br/>
  - Users are sent a message from the bot with a reasoning on their ban.<br/>
- Warn, mute and unmute members within the channel.<br/>
  - Users are notified when they are warned with a reason.
- Create roles, categories, channels with the ability to delete them.<br/>
- Advertise a messsage within a channel every thrity minutes.<br/>
  - The advertisement message can be modified.<br/>
- A modified help function that can provide further description on commands.<br/>
  - The help command can specifically show the format of commands with examples on how to use the command.<br/>
- Send a GIF as a reaction to other members.<br/>
- Checks if users have the correct permissions to execute commands.<br/>

How to use:<br/>
First, you must login to your Discord account from this link and create an application by using the Discord Developer Portal.<br/>
https://discord.com/developers/applications<br/>
<br/>
Once the application is created, there is an option on the left hand sidebar to create an bot. Create a bot with your chosen name for it. Within the Discord application, there is an option on the left hand side bar to make a server. Click the button like within the image and create a server with your chosen settings.<br/><br/>
The Discord Developer Portal has an option on the lefthand side that create an OAuth2 URL. Click OAuth2 and click the dropdown menu option URL Generator in order to make a link to connect the bot to the server. This is done by clicking bot in scope and administrator afterwards.<br/>
There are two environmental variables that will need to be set on your computer or IDE: <br/>
- DISCORD_GUILD - The ID of your guild.<br/>
- DISCORD_TOKEN - The ID of your bot.<br/>

Once these are set, you use the command in a terminal: python3 -m bot <br/>
If this is conducted within an IDE, just execute the bot.py file.


