# Automation

This repo will contain the data files and Python codes necessary for automatic issue creation and progress tracking for the IDEAL project.

## Step 0: Preparing the Assignment File

It could either be a static file (.csv) to be updated later, or a file on the Cloud (such as Google Sheet). And it should at least have the column "Paper ID".

## Step 1: Issues Initialization

There are mainly two pathways to achieve the issue initization on this repo, including upload/update the .csv file (push) and update continuously on Google Sheet. The automation is mainly achieved through Python scripts and Github Action. It enables the detection of new data entry, after which a new issue will be created automatically (the frequency for auto update can be customized).

#### Option 1: Upload the data file (.csv)

For testing purposes, I have extracted a small sample from "Pilot Phase 2 - Stages 1-3 - data extraction and review - All Papers" (named as "test_sample_data.csv").

Click the Actions tab for this repo above, you'll be able to see the Action[XX]. 

#### Option 2: Update the data on Google Sheet

Extra steps needed: 1. Set up the GOOGLE SHEET ID Secrte Variable

## Step 2: Trigger-Action Mapping (More to be Added Later)

- **[Trigger]** When a coder submit a form for the Paper (Paper ID) at the particular stage (i.e.,Stage 1), **[Action]** move to Stage 1 Coded.
- **[Trigger]** When a supervisor review and submit a form for the Paper (Paper ID, sup_survey = 1) , **[Action]** move to Stage 1 Reviewed.

## Step 3: Demo Testing and Feature Iteration

## Step 4: Deployment




