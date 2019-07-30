# Welcome to the Web Scraper Project
#### A few notes on getting started...

## Workflow:
We will be using the Git Flow Workflow. In this workflow, all code is committed to a `feature/feature-name` branch, reviewed, merged to `develop`, tested for `release` and then once a release is complete, merged to `master` for deployment. Find out more [here](https://guides.github.com/introduction/flow/) and [here.](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

```git
git checkout develop
git flow feature start my-feature
git commit -m "This is a change"
.
.
git commit -m "This is my last change for the feature"
git flow feature finish my-feature
```

## Issues:
The project backlog issues are tagged accordingly so they can be filtered out when viewing the issues page, as we do not have the GitHub Kanban Project board available.
When taking on a backlog item, remove the `Not Now/Backlog` label and assign the `NOW` label, then assign the issue yourself or the individual who will work on it.
**Backlog items should never be assigned without changing the tag and should never change the tag without assigning the item.** This can be critical to ensuring that everyone can see what is being worked on and what is not being worked on within the issues view.

