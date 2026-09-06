/**
 * POWER NG TECHNOLOGIE — Axios API Service
 * Centralized HTTP client with JWT auto-refresh and error handling.
 */
import axios from "axios";

// Base Axios instance
const api = axios.create({
  baseURL: "https://powerngtech.onrender.com/api",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// ---------------------------------------------------------------------------
// Request interceptor — attach JWT token
// ---------------------------------------------------------------------------
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ---------------------------------------------------------------------------
// Response interceptor — handle 401 and auto-refresh token
// ---------------------------------------------------------------------------
let isRefreshing = false;
let refreshQueue = [];

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Queue requests while refreshing
        return new Promise((resolve, reject) => {
          refreshQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return api(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const refreshToken = localStorage.getItem("refresh_token");
        if (!refreshToken) throw new Error("No refresh token");

        const { data } = await axios.post("/api/auth/token/refresh/", {
          refresh: refreshToken,
        });

        const newAccessToken = data.access;
        localStorage.setItem("access_token", newAccessToken);

        // Resolve queued requests
        refreshQueue.forEach(({ resolve }) => resolve(newAccessToken));
        refreshQueue = [];

        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed — clear auth state
        refreshQueue.forEach(({ reject }) => reject(refreshError));
        refreshQueue = [];
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/auth/connexion";
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;

// ---------------------------------------------------------------------------
// API endpoint modules
// ---------------------------------------------------------------------------

export const authApi = {
  login: (credentials) => api.post("/auth/login/", credentials),
  register: (data) => api.post("/auth/register/", data),
  logout: (refresh) => api.post("/auth/logout/", { refresh }),
  getProfile: () => api.get("/auth/profile/"),
  updateProfile: (data) => api.patch("/auth/profile/", data),
  changePassword: (data) => api.post("/auth/password-change/", data),
  resetPassword: (email) => api.post("/auth/password-reset/", { email }),
  resetPasswordConfirm: (data) => api.post("/auth/password-reset/confirm/", data),
};

export const formationsApi = {
  getCategories: () => api.get("/formations/categories/"),
  getList: (params) => api.get("/formations/", { params }),
  getLatest: () => api.get("/formations/latest/"),
  getDetail: (slug) => api.get(`/formations/${slug}/`),
  getChapitre: (slug, chapitreId) =>
    api.get(`/formations/${slug}/chapitres/${chapitreId}/`),
  getVideo: (slug, videoId) =>
    api.get(`/formations/${slug}/videos/${videoId}/`),
  getMyFormations: () => api.get("/mes-formations/"),
};

export const boutiqueApi = {
  getCategories: () => api.get("/boutique/produits/categories/"),
  getProducts: (params) => api.get("/boutique/produits/", { params }),
  getLatestProducts: () => api.get("/boutique/produits/latest/"),
  getProduct: (slug) => api.get(`/boutique/produits/${slug}/`),
  createOrder: (data) => api.post("/boutique/commandes/", data),
  getMyOrders: () => api.get("/boutique/mes-commandes/"),
  getOrder: (id) => api.get(`/boutique/mes-commandes/${id}/`),
};

export const servicesApi = {
  getServices: () => api.get("/services/"),
  getAllServices: () => api.get("/services/all/"),
};

export const demandesApi = {
  submit: (data) => api.post("/demandes/", data),
  submitContact: (data) => api.post("/demandes/contact/", data),
};

export const paiementsApi = {
  initiate: (data) => api.post("/paiements/initier/", data),
  getStatus: (reference) => api.get(`/paiements/statut/${reference}/`),
  getHistory: () => api.get("/paiements/historique/"),
};
