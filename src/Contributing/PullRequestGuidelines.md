<!--
Pull Request Guidelines
-->

# Pull Request Guidelines

Cloud aims to support as many mod loaders as possible, so sometimes simple things slip through the cracks causing some mods to be incompatible.
When someone runs into something like that, or maybe they just want to add a new loader, they can make a change to Cloud to support it, and submit that change as a Pull Request on GitHub.

To make the best use of both your and the Cloud team's time, it is recommended to follow some rough guidelines when preparing a Pull Request. The following points are the most important aspects to keep in mind when it comes to writing a good Pull Request.

What Exactly is Cloud?
----------------------

At a high level, Cloud is a mod compatibility layer on top of Minecraft.
Early mods edited Minecraft's code directly (like coremods do now), but they ran into conflicts with each other when they edited the same things. They also ran into issues when one mod changed behavior in ways that the other mods could not anticipate (like coremods do now), causing mysterious issues and lots of headaches.

By using something like Cloud, mods can centralize common changes and avoid conflicts.

When writing a good Cloud Pull Request, you also have to know what Cloud is at a lower level.
There are two main types of code in Cloud: Minecraft patches, and Cloud code.

Patches
-------

Patches are applied as direct changes to Minecraft's source code, and aim to be as minimal as possible.
Every time Minecraft code changes, all the Cloud patches need to be looked over carefully and applied correctly to the new code.
This means that large patches that change lots of things are difficult to maintain, so Cloud aims to avoid those and keep patches as small as possible.
In addition to making sure the code makes sense, reviews for patches will focus on minimizing the size.

There are many strategies to make small patches, and reviews will often point out better methods to do things.
Cloud patches often insert a single line that fires an event or a code hook, which affects the code after it if the event meets some condition.
This allows most of the code to exist outside of the patch, which keeps the patch small and simple.

For more detailed information about creating patches, [see the GitHub wiki][patches].

Cloud Code
----------

Aside from the patches, Cloud code is just normal Java code. It can be event code, compatibility features, or anything else that is not directly editing Minecraft code.
When Minecraft updates, Cloud code has to update just like everything else. However, it is much easier because it is not directly entangled in the Minecraft code.

Because this code stands on its own, there is no size restriction like there is with the patches.

In addition to making sure the code makes sense, reviews will focus on making the code clean: with proper formatting and Java documentation.

Explain Yourself
----------------

All Pull Requests need to answer the question: why is this necessary?
Any code added to Cloud needs to be maintained, and more code means more potential for bugs, so solid justification is needed for adding code.

A common Pull Request issue is offering no explanation, or giving cryptic examples for how the Pull Request might theoretically be used.
This only delays the Pull Request process.
A clear explanation for the general case is good, but also give a concrete example of how your mod needs this Pull Request.

Sometimes there is better way to do what you wanted, or a way to do it without a Pull Request at all. Code changes can not be accepted until those possibilities have been completely ruled out.

Show that it Works
------------------

The code you submit to Cloud should work perfectly, and it is up to you to convince the reviewers that it does.

One of the best ways to do that is to add an example mod or JUnit test to Cloud that makes use of your new code and shows it working.

To set up and run a Cloud Environment with the example mods, see [this guide][cloudenv].

Be Patient, Civil, and Empathetic
--------------------------------

When submitting Pull Requests, you will often have to survive code review and make several changes before it is the best Pull Request possible.
Keep in mind that code review is not judgement against you. Bugs in your code are not personal. Nobody is perfect, and that is why we are working together.

Negativity will not help. Threatening to give up on your Pull Request and write a coremod instead will just make people upset and make the modded ecosystem worse.
It is important that while working together you assume the best intentions of the people who are reviewing your Pull Request and not take things personally.

Review
------

If you do your best to understand the slow and perfectionistic nature of the Pull Request process, we will do our best to understand your point of view as well.

After your Pull Request has been reviewed and cleaned up to the best of everyone's ability, it will be marked for a final review by Lex, who has the final say on what is included in the project or not.

[patches]: https://docs.cloudmc.ml/PullRequestGuidelines.md#conventions-for-coding-patches-for-a-minecraft-class-javapatch
[cloudenv]: ./Contributing.md
