import apiClient from "./api-client"
import { API_PREFIX } from "@/lib/constants"

export const seedApi = {
  seed: async () => {
    const r = await apiClient.post(`${API_PREFIX}/seed`)
    return r.data
  },
}
