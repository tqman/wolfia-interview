import axios from "axios";
import { getApiBaseUrl } from "@/utils/url";

export const API_BASE_URL = getApiBaseUrl();

export const api = axios.create({
  withCredentials: true,
  baseURL: API_BASE_URL,
  timeout: 6000000,
});
