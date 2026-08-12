<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { 
  Rocket, 
  Terminal, 
  FileText, 
  Download, 
  Search, 
  Zap, 
  Cpu, 
  ShieldCheck,
  ChevronRight,
  Sparkles,
  Layout,
  RefreshCcw,
  ArrowRight,
  AlertCircle,
  BookOpen,
  Eye,
  Copy,
  Check,
  X
} from 'lucide-vue-next';
import axios from 'axios';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { marked } from 'marked';

gsap.registerPlugin(ScrollTrigger);

import Navbar from './components/Navbar.vue';
import Hero from './components/Hero.vue';
import Features from './components/Features.vue';
import AgentSwarm from './components/AgentSwarm.vue';
import Workspace from './components/Workspace.vue';
import Footer from './components/Footer.vue';

const topic = ref("");
const jobStatus = ref<"idle" | "running" | "completed" | "error">("idle");
const logs = ref<string[]>([]);
const pdfUrl = ref<string | null>(null);
const blogTitle = ref("");
const blogContent = ref("");
const currentStep = ref(0);

const showReaderModal = ref(false);
const copied = ref(false);

const parsedMarkdown = computed(() => {
  if (!blogContent.value) return '';
  return marked.parse(blogContent.value);
});

const steps = [
  { id: 1, name: 'Analysing Topic', icon: Search },
  { id: 2, name: 'Strategic Planning', icon: Layout },
  { id: 3, name: 'Deep Research', icon: Cpu },
  { id: 4, name: 'AI Drafting', icon: FileText },
  { id: 5, name: 'Polish & Export', icon: ShieldCheck }
];

const startGeneration = async () => {
  if (!topic.value) return;
  
  jobStatus.value = "running";
  logs.value = ["Initiating Swarm Orchestrator..."];
  pdfUrl.value = null;
  blogContent.value = "";
  currentStep.value = 0;

  const el = document.getElementById('workspace-anchor');
  if (el) el.scrollIntoView({ behavior: 'smooth' });

  try {
    const res = await axios.post("/api/run", { topic: topic.value });
    const jobId = res.data.job_id;
    pollStatus(jobId);
    
    const stepInterval = setInterval(() => {
      if (currentStep.value < 4) {
        currentStep.value++;
      } else {
        clearInterval(stepInterval);
      }
    }, 4000);
  } catch (err) {
    jobStatus.value = "error";
    logs.value.push("Error: Failed to connect to backend api.");
  }
};

const pollStatus = async (jobId: string) => {
  const interval = setInterval(async () => {
    try {
      const res = await axios.get(`/api/status/${jobId}`);
      const data = res.data;
      
      logs.value = data.logs;
      
      if (data.status === "completed") {
        clearInterval(interval);
        jobStatus.value = "completed";
        pdfUrl.value = data.pdf_url;
        blogTitle.value = data.title;
        blogContent.value = data.content || "";
        currentStep.value = 4;
        
        gsap.from(".success-state", {
          y: 20,
          opacity: 0,
          duration: 0.8,
          ease: "expo.out"
        });
      } else if (data.status === "error" || data.status === "failed") {
        clearInterval(interval);
        jobStatus.value = "error";
      }
    } catch (err) {
      clearInterval(interval);
      jobStatus.value = "error";
      logs.value.push("System Error: Connection lost.");
    }
  }, 2000);
};

const copyArticleText = async () => {
  if (!blogContent.value) return;
  await navigator.clipboard.writeText(blogContent.value);
  copied.value = true;
  setTimeout(() => { copied.value = false; }, 2000);
};

const scrollToWorkspace = () => {
  const el = document.getElementById('workspace-anchor');
  if (el) el.scrollIntoView({ behavior: 'smooth' });
};

onMounted(() => {
  gsap.from(".hero-content > *", {
    y: 30,
    opacity: 0,
    duration: 1,
    stagger: 0.2,
    ease: "power4.out"
  });

  gsap.utils.toArray<Element>('.scroll-reveal').forEach((el) => {
    gsap.fromTo(el, 
      { y: 50, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 1,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 88%',
          end: 'top 20%',
          toggleActions: 'play none none reverse',
        }
      }
    );
  });

  const staggerGroups = document.querySelectorAll('.scroll-reveal-stagger');
  if (staggerGroups.length > 0) {
    gsap.fromTo(staggerGroups,
      { y: 60, opacity: 0 },
      {
        y: 0,
        opacity: 1,
        duration: 0.8,
        stagger: 0.12,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: staggerGroups[0],
          start: 'top 85%',
          toggleActions: 'play none none reverse',
        }
      }
    );
  }

  gsap.to('.hero-section', {
    y: -80,
    ease: 'none',
    scrollTrigger: {
      trigger: '.hero-section',
      start: 'top top',
      end: 'bottom top',
      scrub: 1.5,
    }
  });
});

