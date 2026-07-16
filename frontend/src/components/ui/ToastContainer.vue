<template>
  <!-- Toast container positioned at top-right -->
  <Teleport to="body">
    <div class="toast-container" role="region" aria-label="Notifications" aria-live="polite">
      <TransitionGroup name="toast">
        <div
          v-for="toast in uiStore.toasts"
          :key="toast.id"
          class="toast"
          :class="`toast--${toast.type}`"
          role="alert"
        >
          <span class="toast-icon"><component :is="icons[toast.type]" :size="20" stroke-width="2" /></span>
          <span class="toast-message">{{ toast.message }}</span>
          <button
            class="toast-close"
            @click="uiStore.removeToast(toast.id)"
            aria-label="Fermer"
          ><X :size="16" stroke-width="2" /></button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useUiStore } from "@/stores/ui";
import { CheckCircle, XCircle, Info, AlertTriangle, X } from 'lucide-vue-next';

const uiStore = useUiStore();
const icons = { success: CheckCircle, error: XCircle, info: Info, warning: AlertTriangle };
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 1.5rem;
  right: 1.5rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  pointer-events: none;
  max-width: 380px;
}
.toast {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  pointer-events: all;
  font-size: 0.875rem;
  font-weight: 500;
  border-left: 4px solid transparent;
}
.toast--success { background: #f0fdf4; color: #15803d; border-left-color: #22c55e; }
.toast--error   { background: #fef2f2; color: #991b1b; border-left-color: #ef4444; }
.toast--info    { background: #eff6ff; color: #1e40af; border-left-color: #3b82f6; }
.toast--warning { background: #fffbeb; color: #92400e; border-left-color: #f59e0b; }
.toast-message  { flex: 1; }
.toast-close {
  background: none; border: none; cursor: pointer;
  opacity: 0.5; transition: opacity var(--transition-fast);
  padding: 0; font-size: 0.8rem;
}
.toast-close:hover { opacity: 1; }
.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from { opacity: 0; transform: translateX(100%); }
.toast-leave-to   { opacity: 0; transform: translateX(100%) scale(0.9); }
</style>
