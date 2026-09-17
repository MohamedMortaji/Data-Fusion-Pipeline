from datetime import datetime
import pandas as pd
from monitoring.case_matching import match_cases


def create_monitoring_report(mosaiq_data, myoncare_data, fusion_data_path):
    """
    Create a monitoring report of the current fusion pipeline state.
    """

    matching = match_cases(mosaiq_data, myoncare_data)

    fusion_path = fusion_data_path / "fusion.csv"

    if fusion_path.exists():
        fusion_data = pd.read_csv(fusion_path)
    else:
        fusion_data = pd.DataFrame()

    report = {
        "monitoring_timestamp": datetime.now().isoformat(),
        "mosaiq_cases": len(set(mosaiq_data["IDA"])),
        "myoncare_cases": len(set(myoncare_data["IDA"])),
        "matched_cases": len(matching["matched_ids"]),
        "mosaiq_only_cases": len( matching["mosaiq_only_ids"]),
        "myoncare_only_cases": len(matching["myoncare_only_ids"]),
        "fusion_records": len( fusion_data),
        "fusion_cases": (fusion_data["IDA"].nunique() if not fusion_data.empty else 0),
    }
    return report

def print_monitoring_report(report):
   
    print()
    print("=" * 50)
    print("             FUSION PIPELINE MONITOR")
    print("=" * 50)

    print()
    print("CASE MATCHING")
    print("-" * 50)

    print(
        f"Mosaiq cases:        "
        f"{report['mosaiq_cases']}"
    )

    print(
        f"Myoncare cases:      "
        f"{report['myoncare_cases']}"
    )

    print(
        f"Matched cases:       "
        f"{report['matched_cases']}"
    )

    print(
        f"Mosaiq only:         "
        f"{report['mosaiq_only_cases']}"
    )

    print(
        f"Myoncare only:       "
        f"{report['myoncare_only_cases']}"
    )

    print()
    print("FUSION DATASET")
    print("-" * 50)

    print(
        f"Total records:       "
        f"{report['fusion_records']}"
    )

    print(
        f"Unique cases:        "
        f"{report['fusion_cases']}"
    )

    print()
    print("=" * 50)


def run_monitoring(mosaiq_data, myoncare_data, fusion_data_path):
    """
    Run all current monitoring checks.
    """

    report = create_monitoring_report( mosaiq_data, myoncare_data, fusion_data_path)
    
    print_monitoring_report(report)

    return report