onUnmounted(() => {
  ScrollTrigger.getAll().forEach(t => t.kill());
});
</script>

<template>
  <div class="min-h-screen bg-[#080808] relative font-plus selection:bg-brand-orange selection:text-white">
    <Navbar />

    <main class="relative z-10">
      <Hero @start="scrollToWorkspace" />

      <Features />
      <AgentSwarm />

      <div id="workspace-anchor" class="scroll-mt-32">
        <Workspace v-model="topic" :loading="jobStatus === 'running'" @submit="startGeneration" />
      </div>

      <section v-if="jobStatus !== 'idle'" class="max-w-7xl mx-auto px-4 pb-32">
        <div class="bento-card p-10 relative overflow-hidden backdrop-blur-md">
          <div class="flex justify-between items-center mb-16 relative z-10 max-w-4xl mx-auto">
            <div v-for="(step, index) in steps" :key="step.id" class="flex flex-col items-center gap-4">
              <div 
                :class="[
                  'w-14 h-14 rounded-full flex items-center justify-center border-2 transition-all duration-700',
                  currentStep >= index ? 'bg-brand-orange border-brand-orange text-white scale-110 shadow-lg shadow-orange-900/40' : 'bg-white/5 border-white/10 text-white/20'
                ]"
              >
                <component :is="step.icon" class="w-6 h-6" />
              </div>
              <span :class="['text-[10px] font-black uppercase tracking-widest', currentStep >= index ? 'text-white' : 'text-white/20']">
                {{ step.name }}
              </span>
            </div>
            <div class="absolute top-7 left-14 right-14 h-[2px] bg-white/8 -z-10">
              <div 
                class="h-full bg-brand-orange transition-all duration-1000"
                :style="{ width: `${(currentStep / 4) * 100}%` }"
              ></div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-5xl mx-auto">
            <div class="bg-black/40 rounded-3xl p-8 border border-white/8 font-mono text-xs h-96 overflow-y-auto relative">
              <div class="sticky top-0 bg-black/60 backdrop-blur pb-4 mb-4 border-b border-white/5 flex items-center gap-2">
                <Terminal class="w-4 h-4 text-brand-orange" />
                <span class="font-bold uppercase tracking-widest text-[10px] text-white/50">Orchestrator Logs</span>
              </div>
              <div v-for="(log, index) in logs" :key="index" class="mb-3 text-white/40 flex gap-4 leading-relaxed">
                <span class="text-white/15">{{ String(index + 1).padStart(2, '0') }}</span>
                <span>{{ log }}</span>
              </div>
              <div v-if="jobStatus === 'running'" class="mt-4 flex items-center gap-2 text-brand-orange font-black italic">
                <span class="w-2 h-2 bg-brand-orange rounded-full animate-ping"></span>
                <span>Awaiting agent response...</span>
              </div>
            </div>

            <div class="flex flex-col justify-center items-center text-center p-10 border border-dashed border-white/8 rounded-3xl bg-white/3">
              <div v-if="jobStatus === 'running'" class="space-y-6">
                <div class="w-24 h-24 bg-white/5 border border-white/10 rounded-full flex items-center justify-center mx-auto animate-pulse">
                  <Rocket class="w-10 h-10 text-brand-orange fill-brand-orange" />
                </div>
                <h3 class="text-2xl font-black text-white">Swarm in Action</h3>
                <p class="text-white/30 font-medium max-w-xs mx-auto">Multi-agent intelligence is active. Neutralizing hallucination risks and validating schemas.</p>
              </div>

              <div v-if="jobStatus === 'completed'" class="success-state space-y-8 w-full">
                <div class="w-20 h-20 bg-brand-orange rounded-full flex items-center justify-center mx-auto text-white shadow-xl shadow-orange-900/40">
                  <ShieldCheck class="w-10 h-10" />
                </div>
                <div>
                  <h3 class="text-2xl font-black mb-3 text-white">{{ blogTitle }}</h3>
                  <p class="text-white/30 font-medium mb-6 text-sm">Generation verified. Choose an export or reading view option below:</p>
                </div>

                <!-- Dual User Options: Read Article vs Download PDF -->
                <div class="flex flex-col sm:flex-row items-center justify-center gap-4 w-full max-w-md mx-auto">
                  <button 
                    @click="showReaderModal = true"
                    class="w-full sm:w-auto px-6 py-3.5 rounded-full bg-white/10 hover:bg-white/15 text-white font-bold text-xs uppercase tracking-widest flex items-center justify-center gap-2 transition-all border border-white/10 active:scale-95"
                  >
                    <BookOpen class="w-4 h-4 text-brand-orange" />
                    Read Article
                  </button>

                  <a 
                    :href="pdfUrl!" 
                    target="_blank"
                    class="w-full sm:w-auto px-6 py-3.5 rounded-full bg-brand-orange hover:bg-orange-500 text-white font-bold text-xs uppercase tracking-widest flex items-center justify-center gap-2 transition-all shadow-lg active:scale-95"
                  >
                    <Download class="w-4 h-4" />
                    Download PDF
                  </a>
                </div>
              </div>

              <div v-if="jobStatus === 'error'" class="space-y-6 text-red-400">
                <AlertCircle class="w-16 h-16 mx-auto stroke-[2.5]" />
                <h3 class="text-2xl font-black">Orchestration Error</h3>
                <p class="font-medium text-red-400/70">System encountered a critical exception during validation.</p>
                <button @click="jobStatus = 'idle'" class="text-white/50 font-black underline uppercase tracking-widest text-xs hover:text-white transition-colors">Re-Initialize</button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- In-App Markdown Article Reader Modal -->
    <div v-if="showReaderModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 md:p-8 bg-black/90 backdrop-blur-xl" @click.self="showReaderModal = false">
      <div class="bg-[#111111] border border-white/12 rounded-3xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl relative">
        
        <!-- Reader Header -->
        <div class="px-8 py-5 border-b border-white/8 flex items-center justify-between bg-black/40">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-xl bg-brand-orange/10 border border-brand-orange/30 flex items-center justify-center text-brand-orange">
              <BookOpen class="w-4 h-4" />
            </div>
            <div>
              <h4 class="font-black text-sm text-white line-clamp-1 max-w-md">{{ blogTitle }}</h4>
              <span class="text-[10px] uppercase tracking-widest text-white/40 font-bold">In-App Article View</span>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <button 
              @click="copyArticleText" 
              class="px-4 py-2 rounded-full bg-white/5 hover:bg-white/10 text-white/70 hover:text-white text-xs font-bold flex items-center gap-2 transition-all border border-white/8"
            >
              <Check v-if="copied" class="w-3.5 h-3.5 text-green-400" />
              <Copy v-else class="w-3.5 h-3.5" />
              <span>{{ copied ? 'Copied!' : 'Copy Text' }}</span>
            </button>

            <a 
              :href="pdfUrl!" 
              target="_blank"
              class="px-4 py-2 rounded-full bg-brand-orange hover:bg-orange-500 text-white text-xs font-bold flex items-center gap-2 transition-all shadow-md"
            >
              <Download class="w-3.5 h-3.5" />
              <span>PDF</span>
            </a>

            <button 
              @click="showReaderModal = false" 
              class="w-8 h-8 rounded-full bg-white/5 hover:bg-white/15 flex items-center justify-center text-white/50 hover:text-white transition-colors"
            >
              <X class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- Markdown Article Body -->
        <div class="p-8 md:p-12 overflow-y-auto font-sans leading-relaxed text-white/80 space-y-6 markdown-body">
          <div v-html="parsedMarkdown"></div>
        </div>

        <!-- Reader Footer -->
        <div class="px-8 py-4 border-t border-white/8 bg-black/40 flex justify-between items-center">
          <span class="text-xs text-white/30 font-medium">Verified by Swarm Agent Orchestrator</span>
          <button 
            @click="showReaderModal = false"
            class="px-6 py-2 rounded-full bg-white/10 hover:bg-white/20 text-white font-bold text-xs uppercase tracking-widest transition-all"
          >
            Close Reader
          </button>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<style>
