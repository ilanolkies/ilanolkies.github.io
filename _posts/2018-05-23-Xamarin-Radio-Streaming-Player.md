---
layout: post
title: Xamarin Radio Streaming Player
author: Ilan Olkies
category: Xamarin
tags: xamarin mobile ios android
permalink: /post/:title
image: img/streaming/front.png
---

In this Xamarin tutorial we are going to create a simple radio streaming player app for iOS and Android. The radio will have 3 simple actions: Play, Stop and Pause.

![front]({{ site.url }}/img/xamarin_streaming/front.png)

## Intro: What are we going to learn and/or practice?
- Create a simple **`View` with a `ViewModel`**.
- Using **images as buttons** for Play, Pause and Stop.
- Use **Data Binding** to change icons when radio start/stops playing. 
- Using **Dependecy Injection**.
- Adding keys to **`Info.PList`**.

> You can go [here](#6_DependencyInjection_for_streaming) if you just need the **Dependency Injection** stuff.

## Ingredients
- Visual Studio updated.
- The streaming links we want to reproduce. To test the links before using them, open them in the respective devices browsers, they must be two different links.
- Some images for play, pause and stop buttons. It's quite borring to use those blue labels...

> Check the <a href="{{ site.baseurl }}/workflow">general workflow</a> of my posts.
 
> **Important: debug after each step!**. It's the most simple and best practice.

## Coding!

{% include repo.html repo="https://github.com/ilanolkies/XamarinRadioStreamingExample" %}

### 1. Create `Xamarin.Forms` project

{% include commit.html commit="https://github.com/ilanolkies/XamarinRadioStreamingExample/commit/ef9d4084a5f6d067433a81d231404605d4ec6d59" %}

Create a **Xamarin.Forms** blank app with Android and iOS projects.

### 2. Dsign the `MainPage`

{% include commit.html commit="https://github.com/ilanolkies/XamarinRadioStreamingExample/commit/3fd6485c4b31e01b760c028d91a06ac4756639a5" %}

For the design of the `MainPage` we are going to use some images for play, pause and stop button. I downloaded them from [FlatIcon music pack](https://www.flaticon.com/packs/music).

> Default main page is located in the Xamarin.Forms project and named _YourSolutinonName.xaml_.

A `Label` is added by default. We must use a [layout](https://docs.microsoft.com/en-us/xamarin/xamarin-forms/user-interface/controls/layouts) to add more elements. I am using `Grid`, because it's easy to size.

Images must be added to both projects:
- In iOS: drop them in _Resources_ folder.
- In Android: drop them in _Resources/drawable_ folder.

Then, we are going to add 3 `Image` tags in the main page, usually named like the project.

```xml
<Image Grid.Row="0" Grid.Column="1"
       Source="play.png"
       VerticalOptions="Center" HorizontalOptions="Center"
       Margin="10">
</Image>
```

In the example I use two Grids to encapsulate the images. As I recently said, it's easier for me to size things with `Grid`.

Now we are going to add `TapGestureRecognizer` to our images. This, as it names says, provides tap gesture recognition and events.

```xml
<Image ...>
    <Image.GestureRecognizers>
        <TapGestureRecognizer Tapped="Play_tapped" />
    </Image.GestureRecognizers>
</Image>
```

Finally, we must implement these callbacks addded to each image. For a while, we are just going to change `IsVisible` properties of the images. 

To do this we must set `x:Name` to the elements we want to show or hide:

```xml
<Grid x:Name="Play">
    <!-- Column and row definitions -->
    <!-- And some content -->
</Grid>
```

And implement the callbacks:

```csharp
private void Play_tapped(object sender, EventArgs e)
{
    Play.IsVisible = false;
    PauseStop.IsVisible = true;
}
```

#### Extra

In the new iPhone X we have to keep some area safe. Our firend Xamarin provides us a method to do this. Let's add it in the _MainPage.xaml.cs_.

```csharp
using Xamarin.Forms.PlatformConfiguration.iOSSpecific;
//...
public StreamingExamplePage()
{
    InitializeComponent();
    On<Xamarin.Forms.PlatformConfiguration.iOS>().SetUseSafeArea(true);
}
```

### 3. Create a `ViewModel` 

{% include commit.html commit="https://github.com/ilanolkies/XamarinRadioStreamingExample/commit/9ab05bc08270fe00a85eca418c8408f714277d06" %}

> <a href="{{ site.baseurl }}/glossary#viewmodel">Glossary</a> for `ViewModel` definition.

All the view logic will be implemented in our `ViewModel`. To create it, add a new class to somewhere in the project. For big projects I use a folder named _ViewModels_, but for this example let's just drop it in the project main folder. I called it `StremingViewModel`.

Now we are going to link our view to the new view model. 

```csharp
private StreamingViewModel ViewModel { get { return (StreamingViewModel)this.BindingContext; } }

public StreamingExamplePage()
{
    //...
    BindingContext = new StreamingViewModel();
}
```

I always creat ViewModel property to avoid casting in each call.

In the view model we are going to implement a _IsPlaying_ property and the three actions:

```csharp
public class StreamingViewModel
{
    public bool IsPlaying { get; set; } = false;

    public void Play()
    {
        IsPlaying = true;
    }
    //Pause() and Stop()
}
```

But this is still useless... Jump to the next step!

### 4. Data Binding to change icons

{% include commit.html commit="https://github.com/ilanolkies/XamarinRadioStreamingExample/commit/7c53084ed3a20fd14b1397c6a279fcc057154c84" %}

> <a href="{{ site.baseurl }}/glossary#data-binding">Glossary</a> for **Data Binding** definition.

We are going to use **Data Binding** with the `IsPLaying` property. 

This step is devided in some mini steps:
1. Inherit view model from `INotifyPropertyChanged`.
2. Invoke `NotifyPropertyChanged()`.
3. Bind properties in the view.

So let's go!
1. First of all we must inherit the view modelfrom `INotifyPropertyChanged`. As name says, this interface is used to notify that a property value has changed. Using it can be devided in 2 steps:

```csharp
using System.ComponentModel;
using System.Runtime.CompilerServices;
//namespace...
public class StreamingViewModel : INotifyPropertyChanged
{
    // INotifyPropertyChanged implementation
    public event PropertyChangedEventHandler PropertyChanged;
    protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
    //...
}
```

2. We are going to call `NotifyPropertyChanged()` from the property setter:

```csharp
public bool DisplayPlay { get => !isPlaying; }
public bool DisplayPauseStop { get => isPlaying; }
        
bool isPlaying;
bool IsPlaying
{
    get => isPlaying;
    set
    {
        isPlaying = value;
        OnPropertyChanged("DisplayPlay");
        OnPropertyChanged("DisplayPauseStop");
    }
}
```

3. And now we must _connect_ all this to our view:

```xml
<Grid IsVisible="{Binding DisplayPlay}" ...>
    <!-- Play button -->
</Grid>
```

### 5. Dependency injection for streaming

{% include commit.html commit="https://github.com/ilanolkies/XamarinRadioStreamingExample/commit/f304be0708af39936c8a2e103d7b98b473db29da" %}

> <a href="{{ site.baseurl }}/glossary#dependency-injection">Glossary</a> for **Dependency Injection** definition.

#### Create interface
Create an interface in the project. I'll drop it in the project folder and call it `IStreaming`.

```csharp
public interface IStreaming
{
    void Play();
    void Pause();
    void Stop();
}
```

We are going to use this interface as a Dependency Injection. This means we are going to implement it separately in each plataform: iOS and Android.

```csharp
using Xamarin.Forms;
// All your stuff...
// public void Play()
{
    DependencyService.Get<IStreaming>().Play();
    IsPlaying = true;
}
```

> Note: you can't run until you implement the injection.
 
Now the most important and interesting part!

#### Implementation in iOS

Just 3 steps:
1. Implement `IStreaming` using native `AVFoundation`
2. Allow streaming domain in `Info.plist`.
3. Allow background audio

So here we go
1. The Foundation framework provides a base layer of functionality for apps and frameworks, including data storage and persistence, text processing, date and time calculations, sorting and filtering, and networking. Xamarin has an implementation of this framework!

```csharp
using System;
using StreamingExample;
using StreamingExample.iOS;
using Xamarin.Forms;
using AVFoundation;
using Foundation;

[assembly: Dependency(typeof(StreamingService))]
namespace StreamingExample.iOS
{
	public class StreamingService : IStreaming
	{
		AVPlayer player;
		bool isPrepared;
		string dataSource = "http://syour.domain.com/stream";

        public void Play()
        {
			AVAudioSession.SharedInstance().SetCategory(AVAudioSessionCategory.Playback);
			if (!isPrepared || player == null)
                player = AVPlayer.FromUrl(NSUrl.FromString(dataSource));

			isPrepared = true;
            player.Play();
        }

		public void Pause()
		{
            player.Pause();
		}
      
		public void Stop()
		{
            player.Dispose();
            isPrepared = false;
		}
	}
}
```

> Obviously, change your.domain.com for your domain.
> 
2. Now we must allow the URL, is just marking it as secure. In _Info.plist_ file in the iOS project add this key:

```xml
<dict>
    <key>NSExceptionDomains</key>
	<dict>
		<key>your.domain.com</key>
		<dict>
			<key>NSIncludesSubdomains</key>
			<true/>
			<key>NSTemporaryExceptionAllowsInsecureHTTPLoads</key>
			<true/>
			<key>NSTemporaryExceptionMinimumTLSVersion</key>
			<string>TLSv1.1</string>
		</dict>
	</dict>
</dict>
```

```
[Dictionary] App Transport Security Settings 
    [Dictionary] Exception Domains 
        [Dictionary] your.domain.com 
                        [Boolean] NSIncludesSubdomains -> True
                        [Boolean] NSTemporaryExceptionAllowsInsecureHTTPLoads -> YES
                        [String] NSTemporaryExceptionMinimumTLSVersion -> TLSv1.1
```

3. Finally, we want to listen to our radio while the app is in background. We are going to add this to _Info.oplist_.

```
<array>
	<string>audio</string>
</array>
```

```
[Array] Required background modes
    [String] App plays audio or streams audio/video using AirPlay
```

> Now you can run iOS project. 

#### Implementation in Android

It is quite simmilar to iOS, but we are going to use native `Android.Media`.
1. First we implement `IStreaming`

```chsarp
using RadioZonica.Interfaces;
using Android.Media;
using RadioZonica.Droid;
using Xamarin.Forms;

[assembly: Dependency(typeof(StreamingService))]
namespace RadioZonica.Droid
{
    public class StreamingService : IStreaming
    {
        MediaPlayer player;
        string dataSource = "rtsp://your.domain.com/stream.stream";

        bool IsPrepared = false;

        public void Play()
        {
            if (!IsPrepared)
            {
                if (player == null)
                    player = new MediaPlayer();
                else
                    player.Reset();

                player.SetDataSource(dataSource);
                player.PrepareAsync();
            }

            player.Prepared += (sender, args) =>
            {
                player.Start();
                IsPrepared = true;
            };
        }

        public void Pause()
        {
            player.Pause();
        }

        public void Stop()
        {
            player.Stop();
            IsPrepared = false;
        }
    }
}
```

2. Now we must allow some stuff in `AndroidManifest`. Add:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.WAKE_LOCK" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

**We have a radio player in Android and iOS!**

## Summary

1. Creat a blank Xamarin.Forms.
2. Add some images to the UI for play, pause and stop actions.
3. Implement `TapGestureRecognizer` to hide and show the images when tapped.
4. Add a `ViewModel` to manage logic. 
5. Set the `ViewModel` as the `BindingContext` of the view.
6. Listen binded display properties.
7. Add interface to manage streaming natively.
8. Implement interface in each device.
9. Call the interface implementations from view model as a Dependency Injection using `DependencyService.Get`.
