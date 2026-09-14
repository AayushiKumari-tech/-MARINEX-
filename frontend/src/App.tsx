import { useState } from "react";
import {
  Anchor,
  Brain,
  CheckCircle2,
  Clock3,
  Navigation,
  ShieldCheck,
  Waves,
  Wind,
  Zap,
} from "lucide-react";

import { planMission } from "./services/api";
import MarineMap from "./components/MarineMap";

function App() {
  const [objective, setObjective] = useState("Fishing mission");
  const [departure, setDeparture] = useState("2026-09-15T06:00");
  const [duration, setDuration] = useState("5");
  const [deadline, setDeadline] = useState("2026-09-15T16:00");

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const handlePlanMission = async () => {
    setLoading(true);
    setError("");

    try {
      const data = await planMission({
        objective: objective,
        departure_time: departure,
        duration_hours: Number(duration),
        return_deadline: deadline,
      });

      setResult(data);
    } catch (err) {
      console.error(err);

      setError(
        "Unable to connect to MARINEX backend. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const recommendation =
    result?.recommendation?.recommended_plan;

  const selectedRanking =
    result?.ranked_plans?.find(
      (plan: any) =>
        plan.plan_id === recommendation?.plan_id
    );

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* HEADER */}
      <header className="border-b border-slate-800 bg-slate-950">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">

          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-cyan-500/10 p-3">
              <Anchor className="h-7 w-7 text-cyan-400" />
            </div>

            <div>
              <h1 className="text-xl font-bold tracking-wide">
                MARINEX
              </h1>

              <p className="text-xs text-slate-400">
                Marine Mission Intelligence & Decision Engine
              </p>
            </div>
          </div>

          <div className="hidden items-center gap-3 sm:flex">

            <div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1.5 text-xs text-emerald-400">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              SYSTEM ONLINE
            </div>

            <div className="rounded-lg border border-slate-800 px-3 py-2 text-xs text-slate-400">
              SIH 2026 · SIH26176
            </div>

          </div>
        </div>
      </header>

      {/* MAIN */}
      <main className="mx-auto max-w-7xl px-6 py-8">

        {/* HERO */}
        <div className="mb-8">

          <div className="mb-3 flex items-center gap-2 text-sm text-cyan-400">
            <Brain className="h-4 w-4" />
            INTELLIGENT MARINE PLANNING
          </div>

          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Turn a marine mission into a
            <span className="text-cyan-400">
              {" "}feasible decision.
            </span>
          </h2>

          <p className="mt-3 max-w-2xl text-slate-400">
            MARINEX combines marine evidence, operational
            constraints and candidate plans to recommend the
            most suitable mission.
          </p>

        </div>

        {/* TOP GRID */}
        <div className="grid gap-6 lg:grid-cols-3">

          {/* MISSION PLANNER */}
          <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">

            <div className="mb-6 flex items-center gap-3">

              <div className="rounded-lg bg-cyan-500/10 p-2">
                <Navigation className="h-5 w-5 text-cyan-400" />
              </div>

              <div>
                <h3 className="font-semibold">
                  Mission Planner
                </h3>

                <p className="text-xs text-slate-500">
                  Define your operational goal
                </p>
              </div>

            </div>

            <div className="space-y-5">

              {/* OBJECTIVE */}
              <div>
                <label className="mb-2 block text-xs font-medium text-slate-400">
                  MISSION OBJECTIVE
                </label>

                <input
                  value={objective}
                  onChange={(event) =>
                    setObjective(event.target.value)
                  }
                  className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none focus:border-cyan-500"
                  placeholder="Fishing mission"
                />
              </div>

              {/* DEPARTURE */}
              <div>
                <label className="mb-2 block text-xs font-medium text-slate-400">
                  DEPARTURE
                </label>

                <input
                  type="datetime-local"
                  value={departure}
                  onChange={(event) =>
                    setDeparture(event.target.value)
                  }
                  className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none focus:border-cyan-500"
                />
              </div>

              {/* DURATION */}
              <div>
                <label className="mb-2 block text-xs font-medium text-slate-400">
                  ACTIVITY DURATION
                </label>

                <div className="relative">

                  <Clock3 className="absolute left-3 top-3 h-4 w-4 text-slate-500" />

                  <input
                    type="number"
                    min="1"
                    value={duration}
                    onChange={(event) =>
                      setDuration(event.target.value)
                    }
                    className="w-full rounded-lg border border-slate-700 bg-slate-950 py-3 pl-10 pr-4 text-sm outline-none focus:border-cyan-500"
                  />

                </div>

                <p className="mt-1 text-xs text-slate-600">
                  Hours
                </p>
              </div>

              {/* DEADLINE */}
              <div>
                <label className="mb-2 block text-xs font-medium text-slate-400">
                  RETURN DEADLINE
                </label>

                <input
                  type="datetime-local"
                  value={deadline}
                  onChange={(event) =>
                    setDeadline(event.target.value)
                  }
                  className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none focus:border-cyan-500"
                />
              </div>

              {/* BUTTON */}
              <button
                onClick={handlePlanMission}
                disabled={loading}
                className="flex w-full items-center justify-center gap-2 rounded-lg bg-cyan-500 px-4 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50"
              >

                <Zap className="h-4 w-4" />

                {loading
                  ? "ANALYZING MISSION..."
                  : "PLAN MISSION"}

              </button>

              {/* ERROR */}
              {error && (
                <div className="rounded-lg border border-red-500/20 bg-red-500/10 p-3 text-xs text-red-300">
                  {error}
                </div>
              )}

            </div>
          </section>

          {/* RIGHT SIDE */}
          <section className="space-y-6 lg:col-span-2">

            {/* RECOMMENDATION */}
            <div className="rounded-2xl border border-cyan-500/20 bg-gradient-to-br from-cyan-500/10 to-slate-900 p-6">

              <div className="mb-5 flex items-center justify-between">

                <div className="flex items-center gap-3">

                  <div className="rounded-lg bg-emerald-500/10 p-2">
                    <CheckCircle2 className="h-6 w-6 text-emerald-400" />
                  </div>

                  <div>

                    <p className="text-xs font-medium text-cyan-400">
                      MARINEX RECOMMENDATION
                    </p>

                    <h3 className="text-xl font-bold">
                      {recommendation?.plan_name ||
                        "Awaiting mission analysis"}
                    </h3>

                  </div>

                </div>

                {selectedRanking && (
                  <div className="text-right">

                    <p className="text-3xl font-bold text-cyan-400">
                      {selectedRanking.ranking_score}
                    </p>

                    <p className="text-xs text-slate-500">
                      DECISION SCORE
                    </p>

                  </div>
                )}

              </div>

              {recommendation ? (

                <div className="grid gap-4 sm:grid-cols-3">

                  <Metric
                    icon={
                      <ShieldCheck className="h-5 w-5" />
                    }
                    label="Risk"
                    value={`${selectedRanking?.risk_score ?? 0}/100`}
                  />

                  <Metric
                    icon={
                      <Waves className="h-5 w-5" />
                    }
                    label="Opportunity"
                    value={`${selectedRanking?.opportunity_score ?? 0}/100`}
                  />

                  <Metric
                    icon={
                      <CheckCircle2 className="h-5 w-5" />
                    }
                    label="Feasibility"
                    value="PASS"
                  />

                </div>

              ) : (

                <p className="text-sm text-slate-400">
                  Enter a mission and click{" "}
                  <span className="text-cyan-400">
                    Plan Mission
                  </span>{" "}
                  to generate a decision.
                </p>

              )}

            </div>

            {/* EVIDENCE + DECISION */}
            <div className="grid gap-6 md:grid-cols-2">

              {/* EVIDENCE */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">

                <div className="mb-5 flex items-center gap-3">

                  <Waves className="h-5 w-5 text-cyan-400" />

                  <h3 className="font-semibold">
                    Marine Evidence
                  </h3>

                </div>

                {result?.evidence_trace?.evidence?.length ? (

                  <div className="space-y-3">

                    {result.evidence_trace.evidence.map(
                      (item: any, index: number) => (

                        <EvidenceRow
                          key={index}
                          variable={item.variable}
                          value={`${item.value} ${
                            item.unit || ""
                          }`}
                          source={item.source}
                        />

                      )
                    )}

                  </div>

                ) : (

                  <p className="text-sm text-slate-500">
                    Evidence will appear after mission analysis.
                  </p>

                )}

              </div>

              {/* DECISION CHAIN */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">

                <div className="mb-5 flex items-center gap-3">

                  <Brain className="h-5 w-5 text-cyan-400" />

                  <h3 className="font-semibold">
                    Decision Evidence Chain
                  </h3>

                </div>

                {result?.evidence_trace?.decision_logic ? (

                  <div className="space-y-4">

                    {result.evidence_trace.decision_logic.map(
                      (step: string, index: number) => (

                        <div
                          key={index}
                          className="flex gap-3"
                        >

                          <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-cyan-500/10 text-xs font-bold text-cyan-400">
                            {index + 1}
                          </div>

                          <p className="text-sm leading-6 text-slate-400">
                            {step}
                          </p>

                        </div>

                      )
                    )}

                  </div>

                ) : (

                  <p className="text-sm text-slate-500">
                    Decision reasoning will appear here.
                  </p>

                )}

              </div>

            </div>

            {/* MAP */}
            <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4">

              <div className="mb-4 flex items-center justify-between px-2">

                <div>

                  <h3 className="font-semibold">
                    Marine Operating Map
                  </h3>

                  <p className="text-xs text-slate-500">
                    Candidate mission zones and feasibility analysis
                  </p>

                </div>

                <div className="hidden rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs text-slate-400 sm:block">
                  Click a zone for details
                </div>

              </div>

              <MarineMap result={result} />

            </section>

          </section>
        </div>

        {/* PLAN COMPARISON */}
        {result?.ranked_plans?.length > 0 && (

          <section className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/60 p-6">

            <div className="mb-5">

              <h3 className="font-semibold">
                Candidate Plan Comparison
              </h3>

              <p className="text-xs text-slate-500">
                Feasible alternatives ranked by opportunity
                and operational risk.
              </p>

            </div>

            <div className="grid gap-4 md:grid-cols-2">

              {result.ranked_plans.map(
                (plan: any, index: number) => (

                  <div
                    key={plan.plan_id}
                    className={`rounded-xl border p-5 ${
                      index === 0
                        ? "border-cyan-500/30 bg-cyan-500/5"
                        : "border-slate-800 bg-slate-950"
                    }`}
                  >

                    <div className="mb-4 flex items-center justify-between">

                      <div>

                        <p className="text-xs text-slate-500">
                          OPTION {index + 1}
                        </p>

                        <h4 className="font-semibold">
                          {plan.plan_name}
                        </h4>

                      </div>

                      {index === 0 && (

                        <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs text-emerald-400">
                          RECOMMENDED
                        </span>

                      )}

                    </div>

                    <div className="grid grid-cols-3 gap-3 text-sm">

                      <MiniStat
                        label="Score"
                        value={plan.ranking_score}
                      />

                      <MiniStat
                        label="Opportunity"
                        value={plan.opportunity_score}
                      />

                      <MiniStat
                        label="Risk"
                        value={plan.risk_score}
                      />

                    </div>

                  </div>

                )
              )}

            </div>

          </section>

        )}

        {/* FOOTER */}
        <div className="mt-8 flex flex-col items-center justify-between gap-2 border-t border-slate-800 pt-5 text-xs text-slate-600 sm:flex-row">

          <span>
            MARINEX · SIH 2026 · SIH26176
          </span>

          <span className="flex items-center gap-2">

            <Wind className="h-3 w-3" />

            Evidence-grounded marine decision intelligence

          </span>

        </div>

      </main>
    </div>
  );
}

/* METRIC */

function Metric({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950/70 p-4">

      <div className="mb-2 flex items-center gap-2 text-slate-500">
        {icon}
        <span className="text-xs">
          {label}
        </span>
      </div>

      <p className="text-lg font-bold">
        {value}
      </p>

    </div>
  );
}

/* EVIDENCE */

function EvidenceRow({
  variable,
  value,
  source,
}: {
  variable: string;
  value: string;
  source: string;
}) {
  return (
    <div className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-950 p-3">

      <div>

        <p className="text-sm font-medium capitalize">
          {variable.replace("_", " ")}
        </p>

        <p className="text-xs text-slate-600">
          {source}
        </p>

      </div>

      <span className="text-sm font-semibold text-cyan-400">
        {value}
      </span>

    </div>
  );
}

/* MINI STAT */

function MiniStat({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <div>

      <p className="text-xs text-slate-600">
        {label}
      </p>

      <p className="mt-1 font-semibold">
        {value}
      </p>

    </div>
  );
}

export default App;