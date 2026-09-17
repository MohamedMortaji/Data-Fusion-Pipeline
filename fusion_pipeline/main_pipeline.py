from pathlib import Path
import argparse

from import_data import import_source_data
from preprocess import preprocess_source_data
from incremental_selection import select_incremental_data
from json_serialization import serialize_records
from fusion import fuse_records, write_pending_records, approve_pending_records, has_pending_records
from monitoring.monitor import run_monitoring
from monitoring.conflicts import save_conflicts, dataframe_to_records, detect_conflicts

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--approval",
        action="store_true",
        help="Save new records to pending for approval."
    )

    parser.add_argument(
        "--approve",
        action="store_true",
        help="Approve and fuse pending records."
    )

    args = parser.parse_args()

    if args.approval and args.approve:
        parser.error("--approval and --approve cannot be used together.")

    fusion_data_path = Path("fusion_data")

    #--approve scenario
    if args.approve:
        approve_pending_records(fusion_data_path)
        return

    # Block normal Mode if pending approval
    if not args.approval and has_pending_records(fusion_data_path):
        print("Pending records exist and must be approved first." )
        print("Run: python main_pipeline.py --approve")
        return
    
    mosaiq_path = Path("Data Samples/mosaiq_sample_new.csv")
    myoncare_path = Path("Data Samples/myoncare_sample_new.csv")

    # 1- Import source data
    mosaiq_data, myoncare_data = import_source_data(mosaiq_path, myoncare_path)

    # 2- Preliminary preprocessing
    mosaiq_data, myoncare_data = preprocess_source_data(mosaiq_data, myoncare_data)

    #Run Monitoring
    run_monitoring(mosaiq_data, myoncare_data, fusion_data_path)

    # Conflict detection
    mosaiq_incoming = dataframe_to_records(mosaiq_data,"mosaiq")
    myoncare_incoming = dataframe_to_records(myoncare_data, "myoncare")

    incoming_records = mosaiq_incoming + myoncare_incoming

    conflicts = detect_conflicts(incoming_records, fusion_data_path)

    if conflicts:
        print(f"Detected {len(conflicts)} conflict(s).")
        save_conflicts(conflicts,fusion_data_path)
    else:
        print("No conflicts detected.")

    # 3- Incremental selection
    mosaiq_new, myoncare_new = select_incremental_data(mosaiq_data, myoncare_data, fusion_data_path)

    # 4- JSON serialization + fusion row creation
    mosaiq_records = serialize_records(mosaiq_new, "mosaiq")
    myoncare_records = serialize_records(myoncare_new, "myoncare")

    #--approval scenario
    if args.approval:
        all_records = mosaiq_records + myoncare_records
    
        write_pending_records(all_records, fusion_data_path)
        print(f"Saved {len(all_records)} records to pending for approval.")
        return

    # 5- Fusion dataset persistence
    fuse_records(mosaiq_records, myoncare_records, fusion_data_path)

    print("Fusion completed successfully.")


if __name__ == "__main__":
    main()