# Overview

Outlined below is a sample assignment designed to test your abilities as a data engineer. You will be introduced to a hypothetical company situation, provided access to a fictional data set, and given a set of requirements to complete. The assignment is limited in scope to just the data and information you are provided below you will not be required to source any additional data or information outside the content in this document. Submission instructions will be provided at the end.

# Assignment

You have just joined the Poplin Office Supplies Company (POSC), a traditional company that does corporate sales of office supplies from their catalog direct to other businesses. The business model for POSC is a traditional sales lead operation where regional managers sell directly to business customers in their assigned regions. The company has had no real time understanding of their performance over the years but has just recently set up a database that streams all their past and present order information.You have been hired to help them with their business intelligence by building a data engineering pipeline for the data analysts to help them with their sales data analysis. This team has no experience with data and so aside from a couple core metrics they feel are important to track, they have no other idea what would be important for them to really measure to understand their business. 

A sample database is provide, you can start it up with docker compose and connect to it to view the data.

The data contains three tables; order, managers, and returns. Managers control regions and customers in orders are identified by region. Managers also have the ability to negotiate sales prices and that is reflected in the orders table by a percentage discount applied. Sometimes not all sales are profitable though and the net profit is reflected in the profits column. Refunds represent a full refund of the total sale amount.

You have been asked to support the data engineering team to move and enrich this data from the database to an analytics warehouse.  Provide an ELT or ETL solution to support this data team initiative.

# Requirements

Create a seperate warehouse database to store your transformed data.
You can use whatever technologies and languages for your solution.
You will be required to define a schema in the warehouse for the data
Introduce any other additional metrics or enrichments that you think would help the data analysts construct their BI dashboards.
You’re encouraged to spend at least 2 hours on the dashboard but avoid going over 5 hours.


Submission
Share your solution with https://github.com/rarescrisan and notify rares@poplin.co and the assignment provider on completion.





