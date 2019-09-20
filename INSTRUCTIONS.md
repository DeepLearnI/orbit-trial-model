# Welcome to Foundations Orbit Online Trial

*Estimated time: 30 minutes*

In this tutorial we will go through an example of what Data Science teams need to do to manage machine learning models in production. We will go through this trial in a gamified setting where you will be in control of what actions to take with the ultimate goal of solving a business problem.

We’re providing you with a fully-managed environment so you can focus on understanding and solving the challenges associated with hosting live models. This trial environment provides you with
* An in-browser Python IDE with popular data science & ML packages pre-installed
* The Foundations Orbit GUI 
* A tutorial with example code & data
* A simulated production environment
* Free cloud compute

To complete this trial, you will need 3 things that you should have received from us:
* Your user_key
* Link to the online code editor
* Link to the Foundations Orbit GUI

## Step 1 of 9: Introduction to the problem

Let’s imagine you work at a meal-kit subscription company, called **Hello, Food**. The business model is to prepare & deliver the ingredients for meals every week to subscribed customers for them to cook themselves. 
  
**Hello, Food**'s revenues are falling as customer attrition has overtaken new subscriptions. In an attempt to retain customers, the company has decided to earmark some money to start a retention initiative by sending special offers to a subset of the customer base.

**You are in charge of this initiative! Good luck!**

<details>
  <summary>  Here are some facts about the business (click to expand, no need to memorize): </summary>

* Revenue per customer: $300 per month
* Number of customers (as of the start of this trial): 5000
* Monthly growth rate: 14% 
* Monthly attrition rate (as of the start of this trial): ~17%
* Special offer capacity: 10%. This means the company has budget to send special offer to 10% of customers each month. For simplicity, let’s assume:
  * If a customer wants to churn and receives an offer before they actually do, their churn likelihood will significantly reduce
  * If a customer has no intention to churn but receives an offer, they will still get the benefits of the special offer. However, this would be a waste of the retention budget
-------------------------------------------------------------------------------------------------------------------------
</details>

**Because the company only has limited resources to address retention, it is critical to predict correctly which customers are likely to churn**. 4 months ago, your team decided to develop a **machine learning model to predict which customers are likely to churn based on their recent behaviour so that they can be targeted for special offers.** Now the model is ready to be deployed and all production systems are wired up. You are getting ready to deploy the model and hopefully it will have a positive impact on the business: **lower churn, more revenue month over month** ($300 x number of active customers that month)

## Step 2 of 9: Introduction to the sample solution code

First, let's open the code editor on a browser using the link that we sent you. 

The code written by **Hello Food**’s Data Scientists can be viewed on this editor. You can navigate to different files using the directory explorer to the left. At a high level, the `model.py` file includes some code to train the model, some code to use the model for inference, and some code to calculate the performance of the model. There are three functions in `model.py`: `train`, `predict`, and `eval`. **There’s no Foundations Orbit feature in them right now.**

<details>
  <summary>Optional reading</summary>

The train function takes in two arguments: start and end dates of your training period. Given these arguments, the train function fetches the data, processes them, trains a simple random forest model, and saves the model to a specified location. 

The predict function takes in one argument: the inference data. Given the inference date, the function pulls from database the data it needs to run prediction for the specified date, then saves the predictions back to the database.

The eval function takes in one argument: the evaluation date. Given evaluation key, the function pulls from database the data it needs to compute metrics as of the evaluation date, computes the metrics, and use Foundations Orbit’s track_production_metrics to log and store the metrics.

-------------------------------------------------------------------------------------------------------------------------
</details>

Now, let’s run the training code to create the model. 

First, open `user_key.py` in the editor by clicking on the file in the directory explorer to the left. Replace `your_data_key_here` with your `user_key`. For example, if the `user_key` we assigned to you is `12.34.56.78`, then line 1 should be:
```python
data_key = "12.34.56.78"
```
_Note: the step above is only for the trial and has nothing to do with Orbit. This is to tell this trial to only access the dataset that has been allocated specifically for you._

Next, navigate to the terminal window by clicking **Terminal** at the top bar and **New Terminal Window**. Enter the following command, then press the ‘Enter’ key:
```bash
python train_driver.py
```
Once it completes, you can see in `fitted_objects/` folder that a new model was created as a result of the training, with the name `model.pkl` unless you change the code

**There is no Orbit magic so far. These are the things that you normally do in a typical data science project, but simplified for illustration purpose.**

