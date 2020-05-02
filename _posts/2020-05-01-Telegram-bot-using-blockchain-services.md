---
layout: post
title: Telegram bot using blockchain services
author: Ilan Olkies
category: javascript
tags: js javascript rif rsksmart rns telegram bot node
permalink: /post/:title
image: /img/telegram_bot_rns/front.png
---

Bots are third-party applications that run inside Telegram. Users can interact with bots by sending them
messages. RIF Name Service enables the identification of blockchain addresses by human-readable names, just
like DNS for websites, but in a decentralized manner. We are going to build a Telegram bot that resolves
addresses for requested domains.

First we need to create a new Telegram bot with the @BotFather<sup><a href="#ref-1">1</a></sup>. The
@BotFather will tell us the API key to use to control the bot using HTTPS requests to the Bot API. Then, in
response to messages, we will query RNS service to answer with the resolved addresses<sup><a href="#ref-2">2</a></sup>.

So the recipe is:

1. Create a bot and get the API key
2. Catch bot messages with a Node application
3. Response to message with blockchain service information

> Find more about RNS in [this blogpost](/post/RNS-Intro)

## Creating a bot

First of all, you need to have the <a href="https://telegram.org/" target="_blank">Telegram application</a>
and an account. Then we can just create a new bot for free:

<ol>
  <li>
    <p>Open the app and search the @BotFather, he will help us to create the bot.</p>
    <div class="center-image-container">
      <img src="/img/telegram_bot_rns/1-create-bot.png" class="shadow-image" />
    </div>
  </li>
  <li>
    <p>A message will appear explaining what you can do with the @BotFather, go ahead with 'Start'.</p>
    <div class="center-image-container">
      <img src="/img/telegram_bot_rns/2-configure-bot.png" class="shadow-image" />
    </div>
  </li>
  <li>
    <p>Let's now go for <code>/newbot</code> option. Send him the keyword <code>/newbot</code> and follow the steps.</p>
    <div class="center-image-container">
      <img src="/img/telegram_bot_rns/3-get-api-key.png" class="shadow-image" />
    </div>
  </li>
  <li>
    <p>You can now chat with your bot going into its link, but nothing will happen.</p>
  </li>
</ol>

## Connecting to the Bot API

{% include commit.html commit="https://github.com/ilanolkies/rns-bot/commit/11fac8974c0d14b71f8e7356a43b6c2571db96d9" %}

We are going to create a Node application to connect to our bot and receive all messages that arrive to him.

Find the public repo: {% include repo.html repo="https://github.com/ilanolkies/rns-bot" %}

1. Create a new Node project
```sh
mkdir rns-bot
cd rns-bot
npm init
```
2. Install the Telegram Bot API<sup><a href="ref-3">3</a></sup>
```sh
npm i node-telegram-bot-api
```
3. Create a new `index.js` file with the following:

```javascript
const TelegramBot = require('node-telegram-bot-api');

// replace the value below with the Telegram token you receive from @BotFather
const token = 'YOUR_TELEGRAM_BOT_TOKEN';

// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(token, { polling: true });

// Matches "/addr [whatever]"
bot.onText(/\/addr (.+)/, (msg, match) => {
  // 'msg' is the received Message from Telegram
  // 'match' is the result of executing the regexp above on the text content
  // of the message

  const chatId = msg.chat.id;
  const resp = `I received ${match[1]}`; // the captured [whatever]

  // answer with resp message
  bot.sendMessage(chatId, resp);
});
```

Run it with:

```sh
node index.js
```

<div class="center-image-container">
  <img src="/img/telegram_bot_rns/4-test-messages.png" class="shadow-image" />
</div>

## Connect to the RIF Name Service

{% include commit.html commit="https://github.com/ilanolkies/rns-bot/commit/c9956a70c104be71bdbc5dc6ac012b97a5e52161" %}

This is really easy to achieve combining RSK public nodes<sup><a href="#ref-4">4</a></sup> with the RNS Javascript library.

Install `Web3.js` client<sup><a href="#ref-5">5</a></sup> to connect to RSK through public nodes and RNS
library<sup><a href="#ref-5">5</a></sup> to make queries to the service.

```sh
npm i web3 @rsksmart/rns
```

Now we are going to:

- Connect to the RSK network with
  ```javascript
  const Web3 = require('web3');

  const web3 = new Web3('https://public-node.rsk.co');
  ```
