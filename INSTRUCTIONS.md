# Welcome to Foundations Orbit Online Trial

*Estimated time: 30 minutes*

In this tutorial we will go through an example of what Data Science teams and business managers need to do to manage machine learning models in a production environment. We will go through this trial in a gamified setting where you will be in control of what actions to take with the ultimate goal of solving a business problem.

We’re providing you with a fully-managed environment so you can focus on understanding and solving the challenges associated with hosting live models. This trial environment provides you with
* An in-browser Python IDE with popular data science & ML packages pre-installed
* The Foundations Orbit GUI 
* A tutorial with example code & data
* A simulated production environment
* Free cloud compute

## Step 1 of 9: Introduction to the problem

Let’s imagine you work at a meal-kit company, called **Hello, Food**. The business model is to prepare & deliver the ingredients for meals every week to subscribed customers for them to cook themselves. 

<placeholder for log>
  
**Hello, Food**'s revenues are falling as customer attrition has overtaken new subscriptions. In an attempt to retain customers, the company has decided to earmark some money to start a retention initiative by sending special offers to a subset of the customer base.

**You are in charge of this initiative! Good luck!**

Here are some facts about the business:
* Revenue per customer: $xxx per month
* Number of customers (as of the start of this trial): xxx
* Monthly growth rate: xxx% 
* Monthly attrition rate (as of the start of this trial): xxx%
* Special offer capacity&ast: xxx%

&ast The company has budget to send special offer to 10% of customers each month. For simplicity, let’s assume:
* If a customer wants to churn and receives an offer before they actually do, their likelihood of churn will significantly reduce
* If a customer has no intention to churn but receives an offer, they will still get the benefits of the special offer. However, this would be a waste of the retention budget

4 months ago, you and your team decided to develop a machine learning model to **predict which customers are likely to churn so that they can be targeted for special offers.** The ultimate measure of success and business metric is **monthly revenue** ($300 x number of customers that month). 

Now the model is ready to be deployed and all production systems are wired up. You are getting ready to deploy the model and hopefully it will have a positive impact on the business: **lower churn, more revenue**

## Step 2 of 9: Introduction to the sample solution code



