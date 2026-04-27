# data_loader.py
import sqlite3
from config import ROOT, BENCHMARKS, MODES, L2_FILTER, CMD_FILTER, CU_FILTER


def get_metric(bench, mode, what, location_filter=L2_FILTER):
    db_path = ROOT / bench / f"{bench}_prefetch_mode_{mode}.sqlite3"
    if not db_path.exists():
        print(f"  Advertencia: No existe {db_path}")
        return 0.0
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(Value) FROM mgpusim_metrics WHERE What=? AND Location LIKE ?",
        (what, location_filter),
    )
    result = cursor.fetchone()[0]
    conn.close()
    return float(result) if result else 0.0


def load_data():
    data = {b: {m: {} for m in MODES} for b in BENCHMARKS}

    print("Extrayendo datos de SQLite...")
    for b in BENCHMARKS:
        for m in MODES:
            d = data[b][m]
            d["time"]           = get_metric(b, m, "kernel_time",          CMD_FILTER)
            d["l2_miss"]        = get_metric(b, m, "read-miss")
            d["l2_hit"]         = get_metric(b, m, "read-hit")
            d["l2_mshr_hit"]    = get_metric(b, m, "read-mshr-hit")
            d["hit_by_pref"]    = get_metric(b, m, "read-hit-by-prefetch")
            d["mshr_hit_by_pref"] = get_metric(b, m, "read-mshr-hit-by-prefetch")
            d["top_demand_read"]  = get_metric(b, m, "top-demand-read-req")
            d["top_prefetch_read"]= get_metric(b, m, "top-prefetch-read-req")
            d["pref_miss"]      = get_metric(b, m, "prefetch-req-miss")
            d["pref_mshr"]      = get_metric(b, m, "prefetch-req-hit-mshr")
            d["pref_l2"]        = get_metric(b, m, "prefetch-req-hit-l2")
            d["pref_hit"]       = get_metric(b, m, "prefetch-hit")
            d["pref_first"]     = get_metric(b, m, "prefetch-first-hit")
            d["pref_evict"]     = get_metric(b, m, "prefetch-evict")
            d["cpi_valu"]       = get_metric(b, m, "CPIStack.VALU",       CU_FILTER)
            d["cpi_vmem"]       = get_metric(b, m, "CPIStack.VMem",       CU_FILTER)
            d["cpi_fetch"]      = get_metric(b, m, "CPIStack.Fetch",      CU_FILTER)
            d["cpi_scalarmem"]  = get_metric(b, m, "CPIStack.ScalarMem",  CU_FILTER)
            d["cpi_total"]      = get_metric(b, m, "CPIStack.total",      CU_FILTER)
            d["l1_pref_abort_l1"]       = get_metric(b, m, "pref-abort-l1-hit", "%L1%")
            d["l1_pref_abort_mshr"]     = get_metric(b, m, "pref-abort-mshr-hit", "%L1%")
            d["l1_pref_abort_port"]     = get_metric(b, m, "pref-abort-port-full", "%L1%")
            d["l1_pref_abort_inflight"] = get_metric(b, m, "pref-abort-inflight-limit", "%L1%")
            d["l1_pref_sent"]           = get_metric(b, m, "pref-sent-to-l2", "%L1%")

    _compute_derived(data)
    return data


