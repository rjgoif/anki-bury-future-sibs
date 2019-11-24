# anki-bury-future-sibs
> anki 2.1 add-on: buries new card siblings of any cards due in the next N days

# Why?
This add-on solves the problem with the following scenario:
You are studying your Anki deck and a new card pops up: 
> Q: What is the former name of Kazakhstan's capital city Nur-Sultan?  A: Astana

You study the card and learn it. Great. *But*, 9 days later, you get the review card:
> Q: What is the capital city of Kazakhstan? A: Nur-Sultan

You immediately recall the answer; the card goes from a 100 day interval to a 250 day interval. But there's a problem! The only reason you knew this answer was because of the new card that came up last week; without that reminder, you would have (appropriately) failed this card and re-learned it. 

If only the new card had been buried until *after* the old card was reviewed (and failed, then relearned). This add-on does just that: buries all new cards that have siblings due in the next N days.

This is ported from a personal (unreleased) Anki 2.0 add-on. Damien is dropping support for Anki 2.0 as of Jan 1, 2020. My hand is forced.

# Compatibility
Anki 2.1.15 tested. 
I suspect that this should work with the updated v2 experimental scheduler, but I have not tested this yet. If you are feeling brave, feel free to do so and report back to me.
Legacy version for Anki 2.0 is included here if you want to manually download and install it. Ankiweb support for 2.0 ceases on Jan 1, 2020 so you can only find the legacy version here.

# Default config values
These can be changed in the config file:
- ahead: how many days ahead do you want to look? Default 21. Anki natively sets this to 0. You can go negative if for some reason you want to only consider overdue cards.
- onStartup: future functionality, too bug-ridden for the initial release. Eventually will allow you to have the add-on run automatically when you first open Anki each day.
- shortcut: keyboard shortcut if you don't want to use the menu option (which appears under Tools). 

# Changelog:
- v2.1.001 initial port from my personal (unreleased) Anki 2.0 add-on. onStartup disabled. 
