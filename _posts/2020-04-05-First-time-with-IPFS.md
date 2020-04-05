---
layout: post
title: First time with IPFS
author: Ilan Olkies
category: javascript
tags: js javascript ipfs rif distributed file-system fs rsksmart rif-storage
permalink: /post/:title
image: /img/first_ipfs/front.png
---

IPFS (Interplanetary File System) is a protocol and network designed to create a content-addressable p2p method for storing and sharing hypermedia on a distributed file system. In this article we are going to learn how to upload and download files to IPFS via command line and from JavaScript using RIF Storage client.

## Brief intro

Let’s say you’re doing some research on aardvarks, you might start by visiting the Wikipedia page on aardvarks at:

```
https://en.wikipedia.org/wiki/Aardvark
```

When you put that URL in your browser’s address bar, your computer asks one of Wikipedia’s computers, which might be somewhere on the other side of the country (or even the planet), for the aardvark page.

However, that’s not the only option for meeting your aardvark needs! There’s a mirror of Wikipedia stored on IPFS, and you could use that instead. If you use IPFS, your computer asks to get the aardvark page like this:

```
/ipfs/QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco/wiki/Aardvark.html
```

IPFS knows how to find that sweet, sweet aardvark information by its contents, not its location. The IPFS-ified version of the aardvark info is represented by that string of numbers in the middle of the URL (QmXo…), and instead of asking one of Wikipedia’s computers for the page, your computer uses IPFS to ask lots of computers around the world to share the page with you. It can get your aardvark info from anyone who has it, not just Wikipedia.

And, when you use IPFS, you don’t just download files from someone else — your computer also helps distribute them. When your friend a few blocks away needs the same Wikipedia page, they might be as likely to get it from you as they would from your neighbor or anyone else using IPFS.

IPFS makes this possible for not only web pages, but also any kind of file a computer might store, whether it’s a document, an email, or even a database record.<sup><a href="#ref-1">1</a></sup>

## Getting started

Let's find Aardvark Wikipedia's file using the IPFS command line tool. Download it [here](https://dist.ipfs.io/#go-ipfs). Once you have it run

```
tar xvfz go-ipfs.tar.gz
cd go-ipfs
./install.sh
ipfs init
```

This should take only minutes. Once you have the app let's try getting the page.

### Downloading files

Run in your terminal

```
ipfs cat QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco/wiki/Aardvark.html
```

This will output all the html content of the file in the console!

### Uploading files

First I will create a simple file:

```
$ echo "hello ipfs" > foo
$ cat foo
hello ipfs
```

Now upload it:

```
$ ipfs add foo
added QmSoASxb8aNVGk3pNWpZvXEZTQKxjGeu9bvpYHuo5bP1VJ foo
 11 B / 11 B [==========================================] 100.00%
```

Now let's get its content:

```
$ ipfs cat QmSoASxb8aNVGk3pNWpZvXEZTQKxjGeu9bvpYHuo5bP1VJ
hello ipfs
```

It's awesome, and seems very easy to use. There's a cool IPFS tutorial about how to use the command line tool in:

```
ipfs cat QmS4ustL54uo8FzR9455qaxZwuMiUhyvMcX9Ba8nUH4uVv/quick-start
```

## Hands on code

We are going to create a script that uplaods an image to IPFS, then downloads it and displays it in the default image viewer.

### Setup

1. Let's create a sample project

    ```
    mkdir ipfs-sample
    cd ipfs-sample
    ```

    We are going to use 3 packages:
    - `fs` to read and write files -- The `fs` module provides an API for interacting with the file system in a manner closely modeled around standard POSIX functions <sup><a href="#ref-2">2</a></sup>
    - `@rsksmart/rif-storage` to connect to IPFS -- Client library integrating distributed storage projects <sup><a href="#ref-3">3</a></sup>
    - `open` to open default image viewer -- Open stuff like URLs, files, executables. Cross-platform <sup><a href="#ref-4">4</a></sup>

    ```
    npm i @rsksmart/rif-storage open
    ```

2. Run IPFS Daemon. This will enable to use port `5001` to interact with IPFS file storage. In another terminal run

    ```
    ipfs daemon
    ```

## Create the app

Let's try getting the file we uploaded with the command line tool, the 'hello ipfs':

```javascript
const RifStorage = require('@rsksmart/rif-storage')
const fs = require('fs')
const open = require('open')

const main = async () => {
  const storage = RifStorage.default(RifStorage.Provider.IPFS, { host: 'localhost', port: '5001', protocol: 'http' })
  const fileHash = 'QmSoASxb8aNVGk3pNWpZvXEZTQKxjGeu9bvpYHuo5bP1VJ'
  const retrievedData = await storage.get(fileHash)
  fs.writeFileSync(fileHash, retrievedData)
  open(fileHash)
};

main();
```

Now let's try uploading a file. I'm going to upload my logo :D

<div style="text-align: center;">
    <img src="../logo.png" height="120" />
</div>

I copy the file into the project folder and code:

```javascript
const RifStorage = require('@rsksmart/rif-storage')
const fs = require('fs')
const open = require('open')

const main = async () => {
  const storage = RifStorage.default(RifStorage.Provider.IPFS, { host: 'localhost', port: '5001', protocol: 'http' })

  const file = fs.readFileSync('logo.png')
  const fileHash = await storage.put(file)
  console.log(fileHash)

  const retrievedData = await storage.get(fileHash)
  fs.writeFileSync(fileHash, retrievedData)
  open(fileHash)
};

main();
```

Run it with `node index.js`. You should find the image you uploaded popping up in your image editor.

## Conclusion

We understood the basic operation of IPFS: it is a content-addressable file storage. We also understood, in broad terms, how it works.

We have operated with IPFS using the command line tool. We upload and download files.

We also made a JavaScript program, using the rif storage ipfs client, which allowed us to upload an image and view its content.

## Now what?

There's a lot more content to research on this exciting distributed file system.

- To use IPFS from your browser, try getting the [IPFS Companion](https://github.com/ipfs-shipyard/ipfs-companion#install) browser extension. After installing it browse to `ipfs://QmSoASxb8aNVGk3pNWpZvXEZTQKxjGeu9bvpYHuo5bP1VJ` or to your recently uploaded image fingerprint.
- Ensure your files are permanently ulpoaded. Read [this article](https://docs.ipfs.io/guides/concepts/pinning/) to understand pining service.
- Use [public gateways](https://ipfs.github.io/public-gateway-checker/) to browse without extension. Try browsing to [https://ipfs.io/ipfs/QmSoASxb8aNVGk3pNWpZvXEZTQKxjGeu9bvpYHuo5bP1VJ](https://ipfs.io/ipfs/QmSoASxb8aNVGk3pNWpZvXEZTQKxjGeu9bvpYHuo5bP1VJ).
- Understand what are [gateways](https://github.com/ipfs/go-ipfs/blob/master/docs/gateway.md) and how they work. Run your own gateway.

## References

1. <a id="ref-1" href="https://docs.ipfs.io/introduction/overview/" target="_blank">IPFS Docs</a>
2. <code><a id="ref-2" href="https://nodejs.org/api/fs.html">fs</a></code>
3. <code><a id="ref-3" href="https://github.com/rsksmart/rif-storage-js" target="_blank">@rsksmart/rif-storage</a></code>
4. <code><a id="ref-4" href="https://github.com/sindresorhus/open" target="_blank">open</a></code>
