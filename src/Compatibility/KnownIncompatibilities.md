<!--
Known Incompatibilities
-->

# Known Incompatibilities

Cloud is compatible with most mods, as long as:

1. They don't directly use a loader's own list of mods (*Fix In Progress*)
2. They aren't from one loader, use it's common tag namespace, and then expect the tags to be in another loader's common namespace (*Will Fix*)
3. They aren't a hybrid mod internally using a loader other than Forge but still use the event bus (*Will fix*)

Other than those few things, everything should work. If something doesn't, check if anyone has created an [issue](https://github.com/CloudLoaderMC/CloudLoader/issues) on it, and if not, create one.

---

**Other Pages:**

[Compatibility](./Compatibility.md)
<br>
[Mod-ID Aliases](./ModIDAliases.md)
