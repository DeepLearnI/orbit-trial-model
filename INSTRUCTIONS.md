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
* Special offer capacity\*: xxx%

\*The company has budget to send special offer to 10% of customers each month. For simplicity, let’s assume:
* If a customer wants to churn and receives an offer before they actually do, their likelihood of churn will significantly reduce
* If a customer has no intention to churn but receives an offer, they will still get the benefits of the special offer. However, this would be a waste of the retention budget

4 months ago, you and your team decided to develop a machine learning model to **predict which customers are likely to churn so that they can be targeted for special offers.** The ultimate measure of success and business metric is **monthly revenue** ($300 x number of customers that month). 

Now the model is ready to be deployed and all production systems are wired up. You are getting ready to deploy the model and hopefully it will have a positive impact on the business: **lower churn, more revenue**

## Step 2 of 9: Introduction to the sample solution code

The code written by Hello Food’s Data Scientists can be viewed on this editor. You can navigate to different files using the directory explorer to the left. 

At a high level, it includes some code to train the model, some code to use the model for inference, some code to evaluate the performance of the model. In the optional reading session below, we will go through different parts of the project code and explain what they do. If you skip this section. Just know that there’s some code that Hello, Food data scientists wrote to tackle this use case. 

Now, let’s run the training code to create the model. Please navigate to the terminal windows, located below, and type the following command followed by the ‘Enter’ key:
```bash
python train_driver.py
```
Once it completes, you can see in fitted_object/ folder that a new model was created as a result of the training, with the name model.pkl unless you change the code

<details>
  <summary>Optional reading</summary>

In the directory explorer, click on the project_code/ folder and open the model.py file in the editor. 

There are three functions in model.py: train, predict, and eval. Except for a couple of lines in eval function, there’s no Foundations Orbit feature so far.

The train function takes in three arguments, start and end dates your training period and a database key. The database key is only for the trial to identify the part of the data that has been allocated for you. Given these arguments, the train function fetches the data, processes them, trains a simple XGBoost model, and save the model to a specified location. 

The predict function takes in two arguments, the inference date and database key. Given the inference date, the function pulls from database the data it needs to run prediction for the specified date, then saves the predictions back to the database.

The eval function takes in two arguments. the evaluation date and database key. Given evaluation key, the function pulls from database the data it needs to compute metrics as of the evaluation date, computes the metrics, and use Foundations Orbit’s track_production_metrics to log and store the metrics.

You can also inspect the dataset on GCP storage bucket: xxxx
</details>


**There is no Orbit magic so far. These are the things that you normally do in a typical data science project, but simplified for illustration purpose.**

## Step 3 of 9: Monitoring model performance using Orbit

Now, we are ready to deploy the model into production, which we will show in the next section. However, one thing is still missing. As soon as we deploy this model into the simulated production environment, it will start being consumed by the production environment and having impacts on the Hello, Food’s business. **How can you track the performance metrics of your model over time, and be able to monitor them easily?**

With Orbit, this is as easy as adding a couple lines of code. Now, let’s add the following lines of code to the `eval(...)` function in `model.py` (after line xxx)

```python
  foundations.track_production_metrics("accuracy", {str(eval_date): accuracy})
  foundations.track_production_metrics("roc_auc", {str(eval_date): roc_auc})
  foundations.track_production_metrics("revenue", {str(eval_date): revenue})
  foundations.track_production_metrics("n_promos", {str(eval_date): n_promos})
  foundations.track_production_metrics("n_active_custs", {str(eval_date): n_active_custs})
```

## Step 4 of 9: Deploying the model

Now, let’s deploy the trained model to our simulated production environment. 

Foundations provides a standard format to seamlessly package machine learning models for production.

We've included a configuration file foundations_package_manifest.yaml which tells Foundations to serve the `predict(...)` function from `model.py`

