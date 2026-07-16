<template>
  <div class="player-page">
    <!-- Sidebar -->
    <aside class="player-sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-header">
        <RouterLink :to="`/formations/${route.params.slug}`" class="sidebar-back">
          ← Retour à la formation
        </RouterLink>
        <button @click="sidebarCollapsed = !sidebarCollapsed" class="sidebar-toggle">
          {{ sidebarCollapsed ? '→' : '←' }}
        </button>
      </div>
      <div class="sidebar-title" v-if="formation">{{ formation.title }}</div>
      <div class="chapters-nav">
        <div v-for="chapter in formation?.chapters" :key="chapter.id" class="nav-chapter">
          <div class="nav-chapter-title">{{ chapter.title }}</div>
          <button
            v-for="video in chapter.videos"
            :key="video.id"
            class="nav-video-item"
            :class="{ active: currentVideoId === video.id }"
            @click="loadVideo(video.id)"
          >
            <span>{{ video.is_preview ? '🔓' : '🔒' }}</span>
            <span class="nav-video-title">{{ video.title }}</span>
            <span class="nav-video-duration">{{ video.duration_minutes }}min</span>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main player area -->
    <main class="player-main">
      <div v-if="!currentVideo && !videoLoading" class="player-welcome">
        <span style="font-size:4rem">▶️</span>
        <h2>Sélectionnez une vidéo pour commencer</h2>
        <p>Choisissez une leçon dans le menu de gauche.</p>
      </div>

      <div v-if="videoLoading" class="player-loading">
        <div class="spinner" style="width:3rem;height:3rem;border-width:3px"></div>
      </div>

      <template v-if="currentVideo && !videoLoading">
        <!-- Video player -->
        <div class="video-player-wrap">
          <video
            v-if="currentVideo.video_file"
            controls
            class="video-player"
            :src="currentVideo.video_file"
            :key="currentVideo.id"
          ></video>
          <iframe
            v-else-if="currentVideo.video_url"
            :src="getEmbedUrl(currentVideo.video_url)"
            class="video-player"
            frameborder="0"
            allowfullscreen
          ></iframe>
        </div>

        <!-- Video info -->
        <div class="video-info container">
          <h1 class="video-title">{{ currentVideo.title }}</h1>
          <p v-if="currentVideo.description" class="video-description">{{ currentVideo.description }}</p>

          <!-- PDF downloads -->
          <div v-if="currentVideo.pdfs?.length" class="pdf-section">
            <h3>📎 Ressources PDF</h3>
            <a
              v-for="pdf in currentVideo.pdfs"
              :key="pdf.id"
              :href="pdf.file"
              class="pdf-link"
              target="_blank"
              download
            >
              📄 {{ pdf.title }}
            </a>
          </div>

          <!-- Navigation -->
          <div class="video-nav">
            <button class="btn btn-outline" :disabled="!prevVideoId" @click="loadVideo(prevVideoId)">
              ← Vidéo précédente
            </button>
            <button class="btn btn-primary" :disabled="!nextVideoId" @click="loadVideo(nextVideoId)">
              Vidéo suivante →
            </button>
          </div>
        </div>
      </template>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { formationsApi } from "@/services/api";

const route = useRoute();
const formation = ref(null);
const currentVideo = ref(null);
const currentVideoId = ref(null);
const videoLoading = ref(false);
const sidebarCollapsed = ref(false);

// Flatten all videos for prev/next navigation
const allVideos = computed(() => {
  if (!formation.value) return [];
  return formation.value.chapters.flatMap(c => c.videos);
});

const currentIndex = computed(() => allVideos.value.findIndex(v => v.id === currentVideoId.value));
const prevVideoId = computed(() => currentIndex.value > 0 ? allVideos.value[currentIndex.value - 1].id : null);
const nextVideoId = computed(() => currentIndex.value < allVideos.value.length - 1 ? allVideos.value[currentIndex.value + 1].id : null);