.success-state {
  animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from { transform: translateY(30px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.markdown-body h1 {
  font-size: 2rem;
  font-weight: 900;
  color: #ffffff;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.markdown-body h2 {
  font-size: 1.5rem;
  font-weight: 800;
  color: #ffffff;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.markdown-body h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #FF5C00;
  margin-top: 1.25rem;
  margin-bottom: 0.5rem;
}

.markdown-body p {
  margin-bottom: 1.25rem;
  color: rgba(255, 255, 255, 0.75);
  font-size: 1rem;
  line-height: 1.8;
}

.markdown-body ul, .markdown-body ol {
  margin-bottom: 1.25rem;
  padding-left: 1.5rem;
  color: rgba(255, 255, 255, 0.75);
}

.markdown-body li {
  margin-bottom: 0.5rem;
}

.markdown-body blockquote {
  border-left: 4px solid #FF5C00;
  padding-left: 1rem;
  margin-bottom: 1.25rem;
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
  background: rgba(255,92,0,0.04);
  padding: 1rem;
  border-radius: 0 1rem 1rem 0;
}

.markdown-body code {
  background: rgba(255, 255, 255, 0.08);
  padding: 0.2rem 0.4rem;
  border-radius: 0.4rem;
  font-family: monospace;
  font-size: 0.875rem;
  color: #FF5C00;
}

.markdown-body pre {
  background: #000000;
  border: 1px solid rgba(255,255,255,0.1);
  padding: 1rem;
  border-radius: 1rem;
  overflow-x: auto;
  margin-bottom: 1.25rem;
}

.markdown-body pre code {
  background: transparent;
  padding: 0;
  color: #e0e0e0;
}
</style>

