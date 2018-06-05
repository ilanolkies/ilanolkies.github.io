---
layout: post
title: Xamarin with Google Analytics
author: Ilan Olkies
category: Xamarin
tags: xamarin mobile ios android googleanalytics firebase google analytics
permalink: /post/:title
image: /img/xamarin_analytics/front.jpg
---

Our goal is to get closer to users and provide them the best application. We need to know what pages they prefer to enter, which ads they mostly click on, at what time and where they open our app, how they move within the app features... the more data we can compile, the better is the product we can offer. Google Analytics is a free web and mobile analytics tool offered by Google to help us analyze our traffic. In this Xamarin.Forms tutorial we are going to connect our app to Google Analytics service.

![front]({{ site.url }}/img/xamarin_analytics/front.jpg)

## Steps
1. Create a Firebase project.
2. Create a simple application.
3. Track users oppening each app.
4. Taking advantage of Google Analytics coming soon...

## Ingredietns
- [Visual Studio](https://www.visualstudio.com) updated.
- [Google account](https://accounts.google.com/signup).
- [Google Analytics](https://analytics.google.com/analytics/web/).
- [Firebase Analytics](console.firebase.google.com).

> [Google Analytics for Firebase](https://firebase.google.com/docs/analytics/) is a free app measurement solution that provides insight on app usage and user engagement. At the heart of Firebase is Google Analytics for Firebase, a free and unlimited analytics solution. Analytics integrates across Firebase features.

## Code!

{% include repo.html repo="https://github.com/ilanolkies/XamarinGAExample" %}

### 1. Create a Firebase Project
Simple: open [Firebase Console](https://console.firebase.google.com) and create a new project (or use an existing one).

**Why Firebase?** Google Analytics provide mobile app solutions across Firebase features.

### 2. Create simple app
{% include commit.html commit="https://github.com/ilanolkies/XamarinGAExample/commit/ff0e0f68fec259d029f8ab77f1733ab1e76a1846" %}

I created a simple **Xamarin.Forms** app using a `TabbedPage` and a `Label`. Of course, you can use your own project.

### 3. Track your apps
We must implement the Firebase instance in each device, so this step is devided in two substeps. We are just going to track app opens.

> We are not going to use any `DependencyInjection`.

#### 3.1. Android
We have our Xamarin.Forms project, and our Firebase project. Also we have an Android app. Let's start creating the **app instance in Firebase**.

- If you are using a new Firebase project, just click on _Add Firebase to your Android app_.
- Otherwise, go to _Project Overivew_ and click on _Add another app_. Add an Android app.

Now we are going to follow Firebase steps.

1. **Complete with your app data**. 
	
	The package name can be found in `AndroidManifest`. The SHA-1 can be get following [this guide](https://docs.microsoft.com/en-us/xamarin/android/deploy-test/signing/keystore-signature?tabs=vswin).

2. **Download `google-services.json`**. This file is going to be used to configure the Firebase tracking.

	Add the configuration file to the Android project: move the file into the Xamarin project, in the Android app main folder. This file must be compiled as a `GoogleServiseJson`. Right click in the file (in Visual Studio) and open the _Build Action_ menu. 

	<img src="{{ site.url }}/img/xamarin_analytics/android_compile_reference.png" alt="Andorid compile reference" class="zoom-image" />

	If `GoogleServiseJson` option apperas, just click it; otherwise do the following:

	Right click in Android project and reveal in folder. Open Android `.Android.csproj` with any text editor.

	Add this to csproj `Project` tag. You can follow this [reference](https://github.com/ilanolkies/XamarinGAExample/commit/5dd09c2596a1028efe1a092168505492dc48b325#diff-f1110251cb5c00ed78619a7e5f212072R100).

	```xml
	<ItemGroup>
	    <GoogleServicesJson Include="google-services.json" />
	</ItemGroup>
	```

	Then remove the _non compiled_ include of the file. Also follow the [reference](https://github.com/ilanolkies/XamarinGAExample/commit/f52360629cbff00961e52abfc114e6275f81bf2f#diff-f1110251cb5c00ed78619a7e5f212072L70):

	```xml
	<None Include="google-services.json" />
	```

	Now clean and rebuild.

3. **Instance Firebase in Xamarin project**. {% include commit.html commit="https://github.com/ilanolkies/XamarinGAExample/commit/5dd09c2596a1028efe1a092168505492dc48b325" %}

    1. **Add Firebase SDK**: right click in the Android Package folder. The _Add a Google Play service..._ Add Firebase.Analytics package. {% include commit.html commit="https://github.com/ilanolkies/XamarinGAExample/commit/161b9a3f716a932419fd3ee9c6dcdc57f96f2035" %}

	    I always get this error when compiling:

	    ```
	    Java.Lang.NoClassDefFoundError
	        Message: Failed resolution of: Lcom/google/android/gms/R$string;
	    ```

	    I just clean and rebuild and it starts working again...

	    > I created an [issue](https://github.com/xamarin/GooglePlayServicesComponents/issues/117) in GooglePlayServicesComponents on Xamarin github. If you get the same error, please react and comment.

    2. Instance Firebase Analytics in `MainActivity.cs`

    ```csharp
    protected override void OnCreate(Bundle bundle)
    {
        TabLayoutResource = Resource.Layout.Tabbar;
        ToolbarResource = Resource.Layout.Toolbar;

        firebaseAnalytics = FirebaseAnalytics.GetInstance(this);

        base.OnCreate(bundle);

        global::Xamarin.Forms.Forms.Init(this, bundle);
        LoadApplication(new App());
    }
    ```

4. **Verify it's working!** Clean, rebuild and run!

#### 3.2. iOS

{% include commit.html commit="https://github.com/ilanolkies/XamarinGAExample/commit/f4f297fc3a8fae2536979c58699f872fac595af5" %}

As in Android, create  the app instance in Firebase. Then follow the steps:

1. **Complete with the app data**. The bundle ID is found in `Info.plist` and the AppStore ID is found in Itunes Connect after creating the app.

2. **Download `GoogleService-Info.plist`**. This will be the configuration file.

    1. Edit the `.plist` file (I use XCode, but any editor is OK), set _IS_ANALYTICS_ENABLED_ property _true_.

		![]({{ site.url }}/img/xamarin_analytics/analytics_enabled.png)
    
    2. Copy the file in the main iOS project folder.
    
    3. Right click in the file and Set _BuildAction_ to _BundleResource_.
    
3. Add `Xamarin.Firebase.iOS.Analytics` Nuget Package. Some errors will appear, you must solve them adding an _mtouch_ argument: `--registrar:static` in project options. To do this open project options (double clicking the project), add the argument, and click OK.

	![]({{ site.url }}/img/xamarin_analytics/mtouch.png)

	Important: this must be done for each compiling configuration!

4. Instance Analytics in `AppDelegate.cs`

	```csharp
	public override bool FinishedLaunching(UIApplication app, NSDictionary options)
	{
	    global::Xamarin.Forms.Forms.Init();
	    LoadApplication(new App());

	    Firebase.Core.App.Configure();
	    Firebase.Analytics.Analytics.LogEvent("app_open", null);

	    return base.FinishedLaunching(app, options);
	}
	```

	> We are logging an event because the package is not working anything without an event raising. I also reported an [issue](https://github.com/xamarin/GoogleApisForiOSComponents/issues/156) about this.

5. **Verify your app!** Clean, rebuild, and run!

### 4. Connect Firebase with Google Analytics

1. Open [Google Analytics](https://analytics.google.com).
2. Open _Admin_ window.
3. Create an account (or choose an existing one).
4. Click in _+ Create property_.
5. What would you like to track? A Mobile app! Se
6. Connect to Firebase: select an app instance.
7. Click in _Connect app_
8. Everything ready! The app is tracking! Open the recently created view in top left corner and whatch the dashboard.

## It's all?

No! We are not taking advantage of Google Analytics at all... In the next tutorials I will explain how to get more and more information about our users!
