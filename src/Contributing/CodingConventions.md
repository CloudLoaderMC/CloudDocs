<!--
Coding Conventions
-->

# Coding Conventions

Prerequisites: Eclipse {or IntelliJ} (3.7 or better is probably good), Git (any version, must be on system PATH))

1. Fork the CloudLoader repository
2. Clone your repository
3. Run `gradlew setup`.
4. Find anywhere you want for your IDE workspace. 
5. Import projects/Clean into your workspace
6. Import projects/Forge into your workspace

- Make sure you run and test your changes
- Run `gradlew genPatches` (in the Cloud root) to generate patch files for Minecraft base classes
- Sign [Contributor License Agreement](https://cla-assistant.io/CloudLoaderMC/CloudLoader)
- Submit a pull request. Explain as much as you did.

### Tips
- Take your time. Make sure your code does what it's supposed to do and does it well. Your PR probably won't be accepted if it doesn't cover all the uses
- Indent your code properly, and follow the conventions (take a look at other classes and read the code before editing). Space instead of tabs, open braces on a new line, etc. [ONLY IF IT IS A NEW CLASS NOT IF IT IS A PATCH TO A MINECRAFT CLASS](https://docs.cloudloader.org/Contributing/CodingConventions.md#conventions-for-coding-patches-for-a-minecraft-class-javapatch). [Here](https://github.com/ForgeEssentials/ForgeEssentials/tree/1.12.2/develop/misc/)'re the IDEs formatters available if you want it.
- To update your repo to latest code from the official repository:
  1. If it's the first time, add a remote for the official repo (`git remote add upstream https://github.com/CloudLoaderMC/CloudLoader`)
  2. Get the updates (`git fetch upstream`), and make sure you're on master (`git checkout 1.19.x`)
  3. If you don't want to rewrite your history (e.g. others have cloned your repository), do a merge (`git merge upstream/1.19.x`). **For keeping pull requests as clean as possible, do a rebase** (`git rebase upstream/1.15.x`). Git may reject your push the first time after each rebase and you'll have to do `git push -f origin master` (or `git push origin 1.15.x --force`).

### Conventions for coding patches for a Minecraft-class (`.java.patch`)
This section applies to the `ClassName.java.patch` section of your contributions.
Whenever a new update of Minecraft is released, these patches are applied to the original code provided by Mojang. To increase compatibility please keep the following conventions:

#### While coding:
- Prevent to add extra spaces/line breaks, even when there are already existing ones in the code between statements. Below is an example that comes from `net.minecraft.entity.item.EntityItem#attackEntityFrom(DamageSource, float)`:
```java
//snip
this.setBeenAttacked();
this.health = (int)((float)this.health - p_70097_2_);

if (this.health <= 0)
{
    this.setDead();
}

return false;
//snip
```
Lets say we add an `if`-statement between `this.setBeenAttacked();` and `this.health = (int)((float)this.health - p_70097_2_);`. It seems that `if`-statements get extra spaces/line breaks in the original code. However, when contributing to a `java.patch`-file you should always try to keep the changes as minimal as possible.
So, don't do:
```java
//snip
this.setBeenAttacked();
++
++  if(isCondition) return false;
++
this.health = (int)((float)this.health - p_70097_2_);

if (this.health <= 0)
{
    this.setDead();
}

return false;
//snip
```
But do:
```java
//snip
this.setBeenAttacked();
++ if(isCondition) return false;
this.health = (int)((float)this.health - p_70097_2_);

if (this.health <= 0)
{
    this.setDead();
}

return false;
//snip
```

- In spirit of the previous point: prevent to add more lines than necessary. If you can reduce your statement to one single line, please do so.
Example here is an `if`-statement that could be written as follows to improve readability:
```java
if((float)this.field_70291_e - p_70097_2_ <= 0.0F)
{
    if(net.minecraftforge.common.ForgeHooks.onItemDeath(this, p_70097_1_))
    {
        return false;
    }
}
```
However, to keep changes to `.java.patch`-files as minimal as possible. Try to write that statement to one single line:
```java
if((float)this.field_70291_e - p_70097_2_ <= 0.0F && net.minecraftforge.common.ForgeHooks.onItemDeath(this, p_70097_1_)) return false;
```
- Prevent using imports and try using full qualifications in the code. Using imports will generate extra lines in patch-files which can be prevented. Imports that are already in the file are not your concern. Example below:
```java
//snip
import net.minecraft.otherimports
import net.minecraftforge.event.GenericEvent
import net.minecraftforge.otherimports
//snip
        if (isCondition) MinecraftForge.EVENT_BUS.post(new GenericEvent());
//snip
```
Instead try to code it as:
```java
//snip
import net.minecraft.otherimports
import net.minecraftforge.otherimports
//snip
        if (isCondition) MinecraftForge.EVENT_BUS.post(new net.minecraftforge.event.GenericEvent());
//snip
```
Sidenote: The previous example can be improved further. As FML/Forge, and Cloud as extension, is trying to move away from imports try to use `net.minecraftforge.common.MinecraftForge` even when an existing import is already there. 
An even better way is to add a function in `net.minecraftforge.event.EventFactory` or `net.minecraftforge.common.ForgeHooks` and use the full qualification function names.

#### Before `gradlew genPatches` & Committing
Before committing, check if your IDE hasn't put in extra spaces/line breaks in the import section of your java-file. 
Eclipse tend to reorganize the imports to improve readability and will cause extra spaces/line breaks to appear in the `.java.patch`-files. Review your patches (`ClassName.java.patch`) and the diff-states of your uncommitted changes on these patches for extra `++`'s or `+ +`'s. This means an extra space/line break has been added.
Keep in mind that the original `.java.patch`-file never add extra spaces/break lines in between imports.
