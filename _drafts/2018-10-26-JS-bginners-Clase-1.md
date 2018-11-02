---
layout: post
title: JS Beginners - Class 1
author: Ilan Olkies
category: javascript
tags: js javascript js-beginners class
permalink: /post/:title
image: /img/js_beginners_class_1/portrait.png
---

## Introduction

This is the begining of a little programming cours for beginners. I will publish some classes explaining the basis of programming and an introduction to JavaScript programming language, used in many contexts like web browsers to build interactive web pages.

## Al little bit of computer architecture

Computers have an architecture easy to understand, made up by different components:

- The **CPU** encharged of processing the logic and aritmetic of a program.
- The **main memory**, the RAM, that stores the instruction and data of the program being executed.
- An **input and output system** that allows the interaction of the user with the system hroguh input and output devices like the keyboard, the mouse, or the screen.
- A **secondary memory** like a hard drive disk to store data atemporarily.

## What does programming implies?

Programming is the process of writing computer programs. Mhh... and what are programs? A series of coded software instructions to control the operation of a computer.

So, programming is creating a recipie that the computer will follow to execute what we want to. For example, we may build a program that displays the age of a person in the screen, or print the bill's items and final price.

## Programming languages and JavaScript

Programming languages are the way we can make a computer understand what oparations has to do to execute what we want to. 

JavaScript is a programming language. Alongside HTML and CSS, JavaScript is one of the three core technologies of the World Wide Web. JavaScript enables interactive web pages and thus is an essential part of web applications. The vast majority of websites use it.

Initially only implemented client-side in web browsers, JavaScript engines are now embedded in many other types of host software, including server-side in web servers and databases, and also in non-web programs.

**Let's begin coding!**

## Variables

Let's think of some boxes that can store any data we want to.

![Variable vacía](/img/js_beginners_class_1/variable-0.png)

We would like to differenciate them, so we will put them a name.

![Variable vacía](/img/js_beginners_class_1/variable-1.png)

Now we will store the data we want to store in them.

![Variable vacía](/img/js_beginners_class_1/variable-2.png)

This boxes are called **variables** and are used in programs to store any data. Variables have different operations like summing or multyplying. Variables are a escential elemnt for programming.

To create a variable we are going to use the keyword `var` followed by it's name.

```js
var name;
var age;
```

What we se here is a program! It does nothing else than creating two variables named `name` y `age`. 

JavaScript programs are interpretated from top to bottom, and at the end of each sentence, we use a `;` to determinate this end.

> There are some exceptions to this rules. JavaScript has many syntaxys avaliable, but we are going to work with some habits to make a good programming. For example, the `;` after each sentence is not a must.

Now we can store the value we want to in it. To do so we use an `=` preceeded by the variable name and followed by the value to asign.

```js
name = 'Ilan';
age = 20;
```

Looks easy! To shorten the wyntaxis we can avrebiate this to steps in just one.

```js
var  name = 'Ilan';
var age = 20;
```

## Operations

We can operate the variables which are of the same type. Numbers have operations between them, words, lists, and some more.

### Number operations

We are going to operate between two variables, and store the result in a third one.

```js
var a = 10;
var b = 7;

var c;

c = a + b; // Sum
c = a - b; // Substraction
c = a * b; // Multiplication
c = a / b; // Division
c = a ^ b; // Power
```

This are some operation between numbers, but not all of them.

The `//` expresion indicates that the words that follows it is a **comment**, so it's not going to process it.

#### Examples

How old are you?

```js
var birthYear = 1998;
var year = 2018:

var age = year - birthYear;
```

How much does the fuit punch costs?

```js
var orangeValue = 10;
var appleValue = 8;
var bananaValue = 5;

var oranges = 4;
var apples = 2;
var bananas = 3;

var orangesPrice = orangeValue * oranges;
var applesPrice = appleValue * apples;
var bananaPrice = bananaValue * bananas;

var fruitPunchPrice = orangesPrice + applesPrice + bananaPrice;
```

### Text operations

For text we are going to use mainly the concatenation. We use it with the  `+` between the text to be joined.

```js
var a = 'Hi';
var b = 'JavaScript';

var c = a + ' '
var c = c + b; // c = 'Hi JavaScript
```
This program stores `'Hi JavaScript'` in `c` variable.

## Functions

Functions are a different type od box, magic boxes. Like variables, have a name, but they store _little programs_ inside. So we put some variables inside this box and the boxes returns us a result.

![Function](/img/js_beginners_class_1/function.png)

As we said, functions receive some that, process it, and returns (or not) an output value. The input elements are called **arguments** and the output is the **return value**.

Functions are declared this way:

```js
function sum (a, b) {
    var result = a + b;
    return result;
}
```

The keyword `function` indicates that the following text is the name. The next element are the names of the arguments, between parenthisys, separated by commas. Then, the curly brackets indicate the beginning and the end of the function, and the keyword `return` indicates the name of the variable that stores the value to be returned.

Functions is the other main element for programming. Now with this two tools we can build a simple program:

```js
function price (apples, oranges, bananas, grapes) {
    var applesPrice = apples * 8;
    var orangesPrice = oranges * 10;
    var bananasPrice = bananas * 5;
    var grapesPrice = grape * 0.1;

    return applesPrice + orangesPrice + bananasPrice + grapesPrice;
}

function twentyDiscount (price) {
    var result = price * 90 / 100;
    return result;
}

var fruitPunchPrice = price(2, 3, 4, 0);
var wine = price(0, 0, 0, 10);
var juice = price(2, 4, 0, 0);

var fruitPunchWithDiscount = twentyDiscount(fruitPunchPrice);
var wineWithDiscount = twentyDiscount(winePrice);
var juiceWithDiscount = twentyDiscount(juicePrice);
```

This program may be used in the grocery to caculate the price of a bag of fruit, and make a discount to frequent clients.

## Conclusion

We learned how to create a simple program in JavaScript mixing three mainframes of the programming world: variables, operations and functions. Variables are used to store values that can be operated using it's types operations. Functions store a little program inside our program, that processes som arguments and return a result.

## Topics

1. [Variables](#variables)
2. [Operations](#operations)
3. [Functions](#functions)

## Excercises

I publish some excersises in [GitHub](https://github.com/ilanolkies/js-beginners). If you don't now nothing about git, you can go to the link and manually download it. Go to excersise-1 folder and read the README file that explains how to complete the excersise.
