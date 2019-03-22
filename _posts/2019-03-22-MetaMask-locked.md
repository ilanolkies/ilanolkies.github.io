---
layout: post
title: MetaMask locked - transactions stuck on pending
author: Ilan Olkies
category: rsk
tags: js javascript rsk ethereum web3 blockchain metamask
permalink: /post/:title
image: /img/metamask_locked/portrait.jpg
---

MetaMask is the state-of-art tool for dApss. It usually have problems with nonce and gas fee when we using non-ehtereum networks. Accounts get stuck on an invalid transaction and the transactions that follow are never broadcasted. In this post I explain how to recover the funds and tokens that are blocked in an account that got locked.

![portrait](/img/metamask_locked/portrait.jpg)

I will show how to do it with RSK MainNet, but this works for any network.

1. Download [MyCrypto desktop](https://github.com/MyCryptoHQ/MyCrypto/releases).
2. Open MyCypto desktop
3. On 'Change Netwrok' select RSK.
4. Go to 'View & Send' and select 'Mnemonic phrase' to unlock your account.
5. For security reasons, go offline for the next steps.
6. Find your 12-words. If you don't have them:
    1. Open MetaMask extension and unlock it.
    2. Go to settings on the top right corner menu.
    3. Go offline for security reasons.
    4. Click on 'REVEAL SEED WORDS' and input your password.
    5. Write the 12 words on a paper.

7. Input the 12 words in order, separated by spaces.
8. Now you might go online!
8. Click on 'Choose address'.
9. In the top 'Addresses' selector choose 'Default (ETH)'.

    ![choose_address](/img/metamask_locked/choose_address.png)

10. This will show up all your MetaMask accounts.
11. Now you can select and unlock the one that got locked!
12. Send the founds and tokens to any account. If you want to continue using MetaMask you can create a new account in the configuration and send the funds to that account.

## Technical explanation

- Why transactions go to pending state?

    Each transaction has a noce value that serves for keeping the transactions ordered. The first transaction of an account has nonce 0, the second 1, and so on.

    When MetaMask sends a transaction that can not be broadcasted, such as onw with 0 gas in mainnet, the wallet stores that transaction was sent and updates the nonce for the next transaction. Then, the following transaction has an invalid nonce, because the previous wasn't broadcasted!

    The blockchain does not allow any transaction to be executed with a nonce that is not the next to the last transaction executed. This is why we see transactions as 'pending', but actually they are never broadcasted.

- Why do I select 'Default (ETH)' to choose addresses.

    MetaMask uses [BIP-44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki) hierarchical deterministic wallet derivation for addresses. But for all networks it uses the same derivation path: `(m/44'/60'/0'/0/i)`, Ethereum derivation path.
    No matter what network you choose, MetaMask will always use this derivation path. That's why we have to choose it in MyCrypto to find the right addresses.

Hope it's usefull!
