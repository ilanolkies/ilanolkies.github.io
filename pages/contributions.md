---
layout: page
title: Contributions
permalink: /contributions
---

<div class="card" style="width: 18rem;">
  <div class="card-body">
    <h5 class="card-title">RSKIP-0060</h5>
    <p class="card-text">
        Addresses can be validated using an injective function that makes capital letters redundant. RSKIP-0060 describes an address checksum mechanism that can be implemented in any network based on [EIP-55](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md).<br>
        This little RSKIP derived on some nice implementations on different repos and languages:
        <ul>
            <li>On [trezor-crypto](https://github.com/trezor/trezor-crypto/blob/4153e662b60a0d83c1be15150f18483a37e9092c/address.c#L62): Heavily optimized cryptography algorithms for embedded devices.</li>
            <li>On [trezor-core](https://github.com/trezor/trezor-core/blob/270bf732121d004a4cd1ab129adaccf7346ff1db/src/apps/ethereum/get_address.py#L32): Source code for 2nd generation of TREZOR called TREZOR model T.</li>
            <li>On [rskjs-util](https://github.com/rsksmart/rskjs-util/blob/5f284ee833ce8d958216804107d0bb90b3feb52e/index.js#L30): A collection of utility functions for RSK.</li>
        </ul>
    </p>
    <a href="https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP60.md" target="_blank" class="btn btn-primary">Have a look at it!</a>
  </div>
</div>