def _compute_derived(data):
    for b in BENCHMARKS:
        baseline_total = data[b]["none"]["top_demand_read"]
        baseline_miss  = data[b]["none"]["l2_miss"]
        baseline_time  = data[b]["none"]["time"]

        for m in MODES:
            d = data[b][m]
            p_miss  = d["pref_miss"]
            p_first = d["pref_first"]
            p_mshr  = d["pref_mshr"]
            p_l2    = d["pref_l2"]

            pref_req_sent   = p_miss + p_mshr + p_l2
            d["pref_req_sent"] = pref_req_sent

            d["precision_pct"]  = (p_first / p_miss  * 100) if p_miss  > 0 else 0.0
            d["coverage_pct"]   = (p_first / baseline_miss * 100) if (m != "none" and baseline_miss > 0) else 0.0
            d["redundancy_pct"] = ((p_mshr + p_l2) / pref_req_sent * 100) if pref_req_sent > 0 else 0.0

            pref_waste        = max(p_miss - p_first, 0)
            d["pref_waste"]   = pref_waste
            d["waste_pct"]    = (pref_waste / p_miss * 100) if p_miss > 0 else 0.0

            d["traffic_overhead_pct"] = (p_miss / baseline_miss * 100) if baseline_miss > 0 else 0.0
            d["speedup"]              = (baseline_time / d["time"]) if d["time"] > 0 else 1.0

            # Hits orgánicos
            d["mshr_hit_organic"] = max(d["l2_mshr_hit"] - d["mshr_hit_by_pref"], 0)
            d["hit_organic"]      = max(d["l2_hit"]      - d["hit_by_pref"],      0)

            l1_attempted = (d["l1_pref_abort_l1"] +
                            d["l1_pref_abort_mshr"] +
                            d["l1_pref_abort_port"] +
                            d["l1_pref_abort_inflight"] +
                            d["l1_pref_sent"])

            d["l1_pref_attempted"] = l1_attempted

            # Porcentaje de descarte silencioso por congestión de red
            d["l1_pref_drop_port_pct"] = (
                (d["l1_pref_abort_port"] / l1_attempted * 100)
                if l1_attempted > 0 else 0.0
            )

            # Porcentaje de descarte por límite de prefetches en vuelo
            d["l1_pref_drop_inflight_pct"] = (
                (d["l1_pref_abort_inflight"] / l1_attempted * 100)
                if l1_attempted > 0 else 0.0
            )

            # Porcentaje de prefetches innecesarios (ya estaban en L1 o en vuelo)
            d["l1_pref_redundant_pct"] = (
                ((d["l1_pref_abort_l1"] + d["l1_pref_abort_mshr"]) / l1_attempted * 100)
                if l1_attempted > 0 else 0.0
            )
            
            # Verificaciones de consistencia
            recon_full = (d["l2_miss"] + d["mshr_hit_by_pref"] + d["hit_by_pref"]
                          + d["mshr_hit_organic"] + d["hit_organic"])
            d["recon_full"] = recon_full
            d["recon_full_error_pct"] = (
                abs(recon_full - baseline_total) / d["top_demand_read"] * 100
                if d["top_demand_read"] > 0 else 0.0
            )

            recon_pref = p_miss + p_mshr + p_l2
            pref_total = d["top_prefetch_read"]
            d["recon_pref_error_pct"] = (
                abs(recon_pref - pref_total) / pref_total * 100
                if pref_total > 0 else 0.0
            )

            d["demand_invariant_ok"] = (
                abs(d["top_demand_read"] - baseline_total) / baseline_total * 100
                if baseline_total > 0 else 0.0
            )

            # Fracciones para gráfica de reclasificación (5 segmentos)
            denom = baseline_total if baseline_total > 0 else 1
            d["miss_remaining_pct"] = d["l2_miss"]          / denom * 100
            d["miss_to_mshr_pct"]   = d["mshr_hit_by_pref"] / denom * 100
            d["miss_to_hit_pct"]    = d["hit_by_pref"]       / denom * 100
            d["mshr_organic_pct"]   = d["mshr_hit_organic"]  / denom * 100
            d["hit_organic_pct"]    = d["hit_organic"]        / denom * 100

            # Memory-bound y Amdahl
            total_mem_cpi       = d["cpi_vmem"] + d["cpi_scalarmem"]
            total_cpi           = d["cpi_total"]
            d["mem_bound_ratio"]        = (total_mem_cpi / total_cpi) if total_cpi > 0 else 0.0
            d["max_theoretical_speedup"] = (
                1.0 / (1.0 - d["mem_bound_ratio"]) if d["mem_bound_ratio"] < 1.0 else 99.0
            )

            # Reclasificación parcial (para tabla maestra)
            d["reconstructed_miss"] = d["l2_miss"] + d["mshr_hit_by_pref"] + d["hit_by_pref"]
            d["recon_error_pct"]    = (
                abs(d["reconstructed_miss"] - baseline_miss) / baseline_miss * 100
                if baseline_miss > 0 else 0.0
            )


def check_all_invariants(data):
    print("\n=== VERIFICACIÓN DE INVARIANTES ===")
    errors = []
    for b in BENCHMARKS:
        baseline_total = data[b]["none"]["top_demand_read"]
        if baseline_total == 0:
            bm   = data[b]["none"]["l2_miss"]
            bh   = data[b]["none"]["l2_hit"]
            bmshr = data[b]["none"]["l2_mshr_hit"]
            if not (bm == 0 and bh == 0 and bmshr == 0):
                errors.append(f"  CRÍTICO: {b}/none top_demand_read=0 pero hay actividad L2")
            continue

        for m in MODES[1:]:
            d = data[b][m]
            if d["recon_full_error_pct"] > 1.0:
                errors.append(
                    f"  ERROR V1 {b}+{m}: recon_full={d['recon_full']:.0f} "
                    f"vs top_demand={d['top_demand_read']:.0f} "
                    f"(error={d['recon_full_error_pct']:.1f}%)"
                )
            if d["recon_pref_error_pct"] > 1.0:
                errors.append(
                    f"  ERROR V2 {b}+{m}: recon_pref={d['pref_req_sent']:.0f} "
                    f"vs top_prefetch={d['top_prefetch_read']:.0f} "
                    f"(error={d['recon_pref_error_pct']:.1f}%)"
                )
            if d["demand_invariant_ok"] > 0.5:
                errors.append(
                    f"  AVISO V3 {b}+{m}: top_demand cambia "
                    f"(baseline={baseline_total:.0f}, mode={d['top_demand_read']:.0f}, "
                    f"diff={d['demand_invariant_ok']:.1f}%)"
                )

    if errors:
        print("Se encontraron problemas:")
        for e in errors:
            print(e)
    else:
        print("Todo correcto: todas las invariantes se cumplen.")
    print("=== FIN VERIFICACIÓN ===\n")