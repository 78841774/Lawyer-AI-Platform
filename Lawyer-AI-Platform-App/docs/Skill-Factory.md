# Skill Factory

Skill Factory is the future operating layer for turning reviewed casework data into reusable Skills, Experience Packages, and evaluation rubrics.

## Current Status

As of v3.6-B, Skill Factory remains in analysis mode.

Current local audit results:

* Existing legacy Skill assets analyzed: 17.
* Existing SkillOpt dataset files analyzed: 19.
* Existing SkillOpt dataset items analyzed: 96.
* Existing SkillOpt output runs analyzed: 14.
* Skill Training main chain unchanged.

No new Skill was created.

No Experience Package was imported.

No Skill Registry record was published.

## Factory Inputs

Future Skill Factory inputs should come from reviewed packages, not raw legacy folders.

Input package categories:

* Dataset packages.
* Runtime rule packages.
* Prompt template packages.
* Report template packages.
* Evaluation rubric packages.
* Read-only reference packages.

## Factory Gates

Before an input can be used for training or publication, it must pass:

* Privacy review.
* Human curation review.
* Schema validation.
* Evaluation rubric completeness check.
* Source reference check.
* Legal safety review.

## v3.6-B Boundary

v3.6-B only adds the legacy analysis script and documentation.

It intentionally avoids:

* Training.
* Registry import.
* Package publication.
* LLM calls.
* Legacy script execution.
* Frontend changes.
