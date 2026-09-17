# Fusion Pipeline

A Python-based pipeline for incrementally combining Mosaiq and Myoncare data into a unified fusion dataset.

## Current Implementation

The pipeline currently supports:

1. **Data Import** 

   * Imports Mosaiq and Myoncare source datasets.
   * Source-specific import functions are separated for future database/file integration.

2. **(Preliminary) Preprocessing**
   * Removes empty rows and whitespace.
   * Cleans column names and string values.
   * Converts `IDA` to integer.
   * Converts timestamps to `datetime`.
   * Sorts records by `IDA` and timestamp.

4. **Incremental Processing**

   * Tracks the latest successfully processed timestamp for each `IDA` and source in `state.json`.
   * Only records with timestamps newer than the stored state are selected for processing.
   * Prevents previously processed records from being inserted again.

5. **JSON Serialization**

   * Each source record is stored as an individual JSON file.
   * `fusion.csv` acts as an index containing the `IDA`, source, timestamp, and path to the corresponding JSON record.

6. **Fusion Persistence**

   * New records are added to the fusion dataset.
   * `fusion.csv` is sorted by `IDA` and timestamp after updates.
   * Processing state is updated only after records have been successfully incorporated.

7. **Approval Mode**

   * The `--approval` argument allows records to be placed in a separate pending area instead of being immediately added to the main fusion dataset.
   * Pending records are stored under `pending/records/` with their metadata in `pending/pending.csv`.
   * The `--approve` argument incorporates pending records into the main fusion dataset and updates the processing state.
   * Normal processing is blocked while pending records are waiting for approval.


## Command-Line Arguments

```bash
python main_pipeline.py
```

Runs the normal pipeline.

```bash
python main_pipeline.py --approval
```

Places newly selected records into the pending area for approval.

```bash
python main_pipeline.py --approve
```

Moves pending records into the main fusion dataset and updates the processing state.