async function loadVideo(videoId) {
  if (!videoId) return;
  currentVideoId.value = videoId;
  videoLoading.value = true;
  try {
    const { data } = await formationsApi.getVideo(route.params.slug, videoId);
    currentVideo.value = data;
  } finally {
    videoLoading.value = false;
  }
}

function getEmbedUrl(url) {
  if (url.includes("youtube.com/watch?v=")) {
    return url.replace("watch?v=", "embed/");
  }
  if (url.includes("youtu.be/")) {
    return "https://www.youtube.com/embed/" + url.split("youtu.be/")[1];
  }
  return url;
}

onMounted(async () => {
  const { data } = await formationsApi.getDetail(route.params.slug);
  formation.value = data;
  // Auto-load first video
  const firstVideo = data.chapters?.[0]?.videos?.[0];
  if (firstVideo) loadVideo(firstVideo.id);
});
</script>

<style scoped>
.player-page { display: flex; height: 100vh; overflow: hidden; }
.player-sidebar {
  width: 320px; flex-shrink: 0;
  background: var(--color-primary-dark); color: #fff;
  overflow-y: auto; transition: width var(--transition-normal);
  display: flex; flex-direction: column;
}
.player-sidebar.collapsed { width: 48px; overflow: hidden; }
.sidebar-header { display: flex; align-items: center; justify-content: space-between; padding: 1rem; border-bottom: 1px solid rgba(255,255,255,.1); flex-shrink: 0; }
.sidebar-back { color: rgba(255,255,255,.7); text-decoration: none; font-size: .8rem; }
.sidebar-back:hover { color: #fff; }
.sidebar-toggle { background: rgba(255,255,255,.1); border: none; color: #fff; border-radius: 6px; cursor: pointer; padding: .3rem .5rem; }
.sidebar-title { padding: 1rem; font-weight: 700; font-size: .875rem; border-bottom: 1px solid rgba(255,255,255,.1); }
.chapters-nav { flex: 1; overflow-y: auto; }
.nav-chapter { border-bottom: 1px solid rgba(255,255,255,.08); }
.nav-chapter-title { padding: .75rem 1rem .4rem; font-size: .7rem; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; color: rgba(255,255,255,.45); }
.nav-video-item { display: flex; align-items: center; gap: .5rem; width: 100%; padding: .55rem 1rem; background: none; border: none; color: rgba(255,255,255,.75); cursor: pointer; text-align: left; font-size: .8rem; transition: background var(--transition-fast); }
.nav-video-item:hover { background: rgba(255,255,255,.07); color: #fff; }
.nav-video-item.active { background: rgba(255,255,255,.12); color: #fff; font-weight: 600; }
.nav-video-title { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.nav-video-duration { font-size: .7rem; color: rgba(255,255,255,.4); flex-shrink: 0; }
.player-main { flex: 1; overflow-y: auto; background: var(--color-neutral-900); }
.player-welcome,.player-loading { min-height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1rem; color: rgba(255,255,255,.7); text-align: center; padding: 2rem; }
.player-welcome h2 { color: rgba(255,255,255,.9); }
.video-player-wrap { background: #000; width: 100%; aspect-ratio: 16/9; }
.video-player { width: 100%; height: 100%; display: block; }
.video-info { padding: 1.5rem 0; color: #fff; }
.video-title { font-size: 1.25rem; font-weight: 700; margin-bottom: .75rem; }
.video-description { color: rgba(255,255,255,.7); line-height: 1.65; margin-bottom: 1.25rem; }
.pdf-section { margin-bottom: 1.5rem; }
.pdf-section h3 { font-size: .9rem; font-weight: 700; margin-bottom: .75rem; }
.pdf-link { display: flex; align-items: center; gap: .5rem; padding: .6rem 1rem; background: rgba(255,255,255,.08); border-radius: var(--radius-md); color: rgba(255,255,255,.8); text-decoration: none; margin-bottom: .5rem; font-size: .875rem; transition: background var(--transition-fast); }
.pdf-link:hover { background: rgba(255,255,255,.15); color: #fff; }
.video-nav { display: flex; gap: 1rem; margin-top: 1.5rem; }
</style>