Next, In the terminal, please enter this command then press ‘Enter’ key
```bash
foundations orbit serve start --project_name=orbit-trial --model_name=model-1 --project_directory=./ --env=scheduler
```
Foundations automatically package up the code and model and wraps it in REST API. Requests can be made to the entrypoints specified by the `foundations_package_manifest.yaml` file.

**Congratulations, you’ve deployed your churn model!**

## Step 5 of 9: Monitoring your model using Orbit GUI

Now, we need to start monitoring how well our model is performing on live data. 

In the real life situation, the following would happen on a monthly basis:
* Every month, the Operations team will get predictions from your model
  * I.e., a list of customers the model predicts to be at risk of churn
* Some actions are performed by the Operations team based on the predictions
  * I.e., actually sending out the special offer to the customers
* As the results, customer behaviours are impacted and captured as data
  * I.e., some customers leave/stay, reflected by their xxx in the database

We’ve created a simulated production environment to mimic what you would face in real life:
* Every 1 minute of the trial equates to 1 month in real life
* Every 1 minute (every month), the simulated environment:
  * Gets predictions from your model
  * Actions on the predictions 
  * Simulates outcome of the actions and updates the database

Now please go to the GUI using the other link that we shared with you (usually in the format of: `<xxxx>-<xxxx>.com/<xxxx>)`. Once you enter the GUI, you will see 1 project in the landing page. Clicking on that leads you into the project. Once you are in the project, you first click the (?) button, located on the top right corner, to go through a quick overview of the GUI.

After that, **keep an eye on the model performance over time, located in the Model Evaluation tab. We recommend that you come back here in a couple of minutes and go through the rest of this tutorial.**

## Step 6 of 9: The big problem

By now, you are probably beginning to see that your model performance is suffering. You can tell by going to Model Evaluation tab, which monitors your model performance in production over time.

**Question:** now that your model performance is decaying, revenue is dropping minute after minute (month as month in real life). What do you do?

**Here are three options you normally have in real-life**
1. If you are a Data Science guru, you roll up your sleeves and head to the IDE and do some investigation on the dataset. You are welcome to write some python code to identify & resolve the problem, and re-deploy your new model following the instructions in Step 2
2. If you are not technical, you can reach out to someone else to assist on the task. Is there a data scientist from your company that can spare the time from other initiatives to help you out?
3. You can email the original model developer at a.lu@dessa.com. He will fix the issue for you. He’s quite busy on his new projects, but he will try his best to get back to you in a couple of weeks

**Regardless of which option you choose, you need to act fast because your company is bleeding money now as you are reading this.**

There is a fourth option. You let Foundations Orbit help you identify & resolve the issue in a few steps in the next section.

## Step 7 of 9: The Orbit way

Machine learning models in production typically suffer from two types of issues: 

1. **Unexpected changes in production data.** IT and operations changes can lead to unexpected data anomalies capable of adversely affecting model performance. These changes aren’t tracked by traditional IT systems, which means that teams don’t notice them until it’s too late. For example, the team that maintains the databases might not know that your model is dependent on a particular column and decided to make changes to it, such as using a different value to encode something. Small changes like that could proliferate through various data systems and eventually leads to drastic changes by the time the data reach your models

2. **Population or concept drift:** Models are trained using historical data, but changes in customer behaviours and business operations happen over time, changing the underlying relationships between model input and output. In reality, models in production degrade in performance. It is only a matter of time before they become obsolete.

Luckily, with very little changes to our code, you can have the power to address these issues using Orbit.

Let’s start by adding these two lines of code to the `train(...)` function in `model.py`:
```python
  dc = DataContract("my_contract", x_train)
  dc.save(".")
```

Add these two lines of code to the `predict(...)` function in `model.py`:
```python
  dc = DataContract.load(".", "my_contract")
  dc.validate(x_train, inference_date)
```
In terminal, run 
```bash
python train_driver.py
```

Add these two lines of code to the end of `foundations_package_manifest.yaml`

```python
```

Then run this in terminal:
```bash
foundations orbit serve start --project_name=orbit-trial --model_name=model-2 --project_directory=./ --env=scheduler
```
