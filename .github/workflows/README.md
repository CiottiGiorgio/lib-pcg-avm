# Decision Record - Workflows
## Reusable Workflows
The steps involved in validating that the code is in good conditions and passes tests need to be shared across CI and CD workflows.
The shared code is captured in `./.github/workflows/validate-*.yml` files.

These steps are meant to be parameterized and reused by any arbitrary workflow that needs them.
We chose reusable workflows rather than actions because of their simplicity (even at the cost of some complexity which will be explained later).

## Skipped Workflows
Seen as this project is a monorepo for four implementations of the same library, it's natural that we may want to skip running CI and/or CD for projects that did not change.

### Skip Criterion
It would be natural to only run automatic workflows only in the event that files within some subprojects have changed.
This, however, leads to missing changes in other important parts of this repository (workflows, testing, etc.).

Instead, we consider that an implementation for language `X` changed if _anything_ changed ignoring other languages `Y, Z, etc`.
This allows us, for example, to run automatically testing for all languages if the tests themselves change.

We also want to ignore changes in linked clients since those live outside the related project and in the `unified-tests` project.

### Required Status Check
We want these validating steps to run successfully whenever we merge a PR.
We can achieve this through GitHub branch protection and selecting the name of the required workflows.
Unfortunately, GitHub refers to workflows that are skipped differently from workflows that are ran.
More info here: [link](https://github.com/orgs/community/discussions/72708)

### Skip Parameter
The decision to skip specific steps should be at the discretion of the caller workflow.
This is easy to do with the `if` clause when calling a reusable workflow.
Since this would change the name that shows up in the `Checks` tab, we pass a `skip` input to the reused workflow to signal if it should actually perform work or not.
