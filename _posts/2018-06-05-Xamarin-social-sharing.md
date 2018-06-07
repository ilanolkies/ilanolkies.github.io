---
layout: post
title: Xamarin social sharing
author: Ilan Olkies
category: Xamarin
tags: xamarin mobile ios android social
permalink: /post/:title
image: /img/xamarin_social/front.png
---

One of the key points to make our app grow in users is to **get spread through social networks**: WhatsApp, Facebook, Twitter, and so on. In this tutorial we are going to learn how to **place a native share button in our apps**.
- Encourage your users to share your app content.
- Make it easy for them to tell their close people about your app.
- Convert shares in new shares.
- Reach new people.

![front]({{ site.url }}{{ page.image }})

## Ingredients
- Visual Studio updated.
- Something to share!

## Steps
 
1. Creating a simple app
2. Designing a Dependency injection
    1. Implementig on Android
    2. Implementig on iOS

## Code!

{% include repo.html repo="https://github.com/ilanolkies/XamarinSocialExample" %}

### 1. Creating a simple app

An exciting beging, creat a Xamarin.Forms blank app! {% include commit.html commit="https://github.com/ilanolkies/XamarinSocialExample/commit/fc2acd3ff7123e9c0b82a64343faacd53c1e1be8" %}

> I will soon upload a tutorial on how to clean your app for the initial commit.

I created a button that will trigger the Social _popup_. This button calls the `Share` method. Just for a minute, I will display an alert.

### 2. Designing a Dependency injection

Create a new interface in your shared project. This will be the `DependencyInjection` interface.

```csharp
namespace XamarinSocial
{
	public interface ISocial
	{
		void Share(string content);
	}
}
```

Now we are going to implement the `DependencyInjection` in both devices. It's just creating a _ShareService.cs_ class that contains the following:

#### 2.1. Implementig on Android {% include commit.html commit="https://github.com/ilanolkies/XamarinSocialExample/commit/b9f2f51f5db4793a3c1d28238c2c251c78d13bfc" %}

```csharp
using Android.Content;
using Xamarin.Forms;
using XamarinSocial.Droid;

[assembly: Dependency(typeof(SocialService))]
namespace XamarinSocial.Droid
{
	public class SocialService : ISocial
    {      
		public void Share(string content)
		{         
			Intent share = new Intent(Intent.ActionSend)
				.SetType("text/plain")
				.AddFlags(ActivityFlags.ClearWhenTaskReset)
				.PutExtra(Intent.ExtraText, content);

			Android.App.Application.Context.StartActivity(Intent.CreateChooser(share, "Compartir!"));
		}
	}
}
 ```

#### 2.2. Implementig on iOS {% include commit.html commit="https://github.com/ilanolkies/XamarinSocialExample/commit/c8a18df9829d5e770c0b33db47e0ec8510ddfe88" %}

```csharp
using Foundation;
using UIKit;
using Xamarin.Forms;
using XamarinSocial.iOS;

[assembly: Dependency(typeof(SocialService))]
namespace XamarinSocial.iOS
{
	public class SocialService : ISocial
	{
		public void Share(string content)
		{
			var activityViewController = new UIActivityViewController(new NSString[] { new NSString(content) }, null);

			UIApplication.SharedApplication.KeyWindow.RootViewController.PresentViewController(activityViewController, true, null);
		}
	}
}
```