## Step 3 of 9: Monitoring model performance using Orbit

Now, we are ready to deploy the model into production. Before we actually do that in the next section, one thing is still missing. As soon as we deploy this model into the simulated production environment, it will start being consumed by the production environment and having impacts on the business. **How can you track the performance metrics of your model over time, and be able to monitor them easily?**

With Orbit, this is as easy as adding a couple lines of code. Now, let’s add the following line of code to the `model.py` after line 9

```python
import foundations
```

Then add the following code to the `eval(...)` function in `model.py` around line 85. After the line `# insert foundations metric tracking here #`

```python
    # insert foundations metric tracking here #
    foundations.track_production_metrics("accuracy", {str(eval_date): accuracy})
    foundations.track_production_metrics("roc_auc", {str(eval_date): roc_auc})
    foundations.track_production_metrics("revenue", {str(eval_date): revenue})
    foundations.track_production_metrics("n_active_custs", {str(eval_date): n_active_custs})
```

<details>
  <summary>What does this orbit feature do? (Optional reading)</summary>

Orbit allows you to specify custom metric calculation code and tracks the resulting metrics. As we will show later, after we deploy this model, Orbit will package the code and automate the execution of these metric calculation function and the tracking of the resulting metrics, which you can visualize in the Orbit GUI.

In this example, we are monitoring 4 metrics. The first two are typical mathematical metrics for classification problems and the last two are business metrics for this initiative

-------------------------------------------------------------------------------------------------------------------------
</details>


## Step 4 of 9: Deploying the model

Now, let’s deploy the trained model to our simulated production environment. 

Foundations provides a standard format to seamlessly package machine learning models for production.

Copy and paste the following code in `foundations_package_manifest.yaml`, which tells Foundations to serve the `predict(...)` function from `model.py`:

```yaml
entrypoints:
  predict:
    module: 'model'
    function: 'predict'
  evaluate:
    module: 'model'
    function: 'eval'
```

Next, In the terminal, enter this command then press ‘Enter’ key:
```bash
foundations orbit serve start --project_name=orbit-trial --model_name=model-v1 --project_directory=./ --env=scheduler
```

<details>
  <summary>What does this orbit feature do? (Optional reading)</summary>

Orbit automatically package up the code and model into what we call a "model package", which is a microservice that can be accessed by any IT systems using REST API. The entrypoints specified in the `foundations_package_manifest.yaml` file will become API endpoints that can receive requests and response with output from/to IT systems. 

Why is this important?
* The packaging aspect of this feature ensures reproducibility of models
* The serving aspect of this feature essentially makes it easy to turn your model into a service that can communicate with modern technology systems via API, making it easier to put models in production

-------------------------------------------------------------------------------------------------------------------------
</details>

**Congratulations, you’ve deployed your churn model!** The model has been deployed to our trial environment running on GCP.

## Step 5 of 9: Monitoring your model using Orbit GUI

Now, we need to start monitoring how well our model is performing on live data. 

In the real life situation, the following would happen on a monthly basis:
* Every month, the Operations team will get predictions from your model (i.e., getting from your model a list of customers the model predicts to be at risk of churning)
* Some actions are performed by the Operations team based on the predictions (i.e., actually sending out the special offer to the customers)
* As the results, customer behaviours are impacted and captured as data (i.e., some customers leave/stay, reflected by their records in the database)

We’ve created a simulated production environment to mimic what you would face in real life, with every 1 minute of the trial equates to 1 month in real life.

Now please go to the GUI using the other link that we shared with you. Once you enter the GUI, you will see 1 project in the landing page. Please do the following
* Click on the "orbit-trial" project
* Once you are in the project, navigate to **Model Management** tab using the side bar
* In **Model Management**, you will see information of the model that you just deployed
* Navigate to **Model Evaluation** tab using the side bar
* You can see the four metrics that we call `track_production_metrics` function with earlier are being tracked

Again, 1 minute of trial simulates 1 month in real life. **keep an eye on the model performance in the Model Evaluation tab. We recommend that you come back here in a couple of minutes and go through the rest of this tutorial.**

At anytime, you can click the (?) button located on the top right corner to go through a quick overview of the GUI.

## Step 6 of 9: The big problem

By now, you are probably beginning to see that your model performance is suffering. You can tell by going to Model Evaluation tab, which monitors your model performance in production over time.

