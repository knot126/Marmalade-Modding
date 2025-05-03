# Marmalade History and Resources

[Marmalade](https://en.wikipedia.org/wiki/Marmalade_(software)), formerly known as Airplay SDK, is a [write once run anywhere](https://en.wikipedia.org/wiki/Write_once,_run_anywhere) platform initially created by [Ideaworks](https://en.wikipedia.org/wiki/Ideaworks_Game_Studio) for early cell phone games, though was later used for many smartphone games.

## Notes

From [Book 1]:

> S3E is short for Segundo Embedded Execution Environment and this is the lowest
> layer of the Marmalade SDK. This naming convention was adopted by the SDK
> during its early days of development, and it remains to this day. As you will
> see later in this book, there are a great many APIs that are prefixed with
> this name.

## Run the SDK without a licence

1. Install the SDK like normal.
2. Try to activate using a junk key and email. (This might not be needed?)
3. Using the old iwlicense.exe, run the following command in the `s3e/bin` dir:

```cmd
iwlicense.exe --verbose --activate --key=12345
```

4. Install the [official patch to run without a licence server](https://web.archive.org/web/20180530031815/https://support.madewithmarmalade.jp/hc/en-us/articles/360001338068-Patch-for-perpetual-usage-without-license-server).
5. Done!

## Loader with debug symbols

The iOS version of the loader is shippped as a static library in `<sdk install dir>/s3e/loader/ios/<arch>/libs3e_debug.a` which contains complete debug symbols.

## Books

1. *[Marmalade SDK Mobile Game Development Essentials](https://www.packtpub.com/product/marmalade-sdk-mobile-game-development-essentials/9781849693363)* (2012, published by Packt)

## Downloads

* [Marmalade SDK 5.0.1](https://archive.org/download/marmalade-sdk-collection/marmalade-sdk-5.0.1-278131-windows.exe) ([Original URL](https://download.informer.com/win-1193091066-a2e8f115-616c152b-b3229e101a7e85d717-bb08c9772d03f392c-3404983886-1308944358/marmalade-sdk-5.0.1-278131-windows.exe))
* [Marmalade SDK 7.6.0](https://web.archive.org/web/20150315201813/https://developer.madewithmarmalade.com/downloads/7.6/7.6.0/marmalade-sdk-7.6.0-425675-windows.exe) ([MacOS version](https://web.archive.org/web/20150315204015/https://developer.madewithmarmalade.com/downloads/7.6/7.6.0/marmalade-sdk-7.6.0-425675-mac.dmg))
* [Marmalade SDK 8.6.0](https://archive.org/download/marmalade-sdk-collection/marmalade-sdk-8.6.0-480999-windows.exe) ([Original URL](https://soft.mydiv.net/win/dlfile311922_68b49-Marmalade-SDK.html/marmalade-sdk-8.6.0-480999-windows.exe))
* [Official patch to run without licence server](https://web.archive.org/web/20180530031815/https://support.madewithmarmalade.jp/hc/en-us/articles/360001338068-Patch-for-perpetual-usage-without-license-server)
* [Documentation for Marmalade 7.3.0 as a PDF](https://web.archive.org/web/20140806205727/http://docs.madewithmarmalade.com/download/attachments/917508/Marmalade_Documentation_730.pdf?version=2&modificationDate=1402329163000&api=v2)

## Other

* https://factorialcomplexity.com/blog/getting-started-with-marmalade-sdk/
* https://stackoverflow.com/questions/19984785/determine-if-android-apk-leverages-marmalade-sdk
