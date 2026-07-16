/**
 * POWER NG TECHNOLOGIE — Auth Store (Pinia)
 * Manages authentication state, JWT tokens, and user profile.
 */
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { authApi } from "@/services/api";

export const useAuthStore = defineStore("auth", () => {
  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------
  const user = ref(null);
  const accessToken = ref(localStorage.getItem("access_token") || null);
  const refreshToken = ref(localStorage.getItem("refresh_token") || null);
  const loading = ref(false);
  const error = ref(null);

  // ---------------------------------------------------------------------------
  // Getters
  // ---------------------------------------------------------------------------
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value);
  const isStaff = computed(() => user.value?.is_staff || false);

  // ---------------------------------------------------------------------------
  // Actions
  // ---------------------------------------------------------------------------

  /**
   * Login with email and password.
   * Stores tokens in localStorage and loads user data.
   */
  async function login(email, password) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await authApi.login({ email, password });
      _setTokens(data.access, data.refresh);
      user.value = data.user;
      return { success: true };
    } catch (err) {
      error.value = _extractError(err);
      return { success: false, error: error.value };
    } finally {
      loading.value = false;
    }
  }

  /**
   * Register a new user account.
   */
  async function register(formData) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await authApi.register(formData);
      _setTokens(data.access, data.refresh);
      user.value = data.user;
      return { success: true };
    } catch (err) {
      error.value = _extractError(err);
      return { success: false, error: error.value };
    } finally {
      loading.value = false;
    }
  }

  /**
   * Logout and clear all auth state.
   */
  async function logout() {
    try {
      if (refreshToken.value) {
        await authApi.logout(refreshToken.value);
      }
    } catch {
      // Ignore logout API errors
    } finally {
      _clearAuth();
    }
  }

  /**
   * Fetch the current user's profile from the API.
   * Used to restore session on page load.
   */
  async function fetchProfile() {
    if (!accessToken.value) return;
    loading.value = true;
    try {
      const { data } = await authApi.getProfile();
      user.value = data;
    } catch {
      _clearAuth();
    } finally {
      loading.value = false;
    }
  }

  /**
   * Update user profile.
   */
  async function updateProfile(formData) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await authApi.updateProfile(formData);
      user.value = data;
      return { success: true };
    } catch (err) {
      error.value = _extractError(err);
      return { success: false, error: error.value };
    } finally {
      loading.value = false;
    }
  }

  // ---------------------------------------------------------------------------
  // Private helpers
  // ---------------------------------------------------------------------------

  function _setTokens(access, refresh) {
    accessToken.value = access;
    refreshToken.value = refresh;
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
  }

  function _clearAuth() {
    user.value = null;
    accessToken.value = null;
    refreshToken.value = null;
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }

  function _extractError(err) {
    const data = err.response?.data;
    if (!data) return "Une erreur inattendue s'est produite.";
    if (typeof data === "string") return data;
    if (data.detail) return data.detail;
    if (data.non_field_errors) return data.non_field_errors[0];
    // Return first field error
    const firstKey = Object.keys(data)[0];
    if (firstKey && Array.isArray(data[firstKey])) return data[firstKey][0];
    return "Une erreur s'est produite.";
  }

  return {
    // State
    user,
    accessToken,
    loading,
    error,
    // Getters
    isAuthenticated,
    isStaff,
    // Actions
    login,
    register,
    logout,
    fetchProfile,
    updateProfile,
  };
});