**Now that your model performance is decaying, revenue is dropping. Do you know what is wrong? What do you do? Here are three options you normally have in real-life**
1. If you are a Data Science guru, you roll up your sleeves and head to the IDE and do some investigation on the dataset. You are welcome to write some python code to identify & resolve the problem, and re-deploy your new model following the instructions in step 4
2. If you are not technical, you can reach out to someone else to assist on the task. Is there a data scientist from your company that can spare the time from other initiatives to help you out?
3. You can email the original model developer at a.lu@dessa.com. He will fix the issue for you. He’s quite busy on his new projects, but he will try his best to get back to you in a couple of weeks

**Regardless of which option you choose, you need to act fast because your company is bleeding money now as you are reading this.**

There is a fourth option. You let Foundations Orbit help you identify & resolve the issue in a few steps in the next section.

## Step 7 of 9: The Orbit way

Machine learning models in production typically suffer from two types of issues: 

1. **Unexpected changes in production data** 
  <details>
    <summary>Click to expand</summary>
  
  IT and operations changes can lead to unexpected data anomalies capable of adversely affecting model performance. These changes aren’t tracked by traditional IT systems, which means that teams don’t notice them until it’s too late. For example, the team that maintains the databases might not know that your model is dependent on a particular column and decided to make changes to it, such as using a different value to encode something. Small changes like that could proliferate through various data systems and eventually leads to drastic changes by the time the data reach your models

-------------------------------------------------------------------------------------------------------------------------
  </details>

2. **Population or concept drift** 
<details>
  <summary>Click to expand</summary>
Models are trained using historical data, but changes in customer behaviours and business operations happen over time, changing the underlying relationships between model input and output. In reality, models in production degrade in performance. It is only a matter of time before they become obsolete.

-------------------------------------------------------------------------------------------------------------------------
</details>

Luckily, with very little changes to our code, you can have the power to address these issues using Orbit.

### To address the first type of issue
Let’s start by adding the following line of code to the `model.py` after line 10

```python
from foundations_orbit import DataContract
```

Add these two lines of code to the `train(...)` function in `model.py`. This should be around line 30. Insert this after the line `# insert DataContract creation code here #`
```python
    # insert DataContract creation code here #
    dc = DataContract("my_contract", x_train)
    dc.save(".")
```

Add these two lines of code to the `predict(...)` function in `model.py`. This should be around line 51. Insert this after the line `# insert DataContract validation code here #`
```python
    # insert DataContract validation code here #
    dc = DataContract.load(".", "my_contract")
    dc.validate(x_inference, inference_date)
```

In terminal, run 
```bash
python train_driver.py
```

<details>
  <summary>What does this orbit feature do? (click to expand)</summary>

Orbit introduces the concept of "Data Contract". It has two components: 
1. The creation of a data contract from a reference dataset, which automatically summarizes the characteristics of a dataset
2. The application of a data contract on another dataset, using its `validate` method. When this is executed, Orbit will automatically runs QA tests on the dataset against expected characteristics stored in a data contract

In our example, we create a data contract called "my_contract" from the dataset that we used to train the model. Then we apply this data contract on the production dataset that the predict function uses to generate predictions.

In practice, you can create multiple Data Contracts and validation points at multiple points of your machine learning pipeline, quality-assuring both input and output of your model predictions.

-------------------------------------------------------------------------------------------------------------------------
</details>

### To address the second type of issue
Edit your `foundations_package_manifest.yaml` to the following:
```yaml
entrypoints:
  predict:
    module: 'model'
    function: 'predict'
  evaluate:
    module: 'model'
    function: 'eval'
  recalibrate:
    module: 'model'
    function: 'train'
```

<details>
  <summary>What does this orbit feature do? (click to expand)</summary>

This is adding a recalibration endpoint for the model package. As we serve this model, Foundations will create a new microservice for this model with a recalibration endpoint that can be hit via API to trigger recalibration. As a user, you can define what API arguments the model microservice is expecting to successfully kickoff a recalibration job. In this example, the `train` function expects two arguments, start and end dates of the training period, and takes care of training a new model given these arguments.

-------------------------------------------------------------------------------------------------------------------------
</details>

### Let's deploy a new model with these fixes
Then run this in terminal:
```bash
foundations orbit serve start --project_name=orbit-trial --model_name=model-v2 --project_directory=./ --env=scheduler
```

