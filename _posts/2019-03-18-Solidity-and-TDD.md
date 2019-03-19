---
layout: post
title: Solidity and TDD - How to build a smart contract
author: Ilan Olkies
category: rsk
tags: js javascript rsk ethereum web3 blockchain tdd unit-test integration-test
permalink: /post/:title
image: /img/first_dapp_rsk/portrait.png
---

The task of writing smart contracts entails the difficulty of maintaining the authenticity of the code against infinite cases. Contracts are part of a public network and expose their vulnerabilities to any attacker, and this becomes critical when it comes to money. This is why the practice of TDD is one of our best friends when developing our smart contracts.

We are going to build a platform for public donations. On one side we have the projects and on other side the donors. We want to connect this two parties directly and transparently. So we need a place where projects are published and a way to send founds to it. We also want this donors to have a public exposure of how much they donated.

## Steps

Let's devide our plataform development in some steps:
1. Prepare the development environment.
2. Create a smart contract.
3. Design a structure that enables projects to receive money.
4. Add direct gas donation functionality.
5. List and expose all donors and their donations.

First of all we need to know some basic concepts to follow this post:
- The basics of [Solidity](https://solidity.readthedocs.io)
- Unit testing in [JavaScript](https://javascript.com) with node assert
- [Truffle](https://trufflesuite.com/truffle) or any blockchain development framework.

## TDD Session

### 1. Truffle framework

{% include repo.html repo="https://github.com/ilanolkies/donate-direct" %}

First we are going to create a Truffle project.

> Go [here](https://www.truffleframework.com/truffle) to install Truffle framework.

```sh
mkdir direct-donations
cd direct-donations
truffle init
```

This creates a porject with a simple structure: a _contracts_ folder where we save our smart contracts, a _migrations_ folder with deployment scripts and a _test_ folder with testing scripts. We also have a `truffle-config.js` file with some Truffle configurations. We are going to use it later to connect to any public network.

`Migrations` contract keeps the record of the successfull compilations.

{% include commit.html commit="https://github.com/ilanolkies/donate-direct/commit/99b9575c3e5d19da902a62310bfb7b584a984028" %}

Run this command on the project folder:

```sh
truffle develop
```

You will see the following:

```
Truffle Develop started at http://127.0.0.1:9545/

Accounts:
(0) 0x627306090abab3a6e1400e9345bc60c78a8bef57
(1) 0xf17f52151ebef6c7334fad080c5704d77216b732
(2) 0xc5fdf4076b8f3a5357c5e395ab970b5b54098fef
(3) 0x821aea9a577a9b44299b9c15c88cf3087f3b5544
(4) 0x0d1d4e623d10f9fba5db95830f7d3839406c6af2
(5) 0x2932b7a2355d6fecc4b5c0b6bd44cc31df247a2e
(6) 0x2191ef87e392377ec08e7c08eb105ef5448eced5
(7) 0x0f4f2ac550a1b4e2280d04c21cea7ebd822934b5
(8) 0x6330a553fc93768f612722bb8c2ec78ac90b3bbc
(9) 0x5aeda56215b167893e80b4fe645ba6d5bab767de

Private Keys:
(0) c87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3
(1) ae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f
(2) 0dbbe8e4ae425a6d2687f1a7e3ba17bc98c673636790f1b8ad91193c05875ef1
(3) c88b703fb08cbea894b6aeff5a544fb92e78a18e19814cd85da83b71f772aa6c
(4) 388c684f0ba1ef5017716adb5d21a053ea8e90277d0868337519f97bede61418
(5) 659cbb0e2411a44db63778987b1e22153c086a95eb6b18bdf89de078917abc63
(6) 82d052c865f5763aad42add438569276c00d3d88a2d062d36b2bae914d58b8c8
(7) aa3680d5d48a8283413f7a108367c7299ca73f553735860a87b08f39395618b7
(8) 0f62d96d6675f32685bbdb8ac13cda7c23436f63efbb9d07700d8669ff12b7c4
(9) 8d5366123cb560bb606379f90a0bfd4769eecc0557f1b362dcae9012b548b1e5

Mnemonic: candy maple cake sugar pudding cream honey rich smooth crumble sweet treat

⚠️  Important ⚠️  : This mnemonic was created for you by Truffle. It is not secure.
Ensure you do not use it on production blockchains, or else you risk losing funds.

truffle(develop)>
```

Truffle spawns a development blockchain locally on port 9545. This means we have a local standalone blockchain, we are our own miners and our blockchain is not connected to the RSK network. It just lives in our computer.

We are gonig to use this blockchain to build and test our smart contracts.

### 2. Creating the smart contract

We are going to build our smart contract with TDD. Tests are placced in `test/direct_donate.js`.

First we want to test out **smart contract creation**. To do this we are going to write a simple test:

```js
const assert = require('assert');
const DirectDonate = artifacts.require('DirectDonate');

contract('DirectDonate', async (accounts) => {
  it('should deploy contract', async () => {
    await DirectDonate.new();
  });
});
```

Of course this test is not passing, because we have no _contracts/DirectDonate.sol_ valid contract. So let's create it with:

```sh
truffle(develop)> create contract DirectDoante
```

{% include commit.html commit="https://github.com/ilanolkies/donate-direct/commit/3446db265012676c9fde986ad5134a679025ec7b" %}

We extract deployment from test because we will re-deploy the contract for each test. This is how we make it work as a unit test module.

```js
contract('DirectDonate', async (accounts) => {
  var directDonate;

  beforeEach(async () => {
    directDonate = await DirectDonate.new({ from: accounts[0] });
  });

  it('should deploy contract', async () => { });
});
```

### 3. The project structure

We want to **store some public projects in a list**. So our first test would be:

```js
it('should begin with no projects', async () => {
  const projectQuantity = await directDonate.projectIndex();

  assert.equal(projectQuantity, 0);
});

it('should add a project', async () => {
  const previousQuantity = await directDonate.projectIndex();

  await directDonate.addProject();

  const projectQuantity = await directDonate.projectIndex();

  assert.equal(projectQuantity, previousQuantity.toNumber() + 1);
});
```

This common pattern in TDD is passed by adding a global `projectIndex` variable, initialize it in the `contructor` with `0` and:

```js
function addProject () public {
    projectIndex++;
}
```

{% include commit.html commit="https://github.com/ilanolkies/donate-direct/commit/ebf0bfcee8dbdaa7a724ea87e20307143718e97d" %}

And we want to **get the first item after adding it**:

```js
it('should add and return the project', async () => {
  const projectName = 'NewProject';

  await directDonate.addProject(projectName);

  const project = await directDonate.projects(0);

  assert.equal(project, projectName);
});
```

Now we store projects in a `string[] public address`, and we use the methods:

```js
function projectIndex () public view returns (uint) {
    return projects.length;
}

function addProject (string projectName) public {
    projects.push(projectName);
}
```

> We have to edit the previous test to support this new interface by adding an empty project.

{% include commit.html commit="https://github.com/ilanolkies/donate-direct/commit/7904b9058babbe919280ddd5fb2692de027c3993" %}

The `view` modifier indicates that the function does not modiffy the state of the contract, and no one need to pay for executing it. It is commonly used for getters, like this one.

Now we want to **extend our project entity**. We want to store an address for the donors to send the money to, and a web page url.

```js
it('should store the project\'s address and url', async () => {
  const projectName = 'NewProject';
  const projectReceiver = accounts[1];
  const projectUrl = 'https://www.kklweb.org/';

  await directDonate.addProject(projectName, projectReceiver, projectUrl);

  const actualProjectName = await directDonate.projectName(0);
  const actualProjectReceiver = await directDonate.projectReceiver(0);
  const actualProjectUrl = await directDonate.projectUrl(0);

  assert.equal(actualProjectName, projectName);
  assert.equal(actualProjectReceiver, projectReceiver);
  assert.equal(actualProjectUrl, projectUrl);
});
```

Instead of an array of strings we are going to store an `Project[] public projects`, where `Project` is a `struct`.

```js
Project[] public projects;

struct Project {
    string name;
    address receiver;
    string url;
}

function addProject (string name, address receiver, string url) public {
    Project memory project;
    project.name = name;
    project.receiver = receiver;
    project.url = url;

    projects.push(project);
}

function projectName (uint index) public view returns(string) {
    return projects[index].name;
}
```

{% include commit.html commit="https://github.com/ilanolkies/donate-direct/commit/d4ba88277078f5e1d338b9620b294905ecadac5f" %}

### 4. Adding direct donation functionality

This smart contract should not be just a 'project storage' where we can find any project given an id. We want to add some functionalities to it. **Anyone may be able to donate directly to a project's receiver** via our smart contract.

```js
it('should send founds to receiver', async () => {
  await addProject();

  const receiver = (await directDonate.projects(0))[1];
  const getReceiverBalance = async () => await web3.eth.getBalance(receiver);

  const previousBalance = await getReceiverBalance();
  const value = 10e18;

  await directDonate.donate(0, { value });

  const balance = await getReceiverBalance();

  assert.equal(balance, previousBalance.toNumber() + value);
});
```

The contract receives money on the transaction, and can send it to another address using `transfer` function. It can transfer founds to any address, either an account or a contract.

```js
function donate (uint index) public payable {
    address receiver = projects[index].receiver;

    receiver.transfer(msg.value);
}
```

{% include commit.html commit="https://github.com/ilanolkies/donate-direct/commit/0aa77a6e8fb7b396bacbcc81d3686de20ec8ef38" %}

Let's another test to ensure many projects can be added. I won't write the test her because it's a little bit long. Check it in the commit {% include commit.html commit="https://github.com/ilanolkies/donate-direct/commit/0c10ccd97164b235243d58b43913e7388fefabd7" %}.


We have a complete and usefull plataform for direct donations. The only thing missing is the donors exposure.

### 5. Listing donors

We want to **get donors by project**.

```js
it('should return project\'s donors', async () => {
  await addProject();

  await directDonate.donate(0, { from: accounts[2], value: 1e18 });

  var donors = await directDonate.donors(0);

  assert.equal(donors.length, 1);
  assert.equal(donors[0], accounts[2]);

  await directDonate.donate(0, { from: accounts[3], value: 1e18 });

  donors = await directDonate.donors(0);

  assert.equal(donors.length, 2);
  assert.equal(donors[0], accounts[2]);
  assert.equal(donors[1], accounts[3]);
});
```

To pass this test we can add an `address[]` to the `Project` struct. Then we must store the donor on the `donate` execution, and we also need a getter to query this donors.

```js
struct Project {
    //...
    address[] donors;
}

function addProject (string name, address receiver, string url) public {
    //...
    address[] memory donors;
    project.donors = donors;

    projects.push(project);
}

function donate (uint index) public payable {
    Project storage project = projects[index];
    address receiver = project.receiver;
    project.donors.push(msg.sender);

    receiver.transfer(msg.value);
}

function donors (uint index) public view returns (address[] memory) {
    return projects[index].donors;
}
```

{% include commit.html commit="https://github.com/ilanolkies/donate-direct/commit/3acdceabb77b3dbfcfd4c29776c1aca4d302cc6c" %}

This looks sufficient but we re going to add only one more feature! We want to store the amount it was donated too.

```js
it('should return project\'s donations', async () => {
  await addProject();

  const value = 1e18;
  await directDonate.donate(0, { from: accounts[2], value });

  var donations = await directDonate.donations(0);

  assert.equal(donations.length, 1);
  assert.equal(donations[0], value);
});
```

To solve this problem we can just add a new array in the struct that stores `uint` values. This values match de donor address in the `donors` array.

```js
function donations (uint index) public view returns (uint[] memory) {
    Project storage project = projects[index];
    return project.donations;
}
```

{% include commit.html commit="https://github.com/ilanolkies/donate-direct/commit/93d2707b93dbe0250089ffe732644c2a60711aca" %}


### Next steps

For the nex Solidity and TDD we are going to store the `owner` value to **manage the projects**. We are going to be able to **close projects**. Then we will add a **maximum of donations accepted** for each project. Last but not least, we are going to **add some validations** to our smart contract, nobody should make a mistake sending money for charity. To conclude this TDD session we will build an **integration test**.

See you soon!
