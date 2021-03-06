## ahead
How many days beyond today do you want Anki to consider due cards for which to bury siblings?
For example, entering 7 will bury all cards that are due any day on or before 7 days from now. Overdue cards are included in this search.

Default Anki behavior is days ahead=0, i.e., siblings of cards due today+0 days will be buried.

## newsAlwaysFirst
If true, the new cards will always be displayed first. Why not just set your real Anki settings to do this? Because sometimes I have to do reviews on iOS/web where thre are no add-ons. If this is the case, I want my new cards last so the siblings will at least be buried after I review any due cards. That way my new cards won't tip me off to my review card answers. Thus I have my deck set to "new cards last" but this add-on can override that when you can *prospectively * bury the new cards. Default is false because I doubt most users need this nuanced behavior.

## shortcut
Menu shortcut to trigger the add-on. Shift+B by default. Configurable in case some other add-on already uses this shortcut.

## onStartup
**Old functionality from of my old 2.0 add-on**. Disabled until I can port it to 2.1.
set to 1 if you want the add-on to run when Anki starts for the first time each day. 
***NOTE *** in Anki 2.0 this would sometimes cause a pop-up saying your collection was corrupt. *It was not actually corrupt, *but rather would throw the error if there were too many (~1000 or more) cards that met the search criterion. The temporary workaround was to start Anki without add-ons by holding shift when you booted the program for the first time that day. The bug would only occur on the first boot of the day. 