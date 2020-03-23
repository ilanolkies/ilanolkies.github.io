---
layout: post
title: Hello world to descentralized applications
author: Ilan Olkies
category: rsk
tags: js javascript rsk ethereum web3 blockchain nifty wallet react
permalink: /post/:title
image: /img/hello_rsk/portrait.png
---

Decentralized applications (dApps) run on a peer-to-peer computer network rather than on a central computer. Nowadays, creating decentralized applications is very easy using blockchain technologies. In this article we are going to understand how dapps work and create our first hello world.

1. Architecture: blockchain and serverless apps
2. Development environment setup
3. The smart contract
4. A simple front-end and its key components
5. Using a public blockchain, the RSK Testnet
6. Connect dApp to the Testnet

By the end of the development session you will be running a dApp like this one: [ilanolkies.com/hello-world-rsk/](https://ilanolkies.com/hello-world-rsk/)

Find the public repo: {% include repo.html repo="https://github.com/ilanolkies/hello-world-rsk" %}

# 1. Architecture: blockchain and serverless apps

The objective is to craete an application that nobody needs to require a third party to use it. For this we will use a _blockchain network of smart contracts_, RSK. It allows us to create a public program that can be run by anyone, and has its own public storage, that is, it can be read by anyone. This public programs are called _smart contracts_.

To read and write information on smart contracts users must connect to the blockchain. For that they use nodes. The nodes are connected to other nodes of the blockchain, and the most up-to-date application information is shared among all of them.

In addition, if a user wants to write in a smart contract they must pay a fee. This fee is equivalent to the computational difficulty of our operation. To pay for this fee they must have a wallet with some funds.

Our front-end will be built on an internet browser, and will allow any user to download a web wallet and use our app without the need for any active back end.

![](/img/hello_rsk/architecture.png)

## 2. Development environment setup

We are going to create the blockchain project from scratch with a folder where we will keep our smart contracts, another folder where we will store the migration scripts to deploy this contracts on the blockchain, and in a third one a basic React application that will use these contracts in a public network.

> I'm using Node v12.16.1 - npm v6.14.3 - yarn v1.19.1. This should work in most of node environments.

1. Create an empty folder

    ```
    mkdir hello-world-rsk
    cd hello-world-rsk
    ```

2. Init npm environment (and why not git too?)

    ```
    npm init
    ```

3. Install [Truffle](https://trufflesuite.com/truffle), a simple blockchain development framework

    ```
    npm i --save-dev truffle
    ```

4. Create a truffle project

    ```
    npx truffle init
    ```

We are done {% include commit.html commit="https://github.com/ilanolkies/hello-world-rsk/commit/e311b9c45d2bc2098fdc603531e46371984f2812" %}! We have `contracts` folder with a `Migrations.sol` smart contract, a `migrations` folder with an initial migraiton script and a `test` empty folder. Then a `truffle-config.js` file that we are going to use soon. We are going to create the React app folder later too.

You can now open your project in your file editor, I use `code .`.

Truffle framework provides us of a local blockchain environment. We can try there our implementaitons before sending them to production. We can also run tests over this local network. Try it with

```
npx truffle develop
truffle(develop)>
```

## 3. The smart contract

Smart contracts are written in Solidity language. It's quite easy to learn because it is simmilar to C# or JavaScript. [Read the docs](https://solidity.readthedocs.io/en/v0.6.4/) to learn further on Solidity, I'm just going to give an example.

To create a smart contract we can run

```
npx truffle create contract HelloWorld
```

This will create a `HelloWorld.sol` file in our `contracts` folder. Let's open it

```solidity
pragma solidity >= 0.5.0 < 0.7.0;

contract HelloWorld {
  constructor() public {
  }
}
```

A contract looks like a class. You can declare some global variables, add some functions to read data from the contract and other functions that can be used to update the state of it, paying for the network fee.

> The `private` statement does not say that no one can read the information on it. It is just an function accessibility descriptor, the contract will not export API to access that information seamlessly.

Our contract will look like this:

```solidity
pragma solidity >= 0.5.0 < 0.7.0;

contract HelloWorld {
  string private message;

  constructor() public {
    message = "Hello world!";
  }

  function getMessage() external view returns(string memory) {
    return message;
  }

  function setMessage(string calldata newMessage) external {
    message = newMessage;
  }
}
```

- It stores a message in the global `string message`.
- They API is:
    - `getMessage` returns the message stored
    - `setMessage` allows to change the message stored

### Deployment script

We have to create a deployment script for this. It is very easy: create a `2_hello_world.js` file in `migrations` folder with:

```javascript
const HelloWorld = artifacts.require('HelloWorld');

module.exports = deployer => deployer.deploy(HelloWorld);
```

This will create a new smart contract in the blockchain using the compilation of contract you wrote in Solidity. To create this new smart contract it will require to pay network fees, but not in your local blockcahin as it is free by default    .

1. Deploy contracts

    ```
    $ npx truffle develop
    Truffle Develop started at http://127.0.0.1:9545/

    Accounts:
    (0) 0xf7ec781fbcfd58fd5d2caf2d00fb9047a1af9ae0
    ...



    truffle(develop)> migrate
    ...
    Compiling your contracts...
    ===========================
    > Compiling ./contracts/HelloWorld.sol
    > Compiling ./contracts/Migrations.sol
    > Artifacts written to /Users/ilanolkies/Desktop/hello-world-rsk/build/contracts
    > Compiled successfully using:
       - solc: 0.5.16+commit.9c3226ce.Emscripten.clang

    ...
    Summary
    =======
    > Total deployments:   2
    > Final cost:          0.00792038 ETH
    ```

2. Use the smart contract

    ```
    truffle(develop)> let helloWorld = await HelloWorld.deployed()
    undefined
    truffle(develop)> helloWorld.getMessage()
    'Hellow world!'
    truffle(develop)> helloWorld.setMessage('Goodbye')
    {
      tx: '0x209355092f5bcd2ac3d054a64c6025a17fa1ecf3eea7978dc8b27c883a11bef9',
      receipt: {
        transactionHash: '0x209355092f5bcd2ac3d054a64c6025a17fa1ecf3eea7978dc8b27c883a11bef9',
        transactionIndex: 0,
        blockHash: '0x99696697ef854394e4c8d54fadd5d1efcbbbee4640ad232187ff59befde504c4',
        blockNumber: 5,
        from: '0xf7ec781fbcfd58fd5d2caf2d00fb9047a1af9ae0',
        to: '0x138a4c489a657ba9419f21c2e0c4d9b265a67341',
        gasUsed: 28905,
        cumulativeGasUsed: 28905,
        contractAddress: null,
        logs: [],
        status: true,
        logsBloom: '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
        rawLogs: []
      },
      logs: []
    }
    truffle(develop)> helloWorld.getMessage()
    'Goodbye'
    truffle(develop)>
    ```

Don't close this terminal, we are going to use it soon. Also take note of the _conract address_ somewhere.

```
2_hello_world.js
================

   Deploying 'HelloWorld'
   ----------------------
   ...
   > contract address:    0x138a4c489A657BA9419f21C2E0c4d9B265a67341
   ...
```

### Add some tests

You can run `mocha` tests over your smart contracts.

1. Create `hello_world.test.js` file in your `test` folder with

    ```javascript
    const assert = require('assert');
    const HelloWorld = artifacts.require('HelloWorld');

    contract('Hello World', () => {
      beforeEach(async () => {
        this.helloWorld = await HelloWorld.new();
      });

      it('should have initial message', async () => {
        const message = await this.helloWorld.getMessage();

        assert.equal(message, 'Hello world!');
      });

      it('should allow to set message', async () => {
        await this.helloWorld.setMessage('Goodbye.');

        const message = await this.helloWorld.getMessage();

        assert.equal(message, 'Goodbye.');
      });
    });
    ```

3. Run the tests

    ```
    npx truffle test
    ```

Now we have:
- A smart contract to get ans set a value
- A unit test for this smart contract
- A script to publish it to a local network

{% include commit.html commit="https://github.com/ilanolkies/hello-world-rsk/commit/bce6cd19fd217cd3ec40a072b4cb501ddf968ac3" %}

## 4. A simple front-end and its key components

To use our application, users will have only one requirement: they must have an internet browser with a wallet plugin installed. We are going to use [Nifty Wallet](https://www.poa.network/for-users/nifty-wallet).

On the programmatic side, this wallet injects the global variable `window.ethereum`, which exposes a JavasSript API to connect to a node on the network. This API also allows us to ask the user to sign transactions that will modify the content of the message of our smart contract.

1. Create a new React project in the blockchain workspace. I use `create-react-app`.

    ```
    create-react-app dapp
    cd dapp
    ```

2. We will need a basic package for our dApp: `Web3`, allows you to interact with a local or remote RSK node. Also add Bootstrap to make it nicer :).

    ```
    yarn add web3 react-bootstrap
    ```

    {% include commit.html commit="https://github.com/ilanolkies/hello-world-rsk/commit/c3ca5ea4523f80042ab20f4a024e6fb1ef6d6ff0" %}

3. Now hands on code! Let's build our component:

### Get the message

Getting the value of the content of our smart contract is free. We can do so using `Web3` API to interact with contracts.

```javascript
import React, { Component } from 'react';
import { Container, Row, Col, Spinner } from 'react-bootstrap';
import Web3 from 'web3';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      message: null,
    };

    this.getMessage = this.getMessage.bind(this);
  }

  componentDidMount() {
    this.getMessage();
  }

  getMessage() {
    this.setState({ message: null });

    const web3 = new Web3('http://localhost:9545');

    const helloWorld = new web3.eth.Contract([
      {
        constant: true,
        inputs: [],
        name: "getMessage",
        outputs: [
          { internalType: "string", name: "", type: "string" }
        ],
        payable: false,
        stateMutability: "view",
        type: "function",
      },
    ], '0x138a4c489A657BA9419f21C2E0c4d9B265a67341');

    helloWorld.methods.getMessage().call().then(message => this.setState({ message }));
  }

  render() {
    const { message } = this.state;

    return (
      <Container>
        <Row>
          <Col>
            <h1>Hello world - RSK</h1>
          </Col>
        </Row>
        <Row>
          <Col>
            Message: {message || <Spinner animation="border" />}
          </Col>
        </Row>
      </Container>
    )
  }
}

export default App;
```

{% include commit.html commit="https://github.com/ilanolkies/hello-world-rsk/commit/3f97f9398c5d69369aac63d2681117a7d6248957" %}


### Setting the message

To set a new value the user will need to sign a transaction and pay for the fees. Our local network is free from fees.

1. First I update the component state and add and bind two methods

    ```javascript
    constructor() {
      super(props);

      this.state = {
      message: null,
      newMessage: '',
      setting: false,
      transactionHash: null,
      error: null,
      };

      this.getMessage = this.getMessage.bind(this);
      this.setMessage = this.setMessage.bind(this);
      this.handleMessageChange = this.handleMessageChange.bind(this);
    }
    ```

2. The new methods

    ```javascript
    handleMessageChange(event) {
      this.setState({ newMessage: event.target.value });
    }

    setMessage() {
      const { newMessage } = this.state;

      if (!newMessage) {
        this.setState({ error: 'Type a message' });
        return;
      }
      this.setState({ setting: true, txHash: null, error: null });

      window.ethereum.enable().then(accounts => {
        const web3 = new Web3(window.ethereum);

        web3.eth.net.getId()
        .then(networkId => {
          if (networkId !== 5777) this.setState({ error: 'Wrong network. Please connect to your local network.' });
          else {
            const helloWorld = new web3.eth.Contract([
              {
                constant: false,
                inputs: [
                  { internalType: "string", name: "newMessage", type: "string" }
                ],
                name: "setMessage",
                outputs: [],
                payable: false,
                stateMutability: "nonpayable",
                type: "function",
              },
            ], '0x138a4c489A657BA9419f21C2E0c4d9B265a67341');

            return helloWorld.methods.setMessage(newMessage).send({ from: accounts[0] })
            .on('receipt', ({ transactionHash }) => this.setState({ transactionHash }))
          }
        });
      }).catch(error => this.setState({ error: error.message, setting: false }))
      .finally(() => this.getMessage());
    }
    ```

3. Last but not least, add some UI. This will check that the user has a browser plugin wallet and, if so, display the input for the new message.

    ```javascript
    render() {
      const { message, newMessage, setting, transactionHash, error } = this.state;
      return (
        <Container>
          <></>
          {
            !window.ethereum ?
            <p>Please install <a href="https://chrome.google.com/webstore/detail/nifty-wallet/jbdaocneiiinmjbjlgalhcelgbejmnid?hl=en" targer="_blank" ref="">Nifty wallet</a> to set the message.</p> :
            <>
              <Row>
                <InputGroup>
                  <FormControl type="text" value={newMessage} onChange={this.handleMessageChange} disabled={setting} />
                  <Button onClick={this.setMessage} disabled={setting}>Set Message</Button>
                </InputGroup>
              </Row>
              {setting && <Row><Col><Spinner animation="border" /></Col></Row>}
              {error && <Row><Col><Alert variant="danger">{error}</Alert></Col></Row>}
              {transactionHash && <Row><Col><Alert variant="success">Success! Transaction id: {transactionHash}</Alert></Col></Row>}
            </>
          }
        </Container>
      )
    ```

{% include commit.html commit="https://github.com/ilanolkies/hello-world-rsk/commit/d95f73cb1f984377bdd2ba6a9a6aff4ea6310d9e" %}

Now let's test our app! It is ready. To do so we need to use the browser wallet:

4. Download [Nifty Wallet](https://chrome.google.com/webstore/detail/nifty-wallet/jbdaocneiiinmjbjlgalhcelgbejmnid?hl=en).
5. Start the wallet, save the 12 words, and connect to the local environment: click on the top left selector (network selector). Select 'Custom RPC', complete RPC Url with _http://127.0.0.1:9545_ and save.
6. `yarn start` the app. try it out!

> When signing transactions, you can set 'gas price' value to 0 to pay zero fees.

## 5. Using a public blockchain, the RSK Testnet

All we've done now works only in our local blockchain. We are going to use a public blockchain now. we will need Truffle framework to deploy the contracts on this network, and connect the user wallet to this network too.

## Deploying on RSK Testnet

RSK Testnet is a public blockchain of free use that works as the productive RSK blockchain.

> You can now stop your local blockchain.

1. Connect Truffle project to RSK Testnet network

    In project workspace
    ```
    npm i --save-dev @truffle/hdwallet-provider
    ```

    Update `truffle-config.js` including RSK Testnet network.

    ```javascript
    const fs = require('fs');
    const HDWalletProvider = require('@truffle/hdwallet-provider');

    let mnemonic;
    try {
      mnemonic = fs.readFileSync('.secret').toString().trim();
    } catch {
      mnemonic = 'INVALID';
    }

    module.exports = {
      networks: {
        rskTestnet: {
          provider: () => new HDWalletProvider(mnemonic, 'https://public-node.testnet.rsk.co'),
          network_id: 31,
          gasPrice: 60000000
        }
      }
    };
    ```

    Create a `.secret` file with a 12 wrods mnemonic phrase. This is the private key that will sign deployment transactions. You can generate one [here](https://iancoleman.io/bip39/). Don't use this for productive environments.

    ```
    hero option vessel shy reject project extra undo alien general cactus sausage
    ```

    To connect to RSK Testnet run
    ```
    $ npx truffle console --network rskTestnet
    truffle(rskTestnet)>
    ```

    Try getting the block number! Is the number last block valid for the blockchain. Try getting the block too.

    ```
    truffle(rskTestnet)> web3.eth.getBlockNumber()
    709372
    truffle(rskTestnet)> web3.eth.getBlock('latest')
    ```

2. Get funds to pay for deployment fee. This is free

    Get your default account, the frist one of the list:
    ```
    truffle(rskTestnet)> web3.eth.getAccounts()
    [
      '0xECD67F27bAba0da3A717995042d2a6a764Da2c5f',
      '0x23b325A023A501cBD4E410283629ba41a3A264Be',
      ...
      '0xfC5E5C4B9D4CFBF6699617Bf8Bf05851D1F9353e'
    ]
    ```

    Browse to [RSK faucet](https://faucet.rsk.co) to get some free funds. Paste your address, fill the captcha and wait for confirmation.

    To ensure you received the funds, try getting the balance for your default account. In my case:

    ```
    truffle(rskTestnet)> web3.eth.getBalance('0xECD67F27bAba0da3A717995042d2a6a764Da2c5f')
    ```

3. Deploy!

    To deploy your contracts run

    ```
    truffle(rskTestnet)> migrate
    ```

    This may take a while. Remember to save the contract address. We will use this to connect our dapp.

Common public networks have an explorer to see its information, and does it RSK.

We can use the [RSK Testnet explorer](https://explorer.testnet.rsk.co/) to browse for our account and contract information. Try searching for your default account address, or your contract address.

My contract was deployed on the address [0xe1db8d54450c45e63f0e60a699cab992aaf8fac2](https://explorer.testnet.rsk.co/address/0xe1db8d54450c45e63f0e60a699cab992aaf8fac2)

{% include commit.html commit="https://github.com/ilanolkies/hello-world-rsk/commit/844c01f713bec168daa1e9fc915917fed9a03e6d" %}

## 6. Connect dApp to the Testnet

We are going to use React env variables to switch between contexts.

To connect to RSK blockchain we are going to use RSK Public nodes, as we deed for deployment.

1. Create two env files in react app

    - `.env`

      ```
      REACT_APP_NODE_ENDPOINT=http://localhost:9545
      REACT_APP_NET_ID=5777
      REACT_APP_HELLO_WORLD_ADDRESS=0x138a4c489A657BA9419f21C2E0c4d9B265a67341
      ```

    - `.env.production`

      ```
      REACT_APP_NODE_ENDPOINT=https://public-node.testnet.rsk.co
      REACT_APP_NET_ID=31
      REACT_APP_HELLO_WORLD_ADDRESS=0xe1db8d54450c45e63f0e60a699cab992aaf8fac2
      ```

    Replace all `localhost:9545`, addresses and network ids from `App.js` for the env variables.

    {% include commit.html commit="https://github.com/ilanolkies/hello-world-rsk/commit/844c01f713bec168daa1e9fc915917fed9a03e6d#diff-f59def248b2ed760e7d02f95a0318e49R29" %}

2. Run the app for development with `yarn start` with your local blockchain running on another terminal.
3. Run the app on production serving `yarn build`. This will connect to RSK Testnet network

    In the dapp react app.

    ```
    yarn build
    ...
    You may serve it with a static server:
          yarn global add serve
          serve -s build
    ```

    Serve it with your desired engine or use the recommended by react.

    Browse to `localhost:5000`. You will need to choose RSK Testnet network in your Nifty wallet network selecto and get some funds in your browser wallet with the [RSK faucet](https://facuet.rsk.co).

Now you can use your dapp in the RSK Testnet!

> If you want to host your dapp I recommend to use `gh-pages` pacakge to deploy on Github Pages to get started. The live expereience of the app encourages to keep up developing. https://dev.to/yuribenjamin/how-to-deploy-react-app-in-github-pages-2a1f

You can find the example running here: [ilanolkies.com/hello-world-rsk](https://ilanolkies.com/hello-world-rsk)

## Summary

We created a smart contract on RSK network that acts as a _descentrlized backend_. The benefit of smart contracts is that anyone can operate with them, executing its program.

We used a browser wallet to provider the user of connection to the public network, where we deployed our smart contracts.

The website connect to the browser wallet with a simple programming interface and requested the user to sign transactions.

This are the three basic componentes of a descentralized application! Thanks!
