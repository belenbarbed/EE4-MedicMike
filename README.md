# EE4-PostBotPat
HCR Coursework 2018

<<<<<<< HEAD

Database Entries

### People

College ID (string?)
College Card ID (string?)
First Name (String)
Surname (string)
Email/Slack (string)
Department (string)

### Parcels

Parcel ID (int) (auto-increment)
Owner College ID (String?)
Address (string)
Parcel Location (int)
Arrival Date (Date) (Generated on arrival)
Arrival Time (Time) (Generated on arrival)
Notified (false)
Collection Date (Date) (default null)
Collection Time (Time) (default null)

=======
## Deadlines
- 1/11: Design Report
- 29/11: Individual Demo
- 13/12: Final Demo
- 20/12: Final Report

## Project Phases
- Phase 1: Can deal with medium sized packages, one person at a time, people only come when they have a package, printed labels. One package per person only.  
- Phase 2: Can have people arrive even if they don't have a package.
- Phase 3: Multiple packages per person allowed.
- Phase 4: Allow for more package sizes.

## Workflow
- New work (features, bug fixes etc.) begins life as an issue (e.g. implement time prediction for pick ups, fix mistaken identity bug).
- New code / assests are created in dev branches.
- A merge request is then opened to merge the dev branch into the integration branch.
- The integration branch is tested and evaluated.
- If testing is successful then the integration branch is merged into master and the issue is closed.
>>>>>>> origin/dev/owen