Now you are ready to head back to the GUI. Once you are back in the GUI, you will see the new model package that you just deployed. Please do the following on the GUI:
* Navigate to **Model Management** tab using the side bar
* Under **Model Registry** click the **Default** checkbox for the model package that you just deployed (named "model_v2" if you followed our instruction)
* Use the information on **Data Health** and **Model Evaluation** tabs to understand performance issues in production

## Step 8 of 9: Catch unexpected abnormality in production data

_Hint: you know that it is happening if you observe sharp decline in your model performance and significant difference in your data from development datasets. For example, if there a way too many or too few null values for some attributes than expected._

Please do the following on the GUI:
* Navigate to **Data Health** tab using the side bar
* Under **Validation Report** drop down, select a validation report from the latest date
* Review reports in the three tabs: **Schema Check**, **Population Shift**, and **Data Quality**
* Check if any of the attributes have a `critical` status
* Select a different validation report to check for issues at different time or different point of our ML pipeline

Once you’ve identify which attribute is having critical issue, remember the name of the attribute, and report that to us. **We will fix the issue for you, but only if you correctly report which attribute is having critical issue.** To report and fix the issue, navigate to the IDE, enter the following command in the Terminal

```bash
curl http://<user_key>:31998/simulator/fix_special_value?column_name=<attribute_name>
```
Replacing `<attribute_name>` with the name of the attribute you want to report and `<user_key>` with your user_key

Once you correctly report the issue, we will fix it. You can tell it is fixed by checking the latest validation report in the **Data Health** tab and checking the latest model performance in the **Model Evaluation** tab.

While it is not part of this trial, the full Orbit platform also offers email and slack notification features so that you can set up monitoring for data issues. The right party will get notified and start investigating right away.

## Step 9 of 9: Address population and concept drift with recalibration

_Hint: you know that it is happening if there’s a gradual performance decline, while there isn’t any glaring issues with the dataset._

Please do the following on the GUI:
* Navigate to **Model Management** tab using the side bar
* Click the **Recalibrate** button of your default model. A modal should appear on the screen
* Under **Model Package Name**, enter a name for the model that you are about to create. For example, enter “model-v3”
* Under **Description**, enter description. For example, enter “recalibrating model using latest data”
* Under **Parameters**, enter the following, use the **+** or **-** button to add/remove parameters
 
 <details>
  <summary>Instructions for parameters, click to expand</summary>
 
  | Key        | Value       |
  | -----------|-------------|
  | start_date | <start_date>|
  | end_date   | <end_date>  |

With `<start_date>` and `<end_date>` being the start and end of the time period that you want to recalibrate your model with. We recommend recalibrating this model with the lastest 3 months of data. 
For example, if the latest date in the simulated production environment, which you can find out by checking the latest date in the **Model Evaluation** tab, is 2020-10-01. You should enter:
 
  | Key        | Value       |
  | -----------|-------------|
  | start_date | 2020-07-01  |
  | end_date   | 2020-10-01  |
-------------------------------------------------------------------------------------------------------------------------
</details>

* Click **Recalibrate** button
* Under **Model Registry** click the **Default** checkbox for the newest model package (named "model-v3" if you followed our instruction)

While not part of this trial, the full Orbit platform also provides more sophisticated control on how the model can be recalibrated, existing features include:
* Scheduled recalibration
* Control how much old vs new data to include
* Performance-triggered recalibration
* Auto-swap
* Canary release for new models

## Congratulations. You’ve completed the trial.

**To Summarize, in this trial, we’ve shown you several key features of Foundations Orbit:**
* Easily convert your models and code into consumable micro-services
* Monitor model performance in production
* Monitor production data issues and distribution shift
* Automatically recalibrate your models with new data

**The product also includes several features that are not in the trial, including:**
* Audit Trail
* A/B, canary, blue-green deploy, and out-of-time testing 
* Notification integration with email and Slack
* Scheduling, automation, and orchestration of various production tasks
* Custom data monitoring functions
* Model version control

## What are the next steps? 

1. We would like to hear your what you think about Foundations Orbit!
Fill out the post-trial survey that we sent you. Tell us what you thought of Foundations Orbit via email or tweet us @Dessa

2. Try this on your own infrastructure and machine learning user cases. There are several options, contact us at 
foundations@dessa.com to learn more

3. Try out our model development platform, Foundations Atlas. This is a tool to give superpower to Data Scientists so they can develop machine learning models better and faster. You download the Community Edition for free at https://www.atlas.dessa.com/
