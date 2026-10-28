# AdventureWorks Fabric Data Engineering

## Project Overview

This project demonstrates a data engineering workflow using Microsoft Fabric, PySpark and a Lakehouse architecture. It uses sales order data from a local SQL Server database to build Bronze, Silver and Gold data layers.

The project is being developed as a practical portfolio project to demonstrate data ingestion, transformation, data quality checks and aggregation.

## Technologies Used

- Microsoft Fabric
- Fabric Lakehouse
- PySpark
- Delta tables
- SQL Server
- GitHub

## Architecture

Local SQL Server → CSV Export → Microsoft Fabric Lakehouse → Bronze → Silver → Gold

## Data Pipeline

### Bronze Layer
- Loaded sales order data into the `Bronze_SalesOrders` table.
- Preserved the initial dataset for further processing.

### Silver Layer
- Created the `Silver_SalesOrders` table from Bronze data.
- Applied basic data quality filtering to exclude records with missing sales order IDs, order dates or customer IDs.

### Gold Layer
- Created the `Gold_SalesByTerritory` table.
- Aggregated total revenue and order count by sales territory.

## Validation

The current sample dataset contains 100 sales orders across 10 territories.

Validation checks confirmed 100 distinct sales orders in Bronze and 100 orders represented in the Gold aggregation.![Gold Layer Output](images/Screenshot%202026-10-26%20at%2004.31.41.png)

## Current Status

The Bronze, Silver and Gold tables have been created and validated in Microsoft Fabric. Data is currently ingested through a manual CSV export, and the project uses a 100-row sample dataset.

## Future Improvements

- Automate data ingestion into Microsoft Fabric.
- Expand the pipeline to process a larger dataset.
- Add more data quality and validation rules.
- Explore incremental data loading.
- Build a Power BI report using the Gold layer.
- Document pipeline execution and testing.
- ## Incremental Loading and Upsert Demonstration

To explore incremental data processing, I created a separate demonstration in Microsoft Fabric using fictional sales order data.

The demonstration covers:

- **Initial load:** Created three sample orders.
- **Incremental load:** Appended two new orders, bringing the total to five.
- **Upsert:** Updated an existing order using Delta Lake `MERGE` logic.
- **Data validation:** Confirmed five total rows and five unique order IDs, with no duplicate orders.
- **Update verification:** Order `900002` was updated from `250.00` to `200.00`, with its `ModifiedDate` reflecting the test update.

This demonstrates how new records can be added and existing records updated without duplicating matching order IDs. The incremental-loading exercise uses simulated data within Fabric and is separate from the main Bronze, Silver and Gold sales pipeline; it is not a live SQL Server integration.