- Connect to the RNS service with
  ```javascript
  const RNS = require('@rsksmart/rns');

  const rns = new RNS(web3);
  ```
- Query the address of a domain with
  ```javascript
  rns.addr(domain)
      .then(addr => { })
      .catch(error => { })
  ```

Putting it all together:

```javascript
const TelegramBot = require('node-telegram-bot-api');
const Web3 = require('web3');
const RNS = require('@rsksmart/rns');

// replace the value below with the Telegram token you receive from @BotFather
const token = 'YOUR_TELEGRAM_BOT_TOKEN';

// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(token, { polling: true });

// Connect to the RSK network
const web3 = new Web3('https://public-node.rsk.co');

// Connect to the RNS service
const rns = new RNS(web3);

// Matches "/addr [whatever]"
bot.onText(/\/addr (.+)/, (msg, match) => {
  // 'msg' is the received Message from Telegram
  // 'match' is the result of executing the regexp above on the text content
  // of the message

  const chatId = msg.chat.id;

  // Query the address of the captured [whatever]
  rns.addr(match[1])
    .then(addr =>  { // answer the address
      const resp = `The address is ${addr}`;
      bot.sendMessage(chatId, resp)
    })
    .catch(error => { // answer error when not found and a reference if existent
      const resp = `Error: ${error.message}. ${error.ref ? `Find more info at ${error.ref}` : ``}`;
      bot.sendMessage(chatId, resp)
    });
});
```

Save your file and run it again with

```sh
node index.js
```

The result:

<div class="center-image-container">
  <img src="/img/telegram_bot_rns/5-use-addr.png" class="shadow-image" />
</div>

This is it! We got it.

## Summary

We created a new Bot, and we connected to it via HTTP with a simple Node server. We programmed our bot to answer
all the messages received prepended with `/addr`, with the RSK address of the domain specified or an error message if appropriate.

Thanks!

## Want to improve it?

This are some cool things you can do to improve your project

### Hide the API key on your repo

{% include commit.html commit="https://github.com/ilanolkies/rns-bot/commit/3717cc35b9cf41bd6f3b195804fe8054009912ba" %}

You can use `dotenv` library<sup><a href="#ref-7">7</a></sup> to move the API key out of your code easily:

1. Install `dotenv` library
```sh
npm install dotenv
```
2. Create a `.env` file
```
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```
3. Use it with
```
require('dotenv').config();
process.env.TELEGRAM_BOT_TOKEN
```
4. Add `.env` to `.gitignore` file

The project should now look like:

```javascript
require('dotenv').config()
const TelegramBot = require('node-telegram-bot-api');
const Web3 = require('web3');
const RNS = require('@rsksmart/rns');

// replace the value below with the Telegram token you receive from @BotFather
const token = process.env.TELEGRAM_BOT_TOKEN;

// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(token, { polling: true });

/* ... */
```

### Change the bot info

You can achieve this talking to @BotFather

Send him a message saying `/mybots`

<div class="center-image-container">
  <img src="/img/telegram_bot_rns/6-choose-bot.png" class="shadow-image" />
</div>

Now choose the bot of yours you want to update and go to 'Edit bot'

<div class="center-image-container">
  <img src="/img/telegram_bot_rns/7-edit-bot.png" class="shadow-image" />
</div>

Choose the options you want to configure. I configured my bot to look like this setting each of the options available.

<div class="center-image-container">
  <img src="/img/telegram_bot_rns/8-configured.png" class="shadow-image" />
</div>

## More info

1. <span id="ref-1"></span> <a href="https://core.telegram.org/bots" target="_blank">Telegram bots</a>
2. <span id="ref-2"></span> <a href="https://rns.rifos.org" target="_blank">RIF Name Service</a>
3. <span id="ref-3"></span> <a href="https://github.com/yagop/node-telegram-bot-api" target="_blank">Bot API</a>
4. <span id="ref-4"></span> <a href="https://developers.rsk.co/rsk/public-nodes/" target="_blank">RSK Public nodes</a>
5. <span id="ref-5"></span> <a href="https://web3js.readthedocs.io/" target="_blank">Web3.js client</a>
6. <span id="ref-6"></span> <a href="https://developers.rsk.co/rif/rns/libs/javascript/" target="_blank">RNS Javascript library</a>
7. <span id="ref-7"></span> <a href="https://www.npmjs.com/package/dotenv" target="_blank">dotenv library</a>
