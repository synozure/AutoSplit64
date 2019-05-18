<h1 align="center"> AutoSplit64 </h1><br>
<p align="center">
  <a href="https://gitpoint.co/">
    <img alt="SM64" title="SM64" src="https://imgur.com/OUFqFx9.png" width="168">
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
  - [Star count won't update](#star-count-wont-update)
  - [Timer won't automatically reset](#timer-wont-automatically-reset)
  - [The star count is detected, but the timer won't split](#the-star-count-is-detected-but-the-timer-wont-split)
  - [Timer won't split on fade-ins](#timer-wont-split-on-fade-ins)
- [Credit](#credit)
- [Contact](#contact)
- [Author](#release)

## Introduction
Inspired by Gerardo Cervantes's [Star Classifier](https://github.com/gerardocervantes8/Star-Classifier-For-Mario-64), AutoSplit64 saves your fingers from getting athritis by splitting for you. *

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
* Automatically convert LiveSplit .lss files to AutoSplit64 routes


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

<p>
  <a href="https://gitpoint.co/">
    <img alt="SM64" title="SM64" src="https://i.imgur.com/f56xwll.png" width="750">
  </a>
</p>

### Game Capture
To be able to run correctly, we must first let AutoSplit64 know where to capture.

Make sure you have your capture software open (i.e., AmaRecTV), then open the Capture Editor (`Right-Click -> Edit Coordinates`):
<p>
  <a href="https://gitpoint.co/">
    <img alt="SM64" title="SM64" src="https://i.imgur.com/Zhf4qjc.png" width="1200">
  </a>
</p>

Select the correct process from the `Process` drop-down and position the `Game Region` selector as shown. Ensure you are as accurate as possible for best results.

When finished, press `Apply` to save changes.

****NOTE:****<br/>
If you are using a correctly configured version of AmaRecTV as shown (with windows size at 100% `right-click AmaRecTV -> 100%`), the default settings should already be set appropriately.

## Troubleshooting
Here you can find a list of common issues and potential fixes.

#### Star count won't update
* Disable any software altering the colours of your screen
* Disable any additional colour settings on your capture (i.e. saturation)
* Ensure the video capture is of a reasonable resolution (640x480 recommended)
* Check your capture coordinates are configured correctly in the capture editor

#### Timer won't automatically reset
* Refer to Star count won't update
* Use the Reset Template tool to generate a custom reset template image

#### The star count is detected, but the timer won't split
* Refer to Timer won't automatically reset
* Check your capture coordinates are configured correctly in the capture editor

#### Timer won't split on fade-ins
* If using an unpowered splitter, often the fade-in will be a light gray rather than white.
  * Lower the white threshold value in settings -> thresholds
  * Manually increase brightness of capture

## Credit
A big thanks to Gerardo Cervantes for open-sourcing his project!

## Contact
Feel free to contact me on discord at Synozure#9813 with any questions!<br/>
Bug reports may also be left on the issues page of this repository.

## Author
Synozure

