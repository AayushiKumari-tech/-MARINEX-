import {
  CircleMarker,
  MapContainer,
  Popup,
  TileLayer,
  useMap,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

type MarineMapProps = {
  result: any;
};

const candidatePlans = [
  {
    id: "PLAN-A",
    name: "High Opportunity Zone",
    latitude: 12.9,
    longitude: 74.9,
  },
  {
    id: "PLAN-B",
    name: "Balanced Safe Zone",
    latitude: 12.88,
    longitude: 74.88,
  },
  {
    id: "PLAN-C",
    name: "Nearshore Zone",
    latitude: 12.86,
    longitude: 74.86,
  },
];

function MapRecenter({
  result,
}: {
  result: any;
}) {
  const map = useMap();

  const selected =
    result?.evidence_trace?.selected_plan;

  if (selected) {
    const currentCenter = map.getCenter();

    const alreadyCentered =
      Math.abs(
        currentCenter.lat -
          selected.target_latitude
      ) < 0.001 &&
      Math.abs(
        currentCenter.lng -
          selected.target_longitude
      ) < 0.001;

    if (!alreadyCentered) {
      map.setView(
        [
          selected.target_latitude,
          selected.target_longitude,
        ],
        11,
        {
          animate: true,
        }
      );
    }
  }

  return null;
}

export default function MarineMap({
  result,
}: MarineMapProps) {
  const evaluations =
    result?.evaluations || [];

  const rankedPlans =
    result?.ranked_plans || [];

  const getEvaluation = (
    planId: string
  ) =>
    evaluations.find(
      (item: any) =>
        item.plan_id === planId
    );

  const getRanking = (
    planId: string
  ) =>
    rankedPlans.find(
      (item: any) =>
        item.plan_id === planId
    );

  return (
    <div className="relative h-[420px] w-full overflow-hidden rounded-2xl border border-slate-800">
      <MapContainer
        center={[12.88, 74.88]}
        zoom={10}
        scrollWheelZoom={true}
        className="h-full w-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <MapRecenter result={result} />

        {candidatePlans.map(
          (plan) => {
            const evaluation =
              getEvaluation(plan.id);

            const ranking =
              getRanking(plan.id);

            const isRecommended =
              result?.recommendation
                ?.recommended_plan
                ?.plan_id === plan.id;

            const isFeasible =
              evaluation?.feasible;

            return (
              <CircleMarker
                key={plan.id}
                center={[
                  plan.latitude,
                  plan.longitude,
                ]}
                radius={
                  isRecommended
                    ? 14
                    : 11
                }
                pathOptions={{
                  color: isRecommended
                    ? "#22c55e"
                    : isFeasible
                      ? "#38bdf8"
                      : "#ef4444",

                  fillColor:
                    isRecommended
                      ? "#22c55e"
                      : isFeasible
                        ? "#38bdf8"
                        : "#ef4444",

                  fillOpacity: 0.8,
                  weight: 3,
                }}
              >
                <Popup>
                  <div className="min-w-[210px] text-slate-900">
                    <h3 className="mb-1 text-base font-bold">
                      {plan.id}
                    </h3>

                    <p className="mb-3 text-sm font-medium">
                      {plan.name}
                    </p>

                    <div className="space-y-1 text-sm">
                      <p>
                        <strong>
                          Coordinates:
                        </strong>{" "}
                        {plan.latitude},{" "}
                        {plan.longitude}
                      </p>

                      {ranking && (
                        <>
                          <p>
                            <strong>
                              Decision score:
                            </strong>{" "}
                            {
                              ranking.ranking_score
                            }
                          </p>

                          <p>
                            <strong>
                              Opportunity:
                            </strong>{" "}
                            {
                              ranking.opportunity_score
                            }
                            /100
                          </p>

                          <p>
                            <strong>
                              Risk:
                            </strong>{" "}
                            {
                              ranking.risk_score
                            }
                            /100
                          </p>
                        </>
                      )}

                      <p>
                        <strong>
                          Feasibility:
                        </strong>{" "}
                        {isFeasible
                          ? "PASS"
                          : "REJECTED"}
                      </p>

                      {evaluation
                        ?.violations
                        ?.length >
                        0 && (
                        <div className="mt-2">
                          <strong>
                            Reason:
                          </strong>

                          <ul className="ml-4 list-disc">
                            {evaluation.violations.map(
                              (
                                violation: string,
                                index: number
                              ) => (
                                <li
                                  key={
                                    index
                                  }
                                >
                                  {
                                    violation
                                  }
                                </li>
                              )
                            )}
                          </ul>
                        </div>
                      )}

                      {isRecommended && (
                        <p className="mt-3 font-bold text-green-700">
                          ✓ RECOMMENDED PLAN
                        </p>
                      )}
                    </div>
                  </div>
                </Popup>
              </CircleMarker>
            );
          }
        )}
      </MapContainer>

      {/* LEGEND */}

      <div className="absolute bottom-4 left-4 z-[1000] rounded-xl border border-slate-700 bg-slate-950/90 p-4 shadow-xl backdrop-blur">
        <p className="mb-3 text-xs font-semibold tracking-wider text-slate-300">
          PLAN STATUS
        </p>

        <div className="space-y-2 text-xs">
          <Legend
            color="bg-green-500"
            label="Recommended"
          />

          <Legend
            color="bg-sky-400"
            label="Feasible alternative"
          />

          <Legend
            color="bg-red-500"
            label="Rejected / infeasible"
          />
        </div>
      </div>

      {/* MAP STATUS */}

      <div className="absolute right-4 top-4 z-[1000] rounded-xl border border-cyan-500/20 bg-slate-950/90 px-4 py-3 backdrop-blur">
        <div className="flex items-center gap-2">
          <div className="h-2 w-2 rounded-full bg-emerald-400" />

          <span className="text-xs font-medium text-slate-300">
            MARINEX OPERATING ZONES
          </span>
        </div>
      </div>
    </div>
  );
}

function Legend({
  color,
  label,
}: {
  color: string;
  label: string;
}) {
  return (
    <div className="flex items-center gap-2">
      <span
        className={`h-2.5 w-2.5 rounded-full ${color}`}
      />

      <span className="text-slate-400">
        {label}
      </span>
    </div>
  );
}