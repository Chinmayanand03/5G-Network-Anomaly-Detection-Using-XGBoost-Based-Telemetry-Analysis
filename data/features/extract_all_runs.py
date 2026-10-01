import pandas as pd

RUNS = [
    {
        "run_id": "normal_01",
        "label": 0,
        "file": "/home/agnihotram-chinmayananad/5g-anomaly-detection/data/normal/normal_signaling_packets.csv",
    },
    {
        "run_id": "normal_02",
        "label": 0,
        "file": "/home/agnihotram-chinmayananad/5g-anomaly-detection/data/normal/run_02/normal_run_02_packets.csv",
    },
    {
        "run_id": "normal_03",
        "label": 0,
        "file": "/home/agnihotram-chinmayananad/5g-anomaly-detection/data/normal/run_03/normal_run_03_packets.csv",
    },
    {
        "run_id": "abnormal_01",
        "label": 1,
        "file": "/home/agnihotram-chinmayananad/5g-anomaly-detection/data/abnormal/abnormal_signaling_packets.csv",
    },
    {
        "run_id": "abnormal_02",
        "label": 1,
        "file": "/home/agnihotram-chinmayananad/5g-anomaly-detection/data/abnormal/registration_burst_02/registration_burst_02_packets.csv",
    },
    {
        "run_id": "abnormal_03",
        "label": 1,
        "file": "/home/agnihotram-chinmayananad/5g-anomaly-detection/data/abnormal/registration_burst_03/registration_burst_03_packets.csv",
    },
]

all_features = []

for run in RUNS:
    print(f"Processing {run['run_id']}...")

    df = pd.read_csv(run["file"])

    df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
    df["Length"] = pd.to_numeric(df["Length"], errors="coerce")
    df["Protocol"] = (
        df["Protocol"]
        .astype(str)
        .str.strip()
        .str.replace('"', "", regex=False)
    )
    df["Info"] = df["Info"].astype(str)

    df = df.dropna(subset=["Time", "Length"])
    df = df.sort_values("Time").reset_index(drop=True)

    # 5-second windows
    df["window"] = (df["Time"] // 5).astype(int)

    rows = []

    for window, g in df.groupby("window"):
        protocols = g["Protocol"]

        row = {
            "run_id": run["run_id"],
            "window": window,
            "packet_count": len(g),

            "mean_packet_length": g["Length"].mean(),
            "max_packet_length": g["Length"].max(),
            "min_packet_length": g["Length"].min(),
            "std_packet_length": g["Length"].std(ddof=0),

            "tcp_count": protocols.eq("TCP").sum(),
            "udp_count": protocols.eq("UDP").sum(),
            "sctp_count": protocols.eq("SCTP").sum(),
            "http2_count": protocols.str.startswith("HTTP2").sum(),
            "pfcp_count": protocols.eq("PFCP").sum(),
            "ngap_count": protocols.isin(
                ["NGAP", "NGAP/NAS-5GS"]
            ).sum(),
            "icmp_count": protocols.eq("ICMP").sum(),
            "mongo_count": protocols.eq("MONGO").sum(),

            "initial_ue_count": g["Info"].str.contains(
                "InitialUEMessage", case=False, na=False
            ).sum(),

            "uplink_nas_count": g["Info"].str.contains(
                "UplinkNASTransport", case=False, na=False
            ).sum(),

            "pdu_setup_req_count": g["Info"].str.contains(
                "PDUSessionResourceSetupRequest",
                case=False,
                na=False,
            ).sum(),

            "pdu_setup_resp_count": g["Info"].str.contains(
                "PDUSessionResourceSetupResponse",
                case=False,
                na=False,
            ).sum(),

            "ue_release_count": g["Info"].str.contains(
                "UEContextRelease", case=False, na=False
            ).sum(),
        }

        if len(g) > 1:
            row["mean_interarrival_ms"] = (
                g["Time"].diff().dropna().mean() * 1000
            )
        else:
            row["mean_interarrival_ms"] = 0.0

        row["label"] = run["label"]
        rows.append(row)

    all_features.append(pd.DataFrame(rows))

result = pd.concat(all_features, ignore_index=True)

output = "/home/agnihotram-chinmayananad/5g-anomaly-detection/data/features/all_runs_features.csv"
result.to_csv(output, index=False)

print("\n========================================")
print("All runs processed successfully")
print("========================================")
print(f"Rows: {len(result)}")
print("\nSamples per run:")
print(result["run_id"].value_counts())

print("\nLabels:")
print(result["label"].value_counts())

print(f"\nSaved: {output}")
