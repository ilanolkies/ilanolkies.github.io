---
layout: post
title: Clean Up Xamarin.Forms
author: Ilan Olkies
category: Xamarin
tags: xamarin mobile goodpractice
permalink: /post/:title
image: /img/xamarin_cleanup/front.png
---

This is a simple example about how to **clean up the `Xamarin.Forms` default new solution content**, before first commit. This is an easy good practice, it will solve many problems later. Follow each step checking commit after each task.

{% include repo.html repo="https://github.com/ilanolkies/XamarinCleanUpExample" %}

1. Start by the `.gitignore` {% include commit.html commit="https://github.com/ilanolkies/XamarinCleanUpExample/commit/20294ceb675bf298d6057ec44bc14fac9367159b" %}
2. This is how the default intial solution looks like, without any changes {% include commit.html commit="https://github.com/ilanolkies/XamarinCleanUpExample/commit/cc9d07ad391a3bb899bc9b71b239a04400487d6a" %}
3. Update NuGet packages: at least `Xamarin.Forms` {% include commit.html commit="https://github.com/ilanolkies/XamarinCleanUpExample/commit/fa82312151c789462619d7fcfbb230cea7d901d7" %}
4. Delete Android _.txt_ files {% include commit.html commit="https://github.com/ilanolkies/XamarinCleanUpExample/commit/fa98a1fa04312757983767103216ba9e4da295e9" %}
5. Remove unnecessary usings {% include commit.html commit="https://github.com/ilanolkies/XamarinCleanUpExample/commit/03119773603cc5b30dd62a043d274933a8115b59" %}
6. Remove comments {% include commit.html commit="https://github.com/ilanolkies/XamarinCleanUpExample/commit/833c753e2a4aadd92acc0cc41d0d82b78962c7c4" %}
7. Remove unnecessary instances {% include commit.html commit="https://github.com/ilanolkies/XamarinCleanUpExample/commit/4314a43ffa8dc6487213f0ac2a10ee670ce935a8" %}
8. Delete iOS Xamarin icons {% include commit.html commit="https://github.com/ilanolkies/XamarinCleanUpExample/commit/7a4ccc5e63a6dae1b0f5a88e76d08bed15afd31e" %}
9. Make _.xaml_ nicer {% include commit.html commit="https://github.com/ilanolkies/XamarinCleanUpExample/commit/405976ec3aed22bb63ea469a782b68978477efa8" %}

> Working on an empty way to delete Android Xamarin icons.