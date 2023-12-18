# CST 435 

This project is to design an instructor-like conversational agent for use in multi-party academic interactions.


## Authors

Made by Kyungchan Im, John Haviland, Andrew Millam, Gabriel Aracena, Nathan Dilla, and Alexander Peltier.

### Setting up on your local machine

1. Clone the repository
2. Add deadsimplechat chat embed to your website
Create Account:
deadsimplechat.com
Add Public Ke, Chat Room ID, to index.html (Developer Tab) (ChatRoom Tab)
const sdk = new DSChatSDK("CHATROOMID", "chat-frame", "PUBLIC_KEY");
Replace chat-frame with your chat-frame (ChatRoom Tab > Edit > Embed Info > (Embed Code))
<iframe id="chat-frame" src="https://deadsimplechat.com/Qs1uFHWMQ" width="100%" height="600px"></iframe>

3. Import Github Repo to Netify 
Create Account:
https://app.netlify.com/
Create Team:
Connect to Github or upload folder of repo:
Change site name to desired name:
