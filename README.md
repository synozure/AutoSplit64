<h1 align="center"> AutoSplit64 </h1><br>
<p align="center">
  <a href="https://gitpoint.co/">
    <img alt="SM64" title="SM64" src="https://imgur.com/B3eyq3A.png" width="168">
  </a>
</p>

## Table of Contents

- [Introduction](#introduction)
- [Release](#release)
- [Features](#features)
- [Quick Setup](#quick-setup)
  - [Interface](#interface)
  - [LiveSplit Server](#livesplit-server)
  - [Game Capture](#game-capture)
- [Troubleshooting](#troubleshooting)
- [Credit](#credit)
- [Contact](#contact)
- [Author](#release)

## Introduction
Inspired by Gerardo Cervantes's [Star Classifier](https://github.com/gerardocervantes8/Star-Classifier-For-Mario-64), AutoSplit 64 saves your fingers from getting athritis by splitting for you. *

AutoSplit64 is primarily designed for console use, however may still function for Emulator.
For details on proper emulator configuration see Giboss's [Setup Guide](https://goo.gl/PKGDn6).

For general Super Mario 64 questions please direct them toward the Super Mario 64 [discord](https://discord.gg/Xvk6AXQ).

\* You're playing Mario so your hands are going to be screwed anyway, sorry.

## Release
Version 0.1.0

## Features
* Automatically start/reset timer on console reset
* Split on fadeout/fadein at specified star count
* Split on DDD enter
* Split on final star grab
* Create custom routes with graphical interface
* Automatically convert LiveSplit .lss files to AutoSplit 64 routes


## Quick Setup
Download the latest release. Extract contents and run `AutoSplit64.exe`.

### Interface
Upon first run, you will encounter a blank interface:
<p>
  <a href="https://gitpoint.co/">
    <img alt="SM64" title="SM64" src="https://i.imgur.com/ca2CXc5.png" width="320">
  </a>
</p>

All windows and options are accessed via the right-click menu:

<p>
  <a href="https://gitpoint.co/">
    <img alt="SM64" title="SM64" src="https://i.imgur.com/GAfy9gR.png" width="320">
  </a>
</p>

### LiveSplit Server
AutoSplit64 communicates with LiveSplit via the LiveSplit Server component. 

Please download the latest version [here](https://github.com/LiveSplit/LiveSplit.Server).

### Game Capture
To be able to run correctly, we must let AutoSplit 64 know where to capture.

Make sure you have your capture software open (i.e., AmaRecTV), then open the Capture Editor (`Right-Click -> Edit Coordinates`):
<p>
  <a href="https://gitpoint.co/">
    <img alt="SM64" title="SM64" src="https://i.imgur.com/Zhf4qjc.png" width="1200">
  </a>
</p>

Select the correct process from the `Process` drop-down and position the `Game Region` selector as shown. Ensure you are as accurate as possible for best results.

When finished, press `Apply` to save changes.

****NOTE:****<br/>
If you are using a correctly configured version of AmaRecTV as shown (with windows size at 100% `Right-Click AmaRecTV -> 100%`), the default settings should already be set appropriately.

### Routes
We must let AutoSplit 64 know when we want splits to occur. This can be done by using the Route Editor (`Right-Click -> Edit Route`) to generate route files.

To create a route, an understanding of how splits occur is important. For a regular split it will trigger when the specified number of stars have been collected, and a set amount of fadeouts or fadeins have occurred after the star count was reached, or the last split occurred.

Every time a star is collected, or a split, undo or skip is triggered, the fadeout and fadein count are reset to 0. 
The Route Editor has been designed to look and function similar to the split editor found in LiveSplit, to make it as familiar as possible.

The easiest method of creating routes is to import your splits you use for LiveSplit. To do this, in the Route Editor, nagivate to `File -> Convert LSS`. Open the `.lss` file you use with LiveSplit. AutoSplit 64 will attempt to fill in as many details as possible to simplify the route creation process, however it is important you check each split to make sure it is correct.

Some of the auto-filled parameters include:
* `Split Title`
* `Star Count` - If the split title contains a number (usually used to indicate star count), this will be copied to the `Star Count` field

## Troubleshooting
If you encounter any issues, please run through all steps below.

* Check capture coordinates are correct (`Right Click -> Edit Coordinates`)
* Ensure LiveSplit server is running (`Right Click LiveSplit -> Control -> Start Server')
* Check the correct route is loaded, and that the route file is accurate (i.e. correct star counts, fadeout/fadein counts)
* Generate reset templates (`Right Click -> Generate Reset Templates`)
* Make sure the captures colour settings (i.e. saturation) are default or close to default

## Credit
A big thanks to Gerardo Cervantes for open-sourcing his project!

## Contact
Feel free to contact me on discord at Synozure#9813 with any questions!<br/>
Bug reports may also be left on the issues page of this repository.

## Author
Synozure

