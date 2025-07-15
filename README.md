# Automation

## Step 0: Preparing the Assignment File

It could either be a static file (.csv) to be updated later, or a file on the Cloud (such as Google Sheet). It should at least have a column "Paper ID".

## Step 1: Issues Initialization

There are mainly two pathways to achieve the issue initization on this repo, including update .csv file (push) and update continuously on Google Sheet. The automation is mainly achieved through Python scripts and Github Action.

#### Option 1: Upload the data file (.csv)



#### Option 2: Update the data on Google Sheet

Extra steps needed: 1. Set up the GOOGLE SHEET ID Secrte Variable

## Step 2: Trigger-Action Mapping

- Ready to Code: When the paper is ready, it will show this default value "Ready to Code", accompanied with a Paper_Stages_Stage 1 Pending. 
- Supervisor Check
- Done
- On hold
- Remove from Pilot

- **[Trigger]** When a coder submit a form for the Paper (Paper ID) at the particular stage (i.e.,Stage 1), **[Action]** move to Stage 1 Coded.
- **[Trigger]** When a supervisor review and submit a form for the Paper (Paper ID, sup_survey = 1) , **[Action]** move to Stage 1 Reviewed.

## Step 3: Demo Testing and Feature Iteration

## Step 4: Deployment




