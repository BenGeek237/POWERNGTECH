/**
 * POWER NG TECHNOLOGIE — UI Store (Pinia)
 * Manages global UI state: loading, toast notifications, modals.
 */
import { defineStore } from "pinia";
import { ref } from "vue";

export const useUiStore = defineStore("ui", () => {
  const globalLoading = ref(false);
  const toasts = ref([]);
  let toastId = 0;

  function showToast(message, type = "success", duration = 4000) {
    const id = ++toastId;
    toasts.value.push({ id, message, type });
    setTimeout(() => removeToast(id), duration);
  }

  function removeToast(id) {
    toasts.value = toasts.value.filter((t) => t.id !== id);
  }

  function showSuccess(message) { showToast(message, "success"); }
  function showError(message)   { showToast(message, "error", 6000); }
  function showInfo(message)    { showToast(message, "info"); }

  return { globalLoading, toasts, showToast, removeToast, showSuccess, showError, showInfo };
});
