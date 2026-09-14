import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export default api;

export async function planMission(mission: any) {
  const response = await api.post("/mission/plan", mission);
  return response.data;
}