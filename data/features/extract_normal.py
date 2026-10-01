import pandas as pd
import numpy as np

INPUT = "/home/agnihotram-chinmayananad/5g-anomaly-detection/data/normal/normal_signaling_packets.csv"
OUTPUT = "/home/agnihotram-chinmayananad/5g-anomaly-detection/data/features/normal_features.csv"

df = pd.read_csv(INPUT)

# Clean columns
df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
df["Length"] = pd.to_numeric(df["Length"], errors="coerce")
df["Protocol"] = df["Protocol"].astype(str).str.strip().str.replace('"', '', regex=False)
df["Info"] = df["Info"].astype(str)

df = df.dropna(subset=["Time", "Length"])
df = df.sort_values("Time").reset_index(drop=True)

# 5-second windows
df["window"] = (df["Time"] // 5).astype(int)

rows = []

for window, g in df.groupby("window"):
    protocols = g["Protocol"]

    row = {
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
        "ngap_count": protocols.isin(["NGAP", "NGAP/NAS-5GS"]).sum(),
        "icmp_count": protocols.eq("ICMP").sum(),
        "mongo_count": protocols.eq("MONGO").sum(),

        # Actual NGAP-related events from the Info field
        "initial_ue_count": g["Info"].str.contains(
            "InitialUEMessage", case=False, na=False
        ).sum(),
        "uplink_nas_count": g["Info"].str.contains(
            "UplinkNASTransport", case=False, na=False
        ).sum(),
        "pdu_setup_req_count": g["Info"].str.contains(
            "PDUSessionResourceSetupRequest", case=False, na=False
        ).sum(),
        "pdu_setup_resp_count": g["Info"].str.contains(
            "PDUSessionResourceSetupResponse", case=False, na=False
        ).sum(),
        "ue_release_count": g["Info"].str.contains(
            "UEContextRelease", case=False, na=False
        ).sum(),

        # Normal baseline label
        "label": 0    }

    # Mean inter-arrival time inside the window
    if len(g) > 1:
        row["mean_interarrival_ms"] = g["Time"].diff().dropna().mean() * 1000
    else:
        row["mean_interarrival_ms"] = 0.0

    rows.append(row)

features = pd.DataFrame(rows)
features.to_csv(OUTPUT, index=False)

print(features)
print(f"\nSaved: {OUTPUT}")
